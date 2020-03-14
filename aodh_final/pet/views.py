from django.shortcuts import render, redirect,HttpResponse
from .models import *
from django.forms.models import model_to_dict
from django.contrib.auth import login, authenticate ,logout
from django.contrib.auth.forms import UserCreationForm
from hashlib import sha1
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from datetime import  timedelta, date
import razorpay
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def doctor_login(request):
	if request.method == "POST":
		mobile=request.POST.get('username')
		password=request.POST.get('password')
		if Doctor.objects.filter(Mobile=mobile,password=password) is not None:
			doc_pk=Doctor.objects.get(Mobile=mobile).id
			request.session['doctor_session_id']=doc_pk
			return redirect ('list_patient',doc_id=doc_pk)
	return render (request,'doctor/Doctor_login.html')



def list_patient(request,doc_id):
	today_date=date.today()
	doc_pk=Doctor.objects.get(id=doc_id)
	doc_list_qs = DoctorLogList.objects.filter(doc_pk=doc_pk)
	if request.method == "GET":
		if 'doctor_session_id' in request.session:
			return render(request,'doctor/Doctor_list_of_patients.html',
			{'doc_list_qs':doc_list_qs,'today_date':today_date,'doc_id':doc_id})
		else:
			return redirect('doctor_login')
	if request.method=='POST':
		purpose_pk=request.POST.get('purpose_id')
		pet_pk = request.POST.get('pet_id')
		return redirect ('visit_purpose2',pet_pk=pet_pk,purpose_pk=purpose_pk,doc_id=doc_id)
	return render(request,'doctor/Doctor_list_of_patients.html',{'doc_list_qs':doc_list_qs,'today_date':today_date,'doc_id':doc_id})

def visit_purpose2(request,pet_pk,purpose_pk,doc_id):
	purpose_pet_obj=PurposeAndDiet.objects.get(id=purpose_pk)
	pet_obj=Pet.objects.filter(id=pet_pk).last()
	purpose_pet_obj_diet=PurposeAndDiet.objects.filter(id=purpose_pk).last()

	purpose_pk=purpose_pk
	if request.method == "GET":
		if 'doctor_session_id' in request.session:
			return render(request,'doctor/Doctor_visit_purpose.html',{'pet_pk':pet_pk,'purpose_pk':purpose_pk,'purpose_pet_obj':purpose_pet_obj,'pet_obj':pet_obj,
			'purpose_pet_obj_diet':purpose_pet_obj_diet,'doc_id':doc_id})
		else:
			return redirect('doctor_login')
	if request.method=='POST':
		return redirect('summary',pet_pk=pet_pk,purpose_pk=purpose_pk)


def symptoms(request,pet_pk,purpose_pk,doc_id):
	pet_obj=Pet.objects.filter(id=pet_pk).last()
	purpose_pet_obj_diet=PurposeAndDiet.objects.filter(id=purpose_pk).last()
	purpose_pk=purpose_pk
	purpose_pet_obj=PurposeAndDiet.objects.get(id=purpose_pk)
	if request.method == "GET":
		if 'doctor_session_id' in request.session:
			return render(request,'doctor/Doctor_symptoms.html',{'pet_pk':pet_pk,'purpose_pet_obj':purpose_pet_obj,'purpose_pk':purpose_pk,'pet_obj':pet_obj,
			'purpose_pet_obj_diet':purpose_pet_obj_diet,'doc_id':doc_id})
		else:
			return redirect('doctor_login')


def vitals(request,pet_pk,purpose_pk,doc_id):
	pet_obj=Pet.objects.filter(id=pet_pk).last()
	purpose_pet_obj_diet=PurposeAndDiet.objects.filter(id=purpose_pk).last()
	purpose_pet_obj=PurposeAndDiet.objects.get(id=purpose_pk)
	purpose_pet_obj_id=purpose_pet_obj.id
	if pet_pk:
		pet_pk=pet_pk
	if request.method == "GET":
		if 'doctor_session_id' in request.session:
			return render(request,'doctor/Doctor_Vitals.html',{'pet_obj':pet_obj,
		'purpose_pet_obj_diet':purpose_pet_obj_diet,'doc_id':doc_id})
		else:
			return redirect('doctor_login')
	if pet_pk:
		pet_pk=pet_pk
		try:
			if request.method=='POST':
						vitals=Vitals()
						vitals.purpose_id=purpose_pet_obj
						vitals.Temperature=request.POST.get('Temperature')
						vitals.Height=request.POST.get('Height')
						vitals.Weight=request.POST.get('Weight')
						vitals.Pulse_rate=request.POST.get('Pulse_rate')
						vitals.Respiration_rate=request.POST.get('Respiration_rate')
						vitals.Age_of_maturity=request.POST.get('Age_of_maturity')
						vitals.Oestrus=request.POST.get('Oestrus')
						vitals.Pregnancy=request.POST.get('Pregnancy')
						vitals.save()
						return redirect('assessment',pet_pk=pet_pk,purpose_pk=purpose_pk,doc_id=doc_id)
		except:
					if Vitals.objects.filter(purpose_id=purpose_pet_obj).exists:
						vitals=Vitals.objects.get(purpose_id=purpose_pet_obj)
						vitals_id=vitals.id
						if request.method=='POST':
							vitals=Vitals()
							purpose_id1=purpose_pet_obj
							purpose_id=purpose_id1
							Temperature=request.POST.get('Temperature')
							Temperature=Temperature
							Height=request.POST.get('Height')
							Height=Height
							Weight=request.POST.get('Weight')
							Weight=Weight
							Pulse_rate=request.POST.get('Pulse_rate')
							Pulse_rate=Pulse_rate
							Respiration_rate=request.POST.get('Respiration_rate')
							Respiration_rate=Respiration_rate
							Age_of_maturity=request.POST.get('Age_of_maturity')
							Age_of_maturity=Age_of_maturity
							Oestrus=request.POST.get('Oestrus')
							Oestrus=Oestrus
							Pregnancy=request.POST.get('Pregnancy')
							Pregnancy=Pregnancy
							Vitals.objects.filter(id=vitals_id).update(purpose_id=purpose_id,Temperature=Temperature,
							Height=Height,Weight=Weight,Pulse_rate=Pulse_rate,Respiration_rate=Respiration_rate,
							Age_of_maturity=Age_of_maturity,Oestrus=Oestrus,Pregnancy=Pregnancy)
						return redirect('assessment',pet_pk=pet_pk,purpose_pk=purpose_pk,doc_id=doc_id)


def Assessment_view(request,pet_pk,purpose_pk,doc_id):
	pet_obj=Pet.objects.filter(id=pet_pk).last()
	purpose_pet_obj_diet=PurposeAndDiet.objects.filter(id=purpose_pk).last()
	purpose_pet_obj=PurposeAndDiet.objects.get(id=purpose_pk)
	if pet_pk:
		pet_pk=pet_pk
	if request.method == "GET":
		if 'doctor_session_id' in request.session:
			return render(request,'doctor/Doctor_assessment.html',{'pet_obj':pet_obj,
				'purpose_pet_obj_diet':purpose_pet_obj_diet,'doc_id':doc_id})
		else:
			return redirect('doctor_login')
	try:
		if request.method=="POST":
			assessment=Assessment()
			assessment.purpose_id=purpose_pet_obj
			assessment.DERMATOLOGY=request.POST.getlist('DERMATOLOGY')
			assessment.EYES=request.POST.getlist('EYES')
			assessment.LUNGS=request.POST.getlist('LUNGS')
			assessment.EARS=request.POST.getlist('EARS')
			assessment.GASTROINTESTINAL=request.POST.getlist('GASTROINTESTINAL')
			assessment.NOSE_THROAT=request.POST.getlist('NOSE_THROAT')
			assessment.UROGENITAL=request.POST.getlist('UROGENITAL')
			assessment.MOUTH_TEETH_GUMS=request.POST.getlist('MOUTH_TEETH_GUMS')
			assessment.MUSKULOSKELETAL=request.POST.getlist('MUSKULOSKELETAL')
			assessment.HEART=request.POST.getlist('HEART')
			assessment.others=request.POST.get('others')
			assessment.save()
			return redirect('diagnostic_prescription',pet_pk=pet_pk,purpose_pk=purpose_pk,doc_id=doc_id)
	except:
		if Assessment.objects.filter(purpose_id=purpose_pet_obj).exists:
			assessment=Assessment.objects.get(purpose_id=purpose_pet_obj)
			assessment_id=assessment.id
			if request.method=="POST":
				purpose_id=purpose_pet_obj
				DERMATOLOGY=request.POST.getlist('DERMATOLOGY')
				EYES=request.POST.getlist('EYES')
				LUNGS=request.POST.getlist('LUNGS')
				EARS=request.POST.getlist('EARS')
				GASTROINTESTINAL=request.POST.getlist('GASTROINTESTINAL')
				NOSE_THROAT=request.POST.getlist('NOSE_THROAT')
				UROGENITAL=request.POST.getlist('UROGENITAL')
				MOUTH_TEETH_GUMS=request.POST.getlist('MOUTH_TEETH_GUMS')
				MUSKULOSKELETAL=request.POST.getlist('MUSKULOSKELETAL')
				HEART=request.POST.getlist('HEART')
				others=request.POST.get('others')
				Assessment.objects.filter(id=assessment_id).update(DERMATOLOGY=DERMATOLOGY,EYES=EYES,
				LUNGS=LUNGS,EARS=EARS,GASTROINTESTINAL=GASTROINTESTINAL,NOSE_THROAT=NOSE_THROAT,UROGENITAL=UROGENITAL,
				MOUTH_TEETH_GUMS=MOUTH_TEETH_GUMS,MUSKULOSKELETAL=MUSKULOSKELETAL,HEART=HEART,others=others)
				return redirect('diagnostic_prescription',pet_pk=pet_pk,purpose_pk=purpose_pk,doc_id=doc_id)


def diagnostic(request,pet_pk,purpose_pk,doc_id):
	pet_obj=Pet.objects.filter(id=pet_pk).last()
	purpose_pet_obj_diet=PurposeAndDiet.objects.filter(id=purpose_pk).last()
	purpose_pet_obj=PurposeAndDiet.objects.get(id=purpose_pk)
	if request.method == "GET":
		if 'doctor_session_id' in request.session:
			return render(request,'doctor/Doctor_diagnostics_and_prescription.html',{'pet_obj':pet_obj,
			'purpose_pet_obj_diet':purpose_pet_obj_diet,'doc_id':doc_id})
		else:
			return redirect('doctor_login')
	try:
		if request.method=='POST':
			purpose_pet_obj=PurposeAndDiet.objects.get(id=purpose_pk)
			diagnostic=Diagnostics()
			diagnostic.purpose_id=purpose_pet_obj
			diagnostic.haematology=request.POST.getlist('haematology')
			diagnostic.biochemistry=request.POST.getlist('biochemistry')
			diagnostic.harmones=request.POST.getlist('harmones')
			diagnostic.microbiology=request.POST.getlist('microbiology')
			diagnostic.parasitology=request.POST.getlist('parasitology')
			diagnostic.serology=request.POST.getlist('serology')
			diagnostic.cytology=request.POST.getlist('cytology')
			diagnostic.rapid_test=request.POST.getlist('rapid test')
			diagnostic.others=request.POST.get('others')
			diagnostic.save()
			prescription=Prescription()
			prescription.purpose_id=purpose_pet_obj
			medicine1=request.POST.get('medicine1')
			medicine1_time=request.POST.get('medicine1_time')
			prescription.medicine1=medicine1+'  '+medicine1_time
			medicine2=request.POST.get('medicine2')
			medicine2_time=request.POST.get('medicine2_time')
			prescription.medicine2=medicine2+'  '+medicine2_time
			medicine3=request.POST.get('medicine3')
			medicine3_time=request.POST.get('medicine3_time')
			prescription.medicine3=medicine3+'  '+medicine3_time
			medicine4=request.POST.get('medicine4')
			medicine4_time=request.POST.get('medicine4_time')
			prescription.medicine4=medicine4+'  '+medicine4_time
			medicine5=request.POST.get('medicine5')
			medicine5_time=request.POST.get('medicine5_time')
			prescription.medicine5=medicine5+' '+medicine5_time
			medicine6=request.POST.get('medicine6')
			medicine6_time=request.POST.get('medicine6_time')
			prescription.medicine6=medicine6+'  '+medicine6_time
			medicine7=request.POST.get('medicine7')
			medicine7_time=request.POST.get('medicine7_time')
			prescription.medicine7=medicine7+'  '+medicine7_time
			prescription.medicine_other=request.POST.get('medicine_other')
			prescription.save()
			return redirect('visit_purpose2',pet_pk=pet_pk,purpose_pk=purpose_pk,doc_id=doc_id)
	except:
		if Diagnostics.objects.filter(purpose_id=purpose_pet_obj).exists or Prescription.objects.filter(purpose_id=purpose_pet_obj).exists :
			diagnostic_id=Diagnostics.objects.get(purpose_id=purpose_pet_obj).id
			prescription_id=Prescription.objects.get(purpose_id=purpose_pet_obj).id
			if request.method=='POST':
				purpose_pet_obj=PurposeAndDiet.objects.get(id=purpose_pk)
				diagnostic=Diagnostics()
				purpose_id=purpose_pet_obj
				haematology=request.POST.getlist('haematology')
				biochemistry=request.POST.getlist('biochemistry')
				harmones=request.POST.getlist('harmones')
				microbiology=request.POST.getlist('microbiology')
				parasitology=request.POST.getlist('parasitology')
				serology=request.POST.getlist('serology')
				cytology=request.POST.getlist('cytology')
				rapid_test=request.POST.getlist('rapid test')
				others=request.POST.get('others')
				prescription=Prescription()
				prescription.purpose_id=purpose_pet_obj
				medicine1=request.POST.get('medicine1')
				medicine1_time=request.POST.get('medicine1_time')
				medicine1=medicine1+'  '+medicine1_time
				medicine2=request.POST.get('medicine2')
				medicine2_time=request.POST.get('medicine2_time')
				medicine2=medicine2+'  '+medicine2_time
				medicine3=request.POST.get('medicine3')
				medicine3_time=request.POST.get('medicine3_time')
				medicine3=medicine3+'  '+medicine3_time
				medicine4=request.POST.get('medicine4')
				medicine4_time=request.POST.get('medicine4_time')
				medicine4=medicine4+'  '+medicine4_time
				medicine5=request.POST.get('medicine5')
				medicine5_time=request.POST.get('medicine5_time')
				medicine5=medicine5+' '+medicine5_time
				medicine6=request.POST.get('medicine6')
				medicine6_time=request.POST.get('medicine6_time')
				medicine6=medicine6+'  '+medicine6_time
				medicine7=request.POST.get('medicine7')
				medicine7_time=request.POST.get('medicine7_time')
				medicine7=medicine7+'  '+medicine7_time
				medicine_other=request.POST.get('medicine_other')

				Diagnostics.objects.filter(id=diagnostic_id).update(haematology=haematology,biochemistry=biochemistry,
				harmones=harmones,microbiology=microbiology,parasitology=parasitology,serology=serology,cytology=cytology,
				rapid_test=rapid_test,others=others)
				Prescription.objects.filter(id=prescription_id).update(medicine1=medicine1,medicine2=medicine2,medicine3=medicine3,
				medicine4=medicine4,medicine5=medicine5,medicine6=medicine6,medicine7=medicine7,medicine_other=medicine_other)

				return redirect('visit_purpose2',pet_pk=pet_pk,purpose_pk=purpose_pk,doc_id=doc_id)

def set_id():
    pet = Pet.objects.all()
    pet_id = 'PET' + str(len(pet) + 1)
    return pet_id
def datenone(value):
	if value=="":
		value='1000-01-01'
	else:
		value=value
	return value
def vaccination(request,pet_pk,purpose_pk,doc_id):
	pet_obj=Pet.objects.filter(id=pet_pk).last()
	purpose_pet_obj_diet=PurposeAndDiet.objects.filter(id=purpose_pk).last()
	pet_obj=Pet.objects.get(id=pet_pk)
	purpose_pet_obj_save=PurposeAndDiet.objects.filter(pet_id=pet_obj).last()
	purpose_pet_obj=PurposeAndDiet.objects.filter(pet_id=pet_obj).last()
	vaccination=Vaccination.objects.filter(pet=pet_obj)
	last_vaccination=Vaccination_coustmer.objects.filter(pet=pet_obj).last()
	if pet_pk:
		pet_pk=pet_pk
	if request.method == "GET":
		if 'doctor_session_id' in request.session:
			return render(request,'doctor/Doctor_vaccination.html',{'last_vaccination':last_vaccination,'pet_obj':pet_obj,
			'purpose_pet_obj_diet':purpose_pet_obj_diet,'doc_id':doc_id,'vaccination':vaccination})
		else:
			return redirect('doctor_login')
	try:
		if request.method=='POST':
			vaccination=Vaccination()
			vaccination.purpose_id = purpose_pet_obj_save
			vaccination.pet=pet_obj
			last_date_rabies = request.POST.get('l_rabies')
			last_date_rabies = datenone(last_date_rabies)
			vaccination.last_date_rabies=last_date_rabies
			due_date_rabies=request.POST.get('d_rabies')
			due_date_rabies = datenone(due_date_rabies)
			vaccination.due_date_rabies=due_date_rabies
			last_date_distemper=request.POST.get('l_distemper')
			last_date_distemper = datenone(last_date_distemper)
			vaccination.last_date_distemper=last_date_distemper
			d_distemper=request.POST.get('d_distemper')
			d_distemper = datenone(d_distemper)
			vaccination.due_date_distemper=d_distemper
			last_date_hepatitis=request.POST.get('l_hepatitis')
			last_date_hepatitis = datenone(last_date_hepatitis)
			vaccination.last_date_hepatitis=last_date_hepatitis
			d_hepatitis=request.POST.get('d_hepatitis')
			d_hepatitis = datenone(d_hepatitis)
			vaccination.due_date_hepatitis=d_hepatitis
			last_date_parovirus=request.POST.get('l_parovirus')
			last_date_parovirus = datenone(last_date_parovirus)
			vaccination.last_date_parovirus=last_date_parovirus
			d_parovirus=request.POST.get('d_parovirus')
			d_parovirus = datenone(d_parovirus)
			vaccination.due_date_parovirus=d_parovirus
			last_date_parainfluenza=request.POST.get('l_parainfluenza')
			last_date_parainfluenza = datenone(last_date_parainfluenza)
			vaccination.last_date_parainfluenza=last_date_parainfluenza
			d_parainfluenza=request.POST.get('d_parainfluenza')
			d_parainfluenza = datenone(d_parainfluenza)
			vaccination.due_date_parainfluenza=d_parainfluenza
			last_date_bordetella=request.POST.get('l_bordetella')
			last_date_bordetella = datenone(last_date_bordetella)
			vaccination.last_date_bordetella=last_date_bordetella
			d_bordetella=request.POST.get('d_bordetella')
			d_bordetella = datenone(d_bordetella)
			vaccination.due_date_bordetella=d_bordetella
			last_date_leptospirosis=request.POST.get('l_leptospirosis')
			last_date_leptospirosis = datenone(last_date_leptospirosis)
			vaccination.last_date_leptospirosis=last_date_leptospirosis
			d_leptospirosis=request.POST.get('d_leptospirosis')
			d_leptospirosis = datenone(d_leptospirosis)
			vaccination.due_date_leptospirosis=d_leptospirosis
			last_date_lymedisease=request.POST.get('l_lymedisease')
			last_date_lymedisease = datenone(last_date_lymedisease)
			vaccination.last_date_lymedisease=last_date_lymedisease
			d_lymedisease=request.POST.get('d_lymedisease')
			d_lymedisease = datenone(d_lymedisease)
			vaccination.due_date_lymedisease=d_lymedisease
			last_date_coronavirus=request.POST.get('l_coronavirus')
			last_date_coronavirus = datenone(last_date_coronavirus)
			vaccination.last_date_coronavirus=last_date_coronavirus
			d_coronavirus=request.POST.get('d_coronavirus')
			d_coronavirus = datenone(d_coronavirus)
			vaccination.due_date_coronavirus=d_coronavirus
			last_date_giardia=request.POST.get('l_giardia')
			last_date_giardia = datenone(last_date_giardia)
			vaccination.last_date_giardia=last_date_giardia
			d_giardia=request.POST.get('d_giardia')
			d_giardia = datenone(d_giardia)
			vaccination.due_date_giardia=d_giardia
			last_date_dhpp=request.POST.get('l_dhpp')
			last_date_dhpp = datenone(last_date_dhpp)
			vaccination.last_date_dhpp=last_date_dhpp
			d_dhpp=request.POST.get('d_dhpp')
			d_dhpp = datenone(d_dhpp)
			vaccination.due_date_dhpp=d_dhpp
			vaccination.save()
			return redirect('visit_purpose2',pet_pk=pet_pk,purpose_pk=purpose_pk,doc_id=doc_id)
	except:
		if Vaccination.objects.filter(purpose_id=purpose_pet_obj_save).exists:
			vaccination_id=Vaccination.objects.get(purpose_id=purpose_pet_obj_save).id
			last_date_rabies = request.POST.get('l_rabies')
			last_date_rabies = datenone(last_date_rabies)
			last_date_rabies=last_date_rabies
			due_date_rabies=request.POST.get('d_rabies')
			due_date_rabies = datenone(due_date_rabies)
			due_date_rabies=due_date_rabies
			last_date_distemper=request.POST.get('l_distemper')
			last_date_distemper = datenone(last_date_distemper)
			last_date_distemper=last_date_distemper
			d_distemper=request.POST.get('d_distemper')
			d_distemper = datenone(d_distemper)
			due_date_distemper=d_distemper
			last_date_hepatitis=request.POST.get('l_hepatitis')
			last_date_hepatitis = datenone(last_date_hepatitis)
			last_date_hepatitis=last_date_hepatitis
			d_hepatitis=request.POST.get('d_hepatitis')
			d_hepatitis = datenone(d_hepatitis)
			due_date_hepatitis=d_hepatitis
			last_date_parovirus=request.POST.get('l_parovirus')
			last_date_parovirus = datenone(last_date_parovirus)
			last_date_parovirus=last_date_parovirus
			d_parovirus=request.POST.get('d_parovirus')
			d_parovirus = datenone(d_parovirus)
			due_date_parovirus=d_parovirus
			last_date_parainfluenza=request.POST.get('l_parainfluenza')
			last_date_parainfluenza = datenone(last_date_parainfluenza)
			last_date_parainfluenza=last_date_parainfluenza
			d_parainfluenza=request.POST.get('d_parainfluenza')
			d_parainfluenza = datenone(d_parainfluenza)
			due_date_parainfluenza=d_parainfluenza
			last_date_bordetella=request.POST.get('l_bordetella')
			last_date_bordetella = datenone(last_date_bordetella)
			last_date_bordetella=last_date_bordetella
			d_bordetella=request.POST.get('d_bordetella')
			d_bordetella = datenone(d_bordetella)
			due_date_bordetella=d_bordetella
			last_date_leptospirosis=request.POST.get('l_leptospirosis')
			last_date_leptospirosis = datenone(last_date_leptospirosis)
			last_date_leptospirosis=last_date_leptospirosis
			d_leptospirosis=request.POST.get('d_leptospirosis')
			d_leptospirosis = datenone(d_leptospirosis)
			due_date_leptospirosis=d_leptospirosis
			last_date_lymedisease=request.POST.get('l_lymedisease')
			last_date_lymedisease = datenone(last_date_lymedisease)
			last_date_lymedisease=last_date_lymedisease
			d_lymedisease=request.POST.get('d_lymedisease')
			d_lymedisease = datenone(d_lymedisease)
			due_date_lymedisease=d_lymedisease
			last_date_coronavirus=request.POST.get('l_coronavirus')
			last_date_coronavirus = datenone(last_date_coronavirus)
			last_date_coronavirus=last_date_coronavirus
			d_coronavirus=request.POST.get('d_coronavirus')
			d_coronavirus = datenone(d_coronavirus)
			due_date_coronavirus=d_coronavirus
			last_date_giardia=request.POST.get('l_giardia')
			last_date_giardia = datenone(last_date_giardia)
			last_date_giardia=last_date_giardia
			d_giardia=request.POST.get('d_giardia')
			d_giardia = datenone(d_giardia)
			due_date_giardia=d_giardia
			last_date_dhpp=request.POST.get('l_dhpp')
			last_date_dhpp = datenone(last_date_dhpp)
			last_date_dhpp=last_date_dhpp
			d_dhpp=request.POST.get('d_dhpp')
			d_dhpp = datenone(d_dhpp)
			due_date_dhpp=d_dhpp

			Vaccination.objects.filter(id=vaccination_id).update(last_date_rabies=last_date_rabies,last_date_distemper=last_date_distemper,
			due_date_rabies=due_date_rabies,last_date_hepatitis=last_date_hepatitis,due_date_hepatitis=due_date_hepatitis,last_date_parovirus=last_date_parovirus,
			due_date_parovirus=due_date_parovirus,last_date_parainfluenza=last_date_parainfluenza,due_date_parainfluenza=due_date_parainfluenza,
			last_date_bordetella=last_date_bordetella,due_date_bordetella=due_date_bordetella,last_date_leptospirosis=last_date_leptospirosis,
			due_date_leptospirosis=due_date_leptospirosis,last_date_lymedisease=last_date_lymedisease,due_date_lymedisease=due_date_lymedisease,
			last_date_coronavirus=last_date_coronavirus,due_date_coronavirus=due_date_coronavirus,last_date_giardia=last_date_giardia,due_date_giardia=due_date_giardia,
			last_date_dhpp=last_date_dhpp,due_date_dhpp=due_date_dhpp)
			return redirect('visit_purpose2',pet_pk=pet_pk,purpose_pk=purpose_pk,doc_id=doc_id)


def deworming(request,pet_pk,purpose_pk,doc_id):
	pet_obj=Pet.objects.filter(id=pet_pk).last()
	purpose_pet_obj_diet=PurposeAndDiet.objects.filter(id=purpose_pk).last()
	pet_obj=Pet.objects.get(id=pet_pk)
	purpose_pet_obj_save=PurposeAndDiet.objects.filter(pet_id=pet_obj).last()
	purpose_pet_obj=PurposeAndDiet.objects.filter(pet_id=pet_obj).all()
	cust_deworming=Vaccination_coustmer.objects.filter(pet=pet_obj).last()
	deworming=Deworming.objects.filter(pet=pet_obj)
	purpose_obj=PurposeAndDiet.objects.get(id=purpose_pk)
	if pet_pk:
		pet_pk=pet_pk

	if request.method == "GET":
		if 'doctor_session_id' in request.session:
			return render(request,'doctor/Doctor_deworming.html',{'last_deworming':deworming,'pet_obj':pet_obj,
			'purpose_pet_obj_diet':purpose_pet_obj_diet,'doc_id':doc_id,'cust_deworming':cust_deworming})
		else:
			return redirect('doctor_login')
	try:
		if request.method=='POST':
			deworming=Deworming()
			purpose_pet_obj_save=PurposeAndDiet.objects.filter(pet_id=pet_obj).last()
			deworming.purpose_id=purpose_pet_obj_save
			pet_obj=Pet.objects.filter(id=pet_pk).last()
			deworming.pet=pet_obj
			last_date=request.POST.get('current_date')
			last_date=datenone(last_date)
			deworming.last_date=last_date
			due_date=request.POST.get('due_date')
			due_date=datenone(due_date)
			deworming.due_date=due_date
			deworming.save()
			return redirect('visit_purpose2',pet_pk=pet_pk,purpose_pk=purpose_pk,doc_id=doc_id)
	except:
		if Deworming.objects.filter(purpose_id=purpose_pet_obj).exists:
			deworming_id=Deworming.objects.get(purpose_id=purpose_obj).id
			pet_obj=Pet.objects.filter(id=pet_pk).last()
			deworming.pet=pet_obj
			last_date=request.POST.get('current_date')
			last_date=datenone(last_date)
			last_date=last_date
			due_date=request.POST.get('due_date')
			due_date=datenone(due_date)
			due_date=due_date
			Deworming.objects.filter(id=deworming_id).update(last_date=last_date,due_date=due_date)
			return redirect('visit_purpose2',pet_pk=pet_pk,purpose_pk=purpose_pk,doc_id=doc_id)


def dict_clean(dict_data):
	dict_data.pop('purpose_id',None)
	dict_data.pop('id',None)
	clean_dict={}
	for k,v in dict_data.items():

		if v != 'NO' and v != '' and v !=None and v != 'no':
			if type(v) == str:
				v=v.replace('[','').replace("'",'').replace(']','').replace(',','').replace('(','').replace(')','')
				clean_dict[k]=v
			if type(v) == int:
				clean_dict[k]=v
	return clean_dict

import datetime
def date_clean(dict_data):
	clean_date={}
	for key,value in [value for value in dict_data if value == '1000-01-01']: del dict_data[key]

def customer_previous(request,customer_id,pet_id):

	if request.method == "GET":
		if 'customer_id' in request.session:
			customer_id=customer_id
			pet_obj=Pet.objects.get(pet_id=pet_id)
			purpose_pet_obj=PurposeAndDiet.objects.filter(pet_id=pet_obj).all()
			print(purpose_pet_obj)
			visite_on=date.today()
			return render(request,'customer/Customer_previous_visit.html',{'purpose_pet_obj':purpose_pet_obj})
		else:
			return redirect('customer_login_home')

def summary_customer(request,purpose_id):


	purpose_pet_obj=PurposeAndDiet.objects.get(id=purpose_id)
	visite_on=date.today()

	try:
		symptoms=Symptoms.objects.filter()
		symptoms=model_to_dict(symptoms)
		clean_dict = dict_clean(symptoms)
		clean_dict=remove_empty_from_dict(clean_dict)
		symptoms = clean_dict

	except:
		symptoms=''
	try:
		vitals=Vitals.objects.filter(purpose_id=purpose_pet_obj).last()
		vitals=model_to_dict(vitals)
		clean_dict = dict_clean(vitals)
		clean_dict=remove_empty_from_dict(clean_dict)
		vitals = clean_dict

	except:
		vitals=''

	try:
		assessment=Assessment.objects.filter(purpose_id=purpose_pet_obj).last()
		assessment=model_to_dict(assessment)
		clean_dict = dict_clean(assessment)
		clean_dict=remove_empty_from_dict(clean_dict)
		assessment = clean_dict
	except:
		assessment=''

	try:

		symptoms=symptoms=purpose_pet_obj
		symptoms=model_to_dict(symptoms)
		clean_dict = dict_clean(symptoms)
		clean_dict=remove_empty_from_dict(clean_dict)
		symptoms.pop('purpose_id',None)
		symptoms.pop('id',None)
		symptoms.pop('pet_id',None)
		symptoms.pop('set1',None)
		symptoms.pop('set2',None)
		symptoms.pop('vaccination_purpose',None)
		symptoms.pop('deworming_purpose',None)
		symptoms.pop('last_deworming',None)
		symptoms.pop('date',None)
	except:
		symptoms=''

	try:

		diagnostic=Diagnostics.objects.filter(purpose_id=purpose_pet_obj).last()
		diagnostic=model_to_dict(diagnostic)
		clean_dict = dict_clean(diagnostic)
		clean_dict=remove_empty_from_dict(clean_dict)
		diagnostic = clean_dict
	except:
		diagnostic=''

	try:
		prescription=Prescription.objects.filter(purpose_id=purpose_pet_obj).last()
		prescription=model_to_dict(prescription)
		prescription.pop('purpose_id',None)
		prescription.pop('id',None)
		clean_dict = dict_clean(prescription)
		clean_dict=remove_empty_from_dict(clean_dict)
	except:
		prescription=''

	try:
		vaccination=Vaccination.objects.filter(purpose_id=purpose_pet_obj).last()
		vaccination=model_to_dict(vaccination)
		vaccination.pop('purpose_id',None)
		vaccination.pop('id',None)
		vaccination.pop('date',None)
		vaccination.pop('pet',None)
		vaccination = { k:v for k,v in vaccination.items() if v!= datetime.date(1000, 1, 1) }

	except:
		pass
	try:
		deworming=Deworming.objects.filter(purpose_id=purpose_pet_obj).last()
		deworming=model_to_dict(deworming)
		deworming.pop('purpose_id',None)
		deworming.pop('id',None)
		deworming.pop('date',None)
		deworming.pop('pet',None)
		deworming = { k:v for k,v in deworming.items() if v!= datetime.date(1000, 1, 1) }
	except:
		pass
	if request.method == "GET":
		if 'customer_id' in request.session:
			return render(request,'customer/Customer_previous_visit_summary.html',{'symptoms':symptoms,'vitals':vitals,'assessment':assessment,'symptoms':symptoms,
				'diagnostic':diagnostic,'purpose_pet_obj':purpose_pet_obj,'vaccination':vaccination,'deworming':deworming,'prescription':prescription})
		else:
			return redirect('customer_login_home')

def remove_empty_from_dict(d):
    if type(d) is dict:
        return dict((k, remove_empty_from_dict(v)) for k, v in d.items() if v and remove_empty_from_dict(v))
    elif type(d) is list:
        return [remove_empty_from_dict(v) for v in d if v and remove_empty_from_dict(v)]
    else:
        return d

def summary(request,pet_pk,purpose_pk):
	purpose_pet_obj=PurposeAndDiet.objects.get(id=purpose_pk)
	visite_on=date.today()
	if pet_pk:
		pet_pk=pet_pk
	else:
		pass

	try:
		vitals=Vitals.objects.filter(purpose_id=purpose_pet_obj,date=visite_on).last()
		vitals=model_to_dict(vitals)
		clean_dict = dict_clean(vitals)
		vitals = clean_dict

	except:
		pass

	try:
		assessment=Assessment.objects.filter(purpose_id=purpose_pet_obj,date=visite_on).last()
		assessment=model_to_dict(assessment)
		clean_dict = dict_clean(assessment)
		clean_dict=remove_empty_from_dict(clean_dict)
		assessment = clean_dict
	except:
		pass

	try:

		symptoms=purpose_pet_obj
		symptoms=model_to_dict(symptoms)
		symptoms.pop('purpose_id',None)
		symptoms.pop('id',None)
		symptoms.pop('pet_id',None)

		symptoms.pop('vaccination_purpose',None)
		symptoms.pop('deworming_purpose',None)
		symptoms.pop('last_deworming',None)
		symptoms = dict_clean(symptoms)
	except:
		pass

	try:

		diagnostic=Diagnostics.objects.filter(purpose_id=purpose_pet_obj,date=visite_on).last()
		diagnostic=model_to_dict(diagnostic)
		clean_dict = dict_clean(diagnostic)
		diagnostic = remove_empty_from_dict(clean_dict)
	except:
		pass

	try:
		prescription=Prescription.objects.filter(purpose_id=purpose_pet_obj).last()
		prescription=model_to_dict(prescription)
		clean_dict=dict_clean(prescription)
		prescription=remove_empty_from_dict(prescription)
		prescription.pop('purpose_id',None)
		prescription.pop('id',None)
		prescription.pop('date',None)

	except:
		pass

	try:
		vaccination=Vaccination.objects.filter(purpose_id=purpose_pet_obj).last()
		vaccination=model_to_dict(vaccination)
		vaccination.pop('purpose_id',None)
		vaccination.pop('id',None)
		vaccination.pop('date',None)
		vaccination.pop('pet',None)
		vaccination = { k:v for k,v in vaccination.items() if v!= datetime.date(1000, 1, 1) }
	except:
		pass
	try:
		deworming=Deworming.objects.filter(purpose_id=purpose_pet_obj).last()
		deworming=model_to_dict(deworming)
		deworming.pop('purpose_id',None)
		deworming.pop('id',None)
		deworming.pop('date',None)
		deworming.pop('pet',None)
		deworming = { k:v for k,v in deworming.items() if v!= datetime.date(1000, 1, 1) }

	except:
		pass

	if request.method == "GET":
		if 'doctor_session_id' in request.session:
			return render(request,'doctor/Doctor_summary.html',{'symptoms':symptoms,'vitals':vitals,'assessment':assessment,'symptoms':symptoms,
				'diagnostic':diagnostic,'prescription':prescription,'vaccination':vaccination,'deworming':deworming,'visite_on':visite_on})
		else:
			return redirect('doctor_login')

	if request.method=='POST':
		doc_id = DoctorLogList.objects.filter(purpose_id=purpose_pet_obj).last().doc_pk
		doc_id=doc_id.id
		DoctorLogList.objects.filter(purpose_id=purpose_pet_obj).last().delete()
		return redirect	('list_patient',doc_id=doc_id)


def doctor(request):
	doclist=Doctor.objects.last()
	doclist=model_to_dict(doclist)
	if request.method == "GET":
		if 'doctor_session_id' in request.session:
			return render(request,'doctorreg.html',{'doclist':doclist})
		else:
			return redirect('doctor_login')
	if request.method=='POST':
		doctor=Doctor()
		doctor.Name_of_doctor=request.POST.get('Name_of_doctor')
		doctor.Qualification=request.POST.get('Qualification')
		doctor.Registration_number=request.POST.get('Registration_number')
		doctor.Gender=request.POST.get('Gender')
		doctor.Date_of_birth=request.POST.get('Date_of_birth')
		doctor.Experience=request.POST.get('Experience')
		doctor.Hospital=request.POST.get('Hospital')
		doctor.Email=request.POST.get('Email')
		doctor.Mobile=request.POST.get('Mobile')
		doctor.Telephone=request.POST.get('Telephone')
		doctor.Address=request.POST.get('Address')
		doctor.save()
		return render(request,'doctorreg.html')



def doctoranalytics(request,doc_id):
	pet_id=DoctorViewLog.objects.filter(doc_pk=doc_id).all()
	if request.method == "GET":
		if 'doctor_session_id' in request.session:
			return render(request,'doctoranalytics.html',{'pet_id':pet_id,'doc_id':doc_id})
		else:
			return redirect('doctor_login')
	if request.method=='POST':
		visit_date=request.POST.get('visit_date')
		pet=request.POST.get('pet')
		id_pk=request.POST.get('pk')
		fee=Log.objects.filter(date=visit_date)
		print('fefeffee',fee)
		pet_2=[]
		for i in fee:
			pet_1=i.purpose_id
			pet_2.append(pet_1)
		for i in pet_2:
			pet_3=i.pet_id.pet_id
		try:
			symptoms=Symptoms.objects.filter(date=visit_date)
		except:
			pass
		pet_obj=Pet.objects.filter(pet_id=pet)

		x=PurposeAndDiet.objects.filter(pet_id__pet_id=pet)
		return render(request,'doctor/doctor_analytics.html',{'visit_date':visit_date,'pk':id_pk,'pet':pet,'fee':fee,'x':x,
			'symptoms':symptoms,'doc_id':doc_id})

def summary_analytics(request,pk,value,doc_id):
	if pk:
		pk=pk
	else:
		pass

	if value:
		value=value
	else:
		pass
	try:
		symptoms=Symptoms.objects.filter(purpose_id__pet_id__pet_id=value).last()
		print(symptoms)
		symptoms=model_to_dict(symptoms)
		symptoms.pop('purpose_id',None)
		symptoms.pop('id',None)
		symptoms.pop('date',None)
		clean_dict = dict_clean(symptoms)
		symptoms=remove_empty_from_dict(clean_dict)
	except:
		pass
	try:
		vitals=Vitals.objects.filter(purpose_id__pet_id__pet_id=value).last()
		vitals=model_to_dict(vitals)
		vitals.pop('purpose_id',None)
		vitals.pop('id',None)
		vitals.pop('date',None)
		clean_dict = dict_clean(vitals)
		vitals=remove_empty_from_dict(clean_dict)
	except:
		pass
	try:
		diagnostics=Diagnostics.objects.filter(purpose_id__pet_id__pet_id=value).last()
		diagnostics=model_to_dict(diagnostics)
		diagnostics.pop('purpose_id',None)
		diagnostics.pop('id',None)
		diagnostics.pop('date',None)
		clean_dict = dict_clean(diagnostics)
		diagnostics=remove_empty_from_dict(clean_dict)
	except:
		pass
	try:
		prescription=Prescription.objects.filter(purpose_id__pet_id__pet_id=value).last()
		prescription=model_to_dict(prescription)
		prescription.pop('purpose_id',None)
		prescription.pop('id',None)
		prescription.pop('date',None)
		clean_dict = dict_clean(prescription)
		prescription=remove_empty_from_dict(clean_dict)

	except:
		pass
	try:
		assessment=Assessment.objects.filter(purpose_id__pet_id__pet_id=value).last()
		assessment=model_to_dict(assessment)
		assessment.pop('purpose_id',None)
		assessment.pop('id',None)
		assessment.pop('date',None)
		clean_dict = dict_clean(assessment)
		assessment=remove_empty_from_dict(clean_dict)
	except:
		pass
	try:
		deworming=Deworming.objects.filter(purpose_id__pet_id__pet_id=value).last()
		deworming=model_to_dict(deworming)
		deworming.pop('purpose_id',None)
		deworming.pop('id',None)
		deworming.pop('date',None)
		deworming.pop('pet',None)
		deworming = { k:v for k,v in deworming.items() if v!= datetime.date(1000, 1, 1) }
	except:
		pass
	try:
		vaccination=Vaccination.objects.filter(purpose_id__pet_id__pet_id=value).last()
		vaccination=model_to_dict(vaccination)
		vaccination.pop('purpose_id',None)
		vaccination.pop('id',None)
		vaccination.pop('date',None)
		vaccination.pop('pet',None)
		vaccination = { k:v for k,v in vaccination.items() if v!= datetime.date(1000, 1, 1) }
	except:
		pass
	if request.method == "GET":
		if 'doctor_session_id' in request.session:
			return render (request,'doctor/summary_analytics.html',{'pk':pk,'symptoms':symptoms,'vitals':vitals,'diagnostic':diagnostics,
				'prescription':prescription,'assessment':assessment,'deworming':deworming,'doc_id':doc_id,'vaccination':vaccination})
		else:
			return redirect('doctor_login')
def doctor_profile(request,doc_id):
	doc=Doctor.objects.get(id=doc_id)
	return render(request,'doctor/doctor_profile.html',{'doc':doc})

def doctor_history(request,pet_pk,purpose_pk):
	today_date=date.today()
	pet_obj=Pet.objects.get(id=pet_pk)
	pet_obj=pet_obj
	purpose_obj=PurposeAndDiet.objects.filter(pet_id=pet_obj).exclude(date=today_date).all()
	if request.method == "GET":
		if 'doctor_session_id' in request.session:
			return render(request,'doctor/Doctor_previous_visit.html',{'purpose_obj':purpose_obj})
		else:
			return redirect('doctor_login')
	if request.method=='POST':
		visite_on=request.POST.get('date')
		obj=request.POST.get('obj')
		return redirect('doctor_history_summary',pet_pk=pet_pk,purpose_pk=obj)

def doctor_history_summary(request,pet_pk,purpose_pk):
	purpose_pet_obj=PurposeAndDiet.objects.get(id=purpose_pk)
	try:
		vitals=Vitals.objects.filter(purpose_id=purpose_pet_obj).last()
		vitals=model_to_dict(vitals)
		clean_dict = dict_clean(vitals)
		vitals = remove_empty_from_dict(clean_dict)
	except:
		pass
	try:
		assessment=Assessment.objects.filter(purpose_id=purpose_pet_obj).last()
		assessment=model_to_dict(assessment)
		print(type(assessment))
		clean_dict = dict_clean(assessment)
		assessment = remove_empty_from_dict(clean_dict)
	except:
		pass
	try:
		symptoms=purpose_pet_obj
		symptoms=model_to_dict(symptoms)
		symptoms.pop('purpose_id',None)
		symptoms.pop('id',None)
		symptoms.pop('pet_id',None)
		symptoms.pop('set1',None)
		symptoms.pop('set2',None)
		symptoms.pop('vaccination_purpose',None)
		symptoms.pop('new_diet',None)
		symptoms.pop('new_diet_state',None)
		symptoms.pop('deworming_purpose',None)
		symptoms.pop('last_deworming',None)
		clean_dict=dict_clean(symptoms)
		symptoms=remove_empty_from_dict(clean_dict)
	except:
		pass
	try:
		diagnostic=Diagnostics.objects.filter(purpose_id=purpose_pet_obj).last()
		diagnostic=model_to_dict(diagnostic)
		clean_dict = dict_clean(diagnostic)
		diagnostic = remove_empty_from_dict(clean_dict)
	except:
		pass
	try:
		prescription=Prescription.objects.filter(purpose_id=purpose_pet_obj).last()
		prescription=model_to_dict(prescription)
		prescription.pop('purpose_id',None)
		prescription.pop('id',None)
		prescription.pop('date',None)
		clean_dict=dict_clean(prescription)
		prescription=remove_empty_from_dict(prescription)
	except:
		pass
	try:
		vaccination=Vaccination.objects.filter(purpose_id=purpose_pet_obj).last()
		vaccination=model_to_dict(vaccination)
		vaccination.pop('purpose_id',None)
		vaccination.pop('id',None)
		vaccination.pop('date',None)
		vaccination.pop('pet',None)
		vaccination = { k:v for k,v in vaccination.items() if v!= datetime.date(1000, 1, 1) }
	except:
		pass
	try:
		deworming=Deworming.objects.filter(purpose_id=purpose_pet_obj).last()
		deworming=model_to_dict(deworming)
		deworming.pop('purpose_id',None)
		deworming.pop('id',None)
		deworming.pop('date',None)
		deworming.pop('pet',None)
		deworming = { k:v for k,v in deworming.items() if v!= datetime.date(1000, 1, 1) }
	except:
		pass
	if request.method == "GET":
		if 'doctor_session_id' in request.session:
			return render(request,'doctor/doctor_history_summary.html',{'symptoms':symptoms,'vitals':vitals,'assessment':assessment,'symptoms':symptoms,
				'diagnostic':diagnostic,'prescription':prescription,'vaccination':vaccination,'deworming':deworming})
		else:
			return redirect('doctor_login')
def purpose_visit(request,customer_id,pet_id,doc_pk_org,purpose_id):
	pets=Pet.objects.filter(customer_id=customer_id).all()
	purpose_id=purpose_id
	doc_pk=doc_pk_org
	customer_id=customer_id
	x = Pet.objects.filter(pet_id=pet_id).last()
	pet_obj=PurposeAndDiet.objects.filter(pet_id=x).last()
	pet_obj = pet_obj.id
	if request.method == "GET":
		if 'customer_id' in request.session:
			return render(request,'customer/Customer_purpose_of_the_visit.html',{'customer_id':customer_id,'x':x,'pets':pets})
		else:
			return redirect('customer_login_home')
	if request.method=='POST':
		purpose=PurposeAndDiet()
		vaccination_purpose=request.POST.get('purpose')
		disease=request.POST.get('disease')
		disease=empty_string_remove(disease)
		symptoms_text=request.POST.get('symptoms_text')
		hello = PurposeAndDiet.objects.filter(id=pet_obj).update(vaccination_purpose=vaccination_purpose,symptoms_text=symptoms_text,disease=disease)
		return redirect('booking_summary',customer_id=customer_id,pet_id=pet_id,doc_pk=doc_pk,purpose_id=purpose_id)
def empty_string_remove(values):
    values=values.split(',')
    if ('' in values):
        values.remove('')
    else:
        values=values
    return ','.join(values)

def booking_summary(request,customer_id,pet_id,purpose_id,doc_pk):
	pets_obj=Pet.objects.filter(customer_id=customer_id).all()
	doc_pk=doc_pk
	customer_id=Customer.objects.get(customer_id=customer_id)
	email=customer_id.email
	mobile=customer_id.mobile
	doctor_id=DoctorViewLog.objects.filter(customer_id=customer_id).last()
	doctor_id=doctor_id.doc_pk
	doctor_id=doctor_id.id
	doctor_name=Doctor.objects.get(id=doctor_id)
	doctor_name=doctor_name.Name_of_doctor
	pets=Pet.objects.filter(pet_id=pet_id).last()
	purpose1=PurposeAndDiet.objects.filter(pet_id=pets).last()
	purpose1=purpose1.pet_id.customer_id
	visit_purpose=PurposeAndDiet.objects.filter(pet_id=pets).last()
	visit_purpose=model_to_dict(visit_purpose)
	visit_purpose.pop("id", None)
	visit_purpose.pop("pet_id", None)
	visit_purpose.pop("set1", None)
	visit_purpose.pop("set2", None)
	visit_purpose.pop("deworming_purpose", None)
	visit_purpose.pop("date", None)
	visit_purpose.pop("last_deworming", None)
	doc_pk_1=DoctorViewLog.objects.filter(doc_pk__id=doc_pk).last()
	doc_pk_1=doc_pk_1.doc_pk
	doctor_fee_obj=Doctor.objects.get(id=doctor_id)
	fee=doctor_fee_obj.consultation_fee
	sub_total=fee+20
	client = razorpay.Client(auth=("rzp_test_YZmJYi68GuRjEX", "gP35hDt1UB7uIDE7ivlFU9Ou"))
	DATA={
	"amount": sub_total,
	"currency": "INR",
	"payment_capture":'1',
	"notes" : {'Shipping address':'hrllll, hyd'}
	}
	order=client.order.create(data=DATA)
	order_id=order.get("id","")
	print(order,'orderdetailsssssssssss')
	if request.method == "GET":
		if 'customer_id' in request.session:
			return render(request,'customer/Customer_booking_summary.html',{'customer_id':customer_id,'doctor_name':doctor_name,'visit_purpose':visit_purpose,'fee':fee,
			'sub_total':sub_total,'pets':pets_obj,'order_id':order_id,"email":email,'mobile':mobile,'doc_pk':doc_pk,'purpose_id':purpose_id,'pet_id':pet_id})
		else:
			return redirect('customer_login_home')
	if request.method == "POST":
		if "pay_at_clinic" in request.POST:
			pass
			return redirect('booking_confirm',customer_id=customer_id,doc_pk=doc_pk,pet_id=pet_id,purpose_id=purpose_id)
		else:
			pass
			return redirect('pay_online_conform',customer_id=customer_id,doc_pk=doc_pk,pet_id=pet_id,purpose_id=purpose_id)
@csrf_exempt
def booking_confirm(request,customer_id,doc_pk,pet_id,purpose_id):
	doctorloglist=DoctorLogList()
	doctorloglist.customer_id=Customer.objects.get(customer_id=customer_id)
	doctorloglist.pet_id=Pet.objects.get(pet_id=pet_id)
	doctorloglist.purpose_id=PurposeAndDiet.objects.get(id=purpose_id)
	doc_pk_1=DoctorViewLog.objects.filter(doc_pk__id=doc_pk).last()
	doc_pk_1=doc_pk_1.doc_pk
	doctorloglist.doc_pk=doc_pk_1
	doctorloglist.payment='collect cash'
	doctorloglist.color='lightgreen'
	log=Log()
	doc=Doctor.objects.get(id=doc_pk)
	log.doctor=doc
	fee=doc.consultation_fee
	log.consultation_fee=fee
	log.final_fee=fee+20
	log.customer=Customer.objects.get(customer_id=customer_id)
	log.purpose_id=PurposeAndDiet.objects.get(id=purpose_id)
	log.pet_id=pet_id
	doctorloglist.save()
	log.save()
	pets=Pet.objects.filter(customer_id=customer_id).all()
	return render(request,'customer/Customer_booking__confirmed.html',{'customer_id':customer_id,'doc_pk':doc_pk,'pets':pets})

@csrf_exempt
def pay_online_conform(request,customer_id,doc_pk,pet_id,purpose_id):
	doctorloglist=DoctorLogList()
	doctorloglist.customer_id=Customer.objects.get(customer_id=customer_id)
	doctorloglist.pet_id=Pet.objects.get(pet_id=pet_id)
	doctorloglist.purpose_id=PurposeAndDiet.objects.get(id=purpose_id)
	doc_pk_1=DoctorViewLog.objects.filter(doc_pk__id=doc_pk).last()
	doc_pk_1=doc_pk_1.doc_pk
	doctorloglist.doc_pk=doc_pk_1
	doctorloglist.payment='paid online'
	doctorloglist.color='lightgreen'
	log=Log()
	doc=Doctor.objects.get(id=doc_pk)
	log.doctor=doc
	fee=doc.consultation_fee
	log.consultation_fee=fee
	log.final_fee=fee+20
	log.customer=Customer.objects.get(customer_id=customer_id)
	log.purpose_id=PurposeAndDiet.objects.get(id=purpose_id)
	log.pet_id=pet_id
	doctorloglist.save()
	log.save()
	pets=Pet.objects.filter(customer_id=customer_id).all()
	return render(request,'customer/Customer_booking__confirmed.html',{'customer_id':customer_id,'doc_pk':doc_pk,'pets':pets})

def pet_profile(request,customer_id):
	customer_id=customer_id
	pet_profile=Pet.objects.filter(customer_id=customer_id).all()
	return render(request,'customer/Customer_pet_profile.html',{'pet_profile':pet_profile})

def last_vaccination(request,customer_id):
	pet_id=customer_id
	pet_obj=Pet.objects.filter(pet_id=pet_id).last()
	purpose_pet_obj=PurposeAndDiet.objects.filter(pet_id=pet_obj).last()
	vaccination=Vaccination.objects.filter(pet=pet_obj)
	x=['Jan. 1, 1000']
	last_vaccination=Vaccination_coustmer.objects.filter(pet=pet_obj).last()
	return render(request,'customer/Customer_vaccination_history.html',{'last_vaccination':last_vaccination,'vaccination':vaccination,'x':x})

def last_deworming(request,customer_id):
	pet_id=customer_id
	pet_obj=Pet.objects.filter(pet_id=pet_id).last()
	purpose_pet_obj=Vaccination_coustmer.objects.filter(pet=pet_obj).last()
	last_deworming=Deworming.objects.filter(pet=pet_obj)
	return render(request,'customer/Customer_deworming_history.html',{'last_deworming':last_deworming,'purpose_pet_obj':purpose_pet_obj})


def cust_id():
    coustmer_id = Customer.objects.all()
    coustmer_id = 'AODH' + str(len(coustmer_id) + 1)
    return coustmer_id

def social_cust_id():
    social_coustmer_id = sociallogin.objects.all()
    social_coustmer_id = 'USER' + str(len(social_coustmer_id) + 1)
    return social_coustmer_id

def customer_registration(request,pk=None):
	customer = Customer()
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
		doc_ip=docip()
		docid=pk
		docobj=Doctor.objects.get(id=docid)
		doc_ip.doc_id=docobj
		doc_ip.ip=ip
		doc_ip.save()
		doctorviewlog=DoctorViewLog()
	if pk :
		doctor=Doctor.objects.filter(id=pk)
		if Doctor.objects.get(id=pk) is not None:
			if request.method == 'POST':
				customer_id = cust_id()
				customer_name = request.POST.get('customer_name')
				email = request.POST.get('email')
				password = request.POST.get('password')
				customer.customer_id=customer_id
				customer.customer_name = request.POST.get('customer_name')
				customer.email = request.POST.get('email')
				customer.mobile = request.POST.get('mobile')
				user=User.objects.create_user(username=customer_name,email=email,password=password)
				password_conf=request.POST.get('password_conf')
				password=request.POST.get('password')
				email=request.POST.get('email')
				mobile=request.POST.get('mobile')
				if len(mobile) == 10:
					if password == password_conf:
						if Customer.objects.filter(email=email).exists():
							return HttpResponse('email alrdy exist')
						elif Customer.objects.filter(mobile=mobile).exists():
							return HttpResponse('mobile alrdy exist')
						else:
							user.save()
							customer.save()
							doctorviewlog=DoctorViewLog()
							customer_id=Customer.objects.get(customer_id=customer_id)
							doctorviewlog.customer_id=customer_id
							doc_pk=Doctor.objects.get(id=pk)
							doctorviewlog.doc_pk=doc_pk
							doctorviewlog.save()
							return redirect('customer_login',pk=pk)
					else:
						return HttpResponse('Both passwords should match')
				else:
					return HttpResponse('mobile number should be 10 digits')
		else:
			return HttpResponse ('select valid doctor')
		return render(request,'customer/Customer_registration.html',{'pk':pk})
	else:
		return HttpResponse ('enter correct url')


def validate_email(request):
	email = request.GET.get('email', None)
	data = {
	'is_taken': Customer.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)

def validate_mobile(request):
	mobile = request.GET.get('mobile', None)
	data = {
	'is_taken': Customer.objects.filter(mobile__iexact=mobile).exists()
	}
	return JsonResponse(data)

def customer_login(request,pk=None):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		if '@' in user_id:
				customer_obj=Customer.objects.get(email=user_id)
				customer_id=customer_obj.customer_id
				doc_pk = DoctorViewLog.objects.filter(customer_id=customer_obj).last()
				doc_pk=doc_pk.doc_pk
				doc_pk=doc_pk.id

		elif '@' not in user_id:
				customer_obj=Customer.objects.get(mobile=user_id)
				customer_id=customer_obj.customer_id
				doc_pk = DoctorViewLog.objects.filter(customer_id=customer_obj).last()
				doc_pk=doc_pk.doc_pk
				doc_pk=doc_pk.id

		else:
			return HttpResponse ('invalid user_id/password')
		customer_obj = Customer.objects.get(customer_id=customer_id)
		password = request.POST.get('password')

		if Pet.objects.filter(customer_id=customer_obj).last() is not None:
			if '@' in user_id:
				user=auth.authenticate(username=User.objects.get(email=user_id),password=password)
				if user is not None:
					request.session['customer_id']=customer_id
					today=date.today()
					if DoctorViewLog.objects.filter(customer_id=customer_obj).last() is not None:
						doc_view_data=DoctorViewLog.objects.filter(customer_id=customer_obj).last()
						doc_view_date=doc_view_data.date
						if doc_view_date == today:
							request.session['customer_id']=customer_id
							doc_pk=pk
							return redirect('second_visit_petdetails',customer_id=customer_id,doc_pk=doc_pk)
						elif doc_view_date != today:
							request.session['customer_id']=customer_id
							doctorviewlog=DoctorViewLog()
							doctorviewlog.customer_id=customer_obj
							doc_pk=Doctor.objects.get(id=pk)
							doctorviewlog.doc_pk=doc_pk
							doctorviewlog.save()
							doc_pk=doc_pk.id
							return redirect('second_visit_petdetails',customer_id=customer_id,doc_pk=doc_pk)
				else:
					return HttpResponse ('invalid email/password')
			elif '@' not in user_id:
				mb=Customer.objects.get(mobile=user_id)
				mb=mb.email
				user=auth.authenticate(username=User.objects.get(email=mb),password=password)
				if user is not None:
					request.session['customer_id']=customer_id
					today=date.today()
					if DoctorViewLog.objects.filter(customer_id=customer_obj).last() is not None:
						doc_view_data=DoctorViewLog.objects.filter(customer_id=customer_obj).last()
						doc_view_date=doc_view_data.date
						if doc_view_date == today:
							doc_pk=pk
							return redirect('second_visit_petdetails',customer_id=customer_id,doc_pk=doc_pk)
						elif doc_view_date != today:
							doctorviewlog=DoctorViewLog()
							doctorviewlog.customer_id=customer_obj
							doc_pk=Doctor.objects.get(id=pk)
							doctorviewlog.doc_pk=doc_pk
							doctorviewlog.save()
							doc_pk=doc_pk.id
							return redirect('second_visit_petdetails',customer_id=customer_id,doc_pk=doc_pk)
				else:
					return HttpResponse ('invalid mobile number/password')
			else:
				return HttpResponse ('enter mobile/email')
		else:
			if '@' in user_id:
				user=auth.authenticate(username=User.objects.get(email=user_id),password=password)
				if user is not None:
					print('successssss')
					auth.login(request, user)
					print(user)
					customer=Customer.objects.get(email=user_id)
					print(customer)
					customer=customer.customer_id
					request.session['customer_id']=customer_id
					if Pet.objects.filter(customer_id=customer).exists():
						pet=Pet.objects.filter(customer_id=customer).last()
						return redirect('second_visit_petdetails',customer_id=customer_id,doc_pk=doc_pk)
					else :
						return redirect('petdetails',customer_id=customer_id,doc_pk=doc_pk)
				else:
					return HttpResponse ('invalid email/password')
			elif '@' not in user_id:
				mb=Customer.objects.get(mobile=user_id)
				mb=mb.email
				user=auth.authenticate(username=User.objects.get(email=mb),password=password)
				if user is not None:
					customer=Customer.objects.get(mobile=user_id)
					request.session['customer_id']=customer.customer_id
					customer=customer.customer_id
					if Pet.objects.filter(customer_id=customer).exists():
						pet=Pet.objects.filter(customer_id=customer).last()

						return redirect('second_visit_petdetails',customer_id=customer_id,doc_pk=doc_pk)
					else:
						return redirect('petdetails',customer_id=customer_id,doc_pk=doc_pk)
				else:
					return HttpResponse ('invalid mobile number/password')
			else:
				return HttpResponse ('enter mobile/email')
	return render (request,'customer/Customer_user_login.html')
def socialreg(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	doctor=docip.objects.filter(ip=ip).last()
	doc_pk_data=doctor.doc_id
	doc_pk_data=doc_pk_data.id
	ipdata=doctor.ip
	email=request.user.email
	social_info = User.objects.filter(email=email).last()
	first_name=social_info.first_name
	if request.method=='POST':
		customer=Customer()
		customer_id=cust_id()
		customer.customer_id=customer_id
		customer.customer_name = first_name
		customer.email = email
		customer.mobile = request.POST.get('mobile')
		customer.save()
		docviewlog=DoctorViewLog()
		if ip==ipdata:
			doc_pk_obj=Doctor.objects.get(id=doc_pk_data)
			customer_obj=Customer.objects.get(customer_id=customer_id)
			docviewlog.doc_pk=doc_pk_obj
			docviewlog.customer_id=customer_obj
			docviewlog.save()
			return redirect('petdetails',customer_id=customer_id,doc_pk=doc_pk_data)
		else:
			return HttpResponse('invalid ip address')

	return render(request,'customer/enter_mobile_page.html')

def second_visit_petdetails(request,customer_id,doc_pk):
	today_date=date.today()
	try:
		email=request.user.email
		if Customer.objects.filter(email=email).exists:
			customer=Customer.objects.get(email=email).customer_id
			pets=Pet.objects.filter(customer_id=customer).all()
		else:
			pass
	except:
		customer=Customer.objects.get(customer_id=customer_id)
		pets=Pet.objects.filter(customer_id=customer_id).all()

	doctorloglist=DoctorLogList.objects.filter(pet_id__customer_id=customer_id,date=today_date).all()
	x=[]
	for pet in doctorloglist:
		pet_id=pet.pet_id.pet_id
		x.append(pet_id)

	if request.method == "GET":
		if 'customer_id' in request.session:
			return render(request,'customer/Customer_pet_details_second_visit.html',{'customer_id':customer_id,'pets':pets,'doc_pk':doc_pk,
			'doctorloglist':doctorloglist,'x':x})
		else:
			return redirect ('customer_login_home')
	if request.method=='POST':
		x=request.POST.get('petid')
		purpose=PurposeAndDiet()
		pet_id1=Pet.objects.get(pet_id=x)
		purpose.pet_id=Pet.objects.get(pet_id=x)
		purpose.save()
		purpose_id=PurposeAndDiet.objects.filter(pet_id=pet_id1).last()
		purpose_id=purpose_id.id
		doctorviewlog=DoctorViewLog()
		doctorviewlog.customer_id=Customer.objects.get(customer_id=customer_id)
		doc_pk_obj=Doctor.objects.get(id=doc_pk)
		doctorviewlog.doc_pk=doc_pk_obj
		doctorviewlog.purpose_id=purpose_id
		doctorviewlog.pet_id=pet_id1.pet_id
		doctorviewlog.save()
		return redirect('pet_dite',customer_id=customer_id,doc_pk_org=doc_pk,purpose_id=purpose_id,pet_id=x)


	pets=Pet.objects.filter(customer_id=customer_id).all()
	doc_pk_org=doc_pk
	try:
		social_info = User.objects.filter(is_staff=False).last()
		mail=social_info.email
		first_name=social_info.first_name
		if User.objects.filter(email=mail).exists:
			print('sucess')
		else:
			customer=Customer()
			customer.customer_id=cust_id()
			customer.customer_name=first_name
			customer.email=mail
			customer.save()
		customer_id=customer_id
	except:
		pass
	if request.method == "GET":
		if 'customer_id' in request.session:
			return render (request,'customer/Customer_pet_details.html',{'customer_id':customer_id,'doc_pk':doc_pk,'pets':pets})
		else:
			return redirect ('customer_login_home')
	if request.method=='POST':
		if 'addpet' in request.POST:
			pet=Pet()
			coustmer_obj=Customer.objects.get(customer_id=customer_id)
			pet.customer_id=coustmer_obj
			pet.name=request.POST.get('name')
			pet.breed=request.POST.get('breed')
			pet.age_year=request.POST.get('age_year')
			pet.age_month=request.POST.get('age_month')
			pet.gender=request.POST.get('gender')

			pet_id_created=set_id()
			pet.pet_id=pet_id_created
			pet.save()
			purpose=PurposeAndDiet()
			pet_obj=Pet.objects.filter(pet_id=pet_id_created).last()
			purpose.pet_id=pet_obj
			vac_coustmer=Vaccination_coustmer()
			last_deworming=request.POST.get('last_date')
			last_deworming=last_deworming
			if last_deworming=="":
				vac_coustmer.last_deworming='1000-01-01'
			else:
				vac_coustmer.last_deworming=last_deworming
			purpose.save()
			main_purpose_id=PurposeAndDiet.objects.get(pet_id=pet_obj).id
			DoctorViewLog.objects.update(pet_id=pet_id_created,purpose_id=main_purpose_id)
			purpose_id=PurposeAndDiet.objects.filter(pet_id__customer_id=customer_id).last()
			# vac_coustmer.purpose_id=purpose_id
			pet_obj=Pet.objects.filter(pet_id=pet_id_created).last()
			vac_coustmer.pet=pet_obj
			last_date_rabies=request.POST.get('l_rabies')
			if last_date_rabies=="":

				vac_coustmer.last_date_rabies='1000-01-01'
			else:
				vac_coustmer.last_date_rabies=last_date_rabies
			last_date_distemper=request.POST.get('l_distemper')
			if last_date_distemper=="":

				vac_coustmer.last_date_distemper='1000-01-01'
			else:
				vac_coustmer.last_date_distemper=last_date_distemper
			last_date_hepatitis=request.POST.get('l_hepatitis')
			if last_date_hepatitis=="":

				vac_coustmer.last_date_hepatitis='1000-01-01'
			else:
				vac_coustmer.last_date_hepatitis=last_date_hepatitis
			last_date_parovirus=request.POST.get('l_parovirus')
			if last_date_parovirus=="":

				vac_coustmer.last_date_parovirus='1000-01-01'
			else:
				vac_coustmer.last_date_parovirus=last_date_parovirus
			last_date_parainfluenza=request.POST.get('l_parainfluenza')
			if last_date_parainfluenza=="":

				vac_coustmer.last_date_parainfluenza='1000-01-01'
			else:
				vac_coustmer.last_date_parainfluenza=last_date_parainfluenza
			last_date_bordetella=request.POST.get('l_bordetella')
			if last_date_bordetella=="":

				vac_coustmer.last_date_bordetella='1000-01-01'
			else:
				vac_coustmer.last_date_bordetella=last_date_bordetella
			last_date_leptospirosis=request.POST.get('l_leptospirosis')
			if last_date_leptospirosis=="":

				vac_coustmer.last_date_leptospirosis='1000-01-01'
			else:
				vac_coustmer.last_date_leptospirosis=last_date_leptospirosis
			last_date_lymedisease=request.POST.get('l_lymedisease')
			if last_date_lymedisease=="":

				vac_coustmer.last_date_lymedisease='1000-01-01'
			else:
				vac_coustmer.last_date_lymedisease=last_date_lymedisease
			last_date_coronavirus=request.POST.get('l_coronavirus')
			if last_date_coronavirus=="":

				vac_coustmer.last_date_coronavirus='1000-01-01'
			else:
				vac_coustmer.last_date_coronavirus=last_date_coronavirus
			last_date_giardia=request.POST.get('l_giardia')
			if last_date_giardia=="":

				vac_coustmer.last_date_giardia='1000-01-01'
			else:
				vac_coustmer.last_date_giardia=last_date_giardia
			last_date_dhpp=request.POST.get('l_dhpp')
			if last_date_dhpp=="":

				vac_coustmer.last_date_dhpp='1000-01-01'
			else:
				vac_coustmer.last_date_dhpp=last_date_dhpp

			vac_coustmer.save()
			doc_pk_org=doc_pk_org
			return redirect('addpet',customer_id=customer_id,doc_pk=doc_pk_org)
		else:
			pet=Pet()
			coustmer_obj=Customer.objects.get(customer_id=customer_id)
			pet.customer_id=coustmer_obj
			petname=request.POST.get('name')
			pet.name=request.POST.get('name')
			pet.breed=request.POST.get('breed')
			pet.age_year=request.POST.get('age_year')
			pet.age_month=request.POST.get('age_month')
			pet.gender=request.POST.get('gender')

			breed=request.POST.get('breed')
			age_year=request.POST.get('age_year')
			age_month=request.POST.get('age_month')
			gender=request.POST.get('gender')
			if Pet.objects.filter(customer_id=customer_id,name=petname).exists():
				petid=Pet.objects.filter(customer_id=customer_id).last()
				petid_objid=petid.id
				petid=petid.pet_id
				updte=Pet.objects.filter(id=petid_objid).update(pet_id=petid,breed=breed,age_year=age_year,age_month=age_month,gender=gender)
				purpose=PurposeAndDiet()
				pet_obj=Pet.objects.filter(customer_id=customer_id).last()
				purpose.pet_id=Pet.objects.filter(customer_id=customer_id).last()
				vac_coustmer=Vaccination_coustmer()
				last_deworming=request.POST.get('last_date')
				last_deworming=last_deworming
				if last_deworming=="":
					vac_coustmer.last_deworming='1000-01-01'
				else:
					vac_coustmer.last_deworming=last_deworming
				purpose.save()
				main_purpose_id=PurposeAndDiet.objects.filter(pet_id=pet_obj).last().id
				DoctorViewLog.objects.update(pet_id=petid,purpose_id=main_purpose_id)
				purpose_id=PurposeAndDiet.objects.filter(pet_id__customer_id=customer_id).last()
				vac_coustmer.purpose_id=purpose_id
				pet_obj=Pet.objects.filter(pet_id=petid).last()
				vac_coustmer.pet=pet_obj
				last_date_rabies=request.POST.get('l_rabies')
				if last_date_rabies=="":
					vac_coustmer.last_date_rabies='1000-01-01'
				else:
					vac_coustmer.last_date_rabies=last_date_rabies
				last_date_distemper=request.POST.get('l_distemper')
				if last_date_distemper=="":
					vac_coustmer.last_date_distemper='1000-01-01'
				else:
					vac_coustmer.last_date_distemper=last_date_distemper
				last_date_hepatitis=request.POST.get('l_hepatitis')
				if last_date_hepatitis=="":
					vac_coustmer.last_date_hepatitis='1000-01-01'
				else:
					vac_coustmer.last_date_hepatitis=last_date_hepatitis
				last_date_parovirus=request.POST.get('l_parovirus')
				if last_date_parovirus=="":
					vac_coustmer.last_date_parovirus='1000-01-01'
				else:
					vac_coustmer.last_date_parovirus=last_date_parovirus
				last_date_parainfluenza=request.POST.get('l_parainfluenza')
				if last_date_parainfluenza=="":
					vac_coustmer.last_date_parainfluenza='1000-01-01'
				else:
					vac_coustmer.last_date_parainfluenza=last_date_parainfluenza
				last_date_bordetella=request.POST.get('l_bordetella')
				if last_date_bordetella=="":
					vac_coustmer.last_date_bordetella='1000-01-01'
				else:
					vac_coustmer.last_date_bordetella=last_date_bordetella
				last_date_leptospirosis=request.POST.get('l_leptospirosis')
				if last_date_leptospirosis=="":
					vac_coustmer.last_date_leptospirosis='1000-01-01'
				else:
					vac_coustmer.last_date_leptospirosis=last_date_leptospirosis
				last_date_lymedisease=request.POST.get('l_lymedisease')
				if last_date_lymedisease=="":
					vac_coustmer.last_date_lymedisease='1000-01-01'
				else:
					vac_coustmer.last_date_lymedisease=last_date_lymedisease
				last_date_coronavirus=request.POST.get('l_coronavirus')
				if last_date_coronavirus=="":
					vac_coustmer.last_date_coronavirus='1000-01-01'
				else:
					vac_coustmer.last_date_coronavirus=last_date_coronavirus
				last_date_giardia=request.POST.get('l_giardia')
				if last_date_giardia=="":
					vac_coustmer.last_date_giardia='1000-01-01'
				else:
					vac_coustmer.last_date_giardia=last_date_giardia
				last_date_dhpp=request.POST.get('l_dhpp')
				if last_date_dhpp=="":
					vac_coustmer.last_date_dhpp='1000-01-01'
				else:
					vac_coustmer.last_date_dhpp=last_date_dhpp
				vac_coustmer.save()
				doc_pk_org=doc_pk_org
				return redirect('second_visit_petdetails',customer_id=customer_id,doc_pk=doc_pk)
			else:
				pet_id_created=set_id()
				pet.pet_id=pet_id_created
				pet.save()
				purpose=PurposeAndDiet()
				pet_obj=Pet.objects.filter(pet_id=pet_id_created).last()
				purpose.pet_id=pet_obj
				vac_coustmer=Vaccination_coustmer()
				last_deworming=request.POST.get('last_date')
				last_deworming=last_deworming
				if last_deworming=="":
					vac_coustmer.last_deworming='1000-01-01'
				else:
					vac_coustmer.last_deworming=last_deworming
				purpose.save()
				main_purpose_id=PurposeAndDiet.objects.get(pet_id=pet_obj).id
				DoctorViewLog.objects.update(pet_id=pet_id_created,purpose_id=main_purpose_id)
				purpose_id=PurposeAndDiet.objects.filter(pet_id__customer_id=customer_id).last()
				vac_coustmer.purpose_id=purpose_id
				pet_obj=Pet.objects.filter(pet_id=pet_id_created).last()
				vac_coustmer.pet=pet_obj
				last_date_rabies=request.POST.get('l_rabies')
				if last_date_rabies=="":
					vac_coustmer.last_date_rabies='1000-01-01'
				else:
					vac_coustmer.last_date_rabies=last_date_rabies
				last_date_distemper=request.POST.get('l_distemper')
				if last_date_distemper=="":
					vac_coustmer.last_date_distemper='1000-01-01'
				else:
					vac_coustmer.last_date_distemper=last_date_distemper
				last_date_hepatitis=request.POST.get('l_hepatitis')
				if last_date_hepatitis=="":
					vac_coustmer.last_date_hepatitis='1000-01-01'
				else:
					vac_coustmer.last_date_hepatitis=last_date_hepatitis
				last_date_parovirus=request.POST.get('l_parovirus')
				if last_date_parovirus=="":
					vac_coustmer.last_date_parovirus='1000-01-01'
				else:
					vac_coustmer.last_date_parovirus=last_date_parovirus
				last_date_parainfluenza=request.POST.get('l_parainfluenza')
				if last_date_parainfluenza=="":
					vac_coustmer.last_date_parainfluenza='1000-01-01'
				else:
					vac_coustmer.last_date_parainfluenza=last_date_parainfluenza
				last_date_bordetella=request.POST.get('l_bordetella')
				if last_date_bordetella=="":
					vac_coustmer.last_date_bordetella='1000-01-01'
				else:
					vac_coustmer.last_date_bordetella=last_date_bordetella
				last_date_leptospirosis=request.POST.get('l_leptospirosis')
				if last_date_leptospirosis=="":
					vac_coustmer.last_date_leptospirosis='1000-01-01'
				else:
					vac_coustmer.last_date_leptospirosis=last_date_leptospirosis
				last_date_lymedisease=request.POST.get('l_lymedisease')
				if last_date_lymedisease=="":
					vac_coustmer.last_date_lymedisease='1000-01-01'
				else:
					vac_coustmer.last_date_lymedisease=last_date_lymedisease
				last_date_coronavirus=request.POST.get('l_coronavirus')
				if last_date_coronavirus=="":
					vac_coustmer.last_date_coronavirus='1000-01-01'
				else:
					vac_coustmer.last_date_coronavirus=last_date_coronavirus
				last_date_giardia=request.POST.get('l_giardia')
				if last_date_giardia=="":
					vac_coustmer.last_date_giardia='1000-01-01'
				else:
					vac_coustmer.last_date_giardia=last_date_giardia
				last_date_dhpp=request.POST.get('l_dhpp')
				if last_date_dhpp=="":
					vac_coustmer.last_date_dhpp='1000-01-01'
				else:
					vac_coustmer.last_date_dhpp=last_date_dhpp

				vac_coustmer.save()
				doc_pk_org=doc_pk_org
				return redirect('pet_dite',customer_id=customer_id,pet_id=pet_id_created,doc_pk_org=doc_pk_org,purpose_id=main_purpose_id)
def petdetails(request,customer_id,doc_pk):
	pets=Pet.objects.filter(customer_id=customer_id).all()
	doc_pk_org=doc_pk
	print(type(doc_pk_org),'asfdghsdfghsfdgh')
	try:
		social_info = User.objects.filter(is_staff=False).last()
		print(social_info,'exitsxcjkvb')
		mail=social_info.email
		print(mail)
		first_name=social_info.first_name

		if User.objects.filter(email=mail).exists:
			print('sucess')
		else:
			customer=Customer()
			customer.customer_id=cust_id()
			customer.customer_name=first_name
			customer.email=mail
			customer.save()
		customer_id=customer_id
	except:
		pass
	if request.method == "GET":
		if 'customer_id' in request.session:
			return render (request,'customer/Customer_pet_details.html',{'customer_id':customer_id,'doc_pk':doc_pk,'pets':pets})
		else:
			return redirect ('customer_login_home')
	if request.method=='POST':
		if 'addpet' in request.POST:
			pet=Pet()
			coustmer_obj=Customer.objects.get(customer_id=customer_id)
			pet.customer_id=coustmer_obj
			pet.name=request.POST.get('name')
			pet.breed=request.POST.get('breed')
			pet.age_year=request.POST.get('age_year')
			pet.age_month=request.POST.get('age_month')
			pet.gender=request.POST.get('gender')
			pet_id_created=set_id()
			pet.pet_id=pet_id_created
			pet.save()
			purpose=PurposeAndDiet()
			pet_obj=Pet.objects.filter(pet_id=pet_id_created).last()
			purpose.pet_id=pet_obj
			vac_coustmer=Vaccination_coustmer()
			last_deworming=request.POST.get('last_date')
			last_deworming=last_deworming
			if last_deworming=="":
				vac_coustmer.last_deworming='1000-01-01'
			else:
				vac_coustmer.last_deworming=last_deworming
			purpose.save()
			main_purpose_id=PurposeAndDiet.objects.get(pet_id=pet_obj).id
			print(main_purpose_id,'123')
			custid=DoctorViewLog.objects.get(customer_id=customer_id)
			customerid=custid.id
			DoctorViewLog.objects.filter(id=customerid).update(pet_id=pet_id_created,purpose_id=main_purpose_id)
			purpose_id=PurposeAndDiet.objects.filter(pet_id__customer_id=customer_id).last()
			# vac_coustmer.purpose_id=purpose_id
			pet_obj=Pet.objects.filter(pet_id=pet_id_created).last()
			vac_coustmer.pet=pet_obj
			last_date_rabies=request.POST.get('l_rabies')
			if last_date_rabies=="":

				vac_coustmer.last_date_rabies='1000-01-01'
			else:
				vac_coustmer.last_date_rabies=last_date_rabies
			last_date_distemper=request.POST.get('l_distemper')
			if last_date_distemper=="":

				vac_coustmer.last_date_distemper='1000-01-01'
			else:
				vac_coustmer.last_date_distemper=last_date_distemper
			last_date_hepatitis=request.POST.get('l_hepatitis')
			if last_date_hepatitis=="":

				vac_coustmer.last_date_hepatitis='1000-01-01'
			else:
				vac_coustmer.last_date_hepatitis=last_date_hepatitis
			last_date_parovirus=request.POST.get('l_parovirus')
			if last_date_parovirus=="":

				vac_coustmer.last_date_parovirus='1000-01-01'
			else:
				vac_coustmer.last_date_parovirus=last_date_parovirus
			last_date_parainfluenza=request.POST.get('l_parainfluenza')
			if last_date_parainfluenza=="":

				vac_coustmer.last_date_parainfluenza='1000-01-01'
			else:
				vac_coustmer.last_date_parainfluenza=last_date_parainfluenza
			last_date_bordetella=request.POST.get('l_bordetella')
			if last_date_bordetella=="":

				vac_coustmer.last_date_bordetella='1000-01-01'
			else:
				vac_coustmer.last_date_bordetella=last_date_bordetella
			last_date_leptospirosis=request.POST.get('l_leptospirosis')
			if last_date_leptospirosis=="":

				vac_coustmer.last_date_leptospirosis='1000-01-01'
			else:
				vac_coustmer.last_date_leptospirosis=last_date_leptospirosis
			last_date_lymedisease=request.POST.get('l_lymedisease')
			if last_date_lymedisease=="":

				vac_coustmer.last_date_lymedisease='1000-01-01'
			else:
				vac_coustmer.last_date_lymedisease=last_date_lymedisease
			last_date_coronavirus=request.POST.get('l_coronavirus')
			if last_date_coronavirus=="":

				vac_coustmer.last_date_coronavirus='1000-01-01'
			else:
				vac_coustmer.last_date_coronavirus=last_date_coronavirus
			last_date_giardia=request.POST.get('l_giardia')
			if last_date_giardia=="":

				vac_coustmer.last_date_giardia='1000-01-01'
			else:
				vac_coustmer.last_date_giardia=last_date_giardia
			last_date_dhpp=request.POST.get('l_dhpp')
			if last_date_dhpp=="":

				vac_coustmer.last_date_dhpp='1000-01-01'
			else:
				vac_coustmer.last_date_dhpp=last_date_dhpp

			vac_coustmer.save()

			print(doc_pk_org,'79847653120.')
			doc_pk_org=doc_pk_org
			print(doc_pk_org)

			return redirect('addpet',customer_id=customer_id,doc_pk=doc_pk_org)
		else:
			pet=Pet()
			coustmer_obj=Customer.objects.get(customer_id=customer_id)
			pet.customer_id=coustmer_obj
			petname=request.POST.get('name')
			pet.name=request.POST.get('name')
			pet.breed=request.POST.get('breed')
			pet.age_year=request.POST.get('age_year')
			pet.age_month=request.POST.get('age_month')
			pet.gender=request.POST.get('gender')

			breed=request.POST.get('breed')
			age_year=request.POST.get('age_year')
			age_month=request.POST.get('age_month')
			gender=request.POST.get('gender')
			if Pet.objects.filter(customer_id=customer_id,name=petname).exists():
				petid=Pet.objects.filter(customer_id=customer_id).last()
				print(petid,'test')
				petid_objid=petid.id
				petid=petid.pet_id
				print(petid,'test')
				updte=Pet.objects.filter(id=petid_objid).update(pet_id=petid,breed=breed,age_year=age_year,age_month=age_month,gender=gender)
				# purpose=PurposeAndDiet()
				# pet_obj=Pet.objects.filter(customer_id=customer_id).last()
				# purpose.pet_id=Pet.objects.filter(customer_id=customer_id).last()
				# disease='disease'
				# purpose.disease=disease
				vac_coustmer=Vaccination_coustmer()
				last_deworming=request.POST.get('last_date')
				last_deworming=last_deworming
				if last_deworming=="":
					vac_coustmer.last_deworming='1000-01-01'
				else:
					vac_coustmer.last_deworming=last_deworming
				# purpose.save()
				# main_purpose_id=PurposeAndDiet.objects.filter(pet_id=pet_obj).last().id
				# print(main_purpose_id,'123')
				# DoctorViewLog.objects.update(pet_id=petid,purpose_id=main_purpose_id)

				# purpose_id=PurposeAndDiet.objects.filter(pet_id__customer_id=customer_id).last()
				# vac_coustmer.purpose_id=purpose_id
				pet_obj=Pet.objects.filter(pet_id=petid).last()
				vac_coustmer.pet=pet_obj
				last_date_rabies=request.POST.get('l_rabies')
				if last_date_rabies=="":

					vac_coustmer.last_date_rabies='1000-01-01'
				else:
					vac_coustmer.last_date_rabies=last_date_rabies
				last_date_distemper=request.POST.get('l_distemper')
				if last_date_distemper=="":

					vac_coustmer.last_date_distemper='1000-01-01'
				else:
					vac_coustmer.last_date_distemper=last_date_distemper
				last_date_hepatitis=request.POST.get('l_hepatitis')
				if last_date_hepatitis=="":

					vac_coustmer.last_date_hepatitis='1000-01-01'
				else:
					vac_coustmer.last_date_hepatitis=last_date_hepatitis
				last_date_parovirus=request.POST.get('l_parovirus')
				if last_date_parovirus=="":

					vac_coustmer.last_date_parovirus='1000-01-01'
				else:
					vac_coustmer.last_date_parovirus=last_date_parovirus
				last_date_parainfluenza=request.POST.get('l_parainfluenza')
				if last_date_parainfluenza=="":

					vac_coustmer.last_date_parainfluenza='1000-01-01'
				else:
					vac_coustmer.last_date_parainfluenza=last_date_parainfluenza
				last_date_bordetella=request.POST.get('l_bordetella')
				if last_date_bordetella=="":

					vac_coustmer.last_date_bordetella='1000-01-01'
				else:
					vac_coustmer.last_date_bordetella=last_date_bordetella
				last_date_leptospirosis=request.POST.get('l_leptospirosis')
				if last_date_leptospirosis=="":

					vac_coustmer.last_date_leptospirosis='1000-01-01'
				else:
					vac_coustmer.last_date_leptospirosis=last_date_leptospirosis
				last_date_lymedisease=request.POST.get('l_lymedisease')
				if last_date_lymedisease=="":

					vac_coustmer.last_date_lymedisease='1000-01-01'
				else:
					vac_coustmer.last_date_lymedisease=last_date_lymedisease
				last_date_coronavirus=request.POST.get('l_coronavirus')
				if last_date_coronavirus=="":

					vac_coustmer.last_date_coronavirus='1000-01-01'
				else:
					vac_coustmer.last_date_coronavirus=last_date_coronavirus
				last_date_giardia=request.POST.get('l_giardia')
				if last_date_giardia=="":

					vac_coustmer.last_date_giardia='1000-01-01'
				else:
					vac_coustmer.last_date_giardia=last_date_giardia
				last_date_dhpp=request.POST.get('l_dhpp')
				if last_date_dhpp=="":

					vac_coustmer.last_date_dhpp='1000-01-01'
				else:
					vac_coustmer.last_date_dhpp=last_date_dhpp

				vac_coustmer.save()

				print(doc_pk_org,'79847653120.')
				doc_pk_org=doc_pk_org
				print(doc_pk_org)

				return redirect('second_visit_petdetails',customer_id=customer_id,doc_pk=doc_pk)
			else:
				pet_id_created=set_id()
				pet.pet_id=pet_id_created
				pet.save()
				purpose=PurposeAndDiet()
				pet_obj=Pet.objects.filter(pet_id=pet_id_created).last()
				purpose.pet_id=pet_obj


				vac_coustmer=Vaccination_coustmer()
				last_deworming=request.POST.get('last_date')
				last_deworming=last_deworming
				if last_deworming=="":
					vac_coustmer.last_deworming='1000-01-01'
				else:
					vac_coustmer.last_deworming=last_deworming
				purpose.save()
				main_purpose_id=PurposeAndDiet.objects.get(pet_id=pet_obj).id
				print(main_purpose_id,'123')
				custid=DoctorViewLog.objects.get(customer_id=customer_id)
				customerid=custid.id
				DoctorViewLog.objects.filter(id=customerid).update(pet_id=pet_id_created,purpose_id=main_purpose_id)

				purpose_id=PurposeAndDiet.objects.filter(pet_id__customer_id=customer_id).last()
				vac_coustmer.purpose_id=purpose_id
				pet_obj=Pet.objects.filter(pet_id=pet_id_created).last()
				vac_coustmer.pet=pet_obj
				last_date_rabies=request.POST.get('l_rabies')
				if last_date_rabies=="":

					vac_coustmer.last_date_rabies='1000-01-01'
				else:
					vac_coustmer.last_date_rabies=last_date_rabies
				last_date_distemper=request.POST.get('l_distemper')
				if last_date_distemper=="":

					vac_coustmer.last_date_distemper='1000-01-01'
				else:
					vac_coustmer.last_date_distemper=last_date_distemper
				last_date_hepatitis=request.POST.get('l_hepatitis')
				if last_date_hepatitis=="":

					vac_coustmer.last_date_hepatitis='1000-01-01'
				else:
					vac_coustmer.last_date_hepatitis=last_date_hepatitis
				last_date_parovirus=request.POST.get('l_parovirus')
				if last_date_parovirus=="":

					vac_coustmer.last_date_parovirus='1000-01-01'
				else:
					vac_coustmer.last_date_parovirus=last_date_parovirus
				last_date_parainfluenza=request.POST.get('l_parainfluenza')
				if last_date_parainfluenza=="":

					vac_coustmer.last_date_parainfluenza='1000-01-01'
				else:
					vac_coustmer.last_date_parainfluenza=last_date_parainfluenza
				last_date_bordetella=request.POST.get('l_bordetella')
				if last_date_bordetella=="":

					vac_coustmer.last_date_bordetella='1000-01-01'
				else:
					vac_coustmer.last_date_bordetella=last_date_bordetella
				last_date_leptospirosis=request.POST.get('l_leptospirosis')
				if last_date_leptospirosis=="":

					vac_coustmer.last_date_leptospirosis='1000-01-01'
				else:
					vac_coustmer.last_date_leptospirosis=last_date_leptospirosis
				last_date_lymedisease=request.POST.get('l_lymedisease')
				if last_date_lymedisease=="":

					vac_coustmer.last_date_lymedisease='1000-01-01'
				else:
					vac_coustmer.last_date_lymedisease=last_date_lymedisease
				last_date_coronavirus=request.POST.get('l_coronavirus')
				if last_date_coronavirus=="":

					vac_coustmer.last_date_coronavirus='1000-01-01'
				else:
					vac_coustmer.last_date_coronavirus=last_date_coronavirus
				last_date_giardia=request.POST.get('l_giardia')
				if last_date_giardia=="":

					vac_coustmer.last_date_giardia='1000-01-01'
				else:
					vac_coustmer.last_date_giardia=last_date_giardia
				last_date_dhpp=request.POST.get('l_dhpp')
				if last_date_dhpp=="":

					vac_coustmer.last_date_dhpp='1000-01-01'
				else:
					vac_coustmer.last_date_dhpp=last_date_dhpp

				vac_coustmer.save()

				print(doc_pk_org,'79847653120.')
				doc_pk_org=doc_pk_org
				print(doc_pk_org)


				return redirect('pet_dite',customer_id=customer_id,pet_id=pet_id_created,doc_pk_org=doc_pk_org,purpose_id=main_purpose_id)


def purpose_and_dite(request,customer_id,pet_id,doc_pk_org,purpose_id):
	purpose_id=purpose_id
	doc_pk=doc_pk_org
	customer_id=customer_id
	pets=Pet.objects.filter(customer_id=customer_id).all()
	if request.method =="GET":
		if 'customer_id' in request.session:
			return render(request,'customer/Customer_diet.html',{'customer_id':customer_id,'doc_pk':doc_pk,'pets':pets})
		else:
			return redirect ('customer_login_home')
	if request.method == "POST":
		purpose=PurposeAndDiet()
		pet_obj=Pet.objects.filter(pet_id=pet_id).last()
		purpose_obj=PurposeAndDiet.objects.filter(pet_id=pet_obj).last()
		purpose_obj=purpose_obj.id
		diet=request.POST.get('set1')
		diet=empty_string_remove(diet)
		diet_state=request.POST.get('set2')
		diet = PurposeAndDiet.objects.filter(id=purpose_obj).update(diet=diet,diet_state=diet_state)
		return redirect('purpose_visit',customer_id=customer_id,pet_id=pet_id,doc_pk_org=doc_pk_org,purpose_id=purpose_id)


def addpet(request,customer_id,doc_pk):
	doc_pk_org=doc_pk
	pets=Pet.objects.filter(customer_id=customer_id).all()
	customer=Customer.objects.get(customer_id=customer_id)
	if request.method =="GET":
		if 'customer_id' in request.session:
			return render(request,'customer/Customer_addpet.html',{'customer_id':customer_id,'doc_pk':doc_pk,'pets':pets})
		else:
			return redirect ('customer_login_home')
	if request.method=='POST':
		pet=Pet()
		coustmer_obj=Customer.objects.get(customer_id=customer_id)
		pet.customer_id=coustmer_obj
		petname=request.POST.get('name')
		pet.name=request.POST.get('name')
		pet.breed=request.POST.get('breed')
		pet.age_year=request.POST.get('age_year')
		pet.age_month=request.POST.get('age_month')
		pet.gender=request.POST.get('gender')

		breed=request.POST.get('breed')
		age_year=request.POST.get('age_year')
		age_month=request.POST.get('age_month')
		gender=request.POST.get('gender')
		if Pet.objects.filter(customer_id=customer_id,name=petname).exists():
			petid=Pet.objects.filter(customer_id=customer_id).last()
			petid_objid=petid.id
			petid=petid.pet_id
			updte=Pet.objects.filter(id=petid_objid).update(pet_id=petid,breed=breed,age_year=age_year,age_month=age_month,gender=gender)
			purpose=PurposeAndDiet()
			pet_obj=Pet.objects.filter(customer_id=customer_id).last()
			purpose.pet_id=Pet.objects.filter(customer_id=customer_id).last()
			vac_coustmer=Vaccination_coustmer()
			last_deworming=request.POST.get('last_date')
			last_deworming=last_deworming
			if last_deworming=="":
				vac_coustmer.last_deworming='1000-01-01'
			else:
				vac_coustmer.last_deworming=last_deworming
			# purpose.save()
			# main_purpose_id=PurposeAndDiet.objects.filter(pet_id=pet_obj).last().id
			# DoctorViewLog.objects.update(pet_id=petid,purpose_id=main_purpose_id)

			# purpose_id=PurposeAndDiet.objects.filter(pet_id__customer_id=customer_id).last()
			# vac_coustmer.purpose_id=purpose_id
			pet_obj=Pet.objects.filter(pet_id=petid).last()
			vac_coustmer.pet=pet_obj
			last_date_rabies=request.POST.get('l_rabies')
			if last_date_rabies=="":

				vac_coustmer.last_date_rabies='1000-01-01'
			else:
				vac_coustmer.last_date_rabies=last_date_rabies
			last_date_distemper=request.POST.get('l_distemper')
			if last_date_distemper=="":
				vac_coustmer.last_date_distemper='1000-01-01'
			else:
				vac_coustmer.last_date_distemper=last_date_distemper
			last_date_hepatitis=request.POST.get('l_hepatitis')
			if last_date_hepatitis=="":
				vac_coustmer.last_date_hepatitis='1000-01-01'
			else:
				vac_coustmer.last_date_hepatitis=last_date_hepatitis
			last_date_parovirus=request.POST.get('l_parovirus')
			if last_date_parovirus=="":
				vac_coustmer.last_date_parovirus='1000-01-01'
			else:
				vac_coustmer.last_date_parovirus=last_date_parovirus
			last_date_parainfluenza=request.POST.get('l_parainfluenza')
			if last_date_parainfluenza=="":
				vac_coustmer.last_date_parainfluenza='1000-01-01'
			else:
				vac_coustmer.last_date_parainfluenza=last_date_parainfluenza
			last_date_bordetella=request.POST.get('l_bordetella')
			if last_date_bordetella=="":
				vac_coustmer.last_date_bordetella='1000-01-01'
			else:
				vac_coustmer.last_date_bordetella=last_date_bordetella
			last_date_leptospirosis=request.POST.get('l_leptospirosis')
			if last_date_leptospirosis=="":
				vac_coustmer.last_date_leptospirosis='1000-01-01'
			else:
				vac_coustmer.last_date_leptospirosis=last_date_leptospirosis
			last_date_lymedisease=request.POST.get('l_lymedisease')
			if last_date_lymedisease=="":
				vac_coustmer.last_date_lymedisease='1000-01-01'
			else:
				vac_coustmer.last_date_lymedisease=last_date_lymedisease
			last_date_coronavirus=request.POST.get('l_coronavirus')
			if last_date_coronavirus=="":
				vac_coustmer.last_date_coronavirus='1000-01-01'
			else:
				vac_coustmer.last_date_coronavirus=last_date_coronavirus
			last_date_giardia=request.POST.get('l_giardia')
			if last_date_giardia=="":
				vac_coustmer.last_date_giardia='1000-01-01'
			else:
				vac_coustmer.last_date_giardia=last_date_giardia
			last_date_dhpp=request.POST.get('l_dhpp')
			if last_date_dhpp=="":
				vac_coustmer.last_date_dhpp='1000-01-01'
			else:
				vac_coustmer.last_date_dhpp=last_date_dhpp

			vac_coustmer.save()
			doc_pk_org=doc_pk_org
			return redirect('second_visit_petdetails',customer_id=customer_id,doc_pk=doc_pk)
		else:
			pet_id_created=set_id()
			pet.pet_id=pet_id_created
			pet.save()
			purpose=PurposeAndDiet()
			pet_obj=Pet.objects.filter(pet_id=pet_id_created).last()
			purpose.pet_id=pet_obj
			vac_coustmer=Vaccination_coustmer()
			last_deworming=request.POST.get('last_date')
			last_deworming=last_deworming
			if last_deworming=="":
				vac_coustmer.last_deworming='1000-01-01'
			else:
				vac_coustmer.last_deworming=last_deworming
			# purpose.save()
			# main_purpose_id=PurposeAndDiet.objects.get(pet_id=pet_obj).id
			# DoctorViewLog.objects.update(pet_id=pet_id_created,purpose_id=main_purpose_id)

			# purpose_id=PurposeAndDiet.objects.filter(pet_id__customer_id=customer_id).last()
			# vac_coustmer.purpose_id=purpose_id
			pet_obj=Pet.objects.filter(pet_id=pet_id_created).last()
			vac_coustmer.pet=pet_obj
			last_date_rabies=request.POST.get('l_rabies')
			if last_date_rabies=="":
				vac_coustmer.last_date_rabies='1000-01-01'
			else:
				vac_coustmer.last_date_rabies=last_date_rabies
			last_date_distemper=request.POST.get('l_distemper')
			if last_date_distemper=="":
				vac_coustmer.last_date_distemper='1000-01-01'
			else:
				vac_coustmer.last_date_distemper=last_date_distemper
			last_date_hepatitis=request.POST.get('l_hepatitis')
			if last_date_hepatitis=="":
				vac_coustmer.last_date_hepatitis='1000-01-01'
			else:
				vac_coustmer.last_date_hepatitis=last_date_hepatitis
			last_date_parovirus=request.POST.get('l_parovirus')
			if last_date_parovirus=="":
				vac_coustmer.last_date_parovirus='1000-01-01'
			else:
				vac_coustmer.last_date_parovirus=last_date_parovirus
			last_date_parainfluenza=request.POST.get('l_parainfluenza')
			if last_date_parainfluenza=="":
				vac_coustmer.last_date_parainfluenza='1000-01-01'
			else:
				vac_coustmer.last_date_parainfluenza=last_date_parainfluenza
			last_date_bordetella=request.POST.get('l_bordetella')
			if last_date_bordetella=="":
				vac_coustmer.last_date_bordetella='1000-01-01'
			else:
				vac_coustmer.last_date_bordetella=last_date_bordetella
			last_date_leptospirosis=request.POST.get('l_leptospirosis')
			if last_date_leptospirosis=="":
				vac_coustmer.last_date_leptospirosis='1000-01-01'
			else:
				vac_coustmer.last_date_leptospirosis=last_date_leptospirosis
			last_date_lymedisease=request.POST.get('l_lymedisease')
			if last_date_lymedisease=="":
				vac_coustmer.last_date_lymedisease='1000-01-01'
			else:
				vac_coustmer.last_date_lymedisease=last_date_lymedisease
			last_date_coronavirus=request.POST.get('l_coronavirus')
			if last_date_coronavirus=="":
				vac_coustmer.last_date_coronavirus='1000-01-01'
			else:
				vac_coustmer.last_date_coronavirus=last_date_coronavirus
			last_date_giardia=request.POST.get('l_giardia')
			if last_date_giardia=="":
				vac_coustmer.last_date_giardia='1000-01-01'
			else:
				vac_coustmer.last_date_giardia=last_date_giardia
			last_date_dhpp=request.POST.get('l_dhpp')
			if last_date_dhpp=="":
				vac_coustmer.last_date_dhpp='1000-01-01'
			else:
				vac_coustmer.last_date_dhpp=last_date_dhpp

			vac_coustmer.save()
			doc_pk_org=doc_pk_org
			return redirect('second_visit_petdetails',customer_id=customer_id,doc_pk=doc_pk)

def customer_doc_list(request):
    return render (request, 'customer_doc_list.html')


def pet_details(request):
    return render (request, 'pet_details_1.html')

###############################################################################################################
# ADMIN VIEWS:

def admin_home(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        users=User.objects.all()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser:
                return render(request,'admin/admin_home.html',{'username':user.username,'superuser':True})
            if user.is_staff:
                return render(request,'admin/admin_home.html',{'username':user.username,'superuser':False})
    return render (request,'admin/admin_login.html')



def doctor_registration(request):
	doctor=Doctor()
	if request.method == 'POST':
		doctor.Name_of_doctor=request.POST.get('first_name')
		doctor.first_name=request.POST.get('first_name')
		doctor.last_name=request.POST.get('last_name')
		doctor.Gender=request.POST.get('gender')
		doctor.Date_of_birth=request.POST.get('dob')
		doctor.Experience=request.POST.get('experience')
		doctor.Hospital=request.POST.get('hospital')
		doctor.Email=request.POST.get('email')
		doctor.Mobile=request.POST.get('mobile')
		doctor.Telephone=request.POST.get('telephone')
		doctor.Address=request.POST.get('address')
		doctor.Registration_number=request.POST.get('reg_no')
		doctor.password=request.POST.get('password')
		doctor.Qualification=request.POST.get('Qualification')
		doctor.consultation_fee=request.POST.get('consultation_fee')
		doctor.save()
		return render(request,'admin/admin_doc_registration.html')
	return render(request,'admin/admin_doc_registration.html')


def doctor_list(request):
    doctor_list=Doctor.objects.all()
    if request.method == 'POST':
        doc_pk=request.POST.get('doc_pk')
        doctor=Doctor.objects.filter(pk=doc_pk)
        return render(request,'admin/doctor_details.html',{'doctor':doctor})
    return render(request,'admin/doctor_list.html',{'doctor_list':doctor_list})

def check(request,pk):
    if pk:
        pk=pk
        return render(request,'admin/check.html',{'pk':pk})
    return render(request,'admin/check.html',)

def registrad_users_list(request):
    users=Customer.objects.all()
    return render(request,'admin/registred_users_list.html',{'user':users})

def patients_list(request):
	doctor_list=Doctor.objects.all()
	log=Log()
	if request.method == 'POST':
		doc_pk=request.POST.get('doc_pk')
		doct_object=Doctor.objects.get(id=doc_pk)
		date=request.POST.get('visit_date')
		doctorviewlog=DoctorViewLog.objects.filter(date=date,doc_pk=doct_object)
		return render(request,'admin/patients_list_detail.html',{'doctorviewlog':doctorviewlog})
	return render(request,'admin/patients_list.html',{'doctor_list':doctor_list})

def payment_anlytics(request):
    return render(request,'admin/payment_anlytics.html')

def doctor_corner(request):
    return render (request,'admin/doctors_corner.html')

def view_confernse(request,pk):
    if pk:
        conference = Conferences.objects.filter(id=pk)
        return render (request, 'admin/view_confernse.html',{'conferences':conference})
    return render (request, 'admin/view_confernse.html')

def conferences(request):
    conferences=Conferences.objects.all()
    if request.method == 'POST':
        con_pk = request.POST.get('con_pk')
        conference = Conferences.objects.filter(id=con_pk).delete()
    return render(request,'admin/conferences.html',{'conferences':conferences})


def create_confernse(request):
    conferences=Conferences()
    if request.method == 'POST':
        conferences.title = request.POST.get('title')
        conferences.location = request.POST.get('location')
        conferences.date = request.POST.get('posted_date')
        timings=request.POST.get('posted_time')
        conferences.timings = timings
        conferences.content = request.POST.get('content')
        conferences.save()
        return render(request,'admin/create_confernse.html')
    return render(request,'admin/create_confernse.html')


def seminars(request):
    seminars=Seminars.objects.all()
    if request.method == 'POST':
        sem_pk = request.POST.get('sem_pk')
        seminar = Seminars.objects.filter(id=sem_pk).delete()
    return render(request,'admin/seminars.html',{'seminars':seminars})

def view_seminar(request,pk):
    if pk:
        seminar = Seminars.objects.filter(id=pk)
        return render (request, 'admin/view_seminar.html',{'seminars':seminar})
    return render (request, 'admin/view_seminar.html')


def create_seminar(request):
    seminars=Seminars()
    if request.method == 'POST':
        seminars.title = request.POST.get('title')
        seminars.location = request.POST.get('location')
        seminars.date = request.POST.get('posted_date')
        timings=request.POST.get('posted_time')
        seminars.timings = timings
        seminars.content = request.POST.get('content')
        seminars.save()
        return render(request,'admin/create_seminar.html')
    return render(request,'admin/create_seminar.html')

def vet_news(request):
    vetnewsobj=Vet_News.objects.all()
    if request.method == 'POST':
        vn_pk = request.POST.get('vn_pk')
        vetnews = Vet_News.objects.filter(id=vn_pk).delete()
    return render(request,'admin/vet_news.html', {'vetnewsobj':vetnewsobj})


def view_vetnews(request,pk):
    if pk:
        vetnews = Vet_News.objects.filter(id=pk)
        return render (request, 'admin/view_vetnews.html',{'vetnews':vetnews})
    return render (request, 'admin/view_vetnews.html')


def create_vetnews(request):
    vet_news=Vet_News()
    if request.method == 'POST':
        vet_news.title = request.POST.get('title')
        vet_news.location = request.POST.get('location')
        vet_news.date = request.POST.get('posted_date')
        timings=request.POST.get('posted_time')
        vet_news.timings = timings
        vet_news.content = request.POST.get('content')
        vet_news.save()
        return render(request,'admin/create_vetnews.html')
    return render(request,'admin/create_vetnews.html')

def articles(request):
    articles=Articles.objects.all()
    if request.method == 'POST':
        art_pk = request.POST.get('art_pk')
        article = Articles.objects.filter(id=art_pk).delete()
    return render(request,'admin/articles.html',{'articles':articles})

def view_article(request,pk):
    if pk:
        article = Articles.objects.filter(id=pk)
        for i in article:
        	pass
        return render (request, 'admin/view_article.html',{'article':article})
    return render (request, 'admin/view_article.html')


def create_article(request):
    article=Articles()
    if request.method == 'POST':
        article.article_title = request.POST.get('title')
        article.summery = request.POST.get('summery')
        article.published_on = request.POST.get('posted_date')
        article.authors = request.POST.get('author')
        article.content = request.POST.get('content')
        article.save()
        return render(request,'admin/create_article.html')
    return render(request,'admin/create_article.html')


def case_reports(request):
    case_reports=Case_Reports.objects.all()
    if request.method == 'POST':
        report_pk = request.POST.get('report_pk')
        case_report = Case_Reports.objects.filter(id=report_pk).delete()
    return render(request,'admin/case_reports.html',{'case_reports':case_reports})


def view_casereport(request,pk):
    if pk:
        casereport = Case_Reports.objects.filter(id=pk)
        return render (request, 'admin/view_casereport.html',{'casereport':casereport})
    return render (request, 'admin/view_casereport.html')


def create_casereport(request):
    casereport=Case_Reports()
    if request.method == 'POST':
        casereport.title = request.POST.get('title')
        casereport.email = request.POST.get('email')
        casereport.published_on = request.POST.get('posted_date')
        casereport.author = request.POST.get('author')
        casereport.link = request.POST.get('link')
        casereport.save()
        return render(request,'admin/create_casereport.html')
    return render(request,'admin/create_casereport.html')

def books(request):
    book = Book()
    if request.method == 'POST' and request.FILES['myfile']:
        book.title = request.POST.get('title')
        book.file =  request.FILES['myfile']
        book.save()
        return render(request,'admin/books.html')
    return render(request,'admin/books.html')

def admin_pet_list(request,customer_id):
	customer_obj=Customer.objects.get(customer_id=customer_id)
	pet_list=Pet.objects.filter(customer_id=customer_obj)
	return render(request,'admin/customer_pets_list.html',{'pet_list':pet_list})

def admin_pet_summery(request,pet_id):
	pet_obj=Pet.objects.get(pet_id=pet_id)
	dates=PurposeAndDiet.objects.filter(pet_id=pet_obj)
	if request.method == "POST":
		date=request.POST.get('datename')
		date=datetime.datetime.strptime(date, '%b. %d, %Y').strftime('%Y-%m-%d')
		purpose_ids=PurposeAndDiet.objects.filter(date=date,pet_id=pet_obj).last()
		purpose_obj=PurposeAndDiet.objects.get(id=purpose_ids.id)
		try:
			vitals=Vitals.objects.filter(purpose_id=purpose_obj).last()
			vitals=model_to_dict(vitals)
			clean_dict = dict_clean(vitals)
			vitals = clean_dict

		except:
			pass

		try:
			assessment=Assessment.objects.filter(purpose_id=purpose_obj).last()
			assessment=model_to_dict(assessment)
			clean_dict = dict_clean(assessment)
			clean_dict=remove_empty_from_dict(clean_dict)
			assessment = clean_dict
		except:
			pass

		try:
			symptoms=purpose_obj
			symptoms=model_to_dict(symptoms)
			symptoms.pop('purpose_id',None)
			symptoms.pop('id',None)
			symptoms.pop('pet_id',None)
			symptoms.pop('vaccination_purpose',None)
			symptoms.pop('deworming_purpose',None)
			symptoms.pop('last_deworming',None)
			symptoms = dict_clean(symptoms)
		except:
			symptoms=""

		try:
			diagnostic=Diagnostics.objects.filter(purpose_id=purpose_obj).last()
			diagnostic=model_to_dict(diagnostic)
			clean_dict = dict_clean(diagnostic)
			diagnostic = remove_empty_from_dict(clean_dict)
		except:
			pass
		try:
			prescription=Prescription.objects.filter(purpose_id=purpose_obj).last()
			prescription=model_to_dict(prescription)
			clean_dict=dict_clean(prescription)
			prescription=remove_empty_from_dict(prescription)
			prescription.pop('purpose_id',None)
			prescription.pop('id',None)
			prescription.pop('date',None)

		except:
			pass
		try:
			vaccination=Vaccination.objects.filter(purpose_id=purpose_obj).last()
			vaccination=model_to_dict(vaccination)
			vaccination.pop('purpose_id',None)
			vaccination.pop('id',None)
			vaccination.pop('date',None)
			vaccination.pop('pet',None)
			vaccination = { k:v for k,v in vaccination.items() if v!= datetime.date(1000, 1, 1) }
		except:
			pass
		try:
			deworming=Deworming.objects.filter(purpose_id=purpose_obj).last()
			deworming=model_to_dict(deworming)
			deworming.pop('purpose_id',None)
			deworming.pop('id',None)
			deworming.pop('date',None)
			deworming.pop('pet',None)
			deworming = { k:v for k,v in deworming.items() if v!= datetime.date(1000, 1, 1) }
		except:
			pass
		return render(request,'admin/admin_pet_summery_date.html',{'symptoms':symptoms,'vitals':vitals,'assessment':assessment,
		'diagnostic':diagnostic,'prescription':prescription,'vaccination':vaccination,'deworming':deworming,})
	return render(request,'admin/admin_pet_summery.html',{'dates':dates,'pet_id':pet_id})

def admin_pet_summery_date(request,pet_id,date):
	pet_obj=Pet.objects.get(pet_id=pet_id)
	return render(request,'admin/admin_pet_summery_date.html',)

def pet_details(request,customer_id):
	customer_id=customer_id
	pet = Pet()
	if request.method =="GET":
		if 'customer_id' in request.session:
			return render (request, 'pet_details.html',{'customer_id':customer_id})
		else:
			return redirect ('customer_login_home')
		if request.method == 'POST':
			pet.name = request.POST.get('petname')
			pet.save()
			return render (request, 'pet_details.html')

def logout_customer(request):
	# logout(request)
	# return redirect('customer_login_home')

	try:
		if request.session.has_key('customer_id'):
			del request.session['customer_id']
			logout(request)
			return redirect('customer_login_home')
       # request.session.flush(
		if request.session.has_key('doctor_session_id'):
			del request.session['doctor_session_id']
			logout(request)
			return redirect('doctor_login')
	except KeyError:
		pass


#----------------------------------------------------------------------
#doctor corner side bar views

def articles_sbar(request,doc_id):
	doctor=Doctor.objects.get(id=doc_id)
	article=Articles.objects.all()
	bookmark=bookmarks_article.objects.filter(doc=doctor).all()
	x=[]
	for i in bookmark:
		x.append(i.article_id.id)
	return render(request,'doctor_corner/Doctors_corner_articles.html',{'article':article,'doc_id':doc_id,'bookmark':bookmark,'y':x})

def view_article_sbar(request,pk):

	if pk:
		article = Articles.objects.filter(id=pk)
		for i in article:
			print(i.article_title)
		return render (request, 'doctor_corner/Doctors_corner_viewarticle.html',{'article':article})
	return render (request, 'doctor_corner/Doctors_corner_viewarticle.html')

def case_reports_sbar(request,doc_id):
	doctor=Doctor.objects.get(id=doc_id)
	case_reports=Case_Reports.objects.all()
	bookmark=bookmarks_case_reports.objects.filter(doc=doctor).all()
	x=[]
	for i in bookmark:
		x.append(i.case_reports.id)
	if request.method == 'POST':
		report_pk = request.POST.get('report_pk')
	return render(request,'doctor_corner/Doctors_corner_case_reports.html',{'case_reports':case_reports,'doc_id':doc_id,'x':x})


def conferences_sbar(request,doc_id):
	doctor=Doctor.objects.get(id=doc_id)
	conferences=Conferences.objects.all()
	bookmark=bookmarks_conferences.objects.filter(doc=doctor).all()
	x=[]
	for i in bookmark:
		x.append(i.conferences.id)
	if request.method == 'POST':
		con_pk = request.POST.get('con_pk')
	return render(request,'doctor_corner/doctors_corner_conferences.html',{'conferences':conferences,'doc_id':doc_id,'x':x})

def vet_news_sbar(request,doc_id):
	doctor=Doctor.objects.get(id=doc_id)
	vetnewsobj=Vet_News.objects.all()
	bookmark=bookmarks_vet_news.objects.filter(doc=doctor).all()
	x=[]
	for i in bookmark:
		x.append(i.vet_news.id)
	if request.method == 'POST':
		vn_pk = request.POST.get('vn_pk')
	return render(request,'doctor_corner/Doctors_corner_vet_news.html', {'vetnewsobj':vetnewsobj,'doc_id':doc_id,'x':x})

def seminars_sbar(request,doc_id):
	doctor=Doctor.objects.get(id=doc_id)
	seminars=Seminars.objects.all()
	bookmark=bookmarks_seminars.objects.filter(doc=doctor).all()
	x=[]
	for i in bookmark:
		x.append(i.seminars.id)
	if request.method == 'POST':
		sem_pk = request.POST.get('sem_pk')

	return render(request,'doctor_corner/Doctors_corner_seminars.html',{'seminars':seminars,'doc_id':doc_id,'x':x})

def view_seminar_sbar(request,pk):
    if pk:
        seminar = Seminars.objects.filter(id=pk)
        return render (request, 'doctor_corner/Doctors_corner_view_seminar.html',{'seminars':seminar,})
    return render (request, 'doctor_corner/Doctors_corner_view_seminar.html')

def books_sbar(request,doc_id):
	doctor=Doctor.objects.get(id=doc_id)
	book=Book.objects.all()
	bookmark=bookmarks_books.objects.filter(doc=doctor).all()
	x=[]
	for i in bookmark:
		x.append(i.books.id)
	return render(request,'doctor_corner/Doctors_corner_books.html',{'book':book,'doc_id':doc_id,'x':x})


def articlepk(request):
	x=request.POST.get('obj',None)
	y=request.POST.get('doc',None)
	bmark=bookmarks_article()
	doc=Doctor.objects.get(id=y)
	article_id=Articles.objects.get(id=x)
	if bookmarks_article.objects.filter(article_id=article_id,doc=doc).exists():
		bookmarks_article.objects.filter(doc=doc,article_id=article_id).last().delete()
	else:
		bmark.doc=Doctor.objects.get(id=y)
		bmark.article_id=Articles.objects.get(id=x)
		bmark.save()
	data ={
		'hello':'hello'
	}
	return JsonResponse(data)

def casereportspk(request):
	x=request.POST.get('obj',None)
	y=request.POST.get('doc',None)
	bmark=bookmarks_case_reports()
	doc=Doctor.objects.get(id=y)
	Case_Reports_id=Case_Reports.objects.get(id=x)
	if bookmarks_case_reports.objects.filter(case_reports=Case_Reports_id,doc=doc).exists():
		bookmarks_case_reports.objects.filter(doc=doc,case_reports=Case_Reports_id).last().delete()
	else:
		bmark.doc=Doctor.objects.get(id=y)
		bmark.case_reports=Case_Reports.objects.get(id=x)
		bmark.save()
	data ={
		'hello':'hello'
	}
	return JsonResponse(data)

def conferencepk(request):
	x=request.POST.get('obj',None)
	y=request.POST.get('doc',None)
	bmark=bookmarks_conferences()
	doc=Doctor.objects.get(id=y)
	conference_id=Conferences.objects.get(id=x)
	if bookmarks_conferences.objects.filter(conferences=conference_id,doc=doc).exists():
		bookmarks_conferences.objects.filter(doc=doc,conferences=conference_id).last().delete()
	else:
		bmark.doc=Doctor.objects.get(id=y)
		bmark.conferences=Conferences.objects.get(id=x)
		bmark.save()
	data ={
		'hello':'hello'
	}
	return JsonResponse(data)

def seminarspk(request):
	x=request.POST.get('obj',None)
	y=request.POST.get('doc',None)
	bmark=bookmarks_seminars()
	doc=Doctor.objects.get(id=y)
	seminars_id=Seminars.objects.get(id=x)
	if bookmarks_seminars.objects.filter(seminars=seminars_id,doc=doc).exists():
		bookmarks_seminars.objects.filter(doc=doc,seminars=seminars_id).last().delete()
	else:
		bmark.doc=Doctor.objects.get(id=y)
		bmark.seminars=Seminars.objects.get(id=x)
		bmark.save()
	data ={
		'hello':'hello'
	}
	return JsonResponse(data)

def vetnewspk(request):
	x=request.POST.get('obj',None)
	y=request.POST.get('doc',None)
	bmark=bookmarks_vet_news()
	doc=Doctor.objects.get(id=y)
	vet_news_id=Vet_News.objects.get(id=x)
	if bookmarks_vet_news.objects.filter(vet_news=vet_news_id,doc=doc).exists():
		bookmarks_vet_news.objects.filter(doc=doc,vet_news=vet_news_id).last().delete()
	else:
		bmark.doc=Doctor.objects.get(id=y)
		bmark.vet_news=Vet_News.objects.get(id=x)
		bmark.save()
	data ={
		'hello':'hello'
	}
	return JsonResponse(data)

def bookspk(request):
	x=request.POST.get('obj',None)
	y=request.POST.get('doc',None)
	bmark=bookmarks_books()
	doc=Doctor.objects.get(id=y)
	books_id=Book.objects.get(id=x)
	if bookmarks_books.objects.filter(books=books_id,doc=doc).exists():
		bookmarks_books.objects.filter(doc=doc,books=books_id).last().delete()
	else:
		bmark.doc=Doctor.objects.get(id=y)
		bmark.books=Book.objects.get(id=x)
		bmark.save()
	data ={
		'hello':'hello'
	}
	return JsonResponse(data)

def bookmarks(request,doc_id):
	doctor=doc_id
	try:
		articles=bookmarks_article.objects.filter(doc=doctor).all()
	except:
		pass
	try:
		case_reports=bookmarks_case_reports.objects.filter(doc=doctor).all()
	except:
		pass
	try:
		conferences=bookmarks_conferences.objects.filter(doc=doctor).all()
	except:
		pass
	try:
		vet_news=bookmarks_vet_news.objects.filter(doc=doctor).all()
	except:
		pass
	try:
		seminars=bookmarks_seminars.objects.filter(doc=doctor).all()
	except:
		pass
	try:
		books=bookmarks_books.objects.filter(doc=doctor).all()
	except:
		pass
	return render(request,'doctor_corner/bookmarks.html',{'articles':articles,'case_reports':case_reports,'conferences':conferences,
	'vet_news':vet_news,'seminars':seminars,'books':books})

def VaccinationDewormingReminder(request):
	remiander_days=2
	last_dict={}
	dict={}
	vacanation_list=[]
	today_date=date.today()
	remindar_date = date.today() + timedelta(days=remiander_days)
	rabies_qs=Vaccination.objects.filter(due_date_rabies=remindar_date)
	print(rabies_qs,'77777')
	for r_q in rabies_qs:
		rabies_due_date=r_q.due_date_rabies
		petid_key=r_q.pet.pet_id
		if rabies_due_date == remindar_date:
			dict[petid_key] = ['rabies']
		else:
			pass
	print(dict,'12')
	distemper_qs=Vaccination.objects.filter(due_date_distemper=remindar_date)
	for d_q in distemper_qs:
		distemper_due_date=d_q.due_date_distemper
		petid_key=d_q.pet.pet_id
		if petid_key in dict:
			if distemper_due_date == remindar_date:
				x=dict.get(petid_key,"")
				x.append("distemper")
			else:
				pass
		else:
			dict[petid_key] = ['distemper']
	hepatitis_qs=Vaccination.objects.filter(due_date_hepatitis=remindar_date)
	for h_q in hepatitis_qs:
		hepatitis_due_date=h_q.due_date_hepatitis
		petid_key=h_q.pet.pet_id
		if petid_key in dict:
			if hepatitis_due_date == remindar_date:
				x=dict.get(petid_key,"")
				x.append("hepatitis")
			else:
				pass
		else:
			dict[petid_key] = ['hepatitis']
	parovirus_qs=Vaccination.objects.filter(due_date_parovirus=remindar_date)
	for p_q in parovirus_qs:
		parovirus_due_date=p_q.due_date_parovirus
		petid_key=p_q.pet.pet_id
		if petid_key in dict:
			if parovirus_due_date == remindar_date:
				x=dict.get(petid_key,"")
				x.append("parovirus")
			else:
				pass
		else:
			if parovirus_due_date == remindar_date:
				dict[petid_key] = ['parovirus']
			else:
				pass
	parainfluenza_qs=Vaccination.objects.filter(due_date_parainfluenza=remindar_date)
	for para_q in parainfluenza_qs:
		parainfluenza_due_date=para_q.due_date_parainfluenza
		petid_key=para_q.pet.pet_id
		if petid_key in dict:
			if parainfluenza_date == remindar_date:
				x=dict.get(petid_key,"")
				x.append("parainfluenza")
			else:
				pass
		else:
			dict[petid_key] = ['parainfluenza']
	bordetella_qs=Vaccination.objects.filter(due_date_bordetella=remindar_date)
	for b_q in bordetella_qs:
		bordetella_due_date=b_q.due_date_bordetella
		petid_key=b_q.pet.pet_id
		if petid_key in dict:
			if bordetella_due_date == remindar_date:
				x=dict.get(petid_key,"")
				x.append("bordetella")
			else:
				pass
		else:
			dict[petid_key] = ['bordetella']
	leptospirosis_qs=Vaccination.objects.filter(due_date_leptospirosis=remindar_date)
	for l_q in leptospirosis_qs:
		leptospirosis_due_date=l_q.due_date_leptospirosis
		petid_key=l_q.pet.pet_id
		if petid_key in dict:
			if leptospirosis_due_date == remindar_date:
				x=dict.get(petid_key,"")
				x.append("leptospirosis")
			else:
				pass
		else:
			dict[petid_key] = ['leptospirosis']
	lymedisease_qs=Vaccination.objects.filter(due_date_lymedisease=remindar_date)
	for ly_q in lymedisease_qs:
		lymedisease_due_date=ly_q.due_date_lymedisease
		petid_key=ly_q.pet.pet_id
		if petid_key in dict:
			if lymedisease_due_date == remindar_date:
				x=dict.get(petid_key,"")
				x.append("lymedisease")
			else:
				pass
		else:
			dict[petid_key] = ['lymedisease']
	coronavirus_qs=Vaccination.objects.filter(due_date_coronavirus=remindar_date)
	for c_q in coronavirus_qs:
		coronavirus_due_date=c_q.due_date_coronavirus
		petid_key=c_q.pet.pet_id
		if petid_key in dict:
			if coronavirus_due_date == remindar_date:
				x=dict.get(petid_key,"")
				x.append("coronavirus")
			else:
				pass
		else:
			dict[petid_key] = ['coronavirus']
	giardia_qs=Vaccination.objects.filter(due_date_giardia=remindar_date)
	for q_q in giardia_qs:
		giardia_due_date=q_q.due_date_giardia
		petid_key=q_q.pet.pet_id
		if petid_key in dict:
			if giardia_due_date == remindar_date:
				x=dict.get(petid_key,"")
				x.append("giardia")
			else:
				pass
		else:
			dict[petid_key] = ['giardia']
	dhpp_qs=Vaccination.objects.filter(due_date_dhpp=remindar_date)
	for dh_q in dhpp_qs:
		dhpp_due_date=dh_q.due_date_dhpp
		petid_key=dh_q.pet.pet_id
		if petid_key in dict:
			if dhpp_due_date == remindar_date:
				x=dict.get(petid_key,"")
				x.append("dhpp")
			else:
				pass
		else:
			dict[petid_key] = ['dhpp']
	dict_keys=dict.keys()
	for item in dict_keys:
		print(item,'hfajkshfkjahfkjahdfkjahskjfhasjkh')
		doctor=DoctorViewLog.objects.filter(pet_id=item).last().doc_pk.Name_of_doctor
		hospital_name=DoctorViewLog.objects.filter(pet_id=item).last().doc_pk.Hospital
		vaccination_remainder=Vccination_Remainder()
		vaccinations=dict.get(item,"")
		pet=Pet.objects.get(pet_id=item)
		customer_obj=pet.customer_id
		vaccination_remainder.pet=pet
		vaccination_remainder.customer=customer_obj
		vaccinations =list(dict.fromkeys(vaccinations))
		vaccination_remainder.vacanation_list=vaccinations
		vaccination_remainder.doctor=doctor
		vaccination_remainder.remiander_date=remindar_date
		vaccination_remainder.hospital=hospital_name
		vaccination_remainder.save()
	#showing vacanation list_patient
	vacanation_list_rem=Vccination_Remainder.objects.filter(remiander_date=remindar_date)
	return render(request,'admin/vaccination.html',{'vacanation_list_rem':vacanation_list_rem,'remindar_date':remindar_date})
