import re
from functools import partial
from itertools import product

from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.db.models import Case, Count, F, Max, Min, Q, Value, When
from django.db.models.functions import Coalesce

from tailslide import Percentile

from . import enums
from .fields import CurrencyField, JSONListField, YesNoBooleanField


REPORT_DATE_REGEX = re.compile(r"Data as of (\w+ \d+)")


Percentile25 = partial(Percentile, percentile=0.25)
Percentile50 = partial(Percentile, percentile=0.5)


class CardSurveyDataQuerySet(models.QuerySet):
    def available_in(self, value):
        """Filter cards by geographic availability.

        A value of None filters to cards that are available nationally.
        Any other value filters by that particular state.
        """
        q = Q(availability_of_credit_card_plan="National")

        if value is not None:
            q |= (
                Q(availability_of_credit_card_plan="One State/Territory")
                & Q(state=value)
            ) | (
                Q(availability_of_credit_card_plan="Regional")
                & Q(state_multiple__contains=value)
            )

        return self.filter(q)

    def with_ratings(self, summary_stats=None):
        qs = self

        # Card ratings are based on how a card's purchase APR relates to the
        # distribution of purchase APRs across other cards for that credit
        # tier. This computation relies on summary statistics for the entire
        # card dataset. If we haven't previously computed those stats, we need
        # to do so now.
        summary_stats = summary_stats or qs.get_summary_statistics()

        # For each card, we annotate six additional columns:
        #
        # purchase_apr_poor_for_sorting
        # purchase_apr_good_for_sorting
        # purchase_apr_great_for_sorting
        # transfer_apr_poor_for_sorting
        # transfer_apr_good_for_sorting
        # transfer_apr_great_for_sorting
        #
        # We want to select the most appropriate APR to use for both purchase
        # APR and transfer APR for each of the three credit tiers: poor, good,
        # and great. We need a single APR for each of these so that we can both
        # sort cards by APR (purchase or transfer) and also rate cards by APR
        # (purchase only, see code further down below).
        #
        # Note that we only include a card in a certain tier if it both has a
        # valid APR for that tier AND if its "targeted_credit_tiers" column
        # includes the tier in its value. It's not enough that a card offers an
        # APR to the tier; it also has to be "targeted" to that tier.
        #
        # Given the above, the logic for choosing which APR to use works as
        # follows, using the purchase APR and the good tier as an example:
        #
        # 1. If the column "targeted_credit_tiers" column doesn't include the
        #    good tier, use an APR of None.
        # 2. Otherwise, if the column "purchase_apr_good" is defined, use it.
        # 2. Otherwise, if both columns "purchase_apr_min" and
        #    "purchase_apr_max" are defined, used "purchase_apr_min".
        # 3. Otherwise, if the column "purchase_apr_median" is defined, use it.
        # 4. Otherwise, use an APR of None.
        #
        # This logic can be represented in SQL roughly as:
        #
        # SELECT
        #   *,
        #   CASE
        #     WHEN
        #       targeted_credit_tiers @> ["Credit score 619 or less"]
        #     THEN
        #       COALESCE(
        #         purchase_apr_good,
        #         CASE
        #           WHEN
        #             purchase_apr_min IS NOT NULL AND
        #             purchase_apr_max IS NOT NULL
        #           THEN
        #             purchase_apr_min,
        #           ELSE NULL
        #         END,
        #         purchase_apr_median
        #       )
        #     ELSE NULL
        #   END AS purchase_apr_good_for_sorting
        # FROM ...;
        #
        # This logic is expressed in Django code here:
        qs = qs.annotate(
            **{
                f"{apr}_apr_{tier_column_suffix}_for_sorting": Case(
                    When(
                        targeted_credit_tiers__contains=tier_value,
                        then=Coalesce(
                            F(f"{apr}_apr_{tier_column_suffix}"),
                            Case(
                                When(
                                    Q(**{f"{apr}_apr_min__isnull": False})
                                    & Q(**{f"{apr}_apr_max__isnull": False}),
                                    then=F(f"{apr}_apr_min"),
                                ),
                                default=Value(None),
                            ),
                            F(f"{apr}_apr_median"),
                        ),
                    ),
                    default=Value(None),
                    output_field=models.FloatField(),
                )
                for apr, (tier_value, tier_column_suffix) in product(
                    ("purchase", "transfer"), enums.CreditTierColumns
                )
            }
        )

        # We additionally annotate these three columns:
        #
        # purchase_apr_poor_rating
        # purchase_apr_good_rating
        # purchase_apr_great_rating
        #
        # These are computed by comparing the three purchase APR columns
        # added above (purchase_apr_{poor, good, great}_for_sorting) with the
        # tier-specific percentiles passed in (or computed) above. Ratings are
        # assigned as:
        #
        #   purchase APR < 25th percentile: 0
        #   purchase APR < 50th percentile: 1
        #   purchase APR >= 50th percentile: 2
        #   null purchase APR: null
        #
        # This logic can be represented in SQL roughly as:
        #
        # SELECT

        # The "or 0"s below are necessary because it's possible that the
        # percentile might have been computed as None, if there are no cards
        # for this tier. This won't happen with real datasets but could happen
        # when testing this code with empty or minimal datasets.
        qs = qs.annotate(
            **{
                f"purchase_apr_{tier_column_suffix}_rating": Case(
                    When(
                        **{
                            f"purchase_apr_{tier_column_suffix}__lt": summary_stats[
                                f"purchase_apr_{tier_column_suffix}_pct25"
                            ]
                            or 0
                        },
                        then=Value(0),
                    ),
                    When(
                        **{
                            f"purchase_apr_{tier_column_suffix}__lt": summary_stats[
                                f"purchase_apr_{tier_column_suffix}_pct50"
                            ]
                            or 0
                        },
                        then=Value(1),
                    ),
                    When(
                            **{
                            f"purchase_apr_{tier_column_suffix}__lte": summary_stats[
                                f"purchase_apr_{tier_column_suffix}_max"
                            ]
                            or 0
                        },
                        then=Value(2),
                    )
                    default=Value(None),
                    output_field=models.IntegerField()
                )
                for tier_column_suffix in dict(
                    enums.CreditTierColumns
                ).values()
            }
        )

        return qs

    def for_credit_tier(self, credit_tier):
        qs = self

        tier_column_suffix = dict(enums.CreditTierColumns)[credit_tier]

        qs = qs.annotate(
            **{
                f"{basename}_apr_for_sorting": F(
                    f"{basename}_apr_{tier_column_suffix}_for_sorting"
                )
                for basename in ("purchase", "transfer")
            }
        )

        qs = qs.annotate(
            purchase_apr_rating=F(f"purchase_apr_{tier_column_suffix}_rating")
        )

                    "purchase_apr_tier_max",
            "purchase_apr_tier_min",
            "purchase_apr_tier_rating",

        # We exclude cards that don't have a purchase APR for this tier.
        qs = qs.exclude(purchase_apr_for_sorting__isnull=True)

        return qs

    def get_summary_statistics(self):
        stats = [
            ("min", Min),
            ("max", Max),
            ("pct25", Percentile25),
            ("pct50", Percentile50),
            ("count", Count),
        ]

        aggregates = {
            f"purchase_apr_{tier_name}_{stat_name}": stat_fn(
                f"purchase_apr_{tier_name}"
            )
            for (stat_name, stat_fn), tier_name in product(
                stats, dict(enums.CreditTierColumns).values()
            )
        }

        aggregates.update(
            {
                "count": Count("pk"),
                "first_report_date": Min("report_date"),
            }
        )

        return self.aggregate(**dict(aggregates))


class CardSurveyData(models.Model):
    slug = models.SlugField(max_length=255, primary_key=True)
    institution_name = models.TextField()
    product_name = models.TextField(db_index=True)
    report_date = models.DateField()
    availability_of_credit_card_plan = models.TextField(
        choices=enums.GeoAvailabilityChoices
    )
    state = models.TextField(choices=enums.StateChoices, null=True, blank=True)
    state_multiple = JSONListField(choices=enums.StateChoices, blank=True)
    pertains_to_specific_counties = YesNoBooleanField(null=True, blank=True)
    requirements_for_opening = YesNoBooleanField()
    requirements_for_opening_types = JSONListField(
        choices=enums.RequirementsForOpeningChoices, blank=True
    )
    geographic_restrictions = models.TextField(null=True, blank=True)
    professional_affiliation = models.TextField(null=True, blank=True)
    other = models.TextField(null=True, blank=True)
    secured_card = YesNoBooleanField()
    targeted_credit_tiers = JSONListField(choices=enums.CreditTierChoices)
    purchase_apr_offered = YesNoBooleanField()
    purchase_apr_vary_by_balance = YesNoBooleanField(null=True, blank=True)
    purchase_apr_balance_tier_1 = models.FloatField(null=True, blank=True)
    purchase_apr_tier_1_from_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_tier_1_to_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_balance_tier_2 = models.FloatField(null=True, blank=True)
    purchase_apr_tier_2_from_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_tier_2_to_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_balance_tier_3 = models.FloatField(null=True, blank=True)
    purchase_apr_tier_3_from_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_tier_3_to_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_balance_tier_4 = models.FloatField(null=True, blank=True)
    purchase_apr_tier_4_from_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_tier_4_to_balance = models.PositiveIntegerField(
        null=True, blank=True
    )
    purchase_apr_index = YesNoBooleanField(null=True, blank=True)
    variable_rate_index = JSONListField(choices=enums.IndexChoices, blank=True)
    index = JSONListField(
        choices=enums.IndexTypeChoices, null=True, blank=True
    )
    purchase_apr_vary_by_credit_tier = YesNoBooleanField(null=True, blank=True)
    purchase_apr_poor = models.FloatField(null=True, blank=True, db_index=True)
    purchase_apr_good = models.FloatField(null=True, blank=True, db_index=True)
    purchase_apr_great = models.FloatField(
        null=True, blank=True, db_index=True
    )
    purchase_apr_min = models.FloatField(null=True, blank=True)
    purchase_apr_median = models.FloatField(null=True, blank=True)
    purchase_apr_max = models.FloatField(null=True, blank=True)
    introductory_apr_offered = YesNoBooleanField()
    introductory_apr_vary_by_credit_tier = YesNoBooleanField(
        null=True, blank=True
    )
    intro_apr_poor = models.FloatField(null=True, blank=True, db_index=True)
    intro_apr_good = models.FloatField(null=True, blank=True, db_index=True)
    intro_apr_great = models.FloatField(null=True, blank=True, db_index=True)
    intro_apr_min = models.FloatField(null=True, blank=True)
    intro_apr_median = models.FloatField(null=True, blank=True)
    intro_apr_max = models.FloatField(null=True, blank=True)
    median_length_of_introductory_apr = models.FloatField(
        null=True, blank=True
    )
    balance_transfer_offered = YesNoBooleanField()
    balance_transfer_apr_vary_by_credit_tier = YesNoBooleanField(
        null=True, blank=True
    )
    transfer_apr_poor = models.FloatField(null=True, blank=True, db_index=True)
    transfer_apr_good = models.FloatField(null=True, blank=True, db_index=True)
    transfer_apr_great = models.FloatField(
        null=True, blank=True, db_index=True
    )
    transfer_apr_min = models.FloatField(null=True, blank=True)
    transfer_apr_median = models.FloatField(null=True, blank=True)
    transfer_apr_max = models.FloatField(null=True, blank=True)
    median_length_of_balance_transfer_apr = models.FloatField(
        null=True, blank=True
    )
    balance_transfer_grace_period = YesNoBooleanField(null=True, blank=True)
    cash_advance_apr_offered = YesNoBooleanField()
    cash_advance_apr_vary_by_credit_tier = YesNoBooleanField(
        null=True, blank=True
    )
    advance_apr_poor = models.FloatField(null=True, blank=True, db_index=True)
    advance_apr_good = models.FloatField(null=True, blank=True, db_index=True)
    advance_apr_great = models.FloatField(null=True, blank=True, db_index=True)
    advance_apr_min = models.FloatField(null=True, blank=True)
    advance_apr_median = models.FloatField(null=True, blank=True)
    advance_apr_max = models.FloatField(null=True, blank=True)
    grace_period_offered = YesNoBooleanField()
    grace_period = models.PositiveIntegerField(null=True, blank=True)
    minimum_finance_charge = YesNoBooleanField()
    minimum_finance_charge_dollars = CurrencyField(null=True, blank=True)
    balance_computation_method = JSONListField(
        choices=enums.BalanceComputationChoices
    )
    balance_computation_method_details = models.TextField(
        null=True, blank=True
    )
    periodic_fee_type = JSONListField(
        choices=enums.PeriodicFeeTypeChoices, blank=True
    )
    annual_fee = CurrencyField(null=True, blank=True)
    monthly_fee = CurrencyField(null=True, blank=True)
    weekly_fee = CurrencyField(null=True, blank=True)
    other_periodic_fee_name = models.TextField(null=True, blank=True)
    other_periodic_fee_amount = CurrencyField(null=True, blank=True)
    other_periodic_fee_frequency = models.TextField(null=True, blank=True)
    fee_varies = YesNoBooleanField(null=True, blank=True)
    periodic_min = CurrencyField(null=True, blank=True)
    periodic_max = CurrencyField(null=True, blank=True)
    fee_explanation = models.TextField(null=True, blank=True)
    purchase_transaction_fees = YesNoBooleanField()
    purchase_transaction_fee_type = JSONListField(
        choices=enums.PurchaseTransactionFeeTypeChoices, blank=True
    )
    purchase_transaction_fee_dollars = CurrencyField(null=True, blank=True)
    purchase_transaction_fee_percentage = models.FloatField(
        null=True, blank=True
    )
    minimum_purchase_transaction_fee_amount = CurrencyField(
        null=True, blank=True
    )
    purchase_transaction_fee_calculation = models.TextField(
        null=True, blank=True
    )
    balance_transfer_fees = YesNoBooleanField(db_index=True)
    balance_transfer_fee_types = JSONListField(
        choices=enums.BalanceTransferFeeTypeChoices, blank=True
    )
    balance_transfer_fee_dollars = CurrencyField(null=True, blank=True)
    balance_transfer_fee_percentage = models.FloatField(null=True, blank=True)
    minimum_balance_transfer_fee_amount = CurrencyField(null=True, blank=True)
    balance_transfer_fee_calculation = models.TextField(null=True, blank=True)
    cash_advance_fees = YesNoBooleanField()
    cash_advance_fee_for_each_transaction = YesNoBooleanField(
        null=True, blank=True
    )
    cash_advance_fee_types = JSONListField(
        choices=enums.CashAdvanceFeeTypeChoices, blank=True
    )
    cash_advance_fee_dollars = CurrencyField(null=True, blank=True)
    cash_advance_fee_percentage = models.FloatField(null=True, blank=True)
    minimum_cash_advance_fee_amount = CurrencyField(null=True, blank=True)
    cash_advance_fee_calculation = models.TextField(null=True, blank=True)
    foreign_transaction_fees = YesNoBooleanField()
    foreign_transaction_fees_types = JSONListField(
        choices=enums.ForeignTransactionFeeTypeChoices, blank=True
    )
    foreign_transaction_fee_dollars = CurrencyField(null=True, blank=True)
    foreign_transaction_fee_percentage = models.FloatField(
        null=True, blank=True
    )
    minimum_foreign_transaction_fee_amount = CurrencyField(
        null=True, blank=True
    )
    foreign_transaction_fee_calculation = models.TextField(
        null=True, blank=True
    )
    late_fees = YesNoBooleanField()
    late_fee_types = JSONListField(
        choices=enums.LateFeeTypeChoices, blank=True
    )
    late_fee_dollars = CurrencyField(null=True, blank=True)
    late_fee_six_month_billing_cycle = CurrencyField(null=True, blank=True)
    late_fee_policy_details = models.TextField(null=True, blank=True)
    fee_varies36 = YesNoBooleanField(null=True, blank=True)
    minimum37 = CurrencyField(null=True, blank=True)
    maximum38 = CurrencyField(null=True, blank=True)
    fee_explanation39 = models.TextField(null=True, blank=True)
    over_limit_fees = YesNoBooleanField()
    over_limit_fee_types = JSONListField(
        choices=enums.OverlimitFeeTypeChoices, blank=True
    )
    over_limit_fee_dollars = CurrencyField(null=True, blank=True)
    overlimit_fee_detail = models.TextField(null=True, blank=True)
    other_fees = YesNoBooleanField()
    additional_fees = YesNoBooleanField(null=True, blank=True)
    other_fee_name = models.TextField(null=True, blank=True)
    other_fee_amount = CurrencyField(null=True, blank=True)
    other_fee_explanation = models.TextField(null=True, blank=True)
    other_fee_name_2 = models.TextField(null=True, blank=True)
    other_fee_amount_2 = CurrencyField(null=True, blank=True)
    other_fee_explanation_2 = models.TextField(null=True, blank=True)
    other_fee_name_3 = models.TextField(null=True, blank=True)
    other_fee_amount_3 = CurrencyField(null=True, blank=True)
    other_fee_explanation_3 = models.TextField(null=True, blank=True)
    other_fee_name_4 = models.TextField(null=True, blank=True)
    other_fee_amount_4 = CurrencyField(null=True, blank=True)
    other_fee_explanation_4 = models.TextField(null=True, blank=True)
    other_fee_name_5 = models.TextField(null=True, blank=True)
    other_fee_amount_5 = CurrencyField(null=True, blank=True)
    other_fee_explanation_5 = models.TextField(null=True, blank=True)
    fee_varies56 = YesNoBooleanField(null=True, blank=True)
    minimum57 = CurrencyField(null=True, blank=True)
    maximum58 = CurrencyField(null=True, blank=True)
    fee_explanation59 = models.TextField(null=True, blank=True)
    services = JSONListField(choices=enums.ServicesChoices, blank=True)
    other_services = models.TextField(null=True, blank=True)
    rewards = JSONListField(choices=enums.RewardsChoices, blank=True)
    other_rewards = models.TextField(null=True, blank=True)
    card_features = JSONListField(choices=enums.FeaturesChoices, blank=True)
    other_card_features = models.TextField(null=True, blank=True)
    contact_information_types = JSONListField(
        choices=enums.ContactTypeChoices, blank=True
    )
    website_for_consumer = models.TextField(null=True, blank=True)
    telephone_number_for_consumers = models.TextField(null=True, blank=True)

    # This field doesn't currently exist in the TCCP dataset.
    # See tccp.management.commands.patch_tccp.
    # Once this is added to the dataset, the default=False can be removed.
    top_25_institution = YesNoBooleanField(default=False, db_index=True)

    class Meta:
        indexes = [
            # Add an index to potentially optimize filtering on the
            # targeted_credit_tiers field. In practice PostgreSQL won't use
            # this index unless it's faster than doing a table scan, which it
            # likely won't be unless we have a very large number of cards.
            # Still,there's no harm in defining the index for future use.
            GinIndex(
                name="tccp_targeted_credit_tiers_idx",
                fields=["targeted_credit_tiers"],
                opclasses=["jsonb_path_ops"],
            ),
            # Do the same for the rewards field.
            GinIndex(
                name="tccp_rewards_idx",
                fields=["rewards"],
                opclasses=["jsonb_path_ops"],
            ),
            # Also add a joint index to speed up sorting by late fees.
            models.Index(
                fields=["late_fees", "late_fee_dollars"],
                name="tccp_late_fee_sorting_idx",
            ),
        ]

    objects = CardSurveyDataQuerySet.as_manager()

    @property
    def state_limitations(self):
        """Get the list of states in which a given card is available.

        Returns None if the card is available everywhere.
        """
        if self.availability_of_credit_card_plan == "One State/Territory":
            return [self.state]
        elif self.availability_of_credit_card_plan == "Regional":
            return self.state_multiple
