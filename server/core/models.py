from django.db import models
from django.contrib.auth.models import User

# Difficulty choices
LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
DIFFICULTY_CHOICES = [(level, level) for level in LEVELS]

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# User related Models
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.user.username

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quizzes_completed = models.IntegerField(default=0)
    quizzes_passed = models.IntegerField(default=0)
    best_accuracy = models.FloatField(default=0.0)
    average_time_per_question = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} has the best accuracy of {self.best_accuracy}!"

class Badge(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
    
# Question Models
class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    prompt = models.TextField()
    hint = models.TextField(blank=True)
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='Beginner'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.prompt[:50]} ({self.difficulty_level})"


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


# Quiz Models
class Quiz(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='Beginner'
    )
    num_questions = models.IntegerField()
    time_limit = models.IntegerField()  # in minutes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quiz: {self.category.name} ({self.difficulty_level})"


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    attempted_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_correct = models.IntegerField(default=0)
    total_incorrect = models.IntegerField(default=0)
    total_time_taken = models.IntegerField(null=True, blank=True)  # in seconds
    accuracy = models.FloatField(null=True, blank=True)
    passed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.quiz}"


class QuizQuestionAttempt(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"Attempt: {self.quiz_attempt} - {self.question}"