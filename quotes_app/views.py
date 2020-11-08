from django.shortcuts import render, redirect
from quotes_app.models import User, Quote, Like
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, "register_login.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.validate_registration(request.POST)
        if len(errors) > 0:
            for key, errormsg in errors.items():
                messages.error(request, errormsg)
            return redirect("/")
        else:
            password = request.POST['password_txt']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            print(pw_hash)
            new_user=User.objects.create(
                first_name=request.POST['first_name_txt'],
                last_name=request.POST['last_name_txt'],
                email=request.POST['email_txt'],
                password=pw_hash
            )
            request.session['user_id'] = new_user.id
            request.session['user_name'] = f'{new_user.first_name} {new_user.last_name}'
            return redirect("/quotes") 
    return redirect("/")

def login(request):
    if request.method =='POST':
        user = User.objects.filter(email=request.POST['email_txt'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password_txt'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                request.session['user_name'] = f'{logged_user.first_name} {logged_user.last_name}'
                return redirect("/quotes")
            else:
                messages.error(request, "Incorrect password.")
        else:
            messages.error(request, "Incorrect username.")
            return redirect("/")
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")

def displayQuotes (request):
    context = {
        'all_quotes':Quote.objects.all().order_by("-created_at"),
        'user':User.objects.get(id=request.session['user_id'])
    }
    return render(request, "quotes_list.html", context)

def addQuote(request):
    if request.method =='POST':
        errors = Quote.objects.validate_data(request.POST)
        if len(errors) > 0:
            for key, errormsg in errors.items():
                messages.error(request, errormsg)
            return redirect("/quotes")
        else:
            new_quote = Quote.objects.create(
                content = request.POST['content_txt'],
                quoted_by=request.POST['author_txt'],
                posted_by = User.objects.get(id=request.session['user_id']),
            )
            return redirect ("/quotes")
    return redirect("/")

def deleteQuote(request, quote_id):
    Quote.objects.get(id=quote_id).delete()
    return redirect("/quotes")

def addLike(request, quote_id):
    if request.method == 'POST':
        errors = Like.objects.validate_like(request, quote_id)
        if len(errors) > 0:
            for key, errormsg in errors.items():
                messages.error(request, errormsg)
            return redirect("/quotes")
        else:
            Like.objects.create(
                user=User.objects.get(id=request.session['user_id']),
                quote=Quote.objects.get(id=quote_id)
            )
            return redirect("/quotes")
    return redirect("/")
    
def displayUser(request, user_id):
    context = {
        'user':User.objects.get(id=user_id),
    }
    return render(request, "user_detail.html", context)

def getUserEditPage(request):
    context={
        'user':User.objects.get(id=request.session['user_id'])
    }
    return render(request,"edit_user.html", context)

def updateUser(request):
    if request.method =='POST':
        errors = User.objects.validate_update(request)
        if len(errors) > 0:
            for key, errormsg in errors.items():
                messages.error(request, errormsg)
            return redirect("/edit_user")
        else:
            updated_user = User.objects.get(id=request.session['user_id'])
            updated_user.first_name=request.POST['first_name_txt']
            updated_user.last_name=request.POST['last_name_txt']
            updated_user.email=request.POST['email_txt']
            updated_user.save()
            return redirect("/quotes")
        return redirect("/edit_user")
    return redirect("/")
    
