from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from django.db.models import F, Sum
from parkings.models import History, UserProfile, Rates


@shared_task
def check_parking_limits():
    try:
        # print('Start checking limits...')

        current_month = now().month
        current_year = now().year
        current_period = f"{current_year}{str(current_month).zfill(2)}"  # Формат YYYYMM
        # print(f'{current_period = }')
        profiles = UserProfile.objects.all()

        # Передбачимо, що у нас є єдина ставка для всіх користувачів
        current_rate = Rates.objects.first().rate  # Отримуємо поточну ставку

        # print(f'{current_rate = }')

        # print('======================================')

        for profile in profiles:
            # print(profile)
            # print(f'{profile.parking_limit = }')
            if profile.parking_limit > 0:
                # Розрахунок суми витрат на завершені паркування для поточного місяця і року
                total_amount_spent = History.objects.filter(
                    plate__user=profile,
                    parking_start__month=current_month,
                    parking_start__year=current_year,
                    is_completed=True
                ).annotate(
                    cost=F('duration') * current_rate  # Використовуємо загальну ставку
                ).aggregate(total=Sum('cost'))['total'] or 0

                # print(f'{profile.user.email = }')
                # print(f'{total_amount_spent = }')

                # Перевіряємо, чи не було вже відправлено повідомлення в поточному місяці
                if total_amount_spent > profile.parking_limit:
                    if profile.last_limit_notification_sent != current_period:
                        # print('It\'s off the limit, sending email')
                        send_mail(
                            '[ParkEasy] Parking limit alert',
                            f'''
Dear Customer,

For the current month, the total cost of parking at ParkEasy network parking lots has exceeded your set monthly limit ({total_amount_spent} UAH out of {profile.parking_limit} UAH limit per month  so far). We highly recommend reviewing your parking history and limits set.

Best regards,
Your ParkEasy Team''',
                            'noreply@edin.ua',
                            [profile.email]
                        )
                        # Оновлюємо поле last_limit_notification_sent після відправки повідомлення
                        profile.last_limit_notification_sent = current_period
                        profile.save()
                        # print(f"Email sent to {profile.user.email} for exceeding parking limit.")
                    else:
                        pass # print('This month email has been already sent.')
                else:
                    pass # print(f"User {profile.user.email} is within the parking limit.")
            else:
                pass # print(f"User {profile.user.email} has no parking limit set.")

        return "Parking limits checked"

    except Exception as e:
        # print(f"Error in check_parking_limits: {str(e)}")
        raise
