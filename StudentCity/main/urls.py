from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('students/', views.Students.as_view(), name='students'),
    path('dorm/', views.Dorm.as_view(), name='dorm'),
    path('dorm/<int:dorm_id>/', views.DormRooms.as_view(), name='dorm_rooms'),
    path('room/<int:room_id>/', views.StudentsInRoom.as_view(), name='students_in_room'),
    path('student/<slug:stud_slug>/', views.ShowStudent.as_view(), name='student'),

    path('addstudent/', views.AddStudent.as_view(), name='addstudent'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
]