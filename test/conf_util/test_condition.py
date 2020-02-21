import unittest

from src.conf_util import condition,common

class Test(unittest.TestCase):
    def test__analyze_condition(self):
        conds = "b=2"
        expect_res = [(condition.NEW_condition, 'b=2')]
        res = condition._analyze_condition(conds)
        self.assertEqual(res, expect_res)

    def test__analyze_condition2(self):
        conds = "b!=2"
        expect_res = [
            (condition.OLD_condition, 'b=2'),
            (condition.NEW_condition, common.default_node)
        ]
        res = condition._analyze_condition(conds)
        self.assertEqual(res, expect_res)

    def test__analyze_condition3(self):
        conds = "b in 2"
        expect_res = [
            (condition.NEW_condition, 'b=2')
        ]
        res = condition._analyze_condition(conds)
        self.assertEqual(res, expect_res)

        conds = "b in 2,3,4"
        expect_res = [
            (condition.NEW_condition, 'b=2'),
            (condition.NEW_condition, 'b=3'),
            (condition.NEW_condition, 'b=4'),
        ]
        res = condition._analyze_condition(conds)
        self.assertEqual(res, expect_res)

    def test__analyze_condition4(self):
        conds = "b not-in 2"
        expect_res = [
            (condition.NEW_condition, common.default_node),
            (condition.OLD_condition, 'b=2')
        ]
        res = condition._analyze_condition(conds)
        self.assertEqual(res, expect_res)

        conds = "b not-in 2,3,4"
        expect_res = [
            (condition.NEW_condition, common.default_node),
            (condition.OLD_condition, 'b=2'),
            (condition.OLD_condition, 'b=3'),
            (condition.OLD_condition, 'b=4'),
        ]
        res = condition._analyze_condition(conds)
        self.assertEqual(res, expect_res)

    def test__join_sub_multi(self):
        conds = [
            [
                (condition.NEW_condition, 'a=1')
            ],
            [
                (condition.NEW_condition, 'b=1')
            ],
        ]
        expect_res = [
            (condition.NEW_condition, ["a=1", "b=1"]),
        ]
        res = condition._join_sub_multi(conds)
        self.assertEqual(res, expect_res)

    def test__join_sub_multi2(self):
        conds = [
            [
                (condition.OLD_condition, 'a=1'),
                (condition.NEW_condition, 'a=2'),
                (condition.NEW_condition, 'a=3'),
            ],
            [
                (condition.OLD_condition, 'b=1'),
                (condition.NEW_condition, 'b=2'),
            ],
            [
                (condition.OLD_condition, 'c=1'),
                (condition.NEW_condition, 'c=2'),
            ],
        ]
        expect_res = [
            (condition.OLD_condition, ["a=1", "b=1", "c=1"]),
            (condition.OLD_condition, ["a=1", "b=1", "c=2"]),
            (condition.OLD_condition, ["a=1", "b=2", "c=1"]),
            (condition.OLD_condition, ["a=1", "b=2", "c=2"]),

            (condition.OLD_condition, ["a=2", "b=1", "c=1"]),
            (condition.OLD_condition, ["a=3", "b=1", "c=1"]),
            (condition.OLD_condition, ["a=2", "b=1", "c=2"]),
            (condition.OLD_condition, ["a=3", "b=1", "c=2"]),

            (condition.OLD_condition, ["a=2", "b=2", "c=1"]),
            (condition.OLD_condition, ["a=3", "b=2", "c=1"]),
            (condition.NEW_condition, ["a=2", "b=2", "c=2"]),
            (condition.NEW_condition, ["a=3", "b=2", "c=2"]),
        ]
        res = condition._join_sub_multi(conds)
        self.assertEqual(sorted(res), sorted(expect_res))

    def test_make_none_condition(self):
        node_id = "a=1&&default"
        conds = ""
        expect_res = []
        res = condition._make_conditions(node_id, conds)
        self.assertEqual(res, expect_res)

        node_id = ""
        conds = ""
        res = condition._make_conditions(node_id, conds)
        self.assertEqual(res, expect_res)

        node_id = "default"
        res = condition._make_conditions(node_id, conds)
        self.assertEqual(res, expect_res)

        conds = "m=1"
        expect_res = [('N', ['m=1'])]
        res = condition._make_conditions(node_id, conds)
        self.assertEqual(res, expect_res)

        node_id = ""
        expect_res = [('N', ['m=1'])]
        res = condition._make_conditions(node_id, conds)
        self.assertEqual(res, expect_res)


    def test_make_condition(self):
        node_id = "a=1&&default"
        conds = "b=2"
        expect_res = [(condition.NEW_condition, ['a=1', 'b=2'])]
        res = condition._make_conditions(node_id, conds)
        self.assertEqual(res, expect_res)

        conds = "b=2&&a=1"
        res = condition._make_conditions(node_id, conds)
        self.assertEqual(res, expect_res)

        conds = "b=2&&m=1"
        expect_res = [('N', ['a=1', 'b=2', 'm=1'])]
        res = condition._make_conditions(node_id, conds)
        self.assertEqual(res, expect_res)

        conds = "b=2&&m=1&&default"
        expect_res = [('N', ['a=1', 'b=2', 'm=1'])]
        res = condition._make_conditions(node_id, conds)
        self.assertEqual(res, expect_res)

    def test_make_condition2(self):
        node_id = "a=1"
        conds = "b!=2&&c=1"
        expect_res = [
            (condition.OLD_condition, ['a=1', 'b=2', 'c=1']),
            (condition.NEW_condition, ['a=1', 'c=1', 'default']),
        ]
        res = condition._make_conditions(node_id, conds)
        self.assertEqual(res, expect_res)
        
        conds = "b!=2&&c!=1"
        expect_res = [
            ('O', ['a=1', 'c=1', 'default']), 
            ('O', ['a=1', 'b=2', 'c=1']), 
            ('O', ['a=1', 'b=2', 'default']), 
            ('N', ['a=1', 'default']),
        ]
        res = condition._make_conditions(node_id, conds)
        self.assertEqual(res, expect_res)

    def test_make_condition3(self):
        node_id = "a=1&&default"
        conds = "b=2||b=2&&a=1"
        expect_res = [('N', ['a=1', 'b=2'])]
        res = condition._make_conditions(node_id, conds)
        self.assertEqual(res, expect_res)

        conds = "b=2&&a=1||b=2&&m=1"
        expect_res = [('N', ['a=1', 'b=2']), ('N', ['a=1', 'b=2', 'm=1'])]
        res = condition._make_conditions(node_id, conds)
        self.assertEqual(res, expect_res)

        conds = "a=5"
        # condition._make_conditions(node_id, conds)
        self.assertRaises(AssertionError, condition._make_conditions, node_id, conds)

        conds = "b=2&&m=1&&default||m=3&&b=4||a=5"
        # condition._make_conditions(node_id, conds)
        self.assertRaises(AssertionError, condition._make_conditions, node_id, conds)

    
    def test__make_append_tree(self):
        old_value = "m1_"
        new_value = "m1a1"

        conditions = ["N", ("m=1", "a=1")]
        expect_res = {
            "default": {"__value": "m1_"},
            "m=1": {
                "a=1": {
                    "__value": "m1a1"
                },
                "default": {"__value": "m1_"}
            }
        }
        res = condition._make_append_tree(old_value, [conditions], new_value)
        self.assertEqual(res, expect_res)

        conditions = ["N", ("m=1", "a=1", "default")]
        expect_res = {
            "default": {"__value": "m1_"},
            "m=1": {
                "a=1": {
                    "__value": "m1a1"
                },
                "default": {"__value": "m1_"}
            }
        }
        res = condition._make_append_tree(old_value, [conditions], new_value)
        self.assertEqual(res, expect_res)

        conditions = ["N", ("m=1", "a=1", "default", "default")]
        expect_res = {
            "default": {"__value": "m1_"},
            "m=1": {
                "a=1": {
                    "__value": "m1a1"
                },
                "default": {"__value": "m1_"}
            }
        }
        res = condition._make_append_tree(old_value, [conditions], new_value)
        self.assertEqual(res, expect_res)

    def test__make_append_tree2(self):
        old_value = "m1_"
        conditions = ["N", ("m=1", "a=1", "b=1")]
        new_value = "m1a1b1"

        expect_res = {
            "default": {"__value": "m1_"},
            "m=1": {
                "a=1": {
                "default": {"__value": "m1_"},
                "b=1": {
                    "__value": "m1a1b1"
                }
                },
                "default": {"__value": "m1_"}
            }
        }
        res = condition._make_append_tree(old_value, [conditions], new_value)
        self.assertEqual(res, expect_res)

    def test__make_append_tree3(self):
        old_value = "m1_"
        conditions = [
            ["N", ("m=1", "a=1", "b=1")],
            ["N", ("m=1", "b=1")],
            ["N", ("m=1", "a=2", "b=3")],
        ]
        new_value = "m1a1b1"

        expect_res = {
            "default": {
                "__value": "m1_"
            },
            "m=1": {
                "a=1": {
                "default": {
                    "__value": "m1_"
                },
                "b=1": {
                    "__value": "m1a1b1"
                }
                },
                "a=2": {
                "default": {
                    "__value": "m1_"
                },
                "b=3": {
                    "__value": "m1a1b1"
                }
                },
                "default": {
                "__value": "m1_"
                },
                "b=1": {
                "__value": "m1a1b1"
                }
            }
        }
        res = condition._make_append_tree(old_value, conditions, new_value)
        self.assertEqual(res, expect_res)

    def test__make_append_tree4(self):
        old_value = "m1_"
        conditions = [
            ["N", ("m=1", "a=1", "b=1")],
            ["N", ("m=1", "b=1")],
            ["O", ("m=1", "a=2", "b=3")],
        ]
        new_value = "m1a1b1"

        expect_res = {
            "default": {
                "__value": "m1_"
            },
            "m=1": {
                "a=1": {
                "default": {
                    "__value": "m1_"
                },
                "b=1": {
                    "__value": "m1a1b1"
                }
                },
                "a=2": {
                "default": {
                    "__value": "m1_"
                },
                "b=3": {
                    "__value": "m1_"
                }
                },
                "default": {
                "__value": "m1_"
                },
                "b=1": {
                "__value": "m1a1b1"
                }
            }
        }
        res = condition._make_append_tree(old_value, conditions, new_value)
        self.assertEqual(res, expect_res)
    
    def test_make_append_tree(self):
        res = condition.make_append_tree("", "m=1", "old", "m1")
        expect_res = {
            "default": {"__value": "old"}, 
            "m=1": {"__value": "m1"}
        }
        self.assertEqual(res, expect_res)

    def test_make_append_tree2(self):
        res = condition.make_append_tree("m=1", "a=2", "m1", "m1a2")
        expect_res = {
            "default": {"__value": "m1"}, 
            "a=2": {
                "default": {"__value": "m1"}, 
                "m=1": {"__value": "m1a2"}
            }
        } 
        self.assertEqual(res, expect_res)

    def test_make_append_tree3(self):
        res = condition.make_append_tree("m=1", "a=2&&b=3", "m1", "m1a2b3")
        expect_res = {
            "default": {"__value": "m1"}, 
            "b=3": {
                "default": {"__value": "m1"}, 
                "a=2": {
                    "default": {"__value": "m1"}, 
                    "m=1": {"__value": "m1a2b3"}
                }
            }
        } 
        self.assertEqual(res, expect_res)
    
    def test_make_append_tree4(self):
        res = condition.make_append_tree("m=1", "a=2||b=3", "m1", "m1a2b3")
        expect_res = {
            'default': {'__value': 'm1'}, 
            'b=3': {
                'default': {'__value': 'm1'}, 
                'm=1': {'__value': 'm1a2b3'}
            }, 
            'a=2': {
                'default': {'__value': 'm1'}, 
                'm=1': {'__value': 'm1a2b3'}
            }
        } 
        self.assertEqual(res, expect_res)
    
    def test_make_append_tree5(self):
        res = condition.make_append_tree("m=1", "a!=2", "m1", "m1a2")
        expect_res = {
            "default": {"__value": "m1"}, 
            "a=2": {
                "default": {"__value": "m1"}, 
                "m=1": {"__value": "m1"}
            }, 
            "m=1": {"__value": "m1a2"}
        } 
        self.assertEqual(res, expect_res)
     
    def test_make_append_tree6(self):
        res = condition.make_append_tree("m=1", "a!=2&&b=2", "m1", "m1a2b2")
        expect_res = {
            "b=2": {
                "default": {
                "__value": "m1"
                },
                "a=2": {
                "default": {
                    "__value": "m1"
                },
                "m=1": {
                    "__value": "m1"
                }
                },
                "m=1": {
                "__value": "m1a2b2"
                }
            },
            "default": {
                "__value": "m1"
            }
        } 
        self.assertEqual(res, expect_res)
    
    def test_make_append_tree7(self):
        res = condition.make_append_tree("m=1", "a!=2||b=2", "m1", "m1a2b2")
        expect_res = {
            "b=2": {
                "default": {"__value": "m1"}, 
                "a=2": {
                    "default": {"__value": "m1"}, 
                    "m=1": {"__value": "m1a2b2"}
                }, 
                "m=1": {"__value": "m1a2b2"}
            }, 
            "default": {"__value": "m1"}, 
            "a=2": {
                "default": {"__value": "m1"}, 
                "m=1": {"__value": "m1"}
            }, 
            "m=1": {"__value": "m1a2b2"}
        } 
        self.assertEqual(res, expect_res)

    def test_make_append_tree8(self):
        res = condition.make_append_tree("m=1", "a!=2||b=2||a=2&&b=2", "m1", "m1a2b2")
        expect_res = {
            "b=2": {
                "default": {"__value": "m1"}, 
                "a=2": {
                    "default": {"__value": "m1"}, 
                    "m=1": {"__value": "m1a2b2"}
                }, 
                "m=1": {"__value": "m1a2b2"}
            }, 
            "default": {"__value": "m1"}, 
            "a=2": {
                "default": {"__value": "m1"}, 
                "m=1": {"__value": "m1"}
            }, 
            "m=1": {"__value": "m1a2b2"}
        } 
        self.assertEqual(res, expect_res)
