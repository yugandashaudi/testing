from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django_password_history.models import UserPasswordHistory
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site  
from .token import account_activation_token  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage  
from django.template.loader import render_to_string  
from django.http import HttpResponse  
from datetime import date, timedelta
import datetime
import time

def RegisterView(request):
    form = CreateUserForm()
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
        
            user.is_active = False  
            user.save()  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
            'user': user,  
            'domain': current_site.domain,  
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
            'token':account_activation_token.make_token(user),  
            })  
            user=form.cleaned_data.get('username')
            messages.success(request,'Account was created for' + user)
            to_email = form.cleaned_data.get('email')  
            print(to_email)
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')
        
           
    context={'form':form}
    return render(request,'register.html',context)

def LoginUser(request):
    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username =form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    time=UserPasswordHistory.objects.get(user=user).updated_at
                    print(time)
                    print(datetime.datetime.now())
                    if date.today() - time.date() < timedelta(days=30):
 
                        messages.info(request,'You have been using the same password for 30days,your password has been expired,please change your password')
                        login(request,user)


                        return redirect('change_password')
                    else:
                        login(request,user)
        
                
        
                       
                        return redirect('home')
                else:
                    pass
            else:
                messages.info(request,'Username or Password is incorrect')
        

           

    context={'form':form}
    return render(request,'login.html',context)

@login_required(login_url='login')
def Home(request):
    return render(request,'home.html')


@login_required(login_url='login')
def ChangePassword(request):
    
    if request.method=="POST":
        user=request.user
        current_password=request.POST.get('current_password')
        new_password=request.POST.get('new_password')
        print(current_password)
        checking_password = user.check_password(current_password)
        print(checking_password)
        if checking_password:
            get_user = UserPasswordHistory.objects.get(user=user).password_is_used
            print(get_user)
            
            
            if get_user:
                messages.info(request,'The password has already used before')
            else:
                user.set_password(new_password)
                user.save()
                messages.success(request,'The password has been Changed sucessfully')
        else:
            print('hello')
            messages.info(request,'Your current password deosnot match')
            
                

            
                
            

    context = {}
    return render(request,'change_password.html',context)
   

def activate(request, uidb64, token):  
     
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        messages.success(request,'Thank you for your email confirmation. Now you can login your account')
        return redirect('login')
    else:  
        return HttpResponse('Activation link is invalid!')  

def Logout(request):
    logout(request) 
    return redirect('login')

    