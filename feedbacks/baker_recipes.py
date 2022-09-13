from model_bakery.recipe import Recipe

from feedbacks.models import Feedback

feedback_test = Recipe(
    Feedback,
    feedback="Eu sou um feedback",
    rate=8,
)
