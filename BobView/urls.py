"""BobView URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from myapp import views
# from myapp.views import UserVerificationView, UserRegistrationView, UserLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.post_list, name='post_list'),
    path('login/', views.llogin, name='login'),
    path('dologin/', views.dologin, name='dologin'),
    path('signup/', views.signup, name='signup'),
    path('dosignup/', views.dosignup, name='dosignup'),
    path('success/', views.success, name='success'),
    # path('user/<pk>/verify/<token>/', UserVerificationView.as_view()),
    path('active/<token>', views.user_active, name='user_active'),
]
