from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PUBLISHED = "published", "Опубликован"

    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField("Слаг", max_length=220, unique_for_date="created")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )
    body = models.TextField("Текст поста")
    status = models.CharField(
        "Статус", max_length=10, choices=Status.choices, default=Status.DRAFT
    )
    created = models.DateTimeField("Создан", auto_now_add=True)
    updated = models.DateTimeField("Обновлён", auto_now=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["-created"])]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("blog_app:post_detail", args=[self.created.year, self.created.month, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Пост"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments",
        verbose_name="Автор",
    )
    name = models.CharField("Имя", max_length=80)
    email = models.EmailField("Email")
    body = models.TextField("Текст комментария")
    is_approved = models.BooleanField("Одобрен", default=True)
    created = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        ordering = ["created"]


    def __str__(self):
        return f"{self.name}: {self.body[:30]}"
