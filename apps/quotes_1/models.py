from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
NAME_RE = re.compile(r'[a-zA-Z]\D{2,}$')

class UserManager(models.Manager):
    #order first_name, last_name, email, pwd, cpwd
    def register(self, *args):
        errormsg = []
        status = True
        if not NAME_RE.match(args[0]):
            errormsg.append('first name need to be 2 character long no numbers and not empty .booooo')
            status = False
        if not NAME_RE.match(args[1]):
            errormsg.append('Last name need to be 2 character long no numbers and not empty .booooo')
            status = False
        if len(Users.objects.filter(email=args[2])) > 0:
            errormsg.append('email is already in the database')
            status = False
        if not EMAIL_REGEX.match(args[2]):
            errormsg.append('email is invalid search google for a correct format ')
            status = False
        if len(args[3]) < 8:
            errormsg.append('password needs to be longer than 8 character')
            status = False
        if args[3] != args[4]:
            errormsg.append('password does not match')
            status = False
        if status == False:
            return {'error': errormsg}
        if status == True:
            password = args[3].encode()
            pwhash= bcrypt.hashpw(password,bcrypt.gensalt())
            super(UserManager, self).create(first_name=args[0], last_name=args[1], email=args[2], password=pwhash)
        return {'first_name': args[0], 'last_name': args[1], 'email' : args[2], 'password': args[3]}

    def login(self, email, password):
        errormsg = []
        status = True
        existing = Users.objects.filter(email=email)
        if len(existing) <= 0:
            errormsg.append('please provided registered credentials')
            status = False
        elif not existing:
            errormsg.append('not {} in database!'.format(request.POST['email']))
            status = False
        elif not bcrypt.checkpw(password.encode(), existing[0].password.encode()):
            errormsg.append('password does not match')
            status = False
        if status == False:
            return {'error': errormsg}
        else:
            return{ 'True': existing[0].id }


class Users(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class QuotesManager(models.Manager):
    def validate(self, postData, user):
        errormsg = []
        status = True

        if len(postData['message'])< 10:
            errormsg.append('needs to be at least 10 characters long')
            status= False
        if len(postData['qby'])< 3:
            errormsg.append('needs to at least 3 charcters')
            status = False
        if status == False:
            return {'error': errormsg}
        else:
            Quotes.objects.create(content = postData['message'], quoteby=postData['qby'], creator = Users.objects.get(id=user))
            return{}
    def favorite(self, userid, qid):

        if len(Quotes.objects.filter(id=qid, favorited__id=userid))>0:
            
            return{'error': 'you favorited this item' }
        else:
            this_quote = Quotes.objects.get(id=qid)
            this_user = Users.objects.get(id=userid)
            this_quote.favorited.add(this_user)
        return {}



class Quotes(models.Model):
    content = models.CharField(max_length=1000)
    creator = models.ForeignKey(Users)
    quoteby = models.CharField(max_length=1000)
    favorited = models.ManyToManyField(Users, related_name = 'users_favorite')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = QuotesManager()
