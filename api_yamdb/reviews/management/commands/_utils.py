import csv
from pprint import pprint

from reviews.models import (
    Category, Genre, Title, Review, Comment, User
)
from api_yamdb.settings import BASE_DIR


FILE_DIR = BASE_DIR + r'\static\data'


def get_data():
    with open(FILE_DIR + r'\category.csv', encoding="utf-8") as csvfile:
        Category.objects.all().delete()
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            category.save()

    with open(FILE_DIR + r'\genre.csv', encoding="utf-8") as csvfile:
        Genre.objects.all().delete()
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            genre.save()

    with open(FILE_DIR + r'\users.csv', encoding="utf-8") as csvfile:
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

    with open(FILE_DIR + r'\titles.csv', encoding="utf-8") as csvfile:
        Title.objects.all().delete()
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            category, created = Category.objects.get_or_create(id=row['category'])
            title = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=category,
            )
            title.save()

    with open(FILE_DIR + r'\genre_title.csv', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            title, created = Title.objects.get_or_create(id=row['title_id'])
            genre, created = Genre.objects.get_or_create(id=row['genre_id'])
            title.genre.add(genre)
            title.save()

    with open(FILE_DIR + r'\review.csv', encoding="utf-8") as csvfile:
        Review.objects.all().delete()
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            title, created = Title.objects.get_or_create(id=row['title_id'])
            author, created = User.objects.get_or_create(id=row['author'])
            review = Review(
                id=row['id'],
                title=title,
                text=row['text'],
                author=author,
                score=row['score'],
                pub_date=row['pub_date'],
            )
            review.save()

    with open(FILE_DIR + r'\comments.csv', encoding="utf-8") as csvfile:
        Comment.objects.all().delete()
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            review_id, created = Review.objects.get_or_create(id=row['review_id'])
            author_id, created = User.objects.get_or_create(id=row['author'])
            p = Comment(
                review=review_id,
                text=row['text'],
                author=author_id,
                pub_date=row['pub_date'],
            )
            p.save()

