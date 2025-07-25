from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='finacial_statements',
            name='is_saving_enough',
            field=models.BooleanField(default=False),
        ),
    ]
