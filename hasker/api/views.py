from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from questions.models import Answer, AnswerVote, Question, QuestionVote
from .permissions import IsOwnerOfQuestionOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    AnswerSerializer,
    AnswerDetailSerializer,
    AnswerVoteSerializer,
    QuestionSerializer,
    QuestionVoteSerializer,
)


class QuestionsTagFilter(filters.BaseFilterBackend):
    """ Filter questions by specified tag.
    """
    def filter_queryset(self, request, queryset, view):
        tag = request.query_params.get("tag", "")
        tag = tag.strip().lower()
        if not tag:
            return queryset
        return queryset.filter(tags__name=tag)


class QuestionsOrderingFilter(filters.BaseFilterBackend):
    """ Ordering for questions.
    """
    VALID_SORTS = {
        "latest": "-posted",
        "popular": "-rating",
        "trending": "-number_of_votes",
    }

    def filter_queryset(self, request, queryset, view):
        sort = request.query_params.get("sort", "")
        sort = sort.strip().lower()
        if sort not in self.VALID_SORTS:
            return queryset
        return queryset.order_by(self.VALID_SORTS[sort])


class QuestionsAPIView(ListCreateAPIView):
    filter_backends = [
        QuestionsOrderingFilter,
        QuestionsTagFilter,
        filters.SearchFilter,
    ]
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ["title", "content"]
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Question.objects.all().select_related("author").prefetch_related("tags")


class QuestionDetailsAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.all().select_related("author").prefetch_related("tags")


# ? get_object_or_404

class QuestionVotesAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = QuestionVoteSerializer

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        super().initial(request, *args, **kwargs)
        self.question = get_object_or_404(Question, pk=self.kwargs.get("pk"))

    def get_queryset(self):
        return QuestionVote.objects.all().select_related("user").filter(to=self.question)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, to=self.question)


class QuestionVoteDetailsAPIView(RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete", "head", "options"]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = QuestionVoteSerializer

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        super().initial(request, *args, **kwargs)
        self.question = get_object_or_404(
            Question, pk=self.kwargs.get("question_pk")
        )

    def get_queryset(self):
        return QuestionVote.objects.filter(to=self.question).select_related("user")


class AnswersAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AnswerSerializer

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        super().initial(request, *args, **kwargs)
        self.question = get_object_or_404(Question, pk=self.kwargs.get("pk"))

    def get_queryset(self):
        return Answer.objects.all().filter(question=self.question) \
            .order_by("-is_accepted", "-rating", "-posted")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, question=self.question)


class AnswerDetailsAPIView(RetrieveUpdateAPIView):
    http_method_names = ["get", "patch", "head", "options"]
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOfQuestionOrReadOnly,
    ]
    serializer_class = AnswerDetailSerializer

    def get_queryset(self):
        return Answer.objects.all().select_related("author")

    def perform_update(self, serializer):
        """ Mark / unmark answer as accepted one
        """
        answer = serializer.instance
        is_accepted_new = serializer.validated_data["is_accepted"]
        # Do nothing if `is_accepted` is not changed
        if answer.is_accepted == is_accepted_new:
            return
        if is_accepted_new:
            answer.mark()
        else:
            answer.unmark()


class AnswerVotesAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AnswerVoteSerializer

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        super().initial(request, *args, **kwargs)
        self.answer = get_object_or_404(Answer, pk=self.kwargs.get("pk"))

    def get_queryset(self):
        return AnswerVote.objects.all().select_related("user").filter(to=self.answer)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, to=self.answer)


class AnswerVoteDetailsAPIView(RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "patch", "delete", "head", "options"]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = AnswerVoteSerializer

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        super().initial(request, *args, **kwargs)
        self.answer = get_object_or_404(Answer, pk=self.kwargs.get("answer_pk"))

    def get_queryset(self):
        return AnswerVote.objects.filter(to=self.answer).select_related("user")
