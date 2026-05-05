from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('school.urls')),
    path('virtual-class/', TemplateView.as_view(template_name='virtual_class.html'), name='virtual_class'),
    path('test-class/', TemplateView.as_view(template_name='test_virtual_class.html'), name='test_class'),
    path('lesson-editor/', TemplateView.as_view(template_name='lesson_editor.html'), name='lesson_editor'),
    path('lesson/', TemplateView.as_view(template_name='lesson_view.html'), name='lesson_view'),
    path('teacher/', TemplateView.as_view(template_name='teacher_panel.html'), name='teacher_panel'),
    path('', TemplateView.as_view(template_name='student_dashboard.html'), name='student_dashboard'),
]
    path('chat/', TemplateView.as_view(template_name='chat.html'), name='chat'),
