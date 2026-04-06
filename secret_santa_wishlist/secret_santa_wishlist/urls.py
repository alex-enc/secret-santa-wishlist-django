"""secret_santa_wishlist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from secretsanta.views import home_view, sign_up_view, log_in_view, log_out_view, dashboard_view, new_group_info_view, my_groups_view, generate_assignments_view, profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view.home, name='home'),
    path('sign_up/', sign_up_view.sign_up, name='sign_up'),
    path('log_in/', log_in_view.log_in, name='log_in'),
    path('log_out', log_out_view.log_out, name='log_out'),
    path('dashboard/', dashboard_view.dashboard, name='dashboard'),
    path('new_group_info/', new_group_info_view.new_group_info, name='new_group_info'),
    path('my_groups/', my_groups_view.my_groups, name='my_groups'),
    path("generate_assignments/<int:group_id>/", generate_assignments_view.generate_assignments, name="generate_assignments"),
    path('profile/', profile_view.profile, name='profile'),
]
