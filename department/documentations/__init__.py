
from collections import namedtuple

Documentation = namedtuple(
    "Documentation",
    ["request", "responses", "parameters"],
    defaults=[None, None, None]
)
