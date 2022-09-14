from django.test import TestCase
from model_bakery import baker


class FeedbacksTestModel(TestCase):
    @classmethod
    def setUp(cls):
        cls.feedback = baker.make_recipe("feedbacks.feedback_test")

    def test_fields_feedbacks(self):
        self.assertEqual(self.feedback.feedback, "Eu sou um feedback")
        self.assertEqual(self.feedback.rate, 8)

    def test_fields_wrong(self):
        self.assertNotEqual(self.feedback.feedback, "Eu não sou um feedback")
        self.assertNotEqual(self.feedback.rate, 9)
