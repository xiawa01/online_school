from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Ученик'),
        ('teacher', 'Учитель'),
        ('moderator', 'Модератор'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    avatar = models.URLField(blank=True)
    email_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    progress = models.JSONField(default=list)
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.URLField(blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    LESSON_TYPES = (
        ('async', 'Асинхронный'),
        ('sync', 'Синхронный'),
    )
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    lesson_type = models.CharField(max_length=10, choices=LESSON_TYPES)
    order = models.IntegerField(default=0)
    
    content_text = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    attachments = models.JSONField(default=list)
    
    test_data = models.JSONField(default=dict)
    homework_task = models.TextField(blank=True)
    
    scheduled_start = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=60)
    enable_recording = models.BooleanField(default=False)
    recording_url = models.URLField(blank=True)
    
    unlock_date = models.DateTimeField(null=True, blank=True)
    requires_previous = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class HomeworkSubmission(models.Model):
    STATUS_CHOICES = (
        ('pending', 'На проверке'),
        ('approved', 'Принято'),
        ('revision', 'На доработке'),
    )
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    attachments = models.JSONField(default=list)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviewed_homeworks')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    revision_number = models.IntegerField(default=0)
    revision_comment = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.lesson.title}"

class StudentProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    test_score = models.IntegerField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'lesson']

class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_url = models.URLField(blank=True)
    verification_code = models.CharField(max_length=64, unique=True)
    
    def __str__(self):
        return f"Сертификат: {self.student.username} - {self.course.title}"


class ExerciseTemplate(models.Model):
    TEMPLATE_TYPES = (
        ('multiple_choice', 'Множественный выбор'),
        ('drag_drop', 'Drag & Drop'),
        ('matching', 'Соответствие'),
        ('fill_blanks', 'Заполнить пропуски'),
        ('speaking', 'Аудирование/говорение'),
        ('code', 'Программирование'),  # для IT-курсов
    )
    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES)
    config = models.JSONField(default=dict)  # настройки шаблона
    preview_image = models.URLField(blank=True)
class ChatMessage(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chat_messages', null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    is_private = models.BooleanField(default=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='received_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.username}: {self.message[:50]}"

class HomeworkFile(models.Model):
    homework_submission = models.ForeignKey('HomeworkSubmission', on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='homeworks/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    file_size = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.filename
