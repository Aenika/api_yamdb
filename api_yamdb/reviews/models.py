from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_not_future
import datetime as dt
from core.models import CreatedModel


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг категории',
        max_length=50
    )


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра',
        max_length=50
    )


class Title(models.Model):
    name = models.CharField(max_length=350, verbose_name='Название')
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[validate_not_future]
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='категория',
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='жанр',
        related_name='titles'
    )


class Review(CreatedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        max_length=500
    )
    score = models.PositiveIntegerField(
        verbose_name='Оценка',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ],
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_reviews')
        ]
        verbose_name = ('Отзыв')
        verbose_name_plural = ('Отзывы')
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(CreatedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст коментария',
        max_length=500
    )

    title = models.ForeignKey(
        Title,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name='Произведение',
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = ('Комментарий')
        verbose_name_plural = ('Комментарии')

    def __str__(self):
        return self.text
