from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Course, Lesson, Quiz, Question, Answer, QuizResult, CreateUserForm, UserProfile
from .models import Quiz_lesson, Question_lesson, Answer_lesson, QuizResult_lesson
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login
from .forms import UserProfileForm
from django.utils import timezone

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tài khoản đã được tạo thành công.')
            # return redirect(reverse_lazy('app:login'))

    context = {'form': form}
    return render(request, 'register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('app:home'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse_lazy('app:home'))
        else:
            messages.error(request, 'Tài khoản hoặc mật khẩu không đúng.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('app:login'))

# def home(request):
#     return render(request, 'home.html')

def huongdan(request):
    context = {}
    if request.user.is_authenticated:
        context['user_authenticated'] = True
    return render(request, 'huongdan.html', context)

def home(request):
    courses = Course.objects.all()
    context = {}
    if request.user.is_authenticated:
        context['user_authenticated'] = True
    # return render(request, 'home.html', context)
    return render(request, 'home.html', {'courses': courses, **context})


def courses(request):
    # Lấy danh sách khóa học từ cơ sở dữ liệu
    courses = Course.objects.all()
    context = {}
    if request.user.is_authenticated:
        context['user_authenticated'] = True
    # return render(request, 'courses.html', {'courses': courses, **context})
    return render(request, 'courses1.html', {'courses': courses, **context})
@login_required
def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course=course)
    quizzes = Quiz.objects.filter(course=course)
    context = {
        'course': course,
        'lessons': lessons,
        'quizzes': quizzes,
    }
    if request.user.is_authenticated:
        context['user_authenticated'] = True
    return render(request, 'course_detail11.html', context)

@login_required
def course_detail2(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course=course)
    quizzes = Quiz.objects.filter(course=course)
    context = {
        'course': course,
        'lessons': lessons,
        'quizzes': quizzes,
    }
    if request.user.is_authenticated:
        context['user_authenticated'] = True
    return render(request, 'course_detail2.html', context)

def lesson_detail(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    quizzes_lesson = Quiz_lesson.objects.filter(lesson=lesson)
    context = {
        'lesson': lesson,
        'quizzes_lesson': quizzes_lesson,
    }
    if request.user.is_authenticated:
        context['user_authenticated'] = True
    return render(request, 'lesson_detail.html', context)

def lesson_detail1(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    quizzes_lesson = Quiz_lesson.objects.filter(lesson=lesson)
    context = {
        'lesson': lesson,
        'quizzes_lesson': quizzes_lesson,
    }
    if request.user.is_authenticated:
        context['user_authenticated'] = True
    return render(request, 'lesson_detail222.html', context)

def quiz_detail_lesson(request, quiz_lesson_id):
    quiz_lesson = Quiz_lesson.objects.get(id=quiz_lesson_id)
    questions_lesson = Question_lesson.objects.filter(quiz_lesson=quiz_lesson)
    context = {
        'quiz_lesson': quiz_lesson,
        'questions_lesson': questions_lesson,
    }
    if request.user.is_authenticated:
        context['user_authenticated'] = True
    return render(request, 'quiz_detail_lesson.html', context)
    # return render(request, 'giaodiencauhoi2.html', context)

def submit_quiz_lesson(request, quiz_lesson_id):
    if request.method == 'POST':
        quiz_lesson = Quiz_lesson.objects.get(id=quiz_lesson_id)
        questions_lesson = Question_lesson.objects.filter(quiz_lesson=quiz_lesson)
        score = 0

        for question_lesson in questions_lesson:
            answer_lesson_id = request.POST.get('question_{}'.format(question_lesson.id))
            if answer_lesson_id:
                answer_lesson = Answer_lesson.objects.get(id=answer_lesson_id)
                if answer_lesson.is_correct:
                    score += 1

        user = request.user if request.user.is_authenticated else None

        quiz_result_lesson = QuizResult_lesson.objects.create(
            user=user,
            quiz_lesson=quiz_lesson,
            score=score,
            completion_date= timezone.now()
        )
        context = {}
        if request.user.is_authenticated:
            context['user_authenticated'] = True
        return render(request, 'quiz_result_lesson.html', {'quiz_result_lesson': quiz_result_lesson, **context})
    else:
        return HttpResponse("Method not allowed")

def quiz_results_lesson(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('app:login'))

    # Lấy danh sách kết quả đã thi của người dùng hiện tại
    quiz_results_lesson = QuizResult_lesson.objects.filter(user=request.user)

    context = {
        'quiz_results_lesson': quiz_results_lesson,
    }
    if request.user.is_authenticated:
        context['user_authenticated'] = True
    return render(request, 'quiz_results_lesson.html', context)

def quiz_detail(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    if request.user.is_authenticated:
        context['user_authenticated'] = True
    # return render(request, 'quiz_detail.html', context)
    return render(request, 'giaodiencauhoi2.html', context)
def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = Quiz.objects.get(id=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        score = 0

        for question in questions:
            answer_id = request.POST.get('question_{}'.format(question.id))
            if answer_id:
                answer = Answer.objects.get(id=answer_id)
                if answer.is_correct:
                    score += 1

        user = request.user if request.user.is_authenticated else None

        quiz_result = QuizResult.objects.create(
            user=user,
            quiz=quiz,
            score=score,
            completion_date= timezone.now()
        )
        context = {}
        if request.user.is_authenticated:
            context['user_authenticated'] = True
        return render(request, 'quiz_result.html', {'quiz_result': quiz_result, **context})
    else:
        return HttpResponse("Method not allowed")

def quiz_results(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('app:login'))

    # Lấy danh sách kết quả đã thi của người dùng hiện tại
    quiz_results = QuizResult.objects.filter(user=request.user)

    context = {
        'quiz_results': quiz_results,
    }
    if request.user.is_authenticated:
        context['user_authenticated'] = True
    return render(request, 'quiz_results.html', context)

@login_required
def profile(request):
    # Truy cập thông tin tài khoản người dùng đã đăng nhập
    user = request.user

    # Kiểm tra xem có mô hình UserProfile liên kết với tài khoản người dùng không
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None

    context = {
        'user_profile': user_profile,
    }
    if request.user.is_authenticated:
        context['user_authenticated'] = True
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('app:profile'))  # Chuyển hướng đến trang profile sau khi lưu thành công
    else:
        form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'edit_profile.html', {'form': form})
