# Generated by Django 2.2.6 on 2020-02-20 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0007_vaccination_coustmer_pet'),
    ]

    operations = [
        migrations.AddField(
            model_name='deworming',
            name='pet',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='pet.Pet'),
            preserve_default=False,
        ),
    ]
