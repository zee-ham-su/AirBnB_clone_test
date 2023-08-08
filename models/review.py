#!/usr/bin/python3
"""
Definition of the review class
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class, representing a review for a place.

    Attributes:
        place_id (str): The ID of the place being reviewed (Place ID).
        user_id (str): The ID of the user who wrote the review
        (User ID).
        text (str): The content of the review.
    """

    place_id = ""
    user_id = ""
    text = ""
