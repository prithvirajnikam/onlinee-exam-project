from django.db import models

# Create your models here.



class Questions(models.Model):
    qno=models.IntegerField(primary_key=True)
    qtext=models.CharField(max_length=100)
    answer=models.CharField(max_length=100)
    subject=models.CharField(max_length=100)
    op1=models.CharField(max_length=100)
    op2=models.CharField(max_length=100)
    op3=models.CharField(max_length=100)
    op4=models.CharField(max_length=100)
    
    
    def __str__(self):
        return f'{self.qno,self.qtext,self.answer,self.subject,self.op1,self.op2,self.op3,self.op4}'
    
    class Meta():
        db_table='questions'
    

class UserData(models.Model):
    username=models.CharField(max_length=100)
    subject=models.CharField(max_length=100)
    percentage=models.IntegerField()
    login_date=models.DateField()
    
    
    def __str__(self):
        return f"{self.username,self.subject,self.percentage}"
    
    
    class Meta():
        db_table="userdata"