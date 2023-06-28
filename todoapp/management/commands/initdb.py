from django.core.management.base import BaseCommand
from ...models import User, Todo


USERS = {"admin": "admin", "alex": "fisheye", "piter": "greenlake"}


class Command(BaseCommand):
    help = "Creates test data in db"

    def handle(self, *args, **options):
        print("Creating data")
        for username, password in USERS.items():
            fields = {"username": username, "password": password}
            if username == "admin":
                fields["is_superuser"] = True
                fields["is_staff"] = True
            u = User(**fields)
            u.save()

            for i in range(1, 10):
                todo = Todo(
                    user=u,
                    title=f"{username}'s todo {i}",
                    description=f"{username}'s todo {i} description...",
                )
                todo.save()

            print(f"Created user {username}:{password} with some todos")
