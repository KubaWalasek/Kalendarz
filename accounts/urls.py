from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user_account/', views.UserAccountView.as_view(), name='user_account'),
    path('delete_account/', views.DeleteAccountView.as_view(), name='delete_account'),
    path('update_password/', views.UpdatePasswordView.as_view(), name='update_password'),
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="../templates/accounts/password_reset_form.html",
        email_template_name="password_reset_email.html",
        success_url="/accounts/password_reset/done/",
    ), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="../templates/accounts/password_reset_done.html",
    ), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="../templates/accounts/password_reset_confirm.html",
        success_url="/accounts/reset/done/",
    ), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="../templates/accounts/password_reset_complete.html",
    ), name="password_reset_complete"),

]