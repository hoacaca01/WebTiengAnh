from django.contrib import admin
from .models import Course, Lesson, Quiz, Question, Answer, QuizResult, Discussion, Vocabulary, UserProgress, UserProfile
from .models import Quiz_lesson, Question_lesson, Answer_lesson, QuizResult_lesson
# Đăng ký models trong trang quản trị
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Question)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_correct', 'question')

admin.site.register(QuizResult)

admin.site.register(Quiz_lesson)
admin.site.register(Question_lesson)
@admin.register(Answer_lesson)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_correct', 'question')
admin.site.register(QuizResult_lesson)

admin.site.register(Discussion)
admin.site.register(Vocabulary)
admin.site.register(UserProgress)
admin.site.register(UserProfile)
