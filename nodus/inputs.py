from typing import TypeVar
from InquirerPy.prompts.checkbox import CheckboxPrompt
from InquirerPy.prompts.confirm import ConfirmPrompt
from InquirerPy.prompts.input import InputPrompt
from InquirerPy.prompts.list import ListPrompt
from InquirerPy.prompts.number import NumberPrompt
from InquirerPy.validator import EmptyInputValidator
from rich.console import Console


console = Console()
T = TypeVar("T")


def get_text(prompt: str) -> str:
    """Global function that prompts the user for text and ensures it is not left blank."""

    text: str = InputPrompt(
        message=prompt,
        validate=EmptyInputValidator("[!] The field cannot be left blank!")).execute()
    return text


def get_number(prompt: str, minimum: int = 1, maximum: int = 100) -> int:
    """Global function that requests an integer within a specified valid range."""

    number = NumberPrompt(
        message=prompt,
        min_allowed=minimum,
        max_allowed=maximum,
        default=minimum,
        validate=EmptyInputValidator("[!] The field cannot be left blank!"),
        invalid_message=f"[yellow][!] Enter a number between {minimum} and {maximum}![/yellow]").execute()

    return int(number)


def get_boolean(prompt: str, value: bool = True) -> bool:
    """Global function that requests a simple "yes" or "no" response."""

    booleano: bool = ConfirmPrompt(
        message=prompt,
        default=value,
        confirm_letter="y",
        reject_letter="n").execute()

    return booleano


def get_single_option(prompt: str, options: list[T]) -> T:
    """Global function that displays a single-selection list."""

    alternative: T = ListPrompt(
        message=prompt,
        choices=options,
        default=options[0] if options else None).execute()

    return alternative


def get_multiple_options(prompt: str, options: list[T]) -> list[T]:
    """Global function that displays a multiple-choice list with checkboxes."""

    alternative: list[T] = CheckboxPrompt(
        message=prompt,
        choices=options,
        validate=lambda resultado: len(resultado) > 0,
        invalid_message="[yellow][!] Select at least one option.![/yellow]").execute()

    return alternative