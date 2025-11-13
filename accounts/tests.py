import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.conftest import user
from accounts.models import Adres

User = get_user_model()


#################################   REGISTER VIEW TESTS ################################################################
@pytest.mark.django_db
def test_register_view_get(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200



@pytest.mark.django_db
def test_register_view_post_success(client):
    url = reverse('register')
    data = {
        'email': 'testuser@example.com',
        'password1': 'Testpassword123',
        'password2': 'Testpassword123',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert User.objects.filter(email='testuser@example.com').exists()


@pytest.mark.django_db
def test_register_view_post_fail_username(client):
    url = reverse('register')
    User.objects.create(email='email@email.com', password='Testpassword')
    data = {
            'email': 'email@email.com',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123'
    }
    response = client.post(url, data)
    print(response.content.decode())
    assert response.status_code == 200
    assert "User with this Email address already exists." in response.content.decode()




#################################   LOGIN VIEW TESTS ################################################################


@pytest.mark.django_db
def test_login_view_get(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()


@pytest.mark.django_db
def test_login_view_post_success(client, user):
    url = reverse('login')
    data = {
        'username': 'testuser@example.com',
        'password': 'Testpassword',
    }
    response = client.post(url, data)
    print(response.content.decode())
    assert response.status_code == 302
    assert response.url == reverse('user_account')


@pytest.mark.django_db
def test_login_view_post_fail(client, user):
    url = reverse('login')
    data ={'username': 'testuser',
           'password': 'testpasswordd'}
    response = client.post(url, data)
    assert response.status_code ==200
    assert 'Invalid username or password' in response.content.decode()


@pytest.mark.django_db
def test_logout_view(client, user):
    client.force_login(user)
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('login')

######################################  User Account View Tests ##################################################

@pytest.mark.django_db
def test_user_account_view(client, user):
    client.force_login(user)
    url = reverse('user_account')
    response = client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()

@pytest.mark.django_db
def test_user_account_view_get_no_profile_data(client, user):
    client.force_login(user)
    url = reverse('user_account')
    # przed wejściem na widok profil nie istnieje
    assert not Adres.objects.filter(user=user).exists()
    response = client.get(url)
    assert response.status_code == 200
    assert 'testuser@example.com' in response.content.decode()
    assert 'testuser@example.com' == user.email
    # po GET profil został utworzony, ale bez danych (NULL)
    assert Adres.objects.filter(user=user).exists()
    adres = Adres.objects.get(user=user)
    assert user.first_name == ''
    assert user.last_name == ''
    assert adres.city == ''
    assert adres.street == ''
    assert adres.house_number == ''
    assert adres.apartment_number == ''
    assert adres.phone_number == ''


@pytest.mark.django_db
def test_user_account_view_get_with_profile_data(client, user, adres):
    client.force_login(user)
    url = reverse('user_account')
    response = client.get(url)
    print(response.content.decode())
    assert response.status_code == 200
    assert user.first_name == ''
    assert user.last_name == ''
    assert adres.post_code == '12345'
    assert adres.city == 'testcity'
    assert adres.street == 'teststreet'
    assert adres.house_number == '1'
    assert adres.apartment_number == '1'
    assert adres.phone_number == '123456789'
    assert '12345' in response.content.decode()
    assert 'testcity' in response.content.decode()
    assert 'teststreet' in response.content.decode()



@pytest.mark.django_db
def test_user_account_view_post_success_new_data(client, user, adres):
    client.force_login(user)
    url = reverse('user_account')
    data = {
            'email': 'email@example.com',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'post_code': '12345',
            'city': 'testcity',
            }
    response = client.post(url, data, follow=True)
    user.refresh_from_db()
    adres.refresh_from_db()
    print(response.content.decode())
    assert response.status_code == 200
    assert 'email@example.com' in response.content.decode()
    assert 'Jan' in response.content.decode()
    assert 'Kowalski' in response.content.decode()
    assert 'Account updated successfully!' in response.content.decode()
    assert user.email == 'email@example.com'
    assert adres.post_code == '12345'
    assert adres.city == 'testcity'
    assert 'testcity' in response.content.decode()




@pytest.mark.django_db
def test_user_account_view_post_success_no_data_updated(client, user):
    client.force_login(user)
    url = reverse('user_account')
    response = client.post(url, data={'email': 'testuser@example.com'}, follow=True )
    print(response.content.decode())
    assert response.status_code == 200
    assert 'No data updated' in response.content.decode()


























