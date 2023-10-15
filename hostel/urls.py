from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('aboutus/', views.aboutus, name='about'),
    path('contactus/', views.contact, name='contactus'),
    path('feedback/', views.feedback, name='feedback'),
    path('signin/', views.profile, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('ownersignup/', views.ownersignup, name='ownersignup'),
    path('login/', views.signin, name='login'),
    path('studenthp/', views.studenthp, name='studenthp'),
    path('ownership/', views.ownership, name='ownership'),
    path('logout/', views.logout_view, name='logout'),
    path('ownerupload/', views.upload, name='ownerupload'),
    path('uploadhostel/', views.upload_hostel, name='upload_hostel'),
    path('uploadroom/', views.upload_room, name='upload_room'),
    path('display/', views.display, name='display'),
    path('display/<str:model_type>/<int:model_id>/', views.display_detail, name='display_detail'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
