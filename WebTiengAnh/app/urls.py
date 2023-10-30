from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('huongdan/', views.huongdan, name='huongdan'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course1/<int:course_id>/', views.course_detail2, name='course_detail2'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson1/<int:lesson_id>/', views.lesson_detail1, name='lesson_detail1'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz_lesson/<int:quiz_lesson_id>/', views.quiz_detail_lesson, name='quiz_detail_lesson'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz_lesson/<int:quiz_lesson_id>/submit/', views.submit_quiz_lesson, name='submit_quiz_lesson'),
    path('quiz_results/', views.quiz_results, name='quiz_results'),
    path('quiz_results_lesson/', views.quiz_results_lesson, name='quiz_results_lesson'),
]
