"""This module tests the Text class."""

from behave import Given, When, Then
import pygame
from m1wengine.text import Text


@Given("pygame is initialized")
def create_text(context: any):
    """Initialize pygame.

    Parameters
    ----------
    context: any
        the retained context of this test
    """
    pygame.init()


@When("the word {text} is created at position {position}")
def when_text(context: any, position: str, text: str):
    """Create text with a given position and string.

    Parameters
    ----------
    context: any
        the retained context of this test
    text: str
        a string of the text to instantiate the object with
    position: str
        the coordinates in a tuple as a string
    """
    pos: list[int] = [int(i) for i in tuple(position) if i.isdigit()]
    x: int = pos[0]
    y: int = pos[1]
    context.created_text = Text(x, y, text)
    context.test_text = text
    context.x = x
    context.y = y


@Then("the string is correct")
def then_text(context: any):
    """Create text with a given string.

    Parameters
    ----------
    context: any
        the retained context of this test
    text: str
        a string of the text to instantiate the object with
    position: str
        the coordinates in a tuple as a string
    """
    resulting_text: str = context.created_text.text_string
    assert resulting_text == context.test_text


@Then("the position is correct")
def then_text(context: any):
    """Create text with a given position.

    Parameters
    ----------
    context: any
        the retained context of this test
    text: str
        a string of the text to instantiate the object with
    position: str
        the coordinates in a tuple as a string
    """
    resulting_x: int = context.created_text.rect.x
    resulting_y: int = context.created_text.rect.y
    assert resulting_x == context.x
    assert resulting_y == context.y
