from django.urls import path
from . import views

urlpatterns = [
	path('new-game', views.create_game, name='new_game'),
	path('game/<int:question_id>/', views.detail, name='detail'),
	path('game/<int:question_id>/guess', views.guess, name='guess'),
]