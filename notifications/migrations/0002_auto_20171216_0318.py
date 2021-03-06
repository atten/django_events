# Generated by Django 2.0 on 2017-12-16 00:18

from django.db import migrations, models
import notifications.validators


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='cas_profile_url',
            field=models.URLField(help_text="e.g. http://example.com/api/v1/profile/%d/. '%d' is a template for user_id.", max_length=255, validators=[notifications.validators.validate_integer_placeholder]),
        ),
    ]
