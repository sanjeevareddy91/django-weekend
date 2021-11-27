from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Register
from .forms import RegisterModelForm,RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import random
import requests
import json
# Create your views here.


def sms_send(msg):
    # mention url
    url = "https://www.fast2sms.com/dev/bulk"
    
    
    # create a dictionary
    my_data = {
        # Your default Sender ID
        'sender_id': 'FSTSMS', 
        
        # Put your message here!
        'message': msg, 
        
        'language': 'english',
        'route': 'p',
        
        # You can send sms to multiple numbers
        # separated by comma.
        'numbers': '9502563925,8688364718'    
    }
    
    # create a dictionary
    headers = {
        'authorization': 'n96mTfqdKo5sVQXLNMW32RG4h8HtUYEwvFkByupAgxIrZlJPiSqGr0D6xJkwb13CSIyQs5u8B9c7HXmt',
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }
    response = requests.request("POST",
                                url,
                                data = my_data,
                                headers = headers)
    returned_msg = json.loads(response.text)
    return returned_msg
    # print the send message
    
def hello(request):
    return HttpResponse("Hello world")

def register_data(request):
    print(request)
    if request.method == "POST":
        print(request.POST)
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        mobile = request.POST['mobile']
        address = request.POST['address']
        print(name,email,password,mobile)
        user_data = User(username=name,email=email)
        user_data.set_password(password)
        user_data.is_active = True
        user_data.is_staff = True
        if request.POST.get('superuser') == 'True':
            user_data.is_superuser=True
        user_data.save()
        Register.objects.create(name=name,email=email,mobile=mobile,address=address,user=user_data)
        msg = "Hi {}, Your registration if successful".format(name)
        send_mail("Registration Confirmation",msg,settings.EMAIL_HOST_USER,[email],fail_silently=False)
        messages.success(request,"Registration Successful")

    return render(request,'register_form.html')

def data_list(request):
    all_data = Register.objects.all()
    return render(request,'list.html',{"data":all_data})

def single_data(request,name):
    data = Register.objects.get(name=name)
    return render(request,"single_data.html",{"data":data})

def update_data(request,name):
    data = Register.objects.get(name=name)
    if request.method == "POST":
        # print(request.POST)
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        print(name,email,mobile)
        data.name = name
        data.email =email
        data.mobile = mobile
        data.save()
        messages.success(request,"Updation Successful")
        return redirect('data_list')
    return render(request,'update_data.html',{"data":data})

def delete_data(request,name):
    data = Register.objects.get(name=name)
    data.delete()
    return HttpResponse("Deleted SuccessFully")

def register_modelform(request):
    form = RegisterModelForm()
    if request.method == "POST":
        form_data = RegisterModelForm(request.POST)
        if form_data.is_valid():
            name = form_data.cleaned_data['name']
            print(name)
            form_data.save()
    return render(request,'register_modelform.html',{'form':form})


def register_normalform(request):
    form = RegisterForm()
    if request.method == "POST":
        form_data = RegisterForm(request.POST)
        if form_data.is_valid():
            name = form_data.cleaned_data['name']
            email = form_data.cleaned_data['email']
            password = form_data.cleaned_data['password']
            mobile = form_data.cleaned_data['mobile']
            print(name,email,password,mobile)
            Register.objects.create(name=name,email=email,mobile=mobile,password=password)
    return render(request,"register_normalform.html",{'form':form})


def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        get_user = User.objects.get(email=email)
        password = request.POST['password']
        logged_user = authenticate(username=get_user.username,password=password)
        if logged_user:
            login(request,logged_user)
            messages.success(request,"Logged in Successfully")
            return redirect('data_list')
        else:
            messages.error(request,"Email and Password Mismatch")
    return render(request,'login.html')

def logout_user(request):
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return redirect('login_user')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        check_email = Register.objects.filter(email=email)
        if check_email:
            new_otp = random.randint(1000,999999)
            msg = "Hi {}, Please use {} OTP for Password Update Verification".format(check_email[0].name,new_otp)
            # send_mail("Password Update Request OTP",msg,settings.EMAIL_HOST_USER,[email],fail_silently=False)
            sms_send(msg)
            check_email[0].otp = new_otp
            check_email[0].save()
            messages.success(request,"Otp Sent to Email")
            return redirect('verify_otp',id=check_email[0].id)
        else:
            messages.error(request,"Enter correct email!")

    return render(request,'forgot_password.html')

def verify_otp(request,id):
    get_info = Register.objects.get(id=id)
    if request.method == "POST":
        otp = request.POST['otp']
        if get_info.otp == otp:
            messages.success(request,"OTP Verified")
            return redirect('confirm_password',id=get_info.id)
        else:
            messages.warning(request,"OTP missmatch check it once!")
    return render(request,"verify_otp.html")

def confirm_password(request,id):
    get_info = Register.objects.get(id=id)
    if request.method == "POST":
        new_password = request.POST['new_password']
        user_data = get_info.user
        print(user_data)
        user_data.set_password(new_password)
        user_data.save()
        messages.success(request,'Password Updated Successfully')
        return redirect('login_user')
    return render(request,"confirm_password.html")