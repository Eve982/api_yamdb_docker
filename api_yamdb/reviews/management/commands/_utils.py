import csv
import os

from reviews.models import (
    Category, Genre, Title, Review, Comment, User
)
from django.conf import settings


FILE_DIR = os.path.join(settings.BASE_DIR, r"static\data")


try:
    def get_data():
        with open(
            os.path.join(FILE_DIR, "category.csv"), encoding="utf-8"
        ) as csvfile:
            Category.objects.all().delete()
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                category = Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                category.save()

        with open(
            os.path.join(FILE_DIR, "genre.csv"), encoding="utf-8"
        ) as csvfile:
            Genre.objects.all().delete()
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                genre = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                genre.save()

        with open(
            os.path.join(FILE_DIR, "users.csv"), encoding="utf-8"
        ) as csvfile:
            User.objects.all().delete()
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                user = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
                user.save()

        with open(
            os.path.join(FILE_DIR, "titles.csv"), encoding="utf-8"
        ) as csvfile:
            Title.objects.all().delete()
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                category, created = Category.objects.get_or_create(
                    id=row['category']
                )
                title = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=category,
                )
                title.save()

        with open(
            os.path.join(FILE_DIR, "genre_title.csv"), encoding="utf-8"
        ) as csvfile:
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

        with open(
            os.path.join(FILE_DIR, "review.csv"), encoding="utf-8"
        ) as csvfile:
            Review.objects.all().delete()
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                title, created = Title.objects.get_or_create(
                    id=row['title_id']
                )
                author, created = User.objects.get_or_create(
                    id=row['author']
                )
                review = Review(
                    id=row['id'],
                    title=title,
                    text=row['text'],
                    author=author,
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
                review.save()

        with open(
            os.path.join(FILE_DIR, "comments.csv"), encoding="utf-8"
        ) as csvfile:
            Comment.objects.all().delete()
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                review_id, created = Review.objects.get_or_create(
                    id=row['review_id']
                )
                author_id, created = User.objects.get_or_create(
                    id=row['author']
                )
                p = Comment(
                    review=review_id,
                    text=row['text'],
                    author=author_id,
                    pub_date=row['pub_date'],
                )
                p.save()
except FileNotFoundError as e:
    raise f"FileNotFoundError successfully handled {e}"
# except Exception as err:
#     print(f"Unexpected {err}, {type(err)}")
#     raise
