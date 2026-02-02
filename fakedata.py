import os
import random

import django
from faker import Faker


def clean_teachers():
    print("Cleaning teachers...")

    Teacher.objects.all().delete()

    print("Cleaned teachers...")


def clean_subject_data():
    print("Cleaning subject data...")

    SubjectData.objects.all().delete()

    print("Cleaned subject data...")


def create_teachers():
    print("Creating teachers...")

    fake = Faker("zh_CN")

    # ids = [fake.unique.random_int(min=1, max=8) for _ in range(50)]
    for _ in range(50):
        teacher = Teacher.objects.create(
            id=fake.year() + str(fake.unique.random_number(digits=3)).zfill(4),
            name=fake.name(),
            birthday=fake.date_of_birth(minimum_age=18, maximum_age=65),
            email=fake.email(),
            phone=fake.phone_number(),
            university_id="10602",
            gender_id=random.randint(1, 2),
            title_id=random.randint(1, 5),
            education_id=random.randint(1, 4),
            degree_id=random.randint(1, 4),
        )

        print("Created teacher {}".format(teacher))

    print("Created teachers {}".format(Teacher.objects.count()))

    print("Created teachers...")


def create_subject_data():
    print("Creating subject data...")

    fake = Faker("zh_CN")

    user = User.objects.get(id=1)

    for _ in range(50):
        level = Level.objects.order_by("?").first()
        indicator = Indicator.objects.order_by("?").first()
        teacher = Teacher.objects.order_by("?").first()
        primary_subject = PrimarySubject.objects.order_by("?").first()
        secondary_subject = SecondarySubject.objects.order_by("?").first()

        data = SubjectData.objects.create(
            year=fake.year(),
            name=fake.text(max_nb_chars=20),
            level=level,
            indicator=indicator,
            primary_subject=primary_subject,
            secondary_subject=secondary_subject,
            teacher=teacher,
            university_id="10602",
            value=fake.profile(),
            creator=user,
            updator=user,
            created_time=fake.date_time(),
            updated_time=fake.date_time(),
        )

        print("Created subject data {}".format(data))

    print("Created subject data {}".format(SubjectData.objects.count()))

    print("Created subject data...")


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "discipline.settings")
    django.setup()

    from accounts.models import Teacher, User
    from indicators.models import SubjectData, Level, Indicator
    from subjects.models import PrimarySubject, SecondarySubject

    clean_teachers()
    create_teachers()

    clean_subject_data()
    create_subject_data()
