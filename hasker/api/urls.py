from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views

urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("questions", views.QuestionsAPIView.as_view(), name="api_questions"),
    path("questions/<int:pk>", views.QuestionDetailsAPIView.as_view(), name="api_question_details"),
    path("questions/<int:pk>/answers", views.AnswersAPIView.as_view(), name="api_answers"),
    path("questions/<int:pk>/votes", views.QuestionVotesAPIView.as_view(), name="api_question_votes"),
    path("questions/<int:question_pk>/votes/<int:pk>", views.QuestionVoteDetailsAPIView.as_view(),
         name="api_question_vote_details"),
    path("answers/<int:pk>", views.AnswerDetailsAPIView.as_view(), name="api_answer_details"),
    path("answers/<int:pk>/votes", views.AnswerVotesAPIView.as_view(), name="api_answer_votes"),
    path("answers/<int:answer_pk>/votes/<int:pk>", views.AnswerVoteDetailsAPIView.as_view(),
         name="api_answer_vote_details"),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
