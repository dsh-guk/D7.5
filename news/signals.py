from .models import Post, Category
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import notify_subscribers


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if instance.postCategory.first():
        if not instance.isUpdated:

            cat = instance.postCategory.first()
            subscribers = cat.subscribers.all()

            user_emails = []
            user_names = []

            for subscriber in subscribers:
                user_emails.append(subscriber.email)
                user_names.append(subscriber.username)
                sub_name = subscriber.username
                sub_email = subscriber.email
                title = instance.postTitle
                pub_time = instance.pubDate.strftime("%d %m %Y")
                pk = instance.pk
                post = Post.objects.get(id=pk)
                category = Post.objects.get(id=pk).postCategory.get().categoryName

                notify_subscribers.delay(sub_name, sub_email, title, category, pub_time, pk)