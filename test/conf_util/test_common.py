import unittest

from src.conf_util import common

class Test(unittest.TestCase):
    def test_sort_condition(self):
        node_info=['m=1', 'b=1', common.default_node]
        common.sort_condition(node_info)
        self.assertEqual(node_info, ['b=1', 'm=1', common.default_node])
        node_info=['m=1', common.default_node, 'b=1']
        common.sort_condition(node_info)
        self.assertEqual(node_info, ['b=1', 'm=1', common.default_node])
        node_info=[common.default_node, 'm=1', 'b=1']
        common.sort_condition(node_info)
        self.assertEqual(node_info, ['b=1', 'm=1', common.default_node])

    def test_sort_condition_2(self):
        node_info=['m=1', 'b=1']
        common.sort_condition(node_info)
        self.assertEqual(node_info, ['b=1', 'm=1'])

    def test_sort_condition_3(self):
        node_info=['b=1', 'm=1']
        common.sort_condition(node_info)
        self.assertEqual(node_info, ['b=1', 'm=1'])

    def test_sort_condition_4(self):
        node_info=['m=1', common.default_node]
        common.sort_condition(node_info)
        self.assertEqual(node_info, ['m=1', common.default_node])
