# Generated by Django 2.2.6 on 2020-02-13 14:51

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name_of_doctor', models.CharField(max_length=50)),
                ('Qualification', models.CharField(max_length=30)),
                ('Registration_number', models.IntegerField()),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('Gender', models.CharField(max_length=10)),
                ('Date_of_birth', models.DateField()),
                ('Experience', models.IntegerField()),
                ('Hospital', models.CharField(max_length=50)),
                ('Email', models.CharField(max_length=50)),
                ('Mobile', models.CharField(max_length=15)),
                ('Telephone', models.CharField(max_length=15)),
                ('Address', models.TextField()),
                ('password', models.CharField(max_length=30)),
                ('date', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_id', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('breed', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='PurposeAndDiet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set1', models.CharField(max_length=30)),
                ('set2', models.CharField(max_length=30)),
                ('disease', models.CharField(max_length=500)),
                ('vaccination_purpose', models.CharField(max_length=100)),
                ('deworming_purpose', models.CharField(max_length=100)),
                ('symptoms_text', models.TextField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('last_deworming', models.DateField(blank=True, null=True)),
                ('new_diet', models.CharField(max_length=30)),
                ('new_diet_state', models.CharField(max_length=30)),
                ('pet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Pet')),
            ],
        ),
        migrations.CreateModel(
            name='Summary_analytics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet', models.CharField(max_length=30)),
                ('id_pk', models.CharField(max_length=30)),
                ('visit_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='testdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('test1', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Vitals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Temperature', models.CharField(blank=True, max_length=30, null=True)),
                ('Height', models.CharField(blank=True, max_length=30, null=True)),
                ('Weight', models.CharField(blank=True, max_length=10, null=True)),
                ('Pulse_rate', models.CharField(blank=True, max_length=10, null=True)),
                ('Respiration_rate', models.CharField(blank=True, max_length=30, null=True)),
                ('Age_of_maturity', models.CharField(blank=True, max_length=10, null=True)),
                ('Oestrus', models.CharField(blank=True, max_length=10, null=True)),
                ('Pregnancy', models.CharField(blank=True, max_length=10, null=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('purpose_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pet.PurposeAndDiet')),
            ],
        ),
        migrations.CreateModel(
            name='Vaccination_coustmer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('l_rabies', models.DateField()),
                ('l_distemper', models.DateField()),
                ('l_hepatitis', models.DateField()),
                ('l_parovirus', models.DateField()),
                ('l_parainfluenza', models.DateField()),
                ('l_bordetella', models.DateField()),
                ('l_leptospirosis', models.DateField()),
                ('l_lymedisease', models.DateField()),
                ('l_coronavirus', models.DateField()),
                ('l_giardia', models.DateField()),
                ('l_dhpp', models.DateField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('purpose_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pet.PurposeAndDiet')),
            ],
        ),
        migrations.CreateModel(
            name='Vaccination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('l_rabies', models.DateField()),
                ('d_rabies', models.DateField()),
                ('l_distemper', models.DateField()),
                ('d_distemper', models.DateField()),
                ('l_hepatitis', models.DateField()),
                ('d_hepatitis', models.DateField()),
                ('l_parovirus', models.DateField()),
                ('d_parovirus', models.DateField()),
                ('l_parainfluenza', models.DateField()),
                ('d_parainfluenza', models.DateField()),
                ('l_bordetella', models.DateField()),
                ('d_bordetella', models.DateField()),
                ('l_leptospirosis', models.DateField()),
                ('d_leptospirosis', models.DateField()),
                ('l_lymedisease', models.DateField()),
                ('d_lymedisease', models.DateField()),
                ('l_coronavirus', models.DateField()),
                ('d_coronavirus', models.DateField()),
                ('l_giardia', models.DateField()),
                ('d_giardia', models.DateField()),
                ('l_dhpp', models.DateField()),
                ('d_dhpp', models.DateField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('purpose_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pet.PurposeAndDiet')),
            ],
        ),
        migrations.CreateModel(
            name='Symptoms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('purpose_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pet.PurposeAndDiet')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine1', models.TextField()),
                ('medicine2', models.TextField()),
                ('medicine3', models.TextField()),
                ('medicine4', models.TextField()),
                ('medicine5', models.TextField()),
                ('medicine6', models.TextField()),
                ('medicine7', models.TextField()),
                ('medicine8', models.TextField()),
                ('medicine_other', models.TextField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('purpose_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pet.PurposeAndDiet')),
            ],
        ),
        migrations.CreateModel(
            name='multipetpayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_date', models.DateField(default=datetime.date.today)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Customer')),
                ('doc_pk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Doctor')),
                ('pet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Pet')),
                ('purpose_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.PurposeAndDiet')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultation_fee', models.CharField(max_length=20)),
                ('final_fee', models.CharField(max_length=20)),
                ('pet_id', models.CharField(max_length=30)),
                ('date', models.DateField(default=datetime.date.today)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Customer')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Doctor')),
                ('purpose_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pet.PurposeAndDiet')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorViewLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose_id', models.CharField(blank=True, max_length=50, null=True)),
                ('pet_id', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Customer')),
                ('doc_pk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorLogList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=20)),
                ('date', models.DateField(default=datetime.date.today)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Customer')),
                ('doc_pk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Doctor')),
                ('pet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Pet')),
                ('purpose_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.PurposeAndDiet')),
            ],
        ),
        migrations.CreateModel(
            name='doctemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_id', models.CharField(max_length=30)),
                ('visited_on', models.DateField(default=datetime.date.today)),
                ('coustmer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Customer')),
                ('purpose_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pet.Pet')),
            ],
        ),
        migrations.CreateModel(
            name='docip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=30)),
                ('doc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Diagnostics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('haematology', models.TextField()),
                ('biochemistry', models.TextField()),
                ('harmones', models.TextField()),
                ('microbiology', models.TextField()),
                ('parasitology', models.TextField()),
                ('serology', models.TextField()),
                ('cytology', models.TextField()),
                ('rapid_test', models.TextField()),
                ('others', models.TextField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('purpose_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pet.PurposeAndDiet')),
            ],
        ),
        migrations.CreateModel(
            name='Deworming',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_date', models.DateField()),
                ('due_date', models.DateField()),
                ('purpose_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pet.PurposeAndDiet')),
            ],
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DERMATOLOGY', models.TextField()),
                ('EYES', models.TextField()),
                ('LUNGS', models.TextField()),
                ('EARS', models.TextField()),
                ('GASTROINTESTINAL', models.TextField()),
                ('NOSE_THROAT', models.TextField()),
                ('UROGENITAL', models.TextField()),
                ('MOUTH_TEETH_GUMS', models.TextField()),
                ('MUSKULOSKELETAL', models.TextField()),
                ('HEART', models.TextField()),
                ('others', models.TextField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('purpose_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pet.PurposeAndDiet')),
            ],
        ),
    ]