from logging.config import IDENTIFIER
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Profile
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from assetpf.forms import PersonalInfoForm, AddPortfolioForm
from .models import *
# Create your views here.


#def home(request):
#   return render(request,'home.html'

def index(request):
    template='users/index.html'
    context={
        'title':'Index',
    }
    return render(request,template,context)

def new(request):
    template='users/new.html'
    context={
        'title':'Index',
    }
    return render(request,template,context)
               

def login_attempt(request):
   
    if request.method == 'POST' :
        username=request.POST.get('username') #get data from post of login.html
        password=request.POST.get('password')
    
        user_obj=User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,'Username is not found')
            return redirect('/login')

        profile_obj=Profile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
            messages.success(request,'Profile is not verified check your mail')
            return redirect('/login')
        
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return render(request,'users/index.html')
        else:   
            messages.success(request,'Wrong Password')
            return redirect('/login')
                
            
        
    return render(request,'users/login.html') 

'''def login_attempt(request):
    template = 'users/login.html'

    if request.method == "POST":
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            # fetching user object from database
            user_obj= User.objects.get(email=email)
            if password == user_obj.password:
                # to store session in django
                request.session['session_email'] = user_obj.email
                if request.session.has_key('session_email'):
                    user_obj = User.objects.get(username=request.session['session_email'])
                    context = {
                        'title': 'CSV | User Index',
                        'msg': 'Login success',
                        'data': user_obj
                    }
                    template = 'users/index.html'
                    
                    return render(request, template, context)
                else:
                    context = {
                        #'form': ul,
                        'title': 'CSV | User Login',
                        'body_title': 'User Login',
                        'msg': 'Unauthorized access'
                    }
                    return render(request, template, context)
            else:
                context = {
                    #'form': ul,
                    'title': 'CSV | User Login',
                    'body_title': 'User Login',
                    'msg': 'Invalid email or password'
                }
                return render(request, template, context)
        except:
            context = {
                #'form': ul,
                'title': 'CSV | User Login',
                'body_title': 'User Login',
                'msg': 'Not registered yet'
            }
            return render(request, template, context)
    else:
        context = {
            #'form': ul,
            'title': 'CSV | User Login',
            'body_title': 'User Login',
            'msg': ''
        }
        return render(request, template, context)'''
           
def register_attempt(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            #Check username and email already taken or not
            if User.objects.filter(username=username).first():
                messages.success(request,'Username is taken')
                return redirect('/register')
            if User.objects.filter(email=email).first():
                messages.success(request,'Email is taken')
                return redirect('/register')
            #make User object as user_obj 
            user_obj=User(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            #user_obj.save() inorder to save set username and password in db
            
            auth_token=str(uuid.uuid4())
            profile_obj=Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            #send mail after registration to reciptent address
            registration_mail(email, auth_token )
            
            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request,'users/register.html')

def sucess(request):
    return render(request,'users/sucess.html')

def token_send(request):
    return render(request,'users/token_send.html')

#Register verificatiom
def verify(request,auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()
        
        if profile_obj:
            #if token generated was already verified by user
            if profile_obj.is_verified:
                messages.success(request,'Your account is already verified.')
                return redirect('/login')
            profile_obj.is_verified=True 
            profile_obj.save()
            messages.success(request, 'Your account has been verified')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')
def registration_mail(email,token):
    subject="Your account need to be verified"
    message=f'Hi click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
def error(request):
    return render(request,'users/error.html')
def dashboard(request):

    return render(request,'users/dashboard.html')
def personal_info(request):
    template='users/personalInfo.html'
    ufm=PersonalInfoForm
    context={
        'title':'Personal Profile',
        'form':ufm
    }
    return render(request,template,context)

#user portfolio add and show 
def addshowPortfolio(request):
    template='portfolio/addshow.html'
    show_portfolio=AddPortfolio.objects.all()
    if request.method=='POST':
        date=request.POST.get('date')
        objective=request.POST.get('objective')
        income=request.POST.get('income')
        expense=request.POST.get('expense')
        add_port=AddPortfolio(date=date,objective=objective,income=income,expense=expense)
        add_port.save()
        return redirect('/portfolio')
    else:
        fm=AddPortfolioForm()
        template='portfolio/addshow.html'
        context={
                    'show':show_portfolio,
                    'form':fm,
                }
        return render(request,template,context)
#user portfolio edit/update
def updatePortfolio(request,id):
    template='portfolio/update.html'
    data=AddPortfolio.objects.get(pk=id)
    if request.method=="POST": 
        fm=AddPortfolioForm(request.POST,instance=data)
        if fm.is_valid():
            fm.save()
            return redirect('addshowPortfolio')
    else:
        fm=AddPortfolioForm(instance=data)
        context={
            'form':fm,
        }
    return render(request,template,context)

#user portfolio delete
def deletePortfolio(request,id):
    if request.method=='POST':
        data_del=AddPortfolio.objects.get(pk=id)
        data_del.delete()
        return redirect('addshowPortfolio')




