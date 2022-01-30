from django.urls import path
from rest_framework import routers

from vacancies.views import VacancyListView, VacancyDetailView, VacancyCreateView, VacancyUpdateView, VacancyDeleteView, \
    SkillViewSet, VacancyLikeView

router = routers.SimpleRouter()
router.register('skill', SkillViewSet)

urlpatterns = [
    path('', VacancyListView.as_view()),
    path('create/', VacancyCreateView.as_view()),
    path('<int:pk>/', VacancyDetailView.as_view()),
    path('<int:pk>/update/', VacancyUpdateView.as_view()),
    path('<int:pk>/delete/', VacancyDeleteView.as_view()),
    path('like/', VacancyLikeView.as_view()),
]

urlpatterns += router.urls
