from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_api, name='login'),
    path('lessons/', views.lessons_list, name='lessons'),
    path('lessons/<int:id>/', views.lesson_detail, name='lesson_detail'),
    path('complete-lesson/', views.complete_lesson, name='complete_lesson'),
    path('homework/<int:lesson_id>/', views.get_homework, name='get_homework'),
    path('submit-homework/', views.submit_homework, name='submit_homework'),
    path('students/add/', views.create_student, name='create_student'),
    path('courses/add-student/', views.add_student_to_course, name='add_student_to_course'),
    path('lessons/create/', views.create_lesson, name='create_lesson'),
    path('lessons/<int:lesson_id>/update/', views.update_lesson, name='update_lesson'),
    path('teacher/courses/', views.get_teacher_courses, name='teacher_courses'),
    path('teacher/courses/<int:course_id>/modules/', views.get_course_modules, name='course_modules'),
    path('teacher/modules/create/', views.create_module, name='create_module'),
    path('teacher/lessons/create/', views.create_lesson_full, name='create_lesson_full'),
]
    path('upload/', views.upload_homework_file, name='upload_file'),
