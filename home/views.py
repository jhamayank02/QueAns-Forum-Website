from django.shortcuts import render, redirect, HttpResponse
from . models import Question, Answer, Reply
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
import json

# Create your views here.

# Function for /home -> Home page
def home(request):
    return render(request, 'home.html')

# Function for /forum -> Forum page
def forum(request):
    # Questions to send in the forum template
    allQuestions = Question.objects.all().order_by('-askedOn')

    # Popular questions (5) based on views
    popularQuestions = Question.objects.all().order_by('-views')[0:5]

    context = {'allQuestions':allQuestions, 'popularQuestions':popularQuestions}
    return render(request, 'forum.html', context)

# Function for /askQuestion -> To ask a question
def askQuestion(request):
    return render(request, 'askQuestion.html')

# Function for /openQue -> When a user wants to view a question
def openQue(request, slug):
    # Open the question which the user has clicked
    question = Question.objects.filter(queSno=slug).first()

    # Increase views by 1 everytime
    question.views = question.views + 1
    question.save()
    allAnswers = Answer.objects.filter(answerOfQue=slug).order_by('-answeredOn')

    # Related questions based on tags, questionShortDesc and questionLongDesc
    for tag in question.tags:
        relatedQuestion1 = Question.objects.filter(tags__icontains= tag)
    
    for shortDesc in question.questionShortDesc:
        relatedQuestion2 = Question.objects.filter(questionShortDesc__icontains= shortDesc)
    
    for longDesc in question.questionLongDesc:
        relatedQuestion3 = Question.objects.filter(questionLongDesc__icontains= longDesc)

    relatedQuestions = relatedQuestion1.union(relatedQuestion2, relatedQuestion3)[0:5]

    # Replies related to particular question
    replies = Reply.objects.filter(queSno=slug)

    context = {'question':question, 'allAnswers':allAnswers, 'relatedQuestions':relatedQuestions, 'replies':replies}
    return render(request, 'openQue.html', context)

# Function for /signup -> For signup
def handlesignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Both passwords are matching or not
        if pass1!=pass2:
            messages.error(request, "Passwords does not match")
            return redirect('/')

        # Password should contain atleast 6 characters
        if len(pass1) < 6 and len(pass2) < 6:
            messages.error(request, "Password should contain atleast 6 characters")
            return redirect('/')

        # Length of username must be between 2 to 10 characters
        if len(username)<2 or len(username)>10:
            messages.error(request, "Username must be between 2 to 10 characters long")
            return redirect('/')

        # Username should not contain any symbols
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('/')

        # Name should only contain alphabets
        if not fname.isalpha() or not lname.isalpha():
            messages.error(request, "First name and last name should only contain letters")
            return redirect('/')

        # Create a new user
        newUser = User.objects.create_user(username=username, email=email, password=pass1)
        newUser.first_name = fname
        newUser.last_name = lname
        newUser.save()
        messages.success(request, "Your account on QueAns has been successfully created")

        return redirect('/')
    
    return HttpResponse('404 - Not Found')

# Function for /login -> For login
def handlelogin(request):
    if request.method == 'POST':
        username = request.POST['loginusername']
        password = request.POST['loginpass']

        # If the user exists log him in
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('/')
        else:
           messages.error(request, "Please make sure that the credentials are correct and try again!")
           return redirect('/')

    return HttpResponse('404 - Not Found')

# Function for /logout -> To logout
def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')

# Function for /postAnswer -> To post an answer
def postAnswer(request):
    if request.method == 'POST':
        answerText = request.POST['answerText']
        queSno = request.POST['queSno']
        currentUser = request.POST['currentUser']

        # If the answer contains <script></script> tag raise error message
        if '<script>' in answerText.lower():
            messages.error(request, "You cannot post answers consisting <script></script> tag due to the security concerns.")
            return redirect(f'/{queSno}')

        if '</script>' in answerText.lower():
            messages.error(request, "You cannot post answers consisting <script></> tag due to the security concerns.")
            return redirect(f'/{queSno}')

        # If the answer is blank raise error message
        if answerText == '':
            messages.error(request, "You cannot post blank answers.")
            return redirect(f'/{queSno}')

        addAnswer = Answer.objects.create(answerOfQue=queSno, answerDesc=answerText, answeredBy=currentUser)
        addAnswer.save()

        # Create a new answer in the database
        answeredQuestion = Question.objects.filter(queSno = queSno).first()
        answeredQuestion.noOfAnswers = answeredQuestion.noOfAnswers + 1
        answeredQuestion.save()
        
        messages.success(request, "Your answer has been posted.")
        return redirect(f'/{queSno}')
    
    return HttpResponse('404 - Not Found')

# Function for /postQuestion -> To post a question
def postQuestion(request):
    if request.method == 'POST':
        currentUser = request.POST['currentUser']
        queShortDesc = request.POST['queShortDesc']
        queLongDesc = request.POST['queLongDesc']
        tags = request.POST['tags']

        # If the question contains <script></script> tag raise error message
        if '<script>' in queShortDesc.lower() or '<script>' in queLongDesc.lower() or '<script>' in  tags.lower():
            messages.error(request, "You cannot post answers consisting <script></script> tag due to the security concerns.")
            return redirect(f'/{queSno}')

        if '</script>' in queShortDesc.lower() or '</script>' in queLongDesc.lower() or '</script>' in  tags.lower():
            messages.error(request, "You cannot post answers consisting <script></> tag due to the security concerns.")
            return redirect(f'/{queSno}')

        # If the question is blank raise error message
        if queShortDesc == '' or queLongDesc == '':
            messages.error(request, "You cannot post blank answers.")
            return redirect(f'/{queSno}')

        # Create a new question in the database
        newQuestion = Question.objects.create(questionShortDesc=queShortDesc, questionLongDesc=queLongDesc, tags=tags, askedBy=currentUser)
        newQuestion.save()        

        messages.success(request, 'Your question has been posted successfully')
        return render(request, 'askQuestion.html')

    return HttpResponse('404 - Not Found')

# Function for /search -> To search for a query
def search(request):
    if request.method == 'POST':
        query = request.POST['query']

        # If the query is blank return none 
        if query == '':
            searchResults = Question.objects.none()

        # If the length of query is more than 100 characters return none
        elif len(query) >= 100:
            messages.error(request, 'Your search query must be between 1 to 100 characters.')
            searchResults = Question.objects.none()

        # Search based on tags, questionShortDesc and questionLongDesc
        else:
            searchByQueShortDesc = Question.objects.filter(questionShortDesc__icontains=query)
            searchByQueLongDesc = Question.objects.filter(questionLongDesc__icontains=query)
            searchByTags = Question.objects.filter(tags__icontains=query)

            searchResults = searchByQueShortDesc.union(searchByQueLongDesc, searchByTags)

        context = {'searchResults':searchResults, 'query':query}

        return render(request, 'search.html', context)
    
    return HttpResponse('404 - Not Found')

# Function for /previouslyAsked -> The questions which the user has asked before
def previouslyAsked(request):

    # Allow only if the user is logged in
    if request.user.is_authenticated:
        currentUser = request.user
        previouslyAskedQuestions = Question.objects.filter(askedBy=currentUser)
        print(previouslyAskedQuestions)
        context = {'Questions':previouslyAskedQuestions, 'title': "Previously Asked Questions"}

        return render(request, 'previous.html', context)

    return HttpResponse('404 - Not Found')    

# Function for /previouslyAnswered -> The questions which the user has answered before
def previouslyAnswered(request):

    # Allow only if the user is logged in
    if request.user.is_authenticated:
        currentUser = request.user
        answers = Answer.objects.filter(answeredBy=currentUser).values('answerOfQue')
        previouslyAnsweredQuestions = Question.objects.filter(queSno__in=answers)

        context = {'Questions':previouslyAnsweredQuestions, 'title': "Previously Answered Questions"}

        return render(request, 'previous.html', context)

    return HttpResponse('404 - Not Found')    

# Function for /postReply -> to post reply for an answer
def postReply(request):
    if request.method == 'POST':
        queSno = request.POST['queSno']

        repliedBy = request.POST['repliedBy']
        replyOfAns = request.POST['replyOfAns']
        replyDesc = request.POST['replyDesc']

        # If the reply to be posted is blank give error message
        if replyDesc != '':
            replyText = Reply.objects.create(replyOfAns=replyOfAns , replyDesc=replyDesc , repliedBy=repliedBy, queSno=queSno)
            replyText.save()
            messages.success(request, 'Your reply has been posted successfully.')

        else:
            messages.error(request, 'You cannot post blank comments.')


        return redirect(f'/{queSno}')

    return HttpResponse('404 - Not Found')    