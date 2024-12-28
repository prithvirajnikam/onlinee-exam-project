from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import Questions
from.models import UserData
from django.utils import timezone
from datetime import timedelta


# Create your views here.


def nextpage(request):
    
    
    
        if 'op' in request.GET:
            Qdict = request.session['answer']
            Qdict[request.GET["qno"]] = [
                request.GET["qno"], 
                request.GET["qtext"], 
                request.GET["answer"], 
                request.GET["op"]
            ]
            print(Qdict)
            
        
        queryset=Questions.objects.filter(subject=request.session['subject'])
        allquestions=list(queryset)


            
        if request.session['questionindex'] < len(allquestions) -1:
                request.session['questionindex'] = request.session['questionindex'] +1
                
                question=allquestions[request.session['questionindex']]
                
                
                questionno=request.session['questionindex'] + 1  
                print(f"ssssssssssssssssssssssssssssssss:-{questionno}")
                
                if request.session['questionindex']==len(allquestions)-1:
                    disable = True
                else:
                      disable = False
                    
                
                
                check=None
                answer_dict=request.session['answer']
                print(f"sss:_{answer_dict}")
                if str(question.qno) in request.session['answer']:
                    check=answer_dict[str(question.qno)][3]
                    print(f'this is value :-{answer_dict}')
                        
                
                return render(request,'app1/question.html',{'question':question,'disable': disable,'check':check,"questionno":questionno})
                                
               
                
      
                
            
        else:  
                questionno = len(allquestions)
                   
                return render(request,'app1/question.html',{'question':allquestions[len(allquestions)-1],"questionno":questionno})

   



def previousQuestion(request):
    
    if 'op' in request.GET:
            Qdict = request.session['answer']
            Qdict[request.GET["qno"]] = [
                request.GET["qno"], #0
                request.GET["qtext"], #1
                request.GET["answer"], #2
                request.GET["op"]#3
            ]
    
    
    queryset=Questions.objects.filter(subject=request.session['subject'])
    allquestions=list(queryset)

   
    if request.session['questionindex']>0:

        request.session['questionindex']=request.session['questionindex'] - 1 
        question=allquestions[request.session['questionindex']]
        
        questionno=request.session['questionindex']+1 
        disable = False
        print(f"aaaaaaaaa:{question.qno}")
        
       
                     
        
        check=None
        answer_dict=request.session['answer']
        print(f"sss:_{answer_dict}")
        
        
        if str(question.qno) in answer_dict:
            check=answer_dict[str(question.qno)][3]
            print(f'this is value :-{answer_dict}')
        
 
        return render(request,'app1/question.html',{'question':question,'disable': disable,'check':check,"questionno":questionno})
            
           
       
    else:
        disable = False
        questionno = 1

        return render(request,'app1/question.html',{'question':allquestions[0],'disable': disable,"questionno":questionno})
    
   
       
def endexam(request):
    
    if 'answer' in request.session:
    
   
      
        if 'op' in request.GET:
            Qdict = request.session['answer']
            Qdict[request.GET["qno"]] = [
                request.GET["qno"], 
                request.GET["qtext"], 
                request.GET["answer"], 
                request.GET["op"]
            ]
        correct_and_wronganslist=[]
        ans_dict=request.session['answer']
        lists=ans_dict.values()
        
        
        for list in lists:
            
            if list[2]==list[3]:
                request.session['score']=request.session['score']+1
                correct_and_wronganslist.append({'qno':list[0],'qtext':list[1],'answer':list[2],'wrong_ans':list[3],'status':'correct'})
            
                
            else:
                request.session["w_score"]= request.session["w_score"]+1
                correct_and_wronganslist.append({'qno':list[0],'qtext':list[1],'answer':list[2],'wrong_ans':list[3],'status':'wrong'})
                
                
        score=request.session['score'] 
        wrong= request.session['w_score']  
        username= request.session['username']
        subject=  request.session["subject"]
        profile_pic= request.session.get('image')
        
        totalquestion=len(ans_dict)
        
        print(score)
        if totalquestion >0:
            percentage=int((score/totalquestion)*100)
            print(percentage)
            
        request.session["percentage"]=percentage
        per= request.session["percentage"]
        
            
        login_date=timezone.now().date()
        
        print(f"'list'={correct_and_wronganslist}")
        
        user=UserData(username=username,percentage=per,subject=subject,login_date=login_date)
        user.save()
        # print(Qdict)
        
           
        auth.logout(request)
            
        return render(request,'app1/results.html',{'score':score,'wrong':wrong,'correct_wrong':correct_and_wronganslist,'username':username,'percentage':percentage,'total_question':totalquestion,"profile_pic":profile_pic})
    
    else:
        
        return render(request,'app1/login.html',{'message1':'Login aging...!'})


@login_required(login_url='/login')    
def starTest(request):
    if request.method=='GET':
        subject_name=request.GET.get('subject')
        request.session["subject"]=subject_name
        
        
        
        queryset=Questions.objects.filter(subject=request.session["subject"])
        questionlist=list(queryset.values())
        print(f"list :-{queryset}")
        print(f"qurestionlist :- {questionlist}")
        
        
        
        request.session['questionlist']=questionlist
        question=request.session['questionlist'][0]
        print(question)
        return render(request,"app1/question.html",{'question':question,"questionno":1})
    return render(request,"app1/question.html",{"questionno":1})





@login_required(login_url='/login') 
def view_resultdata(request):
    
    
    today = timezone.now().date() # current day
    print(today)
    yesterday = today - timedelta(days=1) 
    print(yesterday)

   
    date_filter = request.GET.get('date_filter')
    specific_date = request.GET.get('specific_date')

   
    if date_filter == 'today':
       
        data1 = UserData.objects.filter(login_date=today)
    elif date_filter == 'yesterday':
       
        data1 = UserData.objects.filter(login_date=yesterday)
    elif  specific_date:
       
        specific_date =  specific_date  #YYYY-MM-DD 
        data1 = UserData.objects.filter(login_date=specific_date)
    else:
       
        data1 = UserData.objects.all()

    return render(request, 'app1/admin.html', {"data": data1,'today':today,'yesterday':yesterday})


# def search_page(request):
   
#     data1=UserData.objects.filter(username=request.session["search"])  or UserData.objects.filter(subject=request.session["search"])
    
#     return render(request,"app1/admin.html",{"data": data1})



def search_user(request):
    search=request.GET["search"]
    request.session["search"]=search
    data1= UserData.objects.filter(subject=search) or UserData.objects.filter(username=search)
    
    
    return render(request, 'app1/admin.html', {"data": data1})





def addquestions(request):
    if request.method=="POST":
        qno=request.POST["qestionno"]
        qtext=request.POST['questiontext']
        answer=request.POST['questionanswer']
        subject=request.POST['subject']
        op1=request.POST["op1"]
        op2=request.POST["op2"]
        op3=request.POST["op3"]
        op4=request.POST["op4"]
        
        Que=Questions.objects.create(qno=qno,qtext=qtext,answer=answer,op1=op1,op2=op2,op3=op3,op4=op4,subject=subject)
        Que.save()
 
        return render(request,"app1/questionmangment.html",{"message":'question added...'})
    if request.method=="GET":
            return render(request,"app1/questionmangment.html")

def updatequestions(request):
    if request.method=="POST":
        qno=request.POST["qestionno"]
        qtext=request.POST['questiontext']
        answer=request.POST['questionanswer']
        subject=request.POST['subject']
        op1=request.POST["op1"]
        op2=request.POST["op2"]
        op3=request.POST["op3"]
        op4=request.POST["op4"]
        
        que=Questions.objects.get(qno=qno)
        que.qtext=qtext
        que.answer=answer
        que.subject=subject
        que.op1=op1
        que.op2=op2
        que.op3=op3
        que.op4=op4
        que.save()
        return render(request,"app1/questionmangment.html",{"message":'question updated...'})
    return render(request,"app1/questionmangment.html") 


def viewquestions(request):
    if request.method=="POST":
        qno=request.POST["qestionno"]
        subject=request.POST['subject']
    
        que=Questions.objects.get(qno=qno,subject=subject) 
        return render(request,"app1/questionmangment.html",{'qno':que.qno,'qtext':que.qtext,'answer':que.answer,'op1':que.op1,'op2':que.op2,'op3':que.op3,'op4':que.op4,"message":"question displayed...."})
    return render(request,"app1/questionmangment.html")

def deletequestion(request):
    if request.method=="POST":
        qno=request.POST["qestionno"]
        subject=request.POST['subject']
        
        Questions.objects.get(qno=qno,subject=subject).delete()
        return render(request,"app1/questionmangment.html",{'message':'question deleteed.....'})
    return render(request,"app1/questionmangment.html")

@login_required(login_url='/login')
def managequestiondata(request):
    if request.method=="POST":
         return render(request,'app1/questionmangment.html')
    return render(request,'app1/questionmangment.html')

def backtodashboard(request):
    return render(request,'app1/dashboard.html')