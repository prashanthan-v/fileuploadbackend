from django.db import models

# Create your models here.

class Students(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()


    def __str__(self):
        return f"{self.name} ({self.age} years old),"
    
class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.TextField() 

    def __str__(self):
        return self.name 