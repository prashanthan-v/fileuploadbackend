from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from .models import Students


# Create your views here.


def greetings(request):
  return HttpResponse("Hello world!!")

def stat(request, status):
    actualstat = ""
    if status == 1:
        actualstat = "present"
    else:
        actualstat = "absent"
    
    # Use the actualstat variable to generate a meaningful response
    # return HttpResponse(f"Status: {actualstat}")
    return redirect(reverse("greetingsname"))

# create using models
def create (request):
 
   for i in range(2,6):
      s1 =  Students()
      s1.name = f"name{i}"
      s1.age = i
      s1.save() 
   return HttpResponse("student created")   

# read using model

def read (request):
   allstudents = Students.objects.all()
   return HttpResponse(allstudents)


# update using model

def update (request):
   s3 = Students.objects.get(id=3)
   s3.name = "uma"
   s3.age = 55
   s3.save()
   return HttpResponse("updated")

# delete using model

def delete(request):
   s3 = Students.objects.get(id=2)
   
   s3.delete()
   return HttpResponse("deleted")
