from django.shortcuts import render, redirect, HttpResponse
from .models import Users, Quotes
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'quotes_1/index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    register_check = Users.objects.register(request.POST['first_name'],request.POST['last_name'],request.POST['email'],request.POST['pwd'], request.POST['cpwd'])
    if 'error' in register_check:
        error = register_check['error']
        for msg in error:
            messages.error(request, msg)
        return redirect('/')
    else:
        user = Users.objects.filter(email=request.POST['email'])
        request.session['userid'] = user[0].id

    return redirect('/process')

def login(request):
    if request.method == "GET":
        return redirect('/')
    login_check = Users.objects.login(request.POST['email'],request.POST['pwd'])
    if 'error' in login_check:
        error = login_check['error']
        for msg in error:
            messages.error(request, msg)
        return redirect('/')
    else:
        user = Users.objects.filter(email=request.POST['email'])
        request.session['userid'] = user[0].id
    return redirect('/process')

def process(request):
    if 'userid' not in request.session:
        messages.error(request, "please login cheater")
        return redirect('/')
    context = {'loguser': Users.objects.get(id=request.session['userid']),
               'allquotes': Quotes.objects.all().order_by("-created_at"),
               }
    return render(request, 'quotes_1/success.html', context)

def logout(request):
    if 'userid' not in request.session:
        return redirect('/')
    del request.session['userid']
    return redirect('/')
def any(request):
    return redirect('/')

def addquote(request):
    if 'userid' not in request.session:
        return redirect('/')
    newquote = Quotes.objects.validate(request.POST, request.session['userid'])

    if "error" in newquote:
        error = newquote['error']
        for msg in error:
            messages.error(request, msg)
        return redirect('/process')
    return redirect('/process')

def listquotes(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    quote = Quotes.objects.get(id=id).creator.id
    counts= len(Quotes.objects.filter(creator__id=quote))

    allquotes = Quotes.objects.filter(creator__id=quote).order_by('-created_at')
    context = {
               'loguser': Users.objects.get(id=request.session['userid']),
               'allquotes': allquotes,
               'quotecreator': quote,
               'creator': allquotes[0].creator.first_name,
               'counts':counts
               }

    return render(request, 'quotes_1/users.html', context)

def addfavorite(request, qid):
    if 'userid' not in request.session:
        return redirect('/')
    favoritelist = Quotes.objects.favorite(request.session['userid'], qid)
    if 'error' in favoritelist:
        messages.error(request, favoritelist['error'])
    return redirect('/process')

def removequote(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    remove = Users.objects.get(id=request.session['userid'])
    remove.users_favorite.get(id=id).delete()
    return redirect('/process')
