from django.urls import path
from . import views
from django.contrib.auth import authenticate, login, logout

urlpatterns = [
    path('', views.home, name='home'),
    path('forum', views.forum, name='forum'),
    path('askQuestion', views.askQuestion, name='askQuestion'),
    path('previouslyAsked', views.previouslyAsked, name='previouslyAsked'),
    path('previouslyAnswered', views.previouslyAnswered, name='previouslyAnswered'),
    path('search', views.search, name='search'),
    path('signup', views.handlesignup, name='handlesignup'),
    path('login', views.handlelogin, name='handlelogin'),
    path('logout', views.handlelogout, name='handlelogout'),
    path('postAnswer', views.postAnswer, name='postAnswer'),
    path('postQuestion', views.postQuestion, name='postQuestion'),
    path('postReply', views.postReply, name='postReply'),
    path('<int:slug>', views.openQue, name='openQue')
]