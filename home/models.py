from django.db import models
from datetime import datetime

# Create your models here.
class Question(models.Model):
    queSno = models.AutoField(primary_key=True)
    questionShortDesc = models.TextField()
    questionLongDesc = models.TextField()
    askedOn = models.DateTimeField(default=datetime.now)
    noOfAnswers = models.IntegerField(default=0)
    askedBy = models.TextField()
    views = models.IntegerField(default=0)
    tags = models.TextField()

    def __str__(self):
        return self.questionShortDesc 

class Answer(models.Model):
    answerSno = models.AutoField(primary_key=True)
    answerOfQue = models.IntegerField()
    answerDesc = models.TextField()
    answeredBy = models.TextField()
    answeredOn = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.answerDesc 

class Reply(models.Model):
    replySno = models.AutoField(primary_key=True)
    replyOfAns = models.IntegerField()
    queSno = models.IntegerField()
    replyDesc = models.TextField()
    repliedBy = models.TextField()
    repliedOn = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.replyDesc
