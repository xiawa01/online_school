# school/serializers.py
from rest_framework import serializers
from django.db import models
from .models import Course, Module, Lesson, HomeworkSubmission, StudentProgress

class CourseSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = '__all__'
    
    def get_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from .models import StudentProgress  # Локальный импорт чтобы избежать цикла
            total_lessons = 0
            for module in obj.modules.all():
                total_lessons += module.lessons.count()
            
            if total_lessons == 0:
                return 0
                
            completed = StudentProgress.objects.filter(
                student=request.user, 
                lesson__module__course=obj,
                is_completed=True
            ).count()
            return int((completed / total_lessons) * 100)
        return 0

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title', 'order']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'lesson_type', 'order', 'content_text', 'video_url', 
                  'scheduled_start', 'duration_minutes', 'recording_url']

class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    
    class Meta:
        model = HomeworkSubmission
        fields = ['id', 'lesson', 'lesson_title', 'student', 'student_name', 
                  'answer_text', 'attachments', 'submitted_at', 'status', 
                  'score', 'feedback', 'revision_number']
        read_only_fields = ['student', 'submitted_at', 'revision_number']