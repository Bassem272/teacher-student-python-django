@echo off

REM Start Redis container
docker run -p 6379:6379 redis:7

REM Navigate to the Django project directory (adjust the path as needed)
cd D:\teacher-student-python-django

REM Start Django development server
python manage.py runserver

REM Optionally, to start both commands in parallel:
REM start docker run -d -p 6379:6379 --name redis redis:7
REM start python manage.py runserver
