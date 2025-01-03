import pytest
from app import (
    evaluate_expression,
    InvalidExpressionException,
    ERROR_EMPTY_EXPRESSION,
    ERROR_MISMATCHED_PARENTHESES,
    ERROR_INVALID_OPERATOR,
    ERROR_INVALID_STRUCTURE,
    ERROR_DIVISION_BY_ZERO,
)

@pytest.mark.parametrize(
    "expression, expected_result",
    [
        ("5 + 3", 8),
        ("10 - 7", 3),
        ("4 * 6", 24),
        ("20 / 4", 5.0),
        ("5 + 3 * 2", 11),
        ("(5 + 3) * 2", 16),
        ("// comment // 5 + 3 // comment //", 8),
        ("10 // some comment // - 2", 8),
        ("(4 + 6) // comment // * 2", 20),
    ]
)
def test_valid_expressions(expression, expected_result):
    assert evaluate_expression(expression) == expected_result


@pytest.mark.parametrize(
    "expression, expected_exception, error_message",
    [
        ("5 +", InvalidExpressionException, ERROR_INVALID_STRUCTURE),
        ("5 // missing operand", InvalidExpressionException, ERROR_INVALID_STRUCTURE),
        ("(5 + 3", InvalidExpressionException, ERROR_MISMATCHED_PARENTHESES),
        ("5 + 3)", InvalidExpressionException, ERROR_MISMATCHED_PARENTHESES),
        ("10 / 0", InvalidExpressionException, ERROR_DIVISION_BY_ZERO),
        ("5 + 3 & 2", InvalidExpressionException, ERROR_INVALID_OPERATOR.format("&")),
        ("// only comment //", InvalidExpressionException, ERROR_EMPTY_EXPRESSION),
        ("", InvalidExpressionException, ERROR_EMPTY_EXPRESSION),
    ]
)
def test_invalid_expressions(expression, expected_exception, error_message):
    with pytest.raises(expected_exception) as exif:
        evaluate_expression(expression)
    assert str(exif.value) == error_message
