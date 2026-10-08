from django.contrib import admin
from .models import Task, Habit, HabitCompletion, Profile

admin.site.register(Task)
admin.site.register(Habit)
admin.site.register(HabitCompletion)
admin.site.register(Profile)
