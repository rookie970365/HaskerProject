from itertools import combinations, islice
from string import ascii_lowercase
from typing import NamedTuple

from django.test import SimpleTestCase

from questions.forms import AskForm, VoteForm
from questions.models import Answer, Question
from .fixtures import DataSetupMixin

MAX_TAGS = 3
MAX_TITLE_LENGTH = 255


def random_tags(n: int) -> str:
    """ Generate comma-separated `n` tags.
    """
    items = ("".join(i) for i in combinations(ascii_lowercase, 3))
    return ", ".join(islice(items, n))


class AskFormCase(NamedTuple):
    title: str
    content: str
    tags: str


class TestAskForm(SimpleTestCase):
    invalid_cases = [
        AskFormCase(title="", content="", tags=""),
        AskFormCase(title=" ", content=" ", tags=" "),
        AskFormCase(title="title", content=" ", tags=" "),
        AskFormCase(title=" ", content="content", tags=" "),
        AskFormCase(title=" ", content=" ", tags="tags"),
        AskFormCase(
            title="a" * (MAX_TITLE_LENGTH + 1),
            content="content",
            tags="tags",
        ),
    ]

    def test_invalid_form(self):
        for case in self.invalid_cases:
            with self.subTest(case=case):
                form = AskForm(data=case._asdict())
                self.assertFalse(form.is_valid())

    def test_number_of_tags(self):
        data = {"title": "forms", "content": "how to django forms?", "tags": "python"}
        form = AskForm(data)
        self.assertTrue(form.is_valid())

        data["tags"] = random_tags(MAX_TAGS + 1)
        form = AskForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("tags", form.errors)

        data["tags"] = ["xyz"] * (MAX_TAGS + 1)
        form = AskForm(data)
        self.assertTrue(form.is_valid())


class TestVoteForm(DataSetupMixin):
    def test_vote_for_answer(self):
        data = {"target_id": self.answer_1.pk, "value": 1}
        form = VoteForm(data=data, model=Answer)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["target"].pk, self.answer_1.pk)

        data["value"] = -1
        form = VoteForm(data=data, model=Answer)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["target"].pk, self.answer_1.pk)

        data["value"] = 0
        form = VoteForm(data=data, model=Answer)
        self.assertFalse(form.is_valid())
        self.assertIn("value", form.errors)

    def test_vote_for_question(self):
        data = {"target_id": self.question.pk, "value": 1}
        form = VoteForm(data=data, model=Question)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["target"].pk, self.question.pk)

        data["value"] = -1
        form = VoteForm(data=data, model=Question)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["target"].pk, self.question.pk)

        data["value"] = 0
        form = VoteForm(data=data, model=Question)
        self.assertFalse(form.is_valid())
        self.assertIn("value", form.errors)
