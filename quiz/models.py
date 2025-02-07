from django.db import models

# Create your models here.
class User(models.Model):
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    score=models.IntegerField()
    

class Scenario(models.Model):
    id = models.AutoField(primary_key=True)
    type=models.CharField(max_length=255)
    titre= models.CharField(max_length=255)
    description=models.TextField()
    sender=models.CharField(max_length=255,blank=True)
    sender_mail=models.EmailField(max_length=255,blank=True)
    image=models.ImageField(upload_to='images/',blank=True)
    footer=models.TextField(blank=True)
    button=models.CharField(max_length=255,blank=True)
    url=models.URLField(max_length=255,blank=True)
    objet=models.CharField(max_length=255,blank=True)
    mail_body=models.TextField(blank=True)
    reponse=models.BooleanField()
    explication=models.TextField()
    

class Quiz(models.Model):
    id=models.AutoField(primary_key=True)
    id_user=models.ForeignKey(User, on_delete=models.CASCADE)
    nbre_questions=models.IntegerField()
    nbCorrect=models.IntegerField()
    nbFausse=models.IntegerField()

class Stat(models.Model):
    id=models.AutoField(primary_key=True)
    id_user=models.ForeignKey(User, on_delete=models.CASCADE)
    nbre_questions=models.IntegerField()
    nbCorrect=models.IntegerField()
    nbFausse=models.IntegerField()
    date_test = models.DateTimeField(auto_now_add=True)
    score=models.IntegerField()
    pourcentage=models.FloatField()
    def __str__(self):
        return self.id_user.name
