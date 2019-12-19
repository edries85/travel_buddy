from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
import bcrypt
from django.db.models import Q

def index(request):

    return render(request,'index.html')

def createuser(request):
    print(request.POST)
    validationErrors= User.objects.basic_validator(request.POST)
    if len(validationErrors) > 0:
        for key, value in validationErrors.items():
            messages.error(request, value)
        return redirect('/main')
    else:
        hashedpassword= bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
        newuser= User.objects.create(name= request.POST['name'],username= request.POST['username'], password= hashedpassword)
        print(newuser)
        request.session['loggedInUser']= newuser.id
        return redirect('/travels')


def login(request):
    print(request.POST)
    validationErrors= User.objects.loginValidator(request.POST)
    
    if len(validationErrors) > 0:
        for key, value in validationErrors.items():
            messages.error(request, value)
        return redirect('/main')
    user= User.objects.get(username= request.POST['username'])
    request.session['loggedInUser']= user.id
    return redirect('/travels')




def dashboard(request):
    user= User.objects.get(id= request.session['loggedInUser'])
    usertrips= Destination.objects.filter(Q(travlers= user) | Q(creator=user))
    other_usertrips= Destination.objects.exclude(Q(travlers= user) | Q(creator=user))
    destination= Destination

    Destination.objects.exclude(Q(travlers= user) | Q(creator=user))
    
    
    context={
        'loggedInUser': user,
        'usertrips': usertrips,
        'othertrips': other_usertrips
    }
    
    return render(request,'dashboard.html',context)



def addtrip(request):

    return render(request,'addtrip.html')

def createtrip(request):
    print(request.POST)
    loggedinuser= User.objects.get(id=request.session['loggedInUser'])
    newtrip= Destination.objects.create(location= request.POST['location'], desc= request.POST['description'], start_date=request.POST['start_date'], creator= loggedinuser, end_date=request.POST['end_date'])
    print(newtrip)
    return redirect('/travels')

def jointrip(request,tripsID):
    print(request.POST)
    user= User.objects.get(id= request.session['loggedInUser'])
    destination= Destination.objects.get(id= tripsID)
    destination.travlers.add(user)

    print(destination)

    return redirect('/travels')

def destinationInfo(request, destination_Id):
    this_trip= Destination.objects.get(id= destination_Id)
    travelers= this_trip.travlers.all()    

    context={
        
        'destination': Destination.objects.get(id= destination_Id),
        'this_trip': travelers
    }

    return render(request,'destinfo.html', context)

def logout(request):
    request.session.clear()
    return redirect('/main')

def signin(request):

    return render(request,'signin.html')