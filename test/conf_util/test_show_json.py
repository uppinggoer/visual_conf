import unittest

from src.conf_util import condition,common

class Test(unittest.TestCase):
    def test_make_condition(self):
        node_id = "a=1&&default"
        conds = "b=2"
        conds = "b=2&&a=1"
        conds = "b=2&&m=1&&default"

    def test_make_condition2(self):
        node_id = "a=1"
        conds = "b!=2&&c=1"
        conds = "b!=2&&c!=1"

    def test_make_condition3(self):
        node_id = "a=1&&default"
        conds = "b=2||b=2&&a=1"
        conds = "b=2&&a=1||b=2&&m=1"