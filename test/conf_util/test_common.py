import unittest

from src.conf_util.common import *

condition_list = ["m", "b"]

class Test(unittest.TestCase):
    def test_sort_condition(self):
        node_info=['b=1', 'm=1', default_node]
        sort_condition(node_info, condition_list)
        self.assertEqual(node_info, ['m=1', 'b=1', default_node])
        node_info=['b=1', default_node, 'm=1']
        sort_condition(node_info, condition_list)
        self.assertEqual(node_info, ['m=1', 'b=1', default_node])
        node_info=[default_node, 'b=1', 'm=1']
        sort_condition(node_info, condition_list)
        self.assertEqual(node_info, ['m=1', 'b=1', default_node])

    def test_sort_condition_2(self):
        node_info=['b=1', 'm=1']
        sort_condition(node_info, condition_list)
        self.assertEqual(node_info, ['m=1', 'b=1'])

    def test_sort_condition_3(self):
        node_info=['m=1', 'b=1']
        sort_condition(node_info, condition_list)
        self.assertEqual(node_info, ['m=1', 'b=1'])

    def test_sort_condition_4(self):
        node_info=['m=1', default_node]
        sort_condition(node_info, condition_list)
        self.assertEqual(node_info, ['m=1', default_node])

    def test_cut_by_default_value(self):
        json_value = {
            "a=1": {
                default_node: {leaf_value:1},
                "a=1": {leaf_value:1},
            },
            default_node: {
                default_node: {leaf_value:1},
                "a=1": {leaf_value:1},
            },
        }
        res = cut_by_default_value(json_value)
        expect_res = {
            default_node: {
                default_node: {leaf_value:1},
            }
        }
        self.assertEqual(res, expect_res)

    def test_cut_by_default_value2(self):
        json_value = {
            "a=1": {
                default_node: {leaf_value:1},
                "a=1": {leaf_value:1},
            },
            default_node: {
                default_node: {leaf_value:2},
                "a=1": {leaf_value:2},
            },
        }
        res = cut_by_default_value(json_value)
        expect_res = {
            default_node: {
                default_node: {leaf_value:2},
            },
            "a=1": {
                default_node: {leaf_value:1},
            }
        }
        self.assertEqual(res, expect_res)

    def test_cut_by_default_value3(self):
        json_value = {
            "a=1": {
                default_node: {leaf_value:1},
                "a=1": {
                    default_node: {leaf_value:2},
                    "a=1": {leaf_value:2},
                },
            },
            default_node: {
                default_node: {leaf_value:2},
                "a=1": {leaf_value:2},
            },
        }
        res = cut_by_default_value(json_value)
        expect_res = {
            default_node: {
                default_node: {leaf_value:2},
            },
            "a=1": {
                default_node: {leaf_value:1},
                "a=1": {
                    default_node: {leaf_value:2},
                },
            }
        }
        self.assertEqual(res, expect_res)

class ConditionSymbleTest(unittest.TestCase):
    def test_split_or_condition(self):
        cond = "a=1"
        self.assertEqual(ConditionSymble.split_or_condition(cond), [cond])

        cond = "a=1&&b=1"
        self.assertEqual(ConditionSymble.split_or_condition(cond), [cond])

        cond = "a=1||b=1"
        self.assertEqual(ConditionSymble.split_or_condition(cond), cond.split("||"))

        cond = "   a=1 || b=1 "
        self.assertEqual(ConditionSymble.split_or_condition(cond), ["a=1", "b=1"])

    def test_split_or_condition2(self):
        # cond = "a!=1||b=1"
        # cond_res = "a!=1||b=1||a=1&&b=1"
        # self.assertEqual(ConditionSymble.split_or_condition(cond), cond_res.split("||"))

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
        self.assertEqual(set(ConditionSymble.split_or_condition(cond)), cond_res)




