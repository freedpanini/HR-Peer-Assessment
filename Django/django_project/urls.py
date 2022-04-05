"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from users import views as user_views
from courses.views import course_creation_view, team_creation_view, send_email
from assessments import views as assessment_views

urlpatterns = [
    path('', user_views.home_view, name='home'),
    path('home', user_views.home_view, name='home'),
    path('logout/', user_views.logout_view, name='login'),
    path('admin/', admin.site.urls),
    path('login/', user_views.login_view, name='login'),
    path('register/', user_views.register_view, name='register'),
    path('peer_assessment/', user_views.assessment_view, name = 'peer_assessment'),
    path('assessment_summary/', user_views.summary_view, name = 'assessment_summary'),
    path('create_course/', course_creation_view, name="create_course"),
    path('create_team/',team_creation_view, name="create_team"),
    path('send_email/', send_email, name="send_email"),
    path('create_assessment/', assessment_views.create_assessment, name='create_assessment'),
    path('<int:pk>/create_options/', assessment_views.create_option, name= 'create_option'),
    path('<int:pk>/create_question/', assessment_views.create_question, name = 'create_question')
]