from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(UserProgress)
admin.site.register(UserBadge)
admin.site.register(Badge)

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Option)

admin.site.register(Quiz)
admin.site.register(QuizAttempt)
admin.site.register(QuizQuestionAttempt)
