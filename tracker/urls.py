from django.urls import path

from .views import (
    task_list,
    task_create,
    task_update,
    task_delete,
    habit_list,
    habit_create,
    habit_update,
    habit_delete,
    habit_complete,
    calendar_view,
    weekly_summary,
    toggle_dark_mode,
)


urlpatterns = [
    path("tasks/", task_list, name="task_list"),
    path("tasks/create/", task_create, name="task_create"),
    path("tasks/<int:id>/edit/", task_update, name="task_update"),
    path("tasks/<int:id>/delete/", task_delete, name="task_delete"),

    path("habits/", habit_list, name="habit_list"),
    path("habits/create/", habit_create, name="habit_create"),
    path("habits/<int:id>/edit/", habit_update, name="habit_update"),
    path("habits/<int:id>/delete/", habit_delete, name="habit_delete"),
    path("habits/<int:id>/complete/", habit_complete, name="habit_complete"),
    path("calendar/", calendar_view, name="calendar"),
    path("weekly-summary/", weekly_summary, name="weekly_summary"),
    path("toggle-dark-mode/", toggle_dark_mode, name="toggle_dark_mode"),
]