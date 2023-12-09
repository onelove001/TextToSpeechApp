from django.shortcuts import *
import gtts
from playsound import playsound
import random
from django.contrib.auth import login as dlogin, logout as dlogout, authenticate
from django.contrib.auth.models import User


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password = password)
        if user is not None:
            dlogin(request, user)
            return redirect("welcome-page")
        messages.error(request, "Invalid Login Details")
        return redirect("login-page")
    return render(request, "login.html", {})

def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fullname = request.POST.get("fullname")
        password = request.POST.get("password")
        user = User.objects.create_user(username = username, password = password, first_name = fullname)
        user.save()
        return redirect("login-page")
    context = {}
    return render(request, "register.html", context)
    

def logout_page(request):
    dlogout(request)
    return redirect("/login")


def text_to_speech(speech_text):
        file = open('dd.txt','w')
        file.writelines(f'Hi, an email just came in, it reads: {speech_text} \n')
        file.close()
        file = open('dd.txt','r')
        data= file.read()
        file.close()
        language = 'en'
        myobj = gtts.gTTS(text=data, lang=language, slow=False) 
        i=random.randint(1, 100)
        file='new'+str(i)+'.mp3'
        myobj.save(file)      
        playsound(file)


def index(request):
    if request.method == "POST":
        speech_text = request.POST.get("speech_text")
        text_to_speech(speech_text)
        redirect(request.META.get("HTTP_REFERER"))
    return render(request, "index.html", context = {})



