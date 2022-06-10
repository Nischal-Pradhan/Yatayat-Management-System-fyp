from . import views
from django.contrib import admin
from django.urls import path, include
# from django.conf.urls import url

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('welcome', views.welcome, name="welcome"),
    
    path('about', views.about, name="about"),

    path('tickets', views.tickets, name="tickets"),
    path('bookings', views.bookings, name="bookings"),
    path('cancellings', views.cancellings, name="cancellings"),
    path('seebookings', views.seebookings, name="seebookings"),

    path('routes', views.routes, name="routes"),

    path('contact', views.contact, name="contact"),
    path('settings', views.settings, name="settings"),

]

