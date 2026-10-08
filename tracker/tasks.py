from celery import shared_task
from .views import send_weekly_summary_email


@shared_task
def weekly_summary_email_task():

    send_weekly_summary_email(
        "test@example.com"
    )

    return "Weekly summary email sent successfully."