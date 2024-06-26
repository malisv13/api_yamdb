import uuid

from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_ADMIN


def generate_confirmation_code_and_send_email(user):
    """Функция для генерации кода подтверждения и отправки
    его на email"""

    conf_code = str(uuid.uuid4())

    user.confirmation_code = conf_code
    user.save()

    subject = 'Confirmation code'
    message = f'Your confirmation code is: {conf_code}'
    from_email = EMAIL_ADMIN
    recipient_list = [user.email, ]
    send_mail(subject, message, from_email, recipient_list)
