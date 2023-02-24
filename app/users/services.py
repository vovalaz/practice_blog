from users.models import User
from dataclasses import dataclass


@dataclass
class UserDataClass:
    username: str
    email: str
    password: str = None
    id: int = None

    @classmethod
    def from_instance(cls, user: User):
        return cls(
            username=user.username,
            email=user.email,
            id=user.id,
        )


def create_user(user: UserDataClass) -> UserDataClass:
    instance = User(username=user.username, email=user.email)
    if user.password is not None:
        instance.set_password(user.password)

    instance.save()

    return UserDataClass.from_instance(instance)


def create_superuser(user: UserDataClass) -> UserDataClass:
    instance = User(username=user.username, email=user.email, is_staff=True)
    if user.password is not None:
        instance.set_password(user.password)

    instance.save()

    return UserDataClass.from_instance(instance)
