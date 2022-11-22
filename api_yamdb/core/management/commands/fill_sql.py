import csv
from django.core.management.base import BaseCommand

from django.conf import settings
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

CSV_FILES = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    User: 'users.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = 'Заполняет базу данных из подготовленных csv файлов'

    def handle(self, *args, **kwargs):
        for model, filename in CSV_FILES.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{filename}', encoding='utf-8'
            ) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    row = dict(row)
                    model.objects.create(**row)
