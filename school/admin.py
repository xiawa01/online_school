from django.contrib import admin
from .models import User, Course, Module, Lesson, HomeworkSubmission, StudentProgress, Certificate

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'is_published', 'created_at')
    list_filter = ('is_published', 'teacher')
    search_fields = ('title', 'description')
    filter_horizontal = ('students',)

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    ordering = ('course', 'order')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'lesson_type', 'order')
    list_filter = ('lesson_type', 'module__course')
    search_fields = ('title', 'content_text')
    
    fieldsets = (
        ('Основное', {
            'fields': ('module', 'title', 'lesson_type', 'order')
        }),
        ('Контент', {
            'fields': ('content_text', 'video_url', 'attachments')
        }),
        ('Асинхронный урок', {
            'fields': ('test_data', 'homework_task'),
            'classes': ('collapse',)
        }),
        ('Синхронный урок', {
            'fields': ('scheduled_start', 'duration_minutes', 'enable_recording', 'recording_url'),
            'classes': ('collapse',)
        }),
    )

@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'student', 'status', 'submitted_at', 'score')
    list_filter = ('status', 'lesson__module__course')
    search_fields = ('student__username', 'lesson__title')
    readonly_fields = ('submitted_at', 'revision_number')

@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'is_completed', 'completed_at')
    list_filter = ('is_completed', 'lesson__module__course')
    search_fields = ('student__username', 'lesson__title')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'issued_at', 'verification_code')
    search_fields = ('student__username', 'course__title', 'verification_code')
