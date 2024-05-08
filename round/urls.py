from django.urls import path, include
from . import views

urlpatterns = [
    path('selection/', views.select_course, name="select_course"),
    path('stats/<int:course_id>/<int:holeNum>/<int:score_id>/', views.home, name='golf-home'),
    path('scorecard/', views.printScores, name='golf-scorecard'),
    path('scores/<int:score_id>/delete/', views.delete_score, name='delete_score'),
]