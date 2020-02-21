import unittest

from src.conf_util import common

condition_list = ["m", "b"]

class Test(unittest.TestCase):
    def test_sort_condition(self):
        node_info=['b=1', 'm=1', common.default_node]
        common.sort_condition(node_info, condition_list)
        self.assertEqual(node_info, ['m=1', 'b=1', common.default_node])
        node_info=['b=1', common.default_node, 'm=1']
        common.sort_condition(node_info, condition_list)
        self.assertEqual(node_info, ['m=1', 'b=1', common.default_node])
        node_info=[common.default_node, 'b=1', 'm=1']
        common.sort_condition(node_info, condition_list)
        self.assertEqual(node_info, ['m=1', 'b=1', common.default_node])

    def test_sort_condition_2(self):
        node_info=['b=1', 'm=1']
        common.sort_condition(node_info, condition_list)
        self.assertEqual(node_info, ['m=1', 'b=1'])

    def test_sort_condition_3(self):
        node_info=['m=1', 'b=1']
        common.sort_condition(node_info, condition_list)
        self.assertEqual(node_info, ['m=1', 'b=1'])

    def test_sort_condition_4(self):
        node_info=['m=1', common.default_node]
        common.sort_condition(node_info, condition_list)
        self.assertEqual(node_info, ['m=1', common.default_node])

class ConditionSymbleTest(unittest.TestCase):
    def test_split_or_condition(self):
        cond = "a=1"
        self.assertEqual(common.ConditionSymble.split_or_condition(cond), [cond])

        cond = "a=1&&b=1"
        self.assertEqual(common.ConditionSymble.split_or_condition(cond), [cond])

        cond = "a=1||b=1"
        self.assertEqual(common.ConditionSymble.split_or_condition(cond), cond.split("||"))

        cond = "   a=1 || b=1 "
        self.assertEqual(common.ConditionSymble.split_or_condition(cond), ["a=1", "b=1"])

    def test_split_or_condition2(self):
        # cond = "a!=1||b=1"
        # cond_res = "a!=1||b=1||a=1&&b=1"
        # self.assertEqual(common.ConditionSymble.split_or_condition(cond), cond_res.split("||"))

        cond = "a!=1&&c!=1||b!=1&&d!=1||m!=1&&n!=1"
        cond_res = set([
            'a!=1&&c!=1', 
            'b!=1&&d!=1', 
            'm!=1&&n!=1',
            'bin1&&a!=1&&c!=1', 
            'min1&&a!=1&&c!=1', 
            'din1&&a!=1&&c!=1', 
            'nin1&&a!=1&&c!=1', 
            'ain1&&b!=1&&d!=1', 
            'cin1&&b!=1&&d!=1', 
            'min1&&b!=1&&d!=1', 
            'nin1&&b!=1&&d!=1', 
            'ain1&&m!=1&&n!=1', 
            'cin1&&m!=1&&n!=1', 
            'bin1&&m!=1&&n!=1', 
            'din1&&m!=1&&n!=1', 
        ])
        self.assertEqual(set(common.ConditionSymble.split_or_condition(cond)), cond_res)




