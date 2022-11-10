import csv
import os
from django.conf import settings

from reviews.models import (Category, Genre, Title,
                            Review, Comment, User)

FILE_DIR = os.path.join(settings.BASE_DIR, "static\data")


def import_csv():

    with open(os.path.join(FILE_DIR, "category.csv"), encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        Category.objects.bulk_create(objs=[
            Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            for row in reader
        ])

    with open(os.path.join(FILE_DIR, "genre.csv"), encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        Genre.objects.bulk_create(objs=[
            Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            for row in reader
        ])

    with open(os.path.join(FILE_DIR, "users.csv"), encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        User.objects.bulk_create(objs=[
            User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            for row in reader
        ])

    with open(os.path.join(FILE_DIR, "titles.csv"), encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        Title.objects.bulk_create(objs=[
            Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get_or_create(
                    id=row['category']
                )[0],
            )
            for row in reader
        ])

    with open(os.path.join(FILE_DIR, "genre_title.csv"), encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            title, created = Title.objects.get_or_create(
                id=row['title_id']
            )
            genre, created = Genre.objects.get_or_create(
                id=row['genre_id']
            )
            title.genre.add(genre)
            title.save()

    with open(os.path.join(FILE_DIR, "review.csv"), encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        Review.objects.bulk_create(objs=[
            Review(
                id=row['id'],
                title=Title.objects.get_or_create(
                    id=row['title_id'])[0],
                text=row['text'],
                author=User.objects.get_or_create(
                    id=row['author'])[0],
                score=row['score'],
                pub_date=row['pub_date'],
            )
            for row in reader
        ])

    with open(os.path.join(FILE_DIR, "comments.csv"), encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        Comment.objects.bulk_create(objs=[
            Comment(
                review=Review.objects.get_or_create(
                    id=row['review_id']
                )[0],
                text=row['text'],
                author=User.objects.get_or_create(
                    id=row['author']
                )[0],
                pub_date=row['pub_date'],
            )
            for row in reader
        ])
