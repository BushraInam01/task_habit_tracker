from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Habit, HabitCompletion, Profile
from .forms import TaskForm, HabitForm
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Count, Q
from django.db.models.functions import TruncDay, ExtractWeekDay
from django.core.mail import send_mail


#Task List
def task_list(request):
    tasks = Task.objects.all()

    return render(request, "tracker/task_list.html", {
        "tasks": tasks
    })


#Task Create
def task_create(request):

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("task_list")

    else:
        form = TaskForm()

    return render(request, "tracker/task_form.html", {
        "form": form,
        "is_update": False
    })


# Task Update
def task_update(request, id):

    task = get_object_or_404(Task, id=id)

    if request.method == "POST":

        form = TaskForm(request.POST, instance=task)

        if form.is_valid():

            form.save()

            if request.headers.get("HX-Request"):
                return render(request, "tracker/task_item.html", {
                    "task": task
                })

            return redirect("task_list")

    else:

        form = TaskForm(instance=task)

        if request.headers.get("HX-Request"):
            return render(request, "tracker/task_edit.html", {
                "task": task
            })

    return render(request, "tracker/task_form.html", {
        "form": form,
        "is_update": True
    })


# Task Delete
def task_delete(request, id):

    task = get_object_or_404(Task, id=id)

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "tracker/task_confirm_delete.html", {
        "task": task
    })


# Habit List
def habit_list(request):

    habits = Habit.objects.all()

    today = timezone.localdate()

    completed_habits = HabitCompletion.objects.filter(
        date=today
    ).values_list("habit_id", flat=True)

    return render(request, "tracker/habit_list.html", {
        "habits": habits,
        "completed_habits": completed_habits,
    })



# Habit Create
def habit_create(request):

    if request.method == "POST":
        form = HabitForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("habit_list")

    else:
        form = HabitForm()

    return render(request, "tracker/habit_form.html", {
        "form": form,
        "is_update": False
    })


# Habit Update
def habit_update(request, id):

    habit = get_object_or_404(Habit, id=id)

    if request.method == "POST":
        form = HabitForm(request.POST, instance=habit)

        if form.is_valid():
            form.save()
            return redirect("habit_list")

    else:
        form = HabitForm(instance=habit)

    return render(request, "tracker/habit_form.html", {
        "form": form,
        "is_update": True
    })



# Habit Delete
def habit_delete(request, id):

    habit = get_object_or_404(Habit, id=id)

    if request.method == "POST":
        habit.delete()
        return redirect("habit_list")

    return render(request, "tracker/habit_confirm_delete.html", {
        "habit": habit
    })



# Habit Complete / Uncomplete
def habit_complete(request, id):

    habit = get_object_or_404(Habit, id=id)

    today = timezone.localdate()

    if request.method == "POST":

        completion = HabitCompletion.objects.filter(
            habit=habit,
            date=today
        ).first()

        if completion:
            completion.delete()
        else:
            HabitCompletion.objects.create(
                habit=habit,
                date=today
            )

    completed_habits = HabitCompletion.objects.filter(
        date=today
    ).values_list("habit_id", flat=True)

    return render(request, "tracker/habit_item.html", {
        "habit": habit,
        "completed_habits": completed_habits,
    })



# Calendar View
def calendar_view(request):

    today = timezone.localdate()

    first_day = today.replace(day=1)

    if first_day.month == 12:
        next_month = first_day.replace(
            year=first_day.year + 1,
            month=1
        )
    else:
        next_month = first_day.replace(
            month=first_day.month + 1
        )

    last_day = next_month - timedelta(days=1)

    tasks = Task.objects.filter(
        due_date__gte=first_day,
        due_date__lte=last_day
    )

    habit_completions = HabitCompletion.objects.filter(
        date__gte=first_day,
        date__lte=last_day
    )

    # TruncDay practice
    test_data = HabitCompletion.objects.annotate(
        day=TruncDay("date")
    ).values("day")

    print(list(test_data))

    # ExtractWeekDay practice
    weekday_data = HabitCompletion.objects.annotate(
        weekday=ExtractWeekDay("date")
    ).values("date", "weekday")

    print(list(weekday_data))

    calendar_data = []

    # First day ka weekday
    first_weekday = first_day.isoweekday()

    current_date = first_day

    while current_date <= last_day:

        day_tasks = tasks.filter(
            due_date=current_date
        )

        day_habits = habit_completions.filter(
            date=current_date
        )

        calendar_data.append({
            "date": current_date,
            "weekday": current_date.isoweekday(),
            "tasks": day_tasks,
            "habits": day_habits,
        })

        current_date += timedelta(days=1)

    return render(request, "tracker/calendar.html", {
        "calendar_data": calendar_data,
        "month": first_day.strftime("%B"),
        "year": first_day.year,
        "empty_days": range(first_weekday - 1),
    })


# Weekly Summary View
def weekly_summary(request):

    today = timezone.localdate()

    # Current week Monday
    start_of_week = today - timedelta(days=today.weekday())

    # Current week Sunday
    end_of_week = start_of_week + timedelta(days=6)


    # Tasks of current week
    tasks = Task.objects.filter(
        due_date__gte=start_of_week,
        due_date__lte=end_of_week
    )

    total_tasks = tasks.count()

    completed_tasks = tasks.filter(
        completed=True
    ).count()

    pending_tasks = tasks.filter(
        completed=False
    ).count()


    # Habit completions of current week
    habit_completions = HabitCompletion.objects.filter(
        date__gte=start_of_week,
        date__lte=end_of_week
    )

    total_habit_completions = habit_completions.count()


    # Weekly habit summary
    habit_summary = Habit.objects.annotate(
        weekly_completions=Count(
            "habitcompletion",
            filter=Q(
                habitcompletion__date__gte=start_of_week,
                habitcompletion__date__lte=end_of_week
            )
        )
    )


    return render(request, "tracker/weekly_summary.html", {
        "start_of_week": start_of_week,
        "end_of_week": end_of_week,

        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,

        "total_habit_completions": total_habit_completions,

        "habit_summary": habit_summary,
    })



# Weekly Summary Email
def send_weekly_summary_email(user_email):

    today = timezone.localdate()

    # Current week Monday
    start_of_week = today - timedelta(days=today.weekday())

    # Current week Sunday
    end_of_week = start_of_week + timedelta(days=6)


    # Tasks of current week
    tasks = Task.objects.filter(
        due_date__gte=start_of_week,
        due_date__lte=end_of_week
    )

    total_tasks = tasks.count()

    completed_tasks = tasks.filter(
        completed=True
    ).count()

    pending_tasks = tasks.filter(
        completed=False
    ).count()


    # Habit completions
    habit_completions = HabitCompletion.objects.filter(
        date__gte=start_of_week,
        date__lte=end_of_week
    )

    total_habit_completions = habit_completions.count()


    # Email message
    message = f"""
Weekly Summary
{start_of_week} to {end_of_week}

Tasks
-----
Total Tasks: {total_tasks}
Completed Tasks: {completed_tasks}
Pending Tasks: {pending_tasks}

Habits
------
Total Habit Completions: {total_habit_completions}
"""


    send_mail(
        subject="Your Weekly Summary",
        message=message,
        from_email=None,
        recipient_list=[user_email],
    )


#Dark Mode View
def toggle_dark_mode(request):

    profile = Profile.objects.get(user=request.user)

    profile.dark_mode = not profile.dark_mode
    profile.save()

    return redirect(request.META.get("HTTP_REFERER", "/"))