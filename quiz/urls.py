from django.urls import path
from .views import QuizView, ResultView, ScenarioDeleteView, ScenarioDetailView, ScenarioListView,ScenarioView, StatistiquesAdminAPIView, UpdateScenarioView,nextScenarioView,ScenarioCreateView
urlpatterns = [
    path('quiz',QuizView.as_view()),
    path('scenario',ScenarioView.as_view()),
    path('next',nextScenarioView.as_view()),
    path('result',ResultView.as_view()),
    path('add_scenario',ScenarioCreateView.as_view()),
    path('scenario_list',ScenarioListView.as_view()),
    path('scenario/<int:pk>/delete/', ScenarioDeleteView.as_view(), name='scenario-delete'),
   path('scenarios/<int:pk>/update/', UpdateScenarioView.as_view(), name='update-scenario'),
   path('scenarios/<int:pk>/', ScenarioDetailView.as_view(), name='scenario-detail'),
   path('stat',StatistiquesAdminAPIView.as_view()),
]