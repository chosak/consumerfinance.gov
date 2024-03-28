from rest_framework import serializers

from .models import CardSurveyData


class CardSurveyDataSerializer(serializers.HyperlinkedModelSerializer):
    periodic_fee_type = serializers.JSONField()
    purchase_apr_tier_max = serializers.FloatField()
    purchase_apr_tier_min = serializers.FloatField()
    purchase_apr_tier_rating = serializers.IntegerField()
    rewards = serializers.JSONField()
    transfer_apr_tier_max = serializers.FloatField()
    transfer_apr_tier_min = serializers.FloatField()

    class Meta:
        model = CardSurveyData
        fields = [
            "institution_name",
            "periodic_fee_type",
            "product_name",
            "purchase_apr_tier_max",
            "purchase_apr_tier_min",
            "purchase_apr_tier_rating",
            "rewards",
            "secured_card",
            "state_limitations",
            "top_25_institution",
            "transfer_apr_tier_max",
            "transfer_apr_tier_min",
            "url",
        ]
        extra_kwargs = {
            "url": {"view_name": "tccp:card_detail"},
        }
