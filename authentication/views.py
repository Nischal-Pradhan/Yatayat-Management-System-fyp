from distutils.log import error
import email
from email import message
from multiprocessing import context
from select import select
from tkinter.tix import Form
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .models import User, Bus, Book
from decimal import Decimal
from django.core.mail import send_mail

from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

@login_required(login_url='signin')
def welcome(request):
    return render(request, "authentication/welcome.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpw = request.POST['confirmpw']

        newuser = User.objects.create_user(username, email, password)
        newuser.first_name = fname
        newuser.last_name = lname

        newuser.save()

        messages.success(request, "Your account has been created successfully.")

        return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('welcome')

        else:
            messages.error(request, "Incorrect Credientials. Please try again.")
            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "User Logged Out.")
    return redirect('home')

@login_required(login_url='signin')
def about(request):
    return render(request, "authentication/about.html")

@login_required(login_url='signin')
@csrf_exempt
def tickets(request):
    context = {}
    if request.method == 'POST':
        from_req = request.POST.get('source')
        to_req = request.POST.get('dest')
        date_req = request.POST.get('date')

        available_bus = Bus.objects.filter(source=from_req, dest=to_req, date=date_req)

        if available_bus:
            return render(request, 'authentication/availablebus.html', locals())
        else:
            context["error"] = "Sorry, the bus you are searching for is unavailable."
            return render(request, 'authentication/tickets.html', context)
            
    else:
        return render(request, "authentication/tickets.html")

@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_req = request.POST.get('bus_id')
        seats_req = int(request.POST.get('no_seats'))
        bus = Bus.objects.get(id=id_req)
        if bus:
            if bus.rem > int(seats_req):
                name_req = bus.bus_name
                cost = int(seats_req) * bus.price
                from_req = bus.source
                to_req = bus.dest
                nos_req = Decimal(bus.nos)
                price_req = bus.price
                date_req = bus.date
                time_req = bus.time
                username_req = request.user.username
                email_req = request.user.email
                userid_req = request.user.id
                rem_req = bus.rem - seats_req
                Bus.objects.filter(id=id_req).update(rem=rem_req)
                book = Book.objects.create(name=username_req, email=email_req, userid=userid_req, bus_name=name_req,
                                           source=from_req, busid=id_req,
                                           dest=to_req, price=price_req, nos=seats_req, date=date_req, time=time_req,
                                           status='BOOKED')
                print('------------book id-----------', book.id)
                return render(request, 'authentication/bookings.html', locals())
            else:
                context["error"] = "Please select fewer number of seats. There are no more available seats as per your request."
                return render(request, 'authentication/tickets.html', context)

    else:
        return render(request, 'authentication/tickets.html')

@login_required(login_url='signin')
@csrf_exempt
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_req = request.POST.get('bus_id')
        
        try:
            book = Book.objects.get(id=id_req)
            bus = Bus.objects.get(id=book.busid)
            rem_req = bus.rem + book.nos
            Bus.objects.filter(id=book.busid).update(rem=rem_req)
            Book.objects.filter(id=id_req).update(status='CANCELLED')
            Book.objects.filter(id=id_req).update(nos=0)
            return redirect(seebookings)
            
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that bus"
            return render(request, 'authentication/availablebus.html', context)
    else:
        return render(request, 'authentication/tickets.html')


@login_required(login_url='signin')
def seebookings(request,new={}):
    context = {}
    id_req = request.user.id
    booked_list = Book.objects.filter(userid=id_req)
    if booked_list:
        return render(request, 'authentication/booklist.html', locals())
    else:
        context["error"] = "Sorry no buses booked"
        return render(request, 'authentication/tickets.html', context)


@login_required(login_url='signin')
def routes(request):
    return render(request, "authentication/routes.html")

@login_required(login_url='signin')
def contact(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        selectSubject = request.POST['selectSubject']
        message = request.POST['message']

        data = {
            'username': username,
            'email': email,
            'selectSubject': selectSubject,
            'message': message,
        }
        
        message = '''
        MESSAGE: {}

        FROM: {}
        '''.format(data['message'], data['email'])
        send_mail(data['selectSubject'], message, '', ['info.yatayatmanagement.fyp@gmail.com'])

        messages.success(request, "Your report has been submitted. We will contact you very soon. Stay Tuned, Thank You.")

    return render(request, "authentication/contact.html")

@login_required(login_url='signin')
def settings(request):
    return render(request, "authentication/settings.html")


# ## change password view
# @login_required(login_url='signin')
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('change_password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'accounts/change_password.html', {
#         'form': form
#     })


