from django.shortcuts import render
from django.http import HttpResponse
from .models import Register
# Create your views here.

def hello(request):
    return HttpResponse("Hello world")

def register_data(request):
    # print(request)
    if request.method == "POST":
        # print(request.POST)
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        mobile = request.POST['mobile']
        print(name,email,password,mobile)
        Register.objects.create(name=name,email=email,mobile=mobile,password=password)
        return HttpResponse("Registration Successful")
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
        password = request.POST['password']
        mobile = request.POST['mobile']
        print(name,email,password,mobile)
        data.name = name
        data.email =email
        data.mobile = mobile
        data.password = password
        data.save()
        return HttpResponse("Updation Successful")
    return render(request,'update_data.html',{"data":data})

def delete_data(request,name):
    data = Register.objects.get(name=name)
    data.delete()
    return HttpResponse("Deleted SuccessFully")