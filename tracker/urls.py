from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("expenses/", views.expense_list, name="expense_list"),
    path("expenses/export/", views.export_expenses, name="export_expenses"),
    path("expenses/add/", views.expense_create, name="expense_create"),
    path("expenses/<int:pk>/edit/", views.expense_edit, name="expense_edit"),
    path("expenses/<int:pk>/delete/", views.expense_delete, name="expense_delete"),
    path("budget/", views.budget_set, name="budget_set"),
    path("profile/", views.profile, name="profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("reports/",views.expense_reports,name="expense_reports"),
]
