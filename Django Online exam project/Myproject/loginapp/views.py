from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from  loginapp.models import Myuser

from examapp.models import Questions



def home(request):
    return render(request,"app1/home.html")

def singup(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        email=request.POST["email"]
        password2=request.POST["confirm_password"]
        photo=request.FILES['photo']
        imagepath='/upload/'+photo.name
        
        request.session['image']=imagepath
        
        with open('static/upload/'+photo.name,'wb+') as path:
            for byte in photo.chunks():
                path.write(byte)
        
        
        if password2==password:
            if User.objects.filter(username=username).exists():
                messages.error(request,"username is already exists...!")
                return redirect("/singup")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,"email is already exists...!")
                    return redirect("/singup")
                else:
                     
                    user=Myuser.objects.create_user(username=username,password=password,email=email,imagepath=imagepath)
                    user.save()
                    
                    return render(request,"app1/login.html")   
                            
        else:
            messages.error(request,"password not match...!")
            return redirect("/singup")
    return render(request,"app1/singup.html")



@login_required(login_url="/login")
def dashboard(request):
    if request.method=="GET":
        return render(request,"app1/dashboard.html")
    if request.method=="POST":
         return render(request,"app1/dashboard.html")
        

def logout(request):
    auth.logout(request)
    return redirect("/")



def youtube_search(request):
    data = request.POST["data"]
    return redirect(f"https://maps.google.com/search?q={data}")


#
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        
        

        if user is not None:
            auth.login(request, user)
            
            queryset=Questions.objects.all().values('subject').distinct()
            print(f"ccccc--{list(queryset)}")
            print(f"aaaaa :-{queryset}")
            for op in queryset:
                # for k,v in op.items():
                    print({f"ggggggggggggg---{op['subject']}"})
                # print(f"ddddddn : -- {v}")
            
            
            if user.is_superuser==1:
                return render(request,'app1/dashboard.html')
                
            
            
            request.session["answer"]={}
            request.session['username']=username
            
            request.session["qno"]=0
            request.session['questionindex']=0
            request.session["score"]=0
            request.session["w_score"]=0
            request.session["percentage"]=0
            request.session["subject"]=''
            
            questionlist=Questions.objects.all()

            question=questionlist[0]
            
            myuser=Myuser.objects.filter(user_ptr_id=user.id)
            
            imagepath=myuser[0].imagepath

            return render(request,'app1/startexam.html',{'question':question,'username':request.session['username'],'listofsubject':list(queryset),'imagepath':imagepath})
            
        else:
            messages.error(request, "wrong username")
            return redirect('/login/')
    return render(request, 'app1/login.html')

