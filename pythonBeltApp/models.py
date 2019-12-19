from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        userMatch= User.objects.filter(username= postData['username'])
        if len(userMatch) > 0:
            errors['usermatch']= 'User already exists'        
        if len(postData['name']) < 3:
            errors['name']= 'Name must be at least 3 characters'
        if len(postData['username']) < 3:
            errors['username']= 'Username must be at least 3 characters'
        if len(postData['pw']) < 8:
            errors['pw']= 'Password must be at least 8 characters'
        if postData['pw'] != postData['cpw']:
            errors['cpw']= 'Password and confirm must match' 
        print(errors)
        return errors

    def loginValidator(self, postData):   
        errors={}
        userMatch= User.objects.filter(username= postData['username'])

        if len(userMatch) == 0: 
            errors['userMatch']= 'No User Found'

        else:
            person= userMatch[0]
            if bcrypt.checkpw(postData['pw'].encode(), person.password.encode() ):
                print('password matched')
            else:
                errors['pw']= 'Password is invalid'

        print(errors)
        return errors


class User(models.Model):
    name= models.CharField(max_length= 255)
    username= models.CharField(max_length= 255)
    password= models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= UserManager()


class Destination(models.Model):
    location= models.CharField(max_length= 255)
    desc= models.TextField ()
    start_date= models.DateField()
    end_date= models.DateField()
    creator= models.ForeignKey(User, related_name='created_by', on_delete= models.CASCADE)
    travlers= models.ManyToManyField(User, related_name='friends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)