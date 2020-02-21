import unittest

from test import util
from src.conf_util import middle_json, common

class Test(unittest.TestCase):
    def setUp(self):
        self.blank_tree = {
            "b=2": {
                "a=2": {
                    "default": {
                        "__value": "a2b2_"
                    },
                    "c=2": {
                        "__value": "a2b2c2"
                    },
                },
                "m=1": {
                    "c=2": {
                        "__value": "m1b2c2"
                    },
                }
            },
            "a=2": {
                "default": {
                    "__value": "a2_"
                }
            },
        }

    def test__merge_node_error(self):
        append_tree = {
            "b=2": {
                "a=2": {
                    "__value": "new"
                },
            },
        }

        util.assert_error(self, common.unvaile_append_nodes, lambda: middle_json._merge_node(self.blank_tree, append_tree))

    def test__merge_node(self):
        append_tree = {
            "b=2": {
                "a=2": {
                    "c=1": {
                        "__value": "new1"
                    },
                },
                "m=1": {
                    "c=2": {
                        "c=1": {
                            "__value": "new2"
                        },
                    },
                }
            },
            "a=2": {
                "c=2": {
                    "c=1": {
                        "__value": "new3"
                    },
                },
            }
        }
        expect_res = {
            "b=2": {
                "a=2": {
                    "default": {
                        "__value": "a2b2_"
                    },
                    "c=2": {
                        "__value": "a2b2c2"
                    },
                    "c=1": {
                        "__value": "new1"
                    }
                },
                "m=1": {
                    "c=2": {
                        "c=1": {
                            "__value": "new2"
                        },
                        "default": {
                            "__value": "m1b2c2"
                        }
                    },
                }
            },
            "a=2": {
                "c=2": {
                    "c=1": {
                        "__value": "new3"
                    },
                },
                "default": {
                    "__value": "a2_"
                }
            },
        }
        middle_json._merge_node(self.blank_tree, append_tree)
        self.assertEqual(self.blank_tree, expect_res)
        