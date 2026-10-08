from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Task
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# Habit
class Habit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_streak(self):

        today = timezone.localdate()

        streak = 0

        current_date = today

        while HabitCompletion.objects.filter(
            habit=self,
            date=current_date
        ).exists():

            streak += 1

            current_date -= timezone.timedelta(days=1)

        return streak

    def __str__(self):
        return self.name


# HabitCompletion
class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.habit.name} - {self.date}"


# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username