# Generated by Django 2.0 on 2017-12-16 00:46

from django.db import migrations, models
import notifications.validators


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20171216_0318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notify',
            name='template_slug',
            field=models.CharField(help_text='Single event template slug. "%s" is a language code template variable.', max_length=100, validators=[notifications.validators.validate_str_placeholder]),
        ),
        migrations.AlterField(
            model_name='notify',
            name='template_slug_mult',
            field=models.CharField(help_text='Template slug for bundle of events (packet delivery). "%s" is a language code template.', max_length=100, validators=[notifications.validators.validate_str_placeholder]),
        ),
    ]
