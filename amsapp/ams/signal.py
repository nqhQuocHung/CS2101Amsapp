
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def send_email_to_lecturer(sender, instance, created, **kwargs):
    if created and instance.role == "lecturer":
        subject = 'Thông tin Tài khoản'
        message = f'Chào thầy/cô {instance.get_full_name()},\n\n' \
                  f'Tài khoản của bạn đã được tạo.\nTài khoản: {instance.username}\n' \
                  f'Mật khẩu: {settings.PASSWORD_LECTURER_DEFAULT}\n\n' \
                  f'Vui lòng đổi mật khẩu trong vòng 24 giờ.\n\n'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.email])


def send_notification_email(notification):
    subject = "Thông Báo Mới Từ Trường"
    message = notification.content
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = []

    if notification.group:
        # Lấy tất cả email của thành viên trong nhóm
        recipient_list = notification.group.groupmember_set.all().values_list('user__email', flat=True)
    elif notification.user:
        # Gửi đến một cá nhân
        recipient_list = [notification.user.email]
    else:
        # Gửi đến tất cả người dùng
        recipient_list = User.objects.all().values_list('email', flat=True)

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


@receiver(post_save, sender=User)
def send_mail_confirmation(sender, instance, **kwargs):
    # if instance.role == "alumni" and instance.is_active and instance.is_verified:
    subject = 'Account Confirmation'
    message = f'Chào bạn {instance.get_full_name()} \n\nTài khoản bạn đã được xác nhận.'
    from_email = settings.EMAIL_HOST_USER
    instance.email_user(subject, message, from_email)