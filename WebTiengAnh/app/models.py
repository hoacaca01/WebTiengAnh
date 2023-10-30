from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django import forms
from ckeditor.fields import RichTextField

class CreateUserForm(UserCreationForm):
    class Meta:
        model =  User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_username(self):
        # Kiểm tra tính duy nhất của tên người dùng
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Tên người dùng đã tồn tại.')
        return username

    def clean_email(self):
        # Kiểm tra tính duy nhất của địa chỉ email
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email đã tồn tại.')
        return email

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password1 = cleaned_data.get("password1")
    #     password2 = cleaned_data.get("password2")
    #
    #     if password1 != password2:
    #         raise forms.ValidationError("Mật khẩu và Mật khẩu xác nhận không khớp.")
    def clean_password2(self):
        # Kiểm tra tính hợp lệ của "Mật khẩu xác nhận"
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Mật khẩu và Mật khẩu xác nhận không khớp.")
        return password2

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#         # Kiểm tra xem avatar đã được thiết lập hay chưa
#         if not UserProfile.avatar:
#             # Đặt avatar bằng hình ảnh mặc định
#             UserProfile.avatar = settings.MEDIA_URL + 'avatars/ava.jpg'
#             UserProfile.save()
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        # Kiểm tra xem avatar đã được thiết lập hay chưa
        if not user_profile.avatar:
            # Đặt avatar bằng hình ảnh mặc định
            user_profile.avatar = 'avatars/ava.jpg'
            user_profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to='course_covers/')

    def __str__(self):
        return self.name

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    order = models.PositiveIntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Quiz_lesson(models.Model):
    title = models.CharField(max_length=200)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
class Question_lesson(models.Model):
    mota = RichTextField(null=True)
    text = models.TextField()
    quiz_lesson = models.ForeignKey(Quiz_lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Answer_lesson(models.Model):
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField()
    question_lesson = models.ForeignKey(Question_lesson, on_delete=models.CASCADE, name='question')

    def __str__(self):
        return self.text

class QuizResult_lesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_lesson = models.ForeignKey(Quiz_lesson, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    completion_date = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Answer(models.Model):
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, name='question')

    def __str__(self):
        return self.text

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    completion_date = models.DateTimeField(auto_now_add=True)

class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Vocabulary(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.TextField()
    example_usage = models.TextField()

    def __str__(self):
        return self.word

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.PositiveIntegerField()
    last_update = models.DateTimeField(auto_now=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username