from datetime import date
from platform import platform, python_version
from sys import argv, gettrace
from textwrap import fill

from teletype import VERSION as teletype_version

from stonky.__version__ import VERSION
from stonky.enums import SortType

IS_DEBUG = gettrace() is not None
SYSTEM = {
    "date": date.today(),
    "platform": platform(),
    "arguments": argv[1:],
    "python version": python_version(),
    "stonky version": VERSION,
    "teletype version": teletype_version,
}

EPILOG = fill(
    f"""FIELDS can be one of {", ".join(SortType.arg_choices())}.

Visit https://github.com/jkwill87/stonky for more information.
""",
    80,
)
