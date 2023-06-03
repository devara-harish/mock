from django.http import HttpResponse

from django.http import HttpResponse
from django.core.mail import send_mail
from app1.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView,DetailView


def registration(request):
    ufo=UserForm()
    d={'ufo':ufo}
    if request.method=='POST':
        ufd=UserForm(request.POST)
        if ufd.is_valid():
            NSUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()
            

            return render(request,'registration_done.html')
        else:
            return render(request,'reg_not_done.html')
    return render(request,'registration.html',d)

def reg_done(request):
    return render(request, 'reg_not_done.html')

def reg_not(request):
    return render(request, 'reg_not')




class QuestionList(ListView):
    model = Question
    context_object_name='questions'

class QuestionDetail(DetailView):
    model =Question
    context_object_name='Qcl'


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('questions'))
        else:
            return render(request,'reg_not_done.html')
        
    return render (request,'user_login.html')


@login_required
def ask_question(request):
    qfo= QuestionForm()
    d={'qfo':qfo}
    if request.method == 'POST':
        qfd = QuestionForm(request.POST)
        if  qfd.is_valid():
            username=request.session['username']
            UO=User.objects.get(username=username)

            NSAQO = qfd.save(commit=False)
            NSAQO.user = UO
            NSAQO.save()
            return HttpResponseRedirect(reverse('questions'))
        else:
            return HttpResponse('quiestion not asked successfully')
        
    return render(request, 'asking_question.html',d)

    
@login_required
def answer_question(request):
    aqo = AnswerForm()
    d={'aqo':aqo}
    question = Question.objects.all()
    if request.method == 'POST':
        aqd= AnswerForm(request.POST)
        if aqd.is_valid():
            username=request.session['username']
            UO=User.objects.get(username=username)
            NSAQO = aqd.save(commit=False)
            NSAQO.user = UO
            NSAQO.save()
            Q=NSAQO.question
            AO=Answer.objects.filter(question=Q)
            d1={'AO':AO}
            return HttpResponseRedirect(reverse('questions'))
        else:
            return HttpResponse('quiestion not asked successfully')
        
    return render(request, 'answering_question.html',d)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('questions'))
