from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('aboutus', views.aboutus, name='about'),
    path('contactus', views.contact, name='contactus'),
    path('feedback', views.feedback, name='feedback'),
    path('signin', views.profile, name='signin'),
    path('signup', views.signup, name='signup'),
    path('ownersignup', views.ownersignup, name='ownersignup'),
    path('login/', views.signin, name='login'),
]
