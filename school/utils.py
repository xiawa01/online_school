from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
from django.conf import settings

def generate_certificate(student_name, course_name, completion_date):
    """Генерация PDF сертификата"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Фон (можно добавить изображение)
    c.setFillColorRGB(0.95, 0.95, 1)
    c.rect(0, 0, width, height, fill=1)
    
    # Заголовок
    c.setFont("Helvetica-Bold", 36)
    c.setFillColorRGB(0.2, 0.5, 0.9)
    c.drawCentredString(width/2, height - 100, "СЕРТИФИКАТ")
    
    # Текст
    c.setFont("Helvetica", 16)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(width/2, height - 180, "Настоящим подтверждается, что")
    
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 240, student_name)
    
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height - 300, "успешно завершил(а) курс")
    
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 350, course_name)
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 450, f"Дата выдачи: {completion_date}")
    
    c.save()
    buffer.seek(0)
    return buffer
