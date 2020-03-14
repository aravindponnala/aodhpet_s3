from __future__ import unicode_literals
from django.db import models

# Create your models here.
from django.db import models
from datetime import date
from django.contrib.auth.models import User



# Create your models here.

class Customer(models.Model):
	customer_id = models.CharField(max_length=20, primary_key=True)
	customer_name = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	mobile = models.CharField(max_length=15)
	password = models.CharField(max_length=50)

	def __str__(self):
		return self.customer_id



class Pet(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pet_id = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    breed = models.CharField(max_length=30)
    age_year = models.IntegerField()
    age_month = models.IntegerField()
    gender = models.CharField(max_length=10)


class PurposeAndDiet(models.Model):
	pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE)
	diet = models.CharField(max_length=30)
	diet_state = models.CharField(max_length=30)
	disease = models.CharField(max_length=500)
	vaccination_purpose = models.CharField(max_length=100)
	symptoms_text=models.TextField()
	date = models.DateField(default=date.today)





class Assessment(models.Model):
	purpose_id = models.OneToOneField(PurposeAndDiet, on_delete=models.CASCADE)
	DERMATOLOGY=models.TextField()
	EYES=models.TextField()
	LUNGS=models.TextField()
	EARS=models.TextField()
	GASTROINTESTINAL=models.TextField()
	NOSE_THROAT=models.TextField()
	UROGENITAL=models.TextField()
	MOUTH_TEETH_GUMS=models.TextField()
	MUSKULOSKELETAL=models.TextField()
	HEART=models.TextField()
	others=models.TextField()
	date = models.DateField(default=date.today)


class Vitals(models.Model):
	purpose_id = models.OneToOneField(PurposeAndDiet, on_delete=models.CASCADE)
	Temperature=models.CharField(max_length=30,blank=True,null=True)
	Height=models.CharField(max_length=30,blank=True,null=True)
	Weight=models.CharField(max_length=10,blank=True,null=True)
	Pulse_rate=models.CharField(max_length=10,blank=True,null=True)
	Respiration_rate=models.CharField(max_length=30,blank=True,null=True)
	Age_of_maturity=models.CharField(max_length=10,blank=True,null=True)
	Oestrus=models.CharField(max_length=10,blank=True,null=True)
	Pregnancy=models.CharField(max_length=10,blank=True,null=True)
	date = models.DateField(default=date.today)


class Deworming(models.Model):
	purpose_id = models.OneToOneField(PurposeAndDiet, on_delete=models.CASCADE)
	pet=models.ForeignKey(Pet,on_delete=models.CASCADE)
	last_date = models.DateField()
	due_date = models.DateField()



class Diagnostics(models.Model):
	purpose_id = models.OneToOneField(PurposeAndDiet, on_delete=models.CASCADE)
	haematology=models.TextField()
	biochemistry=models.TextField()
	harmones=models.TextField()
	microbiology=models.TextField()
	parasitology=models.TextField()
	serology=models.TextField()
	cytology=models.TextField()
	rapid_test=models.TextField()
	others=models.TextField()
	date = models.DateField(default=date.today)

class Vaccination_coustmer(models.Model):
	pet=models.ForeignKey(Pet,on_delete=models.CASCADE)
	last_date_rabies = models.DateField()
	last_date_distemper = models.DateField()
	last_date_hepatitis = models.DateField()
	last_date_parovirus = models.DateField()
	last_date_parainfluenza = models.DateField()
	last_date_bordetella = models.DateField()
	last_date_leptospirosis = models.DateField()
	last_date_lymedisease = models.DateField()
	last_date_coronavirus = models.DateField()
	last_date_giardia = models.DateField()
	last_date_dhpp = models.DateField()
	last_deworming = models.DateField(blank=True,null=True)
	date = models.DateField(default=date.today)

class Vaccination(models.Model):
	purpose_id = models.OneToOneField(PurposeAndDiet, on_delete=models.CASCADE)
	pet=models.ForeignKey(Pet,on_delete=models.CASCADE)
	last_date_rabies = models.DateField()
	due_date_rabies = models.DateField()
	last_date_distemper = models.DateField()
	due_date_distemper = models.DateField()
	last_date_hepatitis = models.DateField()
	due_date_hepatitis = models.DateField()
	last_date_parovirus = models.DateField()
	due_date_parovirus = models.DateField()
	last_date_parainfluenza = models.DateField()
	due_date_parainfluenza = models.DateField()
	last_date_bordetella = models.DateField()
	due_date_bordetella = models.DateField()
	last_date_leptospirosis = models.DateField()
	due_date_leptospirosis = models.DateField()
	last_date_lymedisease = models.DateField()
	due_date_lymedisease = models.DateField()
	last_date_coronavirus = models.DateField()
	due_date_coronavirus = models.DateField()
	last_date_giardia = models.DateField()
	due_date_giardia = models.DateField()
	last_date_dhpp = models.DateField()
	due_date_dhpp = models.DateField()
	date = models.DateField(default=date.today)


class Prescription(models.Model):
	purpose_id = models.OneToOneField(PurposeAndDiet, on_delete=models.CASCADE)
	medicine1=models.TextField()
	medicine2=models.TextField()
	medicine3=models.TextField()
	medicine4=models.TextField()
	medicine5=models.TextField()
	medicine6=models.TextField()
	medicine7=models.TextField()
	medicine_other=models.TextField()
	date = models.DateField(default=date.today)

class Symptoms(models.Model):
	purpose_id = models.OneToOneField(PurposeAndDiet, on_delete=models.CASCADE)
	notes = models.TextField()
	date = models.DateField(default=date.today)


class Doctor(models.Model):
    Name_of_doctor=models.CharField(max_length=50)
    Qualification=models.CharField(max_length=30)
    Registration_number = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    Gender = models.CharField(max_length=10)
    Date_of_birth = models.DateField()
    Experience = models.IntegerField()
    Hospital = models.CharField(max_length=50)
    Email = models.CharField(max_length=50)
    Mobile = models.CharField(max_length=15)
    Telephone = models.CharField(max_length=15)
    Address = models.TextField()
    consultation_fee=models.IntegerField()
    password = models.CharField(max_length=30)
    date = models.DateField(default=date.today)




class doctemp(models.Model):
	purpose_id = models.OneToOneField(Pet, on_delete=models.CASCADE)
	coustmer_id=models.ForeignKey(Customer,on_delete=models.CASCADE)
	pet_id = models.CharField(max_length=30)
	visited_on = models.DateField(default=date.today)





class Log(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	consultation_fee = models.CharField(max_length=20)
	final_fee = models.CharField(max_length=20)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	purpose_id = models.OneToOneField(PurposeAndDiet, on_delete=models.CASCADE)
	pet_id=models.CharField(max_length=30)
	date = models.DateField(default=date.today)

class Summary_analytics(models.Model):
	pet=models.CharField(max_length=30)
	id_pk=models.CharField(max_length=30)
	visit_date=models.DateField()

class DoctorViewLog(models.Model):
	purpose_id = models.CharField(max_length=50,null=True,blank=True)
	customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
	doc_pk = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	pet_id = models.CharField(max_length=50,null=True,blank=True)
	date = models.DateField(default=date.today)


class DoctorLogList(models.Model):
	purpose_id = models.ForeignKey(PurposeAndDiet,on_delete=models.CASCADE)
	customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
	doc_pk = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	pet_id = models.ForeignKey(Pet,on_delete=models.CASCADE)
	payment=models.CharField(max_length=20)
	color=models.CharField(max_length=20)
	date = models.DateField(default=date.today)



class multipetpayment(models.Model):
	purpose_id = models.ForeignKey(PurposeAndDiet,on_delete=models.CASCADE)
	customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
	doc_pk = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	pet_id = models.ForeignKey(Pet,on_delete=models.CASCADE)
	visit_date=models.DateField(default=date.today)

class docip(models.Model):
	doc_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
	ip=models.CharField(max_length=30)




class Conferences(models.Model):
	title = models.CharField(max_length=250)
	location = models.CharField(max_length=150)
	content = models.TextField()
	timings = models.TimeField()
	date = models.DateField()


class Seminars(models.Model):
	title = models.CharField(max_length=250)
	location = models.CharField(max_length=150)
	content = models.TextField()
	timings = models.TimeField()
	date = models.DateField()


class Vet_News(models.Model):
	title = models.CharField(max_length=250)
	location = models.CharField(max_length=150)
	content = models.TextField()
	timings = models.TimeField()
	date = models.DateField()



class Articles(models.Model):
	article_title = models.CharField(max_length=250)
	summery = models.CharField(max_length=500)
	authors = models.CharField(max_length=150)
	content = models.TextField()
	published_on = models.DateField()



class Case_Reports(models.Model):
	title = models.CharField(max_length=250)
	author = models.CharField(max_length=50)
	email = models.EmailField()
	published_on = models.DateField()
	link = models.CharField(max_length=600)

class Book(models.Model):
	title = models.CharField(max_length=50)
	file = models.FileField(upload_to='books/%Y/%m/%d/')

class bookmarks_article(models.Model):
	doc= models.ForeignKey(Doctor,on_delete=models.CASCADE)
	article_id= models.ForeignKey(Articles, verbose_name="Articles",on_delete=models.CASCADE)

class bookmarks_case_reports(models.Model):
	doc= models.ForeignKey(Doctor,on_delete=models.CASCADE)
	case_reports= models.ForeignKey(Case_Reports, verbose_name="Case_Reports",on_delete=models.CASCADE)

class bookmarks_conferences(models.Model):
	doc= models.ForeignKey(Doctor,on_delete=models.CASCADE)
	conferences= models.ForeignKey(Conferences, verbose_name="Conferences",on_delete=models.CASCADE)

class bookmarks_vet_news(models.Model):
	doc= models.ForeignKey(Doctor,on_delete=models.CASCADE)
	vet_news= models.ForeignKey(Vet_News, verbose_name="Vet_News",on_delete=models.CASCADE)
class bookmarks_seminars(models.Model):
	doc= models.ForeignKey(Doctor,on_delete=models.CASCADE)
	seminars= models.ForeignKey(Seminars, verbose_name="Seminars",on_delete=models.CASCADE)

class bookmarks_books(models.Model):
	doc= models.ForeignKey(Doctor,on_delete=models.CASCADE)
	books= models.ForeignKey(Book, verbose_name="Book",on_delete=models.CASCADE)

class Vccination_Remainder(models.Model):
	pet = models.ForeignKey(Pet,on_delete=models.CASCADE)
	vacanation_list=models.TextField()
	customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
	hospital=models.CharField(max_length=50)
	doctor=models.CharField(max_length=30)
	remiander_date = models.DateField(default=date.today)
	date = models.DateField(default=date.today)
