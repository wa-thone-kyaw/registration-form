from django.db import models


class Book(models.Model):
    myanname = models.CharField(max_length=200)
    engname = models.CharField(max_length=200)
    nrc = models.CharField(max_length=200)
    birthDay = models.DateField()
    nation = models.CharField(max_length=200)
    seatno = models.CharField(max_length=200)
    score = models.CharField(max_length=200)
    passedseat_no = models.CharField(max_length=200)
    currentseat_no = models.CharField(max_length=200)
    myanfathername = models.CharField(max_length=200)
    engfathername = models.CharField(max_length=200)
    fathernrc = models.CharField(max_length=200)
    fathernation = models.CharField(max_length=200)
    fatherjob = models.CharField(max_length=200)
    mothername = models.CharField(max_length=200)
    mothernrc = models.CharField(max_length=200)
    mothernation = models.CharField(max_length=200)
    motherjob = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=200)
    student_no = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="photos/")

    def __str__(self):
        return self.title
    
    class FirstYear(models.Model):
    myanname = models.CharField(max_length=200)
    engname = models.CharField(max_length=200)
    nrc = models.CharField(max_length=200)
    birthDay = models.DateField()
    nation = models.CharField(max_length=200)
    seatno = models.CharField(max_length=200)
    score = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    passedseat_no = models.CharField(max_length=200)
    myanfathername = models.CharField(max_length=200)
    engfathername = models.CharField(max_length=200)
    fathernrc = models.CharField(max_length=200)
    fathernation = models.CharField(max_length=200)
    fatherjob = models.CharField(max_length=200)
    mothername = models.CharField(max_length=200)
    mothernrc = models.CharField(max_length=200)
    mothernation = models.CharField(max_length=200)
    motherjob = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=200)
    student_no = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="photos/")
    selectedValue=models.CharField(max_length=50)
    selectedValue2=models.CharField(max_length=50)
    selectedValue3=models.CharField(max_length=50)
    selectedValue4=models.CharField(max_length=50)
    selectedValue5=models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
    
