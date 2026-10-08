from django import forms
from .models import Task, Habit


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["title", "description", "priority", "due_date", "completed"]


class HabitForm(forms.ModelForm):

    class Meta:
        model = Habit
        fields = ["name", "description"]