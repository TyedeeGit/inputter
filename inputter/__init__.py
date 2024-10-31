"""
A library for user input processing.
"""
from .condition import (Condition, int_condition, float_condition, gt_condition, ge_condition, lt_condition,
                        le_condition, eq_condition, contains_condition, range_condition, nonempty_condition, null_condition)
from .inputter import Inputter, yes_no_inputter
from .handler import Handler
