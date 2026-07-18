# Shared fixtures, available to every test in the project.
# pytest auto-discovers this file by name

import pytest
from ninja_jwt.tokens import RefreshToken

from apps.game.models import LevelType
from apps.users.models import User


@pytest.fixture
def user(db):
    
    return User.objects.create_user(email="player@example.com", password="pw12345678")


@pytest.fixture
def admin(db): # creates supseruser with every perm

    return User.objects.create_superuser(email="admin@example.com", password="pw12345678")


@pytest.fixture
def auth_headers(user):
   
    token = RefreshToken.for_user(user).access_token
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}

