"""aodh_pet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from pet import  views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('social_django.urls', namespace='social')),
    path('reg/',views.doctor),
    path('patients/list/<int:doc_id>/',views.list_patient,name='list_patient'),
    path('visitp/<str:pet_pk>/<str:purpose_pk>/<int:doc_id>/',views.visit_purpose2,name='visit_purpose2'),
    path('symptoms/<int:pet_pk>/<str:purpose_pk>/<int:doc_id>/',views.symptoms,name='symptoms'),
    path('vitals/<int:pet_pk>/<str:purpose_pk>/<int:doc_id>/',views.vitals,name='vitals'),
    path('assessment/<int:pet_pk>/<str:purpose_pk>/<int:doc_id>/',views.Assessment_view,name='assessment'),
    path('diagnostic/<int:pet_pk>/<str:purpose_pk>/<int:doc_id>/',views.diagnostic,name='diagnostic_prescription'),
    path('vaccination/<int:pet_pk>/<str:purpose_pk>/<int:doc_id>/',views.vaccination,name='vaccination'),
    path('deworming/<int:pet_pk>/<str:purpose_pk>/<int:doc_id>/',views.deworming,name='deworming'),
    path('summary/<int:pet_pk>/<str:purpose_pk>/',views.summary,name='summary'),
    path('doctor_history/<int:pet_pk>/<str:purpose_pk>/',views.doctor_history,name='doctor_history'),
    path('doctor_history_summary/<int:pet_pk>/<str:purpose_pk>/',views.doctor_history_summary,name='doctor_history_summary'),
    path('danalytics/<int:doc_id>/',views.doctoranalytics,name='danalytics'),
    path('analyticssummary/(?p<pk>[0-9]+)/(?p<value>[0-9]+)/<int:doc_id>/',views.summary_analytics,name='summary_analytics'),
    path('doctor_profile/<int:doc_id>/',views.doctor_profile,name='doctor_profile'),
    path('petdetails/<str:customer_id>/<str:doc_pk>/',views.petdetails,name='petdetails'),
    path('purpose_visit/<str:customer_id>/<str:pet_id>/<str:doc_pk_org>/<int:purpose_id>/',views.purpose_visit,name='purpose_visit'),
    path('petdite/<str:customer_id>/<str:pet_id>/<str:doc_pk_org>/<int:purpose_id>/',views.purpose_and_dite,name='pet_dite'),
    path('booking_summary/<str:customer_id>/<pet_id>/<str:doc_pk>/<int:purpose_id>/',views.booking_summary,name='booking_summary'),
    path('pay_online_conform/<str:customer_id>/<str:doc_pk>/<str:pet_id>/<str:purpose_id>/',views.pay_online_conform,name='pay_online_conform'),
    path('booking_confirm/<str:customer_id>/<str:doc_pk>/<str:pet_id>/<str:purpose_id>/',views.booking_confirm,name='booking_confirm'),
    path('customer/reg/<int:pk>/',views.customer_registration, name='customer_registration'),
    path('customer/login/', views.customer_login, name='customer_login_home'),
    path('customer/login/<int:pk>/', views.customer_login, name='customer_login'),
    path('customer/doclist/', views.customer_doc_list, name='customer_doc_list'),
    path('petprofile/<str:customer_id>/', views.pet_profile, name='pet_profile'),
    path('last_vaccination/<str:customer_id>/', views.last_vaccination, name='last_vaccination'),
    path('last_deworming/<str:customer_id>/', views.last_deworming, name='last_deworming'),
    path('summary_customer/<str:customer_id>/<pet_id>/',views.customer_previous,name='summary_customer'),
    path('customer_previous_visit/<purpose_id>/',views.summary_customer,name='customer_previous_visit'),
    path('doctorlogin', views.doctor_login, name='doctor_login'),
    path('home/login',views.admin_home, name='admin_home'),
    path('doctor/registration',views.doctor_registration, name='doctor_registration'),
    path('doctor/list',views.doctor_list, name='doctor_list'),
    path('doctor/check/(?P<pk>[0-9]+)/',views.check, name='check'),
    path('registradusers/list',views.registrad_users_list, name='registrad_users_list'),
    path('patients/list',views.patients_list, name='patients_list'),
    path('payment_anlytics',views.payment_anlytics, name='payment_anlytics'),
    path('doctorscorner',views.doctor_corner, name='doctors_corner'),
    path('conferences',views.conferences, name='conferences'),
    path('createconfernse',views.create_confernse, name='create_confernse'),
    path('viewconfernse/<int:pk>/',views.view_confernse, name='view_confernse'),
    path('seminars',views.seminars, name='seminars'),
    path('createseminar',views.create_seminar, name='create_seminar'),
    path('viewseminar/<int:pk>/',views.view_seminar, name='view_seminar'),
    path('vetnews',views.vet_news, name='vet_news'),
    path('createvetnews',views.create_vetnews, name='create_vetnews'),
    path('viewvetnews/<int:pk>/',views.view_vetnews, name='view_vetnews'),
    path('articles',views.articles, name='articles'),
    path('createarticle',views.create_article, name='create_article'),
    path('viewarticle/<int:pk>/',views.view_article, name='view_article'),
    path('books',views.books, name='books'),
    path('casereports',views.case_reports, name='case_reports'),
    path('createcasereport',views.create_casereport, name='create_casereport'),
    path('viewcasereport/<int:pk>/',views.view_casereport, name='view_casereport'),
    path('admin/pet/list/<str:customer_id>/', views.admin_pet_list, name='admin_pet_list'),
    path('admin/pet/summery/<str:pet_id>/', views.admin_pet_summery, name='admin_pet_summery'),
    path('admin/pet/summery/date/<str:pet_id>/', views.admin_pet_summery_date, name='admin_pet_summery_date'),
    path('admin/vaccination/',views.VaccinationDewormingReminder,name="vaccination_remainder"),

    #second visit urls
    path('secondtimepet/<str:customer_id>/<str:doc_pk>/',views.second_visit_petdetails,name='second_visit_petdetails'),
    path('addpet/<str:customer_id>/<str:doc_pk>/',views.addpet,name='addpet'),
    path('socialreg/',views.socialreg,name="socialreg"),

    path('logout',views.logout_customer,name='logout'),
    path('ajax/validate_email/', views.validate_email, name='validate_email'),
    path('ajax/validate_mobile/', views.validate_mobile, name='validate_mobile'),
       #doctors_corner
    path('articles_sbar/<str:doc_id>/', views.articles_sbar, name='articles_sbar'),
    path('articles_sbar_view/<int:pk>/', views.view_article_sbar, name='view_article_sbar'),
    path('case_reports_sbar/<str:doc_id>/', views.case_reports_sbar, name='case_reports_sbar'),
    path('conferences_sbar/<str:doc_id>/', views.conferences_sbar, name='conferences_sbar'),
    path('vet_news_sbar/<str:doc_id>/', views.vet_news_sbar, name='vet_news_sbar'),
    path('seminars_sbar/<str:doc_id>/', views.seminars_sbar, name='seminars_sbar'),
    path('view_seminar_sbar/<int:pk>/', views.view_seminar_sbar, name='view_seminar_sbar'),
    path('books_sbar/<str:doc_id>/', views.books_sbar, name='books_sbar'),
    path('x/',views.articlepk),
    path('casereportspk/',views.casereportspk),
    path('conferencepk/',views.conferencepk),
    path('seminarspk/',views.seminarspk),
    path('vetnewspk/',views.vetnewspk),
    path('bookspk/',views.bookspk),
    path('bookmarks/<str:doc_id>/',views.bookmarks,name="bookmarks"),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='commons/password-reset/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='commons/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='commons/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='commons/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
