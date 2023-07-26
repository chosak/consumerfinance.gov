# Generated by Django 3.2.18 on 2023-05-04 15:13

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks

import modelcluster.fields
import mptt.fields

import teachers_digital_platform.fields


class Migration(migrations.Migration):

    replaces = [('teachers_digital_platform', '0001_2022_squash'), ('teachers_digital_platform', '0002_alter_activitytopic_tree_id'), ('teachers_digital_platform', '0003_tdp_taxonomy_updates'), ('teachers_digital_platform', '0004_activitypage_search_tags'), ('teachers_digital_platform', '0005_add_use_json_field_to_streamfields')]

    initial = True

    dependencies = [
        ('wagtaildocs', '0010_document_file_hash'),
        ('v1', '0001_squashed_0235_add_use_json_field_to_streamfields'),
        ('wagtaildocs', '0007_merge'),
        ('wagtailimages', '0019_delete_filter'),
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
                ('activity_type', modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityType')),
                ('age_range', modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityAgeRange')),
                ('blooms_taxonomy_level', modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityBloomsTaxonomyLevel')),
                ('building_block', modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityBuildingBlock')),
                ('council_for_economic_education', modelcluster.fields.ParentalManyToManyField(blank=True, to='teachers_digital_platform.ActivityCouncilForEconEd', verbose_name='National Standards')),
                ('grade_level', modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityGradeLevel')),
                ('handout_file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.document', verbose_name='Student file 1')),
                ('jump_start_coalition', modelcluster.fields.ParentalManyToManyField(blank=True, to='teachers_digital_platform.ActivityJumpStartCoalition', verbose_name='Jump$tart Coalition')),
                ('school_subject', modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivitySchoolSubject')),
                ('student_characteristics', modelcluster.fields.ParentalManyToManyField(blank=True, to='teachers_digital_platform.ActivityStudentCharacteristics')),
                ('teaching_strategy', modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityTeachingStrategy')),
                ('topic', teachers_digital_platform.fields.ParentalTreeManyToManyField(to='teachers_digital_platform.ActivityTopic')),
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
                ('header', wagtail.fields.StreamField([('text_introduction', wagtail.blocks.StructBlock([('eyebrow', wagtail.blocks.CharBlock(help_text='Optional: Adds an H5 eyebrow above H1 heading text. Only use in conjunction with heading.', label='Pre-heading', required=False)), ('heading', wagtail.blocks.CharBlock(required=False)), ('intro', wagtail.blocks.RichTextBlock(required=False)), ('body', wagtail.blocks.RichTextBlock(required=False)), ('links', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(required=False)), ('aria_label', wagtail.blocks.CharBlock(help_text='Add an ARIA label if the link text does not describe the destination of the link (e.g. has ambiguous text like "Learn more" that is not descriptive on its own).', required=False)), ('url', wagtail.blocks.CharBlock(default='/', required=False))]), required=False)), ('has_rule', wagtail.blocks.BooleanBlock(help_text='Check this to add a horizontal rule line to bottom of text introduction.', label='Has bottom rule', required=False))])), ('notification', wagtail.blocks.StructBlock([('type', wagtail.blocks.ChoiceBlock(choices=[('information', 'Information'), ('warning', 'Warning')])), ('message', wagtail.blocks.CharBlock(help_text='The main notification message to display.', required=True)), ('explanation', wagtail.blocks.TextBlock(help_text='Explanation text appears below the message in smaller type.', required=False)), ('links', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock(required=False)), ('aria_label', wagtail.blocks.CharBlock(help_text='Add an ARIA label if the link text does not describe the destination of the link (e.g. has ambiguous text like "Learn more" that is not descriptive on its own).', required=False)), ('url', wagtail.blocks.CharBlock(default='/', required=False))]), help_text='Links appear on their own lines below the explanation.', required=False))]))], blank=True, use_json_field=True)),
                ('header_sidebar', wagtail.fields.StreamField([('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Should be exactly 390px tall, and up to 940px wide, unless this is an overlay or bleeding style hero.')), ('small_image', wagtail.images.blocks.ImageChooserBlock(help_text='Provide an alternate image for small displays when using a bleeding or overlay hero.', required=False))]))], blank=True, use_json_field=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'TDP Activity search page',
            },
            bases=('v1.cfgovpage',),
        ),
    ]
