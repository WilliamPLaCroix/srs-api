import pytest


def test_review_imports():
    import app.modules.reviews.schemas
    #import app.modules.reviews.services
    #import app.modules.reviews.create
    #import app.modules.reviews.api
    #import app.modules.reviews.db


from app.modules.reviews.schemas import ReviewSchema
def test_review_schema_can_be_instantiated():
    review = ReviewSchema()
    assert review is not None


def test_review_schema_fields():
    review = ReviewSchema(card_id=1, rating=5)
    assert review.card_id == 1
    assert review.rating == 5

# from app.modules.reviews.create import create_review
# def test_create_review_function_exists():
#     assert callable(create_review)