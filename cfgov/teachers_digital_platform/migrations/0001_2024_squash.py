# Generated by Django 4.2.17 on 2024-12-26 16:03

from django.db import migrations, models
import django.db.migrations.operations.special
import django.db.models.deletion
import django.utils.timezone
import modelcluster.fields
import mptt.fields
import teachers_digital_platform.fields
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('wagtaildocs', '0007_merge'),
        ('wagtaildocs', '0010_document_file_hash'),
        ('v1', '0001_2024_squash'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityAgeRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['weight', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityBloomsTaxonomyLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['weight', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityBuildingBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('weight', models.IntegerField(default=0)),
                ('svg_icon', models.CharField(blank=True, choices=[('settings', 'Executive function'), ('split', 'Financial knowledge and decision making'), ('piggy-bank-check', 'Financial habits and norms')], max_length=60, null=True)),
            ],
            options={
                'ordering': ['weight', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityCouncilForEconEd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'National standard',
                'verbose_name_plural': 'National Standards for Personal Financial Education',
            },
        ),
        migrations.CreateModel(
            name='ActivityDuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['weight', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityGradeLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['weight', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityJumpStartCoalition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['weight', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivitySchoolSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['weight', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityTeachingStrategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['weight', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='teachers_digital_platform.activitytopic')),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['weight', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityStudentCharacteristics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['weight', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='v1.cfgovpage')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Updated')),
                ('summary', models.TextField(verbose_name='Summary')),
                ('big_idea', wagtail.fields.RichTextField(verbose_name='Big idea')),
                ('essential_questions', wagtail.fields.RichTextField(verbose_name='Essential questions')),
                ('objectives', wagtail.fields.RichTextField(verbose_name='Objectives')),
                ('what_students_will_do', wagtail.fields.RichTextField(verbose_name='What students will do')),
                ('activity_duration', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teachers_digital_platform.activityduration')),
                ('activity_file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.document', verbose_name='Teacher guide')),
                ('activity_type', modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.activitytype')),
                ('age_range', modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.activityagerange')),
                ('blooms_taxonomy_level', modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.activitybloomstaxonomylevel')),
                ('building_block', modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.activitybuildingblock')),
                ('council_for_economic_education', modelcluster.fields.ParentalManyToManyField(blank=True, to='teachers_digital_platform.activitycouncilforeconed', verbose_name='National Standards')),
                ('grade_level', modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.activitygradelevel')),
                ('handout_file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.document', verbose_name='Student file 1')),
                ('jump_start_coalition', modelcluster.fields.ParentalManyToManyField(blank=True, to='teachers_digital_platform.activityjumpstartcoalition', verbose_name='Jump$tart Coalition')),
                ('school_subject', modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.activityschoolsubject')),
                ('student_characteristics', modelcluster.fields.ParentalManyToManyField(blank=True, to='teachers_digital_platform.activitystudentcharacteristics')),
                ('teaching_strategy', modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.activityteachingstrategy')),
                ('topic', teachers_digital_platform.fields.ParentalTreeManyToManyField(to='teachers_digital_platform.activitytopic')),
                ('handout_file_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.document', verbose_name='Student file 2')),
                ('handout_file_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.document', verbose_name='Student file 3')),
                ('search_tags', models.TextField(blank=True, help_text="These words will match for the site's internal Activities search. This content will not be visible by users.", verbose_name='Activity search tags')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'TDP Activity page',
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.CreateModel(
            name='ActivityPageHandoutDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('documents', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtaildocs.document', verbose_name='Student file')),
                ('project', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='handout_documents', to='teachers_digital_platform.activitypage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityPageActivityDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('documents', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtaildocs.document', verbose_name='Teacher guide')),
                ('project', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_documents', to='teachers_digital_platform.activitypage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivitySetUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_setup', models.JSONField(blank=True, null=True)),
                ('card_order', models.JSONField(blank=True, null=True)),
                ('facet_setup', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityIndexPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='v1.cfgovpage')),
                ('header', wagtail.fields.StreamField([('text_introduction', 9), ('notification', 14)], blank=True, block_lookup={0: ('wagtail.blocks.CharBlock', (), {'help_text': 'Optional: Adds an H5 eyebrow above H1 heading text. Only use in conjunction with heading.', 'label': 'Pre-heading', 'required': False}), 1: ('wagtail.blocks.CharBlock', (), {'required': False}), 2: ('wagtail.blocks.RichTextBlock', (), {'required': False}), 3: ('wagtail.blocks.CharBlock', (), {'help_text': 'Add an ARIA label if the link text does not describe the destination of the link (e.g. has ambiguous text like "Learn more" that is not descriptive on its own).', 'required': False}), 4: ('wagtail.blocks.CharBlock', (), {'default': '/', 'required': False}), 5: ('wagtail.blocks.BooleanBlock', (), {'default': False, 'required': False}), 6: ('wagtail.blocks.StructBlock', [[('text', 1), ('aria_label', 3), ('url', 4), ('is_link_boldface', 5)]], {}), 7: ('wagtail.blocks.ListBlock', (6,), {'required': False}), 8: ('wagtail.blocks.BooleanBlock', (), {'help_text': 'Check this to add a horizontal rule line to bottom of text introduction.', 'label': 'Has bottom rule', 'required': False}), 9: ('wagtail.blocks.StructBlock', [[('eyebrow', 0), ('heading', 1), ('intro', 2), ('body', 2), ('links', 7), ('has_rule', 8)]], {}), 10: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('information', 'Information'), ('warning', 'Warning')]}), 11: ('wagtail.blocks.CharBlock', (), {'help_text': 'The main notification message to display.', 'required': True}), 12: ('wagtail.blocks.TextBlock', (), {'help_text': 'Explanation text appears below the message in smaller type.', 'required': False}), 13: ('wagtail.blocks.ListBlock', (6,), {'help_text': 'Links appear on their own lines below the explanation.', 'required': False}), 14: ('wagtail.blocks.StructBlock', [[('type', 10), ('message', 11), ('explanation', 12), ('links', 13)]], {})})),
                ('header_sidebar', wagtail.fields.StreamField([('image', 2)], blank=True, block_lookup={0: ('wagtail.images.blocks.ImageChooserBlock', (), {'help_text': 'Should be exactly 390px tall, and up to 940px wide, unless this is an overlay or bleeding style hero.'}), 1: ('wagtail.images.blocks.ImageChooserBlock', (), {'help_text': 'Provide an alternate image for small displays when using a bleeding or overlay hero.', 'required': False}), 2: ('wagtail.blocks.StructBlock', [[('image', 0), ('small_image', 1)]], {})})),
            ],
            options={
                'abstract': False,
                'verbose_name': 'TDP Activity search page',
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.RunPython(
            code=django.db.migrations.operations.special.RunPython.noop,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name='activityindexpage',
            name='header_sidebar',
        ),
    ]
