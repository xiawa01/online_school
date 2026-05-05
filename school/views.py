import json
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from .models import User, Lesson, StudentProgress

@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except:
            return JsonResponse({'success': False, 'message': 'Неверный формат запроса'}, status=400)
        
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'name': user.first_name or user.username,
                        'progress': user.progress,
                        'role': user.role
                    }
                })
            else:
                return JsonResponse({'success': False, 'message': 'Неверный пароль'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Пользователь не найден'}, status=401)
    
    return JsonResponse({'success': False, 'message': 'Метод не разрешен'}, status=405)

def lessons_list(request):
    lessons = Lesson.objects.all().values('id', 'title')
    return JsonResponse(list(lessons), safe=False)

def lesson_detail(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    return JsonResponse({
        'id': lesson.id,
        'title': lesson.title,
        'content': lesson.content_text or 'Содержание урока',
        'homework_task': lesson.homework_task or 'Нет задания'
    })

@csrf_exempt
def complete_lesson(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        user = get_object_or_404(User, id=data.get('userId'))
        lesson_id = data.get('lessonId')
        if lesson_id not in user.progress:
            user.progress.append(lesson_id)
            user.save()
        return JsonResponse({'success': True, 'progress': user.progress})
    return JsonResponse({'success': False}, status=405)

def get_homework(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return JsonResponse({'task': lesson.homework_task or 'Нет домашнего задания'})

@csrf_exempt
def submit_homework(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        answer = data.get('answer', '')
        if len(answer) < 10:
            feedback = "🤔 Попробуйте дать более развернутый ответ."
        else:
            feedback = "✅ Отлично! Задание принято!"
        return JsonResponse({'success': True, 'feedback': feedback})
    return JsonResponse({'success': False}, status=405)

@csrf_exempt
def add_student_to_course(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        course_id = data.get('course_id')
        student_username = data.get('student_username')
        
        try:
            course = Course.objects.get(id=course_id)
            student = User.objects.get(username=student_username, role='student')
            course.students.add(student)
            return JsonResponse({'success': True, 'message': f'Ученик {student_username} добавлен'})
        except Course.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Курс не найден'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Ученик не найден'}, status=404)
    return JsonResponse({'success': False}, status=405)

@csrf_exempt
def create_student(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        
        from django.contrib.auth.hashers import make_password
        try:
            student = User.objects.create(
                username=username,
                password=make_password(password),
                email=email,
                role='student',
                progress=[]
            )
            return JsonResponse({'success': True, 'user': {'id': student.id, 'username': student.username}})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return JsonResponse({'success': False}, status=405)

@csrf_exempt
def add_student_to_course(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        course_id = data.get('course_id')
        student_username = data.get('student_username')
        
        try:
            course = Course.objects.get(id=course_id)
            student = User.objects.get(username=student_username, role='student')
            course.students.add(student)
            return JsonResponse({'success': True, 'message': f'Ученик {student_username} добавлен'})
        except Course.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Курс не найден'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Ученик не найден'}, status=404)
    return JsonResponse({'success': False}, status=405)

@csrf_exempt
def create_student(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        
        from django.contrib.auth.hashers import make_password
        try:
            student = User.objects.create(
                username=username,
                password=make_password(password),
                email=email,
                role='student',
                progress=[]
            )
            return JsonResponse({'success': True, 'user': {'id': student.id, 'username': student.username}})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return JsonResponse({'success': False}, status=405)

@csrf_exempt
def create_lesson(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        course_id = data.get('course_id')
        module_title = data.get('module_title', 'Основной модуль')
        lesson = Lesson.objects.create(
            module_id=module_id,
            title=data.get('title'),
            lesson_type=data.get('lesson_type', 'async'),
            content_text=data.get('content_text', ''),
            video_url=data.get('video_url', ''),
            homework_task=data.get('homework_task', ''),
            test_data=data.get('test_data', {}),
            scheduled_start=data.get('scheduled_start') if data.get('lesson_type') == 'sync' else None,
            duration_minutes=data.get('duration_minutes', 60)
        )
        return JsonResponse({'success': True, 'lesson_id': lesson.id})
    return JsonResponse({'success': False}, status=405)

@csrf_exempt
def update_lesson(request, lesson_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        lesson = get_object_or_404(Lesson, id=lesson_id)
        lesson.title = data.get('title', lesson.title)
        lesson.content_text = data.get('content_text', lesson.content_text)
        lesson.video_url = data.get('video_url', lesson.video_url)
        lesson.homework_task = data.get('homework_task', lesson.homework_task)
        lesson.test_data = data.get('test_data', lesson.test_data)
        lesson.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=405)

def get_teacher_courses(request):
    """Получить все курсы учителя"""
    courses = Course.objects.filter(teacher=request.user).values('id', 'title')
    return JsonResponse(list(courses), safe=False)

def get_course_modules(request, course_id):
    """Получить модули курса"""
    modules = Module.objects.filter(course_id=course_id).values('id', 'title', 'order')
    return JsonResponse(list(modules), safe=False)

@csrf_exempt
def create_module(request):
    """Создать новый модуль в курсе"""
    if request.method == 'POST':
        data = json.loads(request.body)
        course = get_object_or_404(Course, id=data.get('course_id'), teacher=request.user)
        module = Module.objects.create(
            course=course,
            title=data.get('title'),
            order=data.get('order', 999)
        )
        return JsonResponse({'success': True, 'module_id': module.id})
    return JsonResponse({'success': False}, status=405)

@csrf_exempt
def create_lesson_full(request):
    """Создать урок (полная версия с контентом)"""
    if request.method == 'POST':
        data = json.loads(request.body)
        
        module = get_object_or_404(Module, id=data.get('module_id'))
        
        lesson = Lesson.objects.create(
            module=module,
            title=data.get('title'),
            lesson_type=data.get('lesson_type', 'async'),
            order=data.get('order', 999),
            content_text=data.get('content_text', ''),
            video_url=data.get('video_url', ''),
            homework_task=data.get('homework_task', ''),
            test_data=data.get('test_data', {}),
            scheduled_start=data.get('scheduled_start') if data.get('lesson_type') == 'sync' else None,
            duration_minutes=data.get('duration_minutes', 60),
            enable_recording=data.get('enable_recording', False)
        )
        
        return JsonResponse({
            'success': True, 
            'lesson_id': lesson.id,
            'message': f'Урок "{lesson.title}" создан!'
        })
    return JsonResponse({'success': False}, status=405)

def create_student(request):
    return JsonResponse({'success': False, 'message': 'В разработке'}, status=501)

def add_student_to_course(request):
    return JsonResponse({'success': False, 'message': 'В разработке'}, status=501)

def create_lesson(request):
    return JsonResponse({'success': False, 'message': 'В разработке'}, status=501)

def update_lesson(request, lesson_id):
    return JsonResponse({'success': False, 'message': 'В разработке'}, status=501)

def get_teacher_courses(request):
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return JsonResponse({'error': 'Доступ запрещен'}, status=403)
    courses = Course.objects.filter(teacher=request.user).values('id', 'title')
    return JsonResponse(list(courses), safe=False)

def get_course_modules(request, course_id):
    modules = Module.objects.filter(course_id=course_id).values('id', 'title', 'order')
    return JsonResponse(list(modules), safe=False)

def create_module(request):
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)
    import json
    data = json.loads(request.body)
    course = get_object_or_404(Course, id=data.get('course_id'))
    module = Module.objects.create(
        course=course,
        title=data.get('title'),
        order=data.get('order', 999)
    )
    return JsonResponse({'success': True, 'module_id': module.id})

def create_lesson_full(request):
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)
    import json
    data = json.loads(request.body)
    module = get_object_or_404(Module, id=data.get('module_id'))
    lesson = Lesson.objects.create(
        module=module,
        title=data.get('title'),
        lesson_type=data.get('lesson_type', 'async'),
        order=data.get('order', 999),
        content_text=data.get('content_text', ''),
        video_url=data.get('video_url', ''),
        homework_task=data.get('homework_task', ''),
        test_data=data.get('test_data', {}),
        scheduled_start=data.get('scheduled_start') if data.get('lesson_type') == 'sync' else None,
        duration_minutes=data.get('duration_minutes', 60),
        enable_recording=data.get('enable_recording', False)
    )
    return JsonResponse({'success': True, 'lesson_id': lesson.id, 'message': f'Урок "{lesson.title}" создан!'})

@csrf_exempt
def upload_homework_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        # Сохраняем файл (пока локально, потом на S3)
        import os
        from django.conf import settings
        
        filename = f"{timezone.now().timestamp()}_{file.name}"
        filepath = os.path.join(settings.MEDIA_ROOT, 'homeworks', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)
        
        return JsonResponse({
            'success': True,
            'file_url': f'/media/homeworks/{filename}',
            'filename': file.name,
            'size': file.size
        })
    return JsonResponse({'success': False, 'error': 'No file'}, status=400)
from django.http import FileResponse
from .utils import generate_certificate
from .models import Certificate

def download_certificate(request, certificate_id):
    cert = get_object_or_404(Certificate, id=certificate_id, student=request.user)
    pdf_buffer = generate_certificate(
        student_name=request.user.get_full_name() or request.user.username,
        course_name=cert.course.title,
        completion_date=cert.issued_at.strftime('%d.%m.%Y')
    )
    return FileResponse(pdf_buffer, as_attachment=True, filename=f'certificate_{certificate_id}.pdf')
