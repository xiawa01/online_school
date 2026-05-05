from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('school.urls')),
    path('teacher/', TemplateView.as_view(template_name='teacher_panel.html'), name='teacher_panel'),
    path('student/', TemplateView.as_view(template_name='student_dashboard.html'), name='student_dashboard'),
    path('virtual-class/', TemplateView.as_view(template_name='virtual_class.html'), name='virtual_class'),
    path('lesson-editor/', TemplateView.as_view(template_name='lesson_editor.html'), name='lesson_editor'),
    path('lesson/', TemplateView.as_view(template_name='lesson_view.html'), name='lesson_view'),
    path('chat/', TemplateView.as_view(template_name='chat.html'), name='chat'),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]
