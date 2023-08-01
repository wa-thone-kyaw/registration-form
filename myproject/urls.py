"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from student_registration import views

urlpatterns = [
    path("student_registration/insert/", views.insert, name="insert"),
    path("student_registration/student_list/", views.student_list, name="student_list"),
    path(
        "student_registration/match_burmese_data",
        views.match_burmese_data,
        name="match_burmese_data",
    ),
    path(
        "student_registration/delete_document/<str:doc_id>/",
        views.delete_document,
        name="delete_document",
    ),
    path(
        "student_registration/second_year",
        views.add_student_second_year,
        name="second_year",
    ),
    path(
        "student_registration/third_year",
        views.add_student_third_year,
        name="third_year",
    ),
    path(
        "student_registration/fourth_year",
        views.add_student_fourth_year,
        name="fourth_year",
    ),
    path(
        "student_registration/fifth_year",
        views.add_student_fifth_year,
        name="fourth_year",
    ),
    path(
        "student_registration/final_year",
        views.add_student_final_year,
        name="final_year",
    ),
    path(
        "student_registration/first_year",
        views.add_student_first_year,
        name="first_year",
    ),
    path(
        "student_registration/admin_add_student_secondyear_IT/",
        views.admin_add_student_secondyear_IT,
        name="admin_add_student_secondyear_IT",
    ),
    path(
        "student_registration/photo_upload_view",
        views.photo_upload_view,
        name="photo_upload_view",
    ),
    path(
        "student_registration/search_by_myanname",
        views.search_by_myanname,
        name="search_by_myanname",
    ),
    path("student_registration/register", views.register, name="register"),
    path("student_registration/signup", views.signup, name="signup"),
    path("student_registration/login", views.login, name="login"),
    path("admin/", admin.site.urls),
]
