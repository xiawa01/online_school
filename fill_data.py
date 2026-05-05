import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from django.contrib.auth.hashers import make_password
from school.models import User, Course, Module, Lesson

print("Заполняем базу данных...")

# Создаём учителя
teacher, _ = User.objects.get_or_create(
    username='teacher',
    defaults={
        'password': make_password('teacher123'),
        'first_name': 'Анна',
        'role': 'teacher',
        'progress': []
    }
)

# Создаём ученика
student, _ = User.objects.get_or_create(
    username='student',
    defaults={
        'password': make_password('student123'),
        'first_name': 'Алексей',
        'role': 'student',
        'progress': []
    }
)

# Создаём курс
course, created = Course.objects.get_or_create(
    title='Python для начинающих',
    defaults={
        'description': 'Полный курс по Python',
        'teacher': teacher,
        'is_published': True
    }
)

if created:
    course.students.add(student)

# Создаём модуль
module, _ = Module.objects.get_or_create(
    course=course,
    title='Основы Python',
    defaults={'order': 1}
)

# Создаём урок
lesson, _ = Lesson.objects.get_or_create(
    module=module,
    title='Переменные и типы данных',
    defaults={
        'lesson_type': 'async',
        'order': 1,
        'content_text': 'Переменные в Python',
        'homework_task': 'Создайте 3 переменные'
    }
)

print("Готово!")
print(f"Учитель: teacher / teacher123")
print(f"Ученик: student / student123")
