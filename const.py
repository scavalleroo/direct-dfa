SYMBOLS = {
    "*": 4,
    ".": 3,
    "|": 2,
    "(": 1,
    ")": 1,
}

ERRORS = (
    # 0
    "Syntax error: missing matching brackets in regular expression",
    # 1
    "Syntax error: missing arguments in the | operator",
    # 2
    "Syntax error: empty regular expression",
    # 3
    "MISMATCH, the expression does not match the ending",
    # 4
    "The regular expression must end with the # terminator.\n"
    "Re-enter the expression",
    # 5
    "The regular expression must not contain the ‘.’ symbol.\n"
    "Re-enter the expression",
)
