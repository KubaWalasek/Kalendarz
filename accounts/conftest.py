import pytest
from django.contrib.auth import get_user_model
from accounts.models import Adres



@pytest.fixture
def user():
    User = get_user_model()
    user=User.objects.create(email='testuser@example.com')
    user.set_password('Testpassword')
    user.save()
    return user


@pytest.fixture
def adres(user):
    adres = Adres.objects.create(
        user=user,
        post_code='12345',
        city='testcity',
        street='teststreet',
        house_number='1',
        apartment_number='1',
        phone_number='123456789'
    )
    return adres




