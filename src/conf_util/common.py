# -*- coding: utf-8 -*-
import os
import json
import copy

leaf_value = "__value"
default_node = "default"
key_conf_path = os.path.abspath(os.path.dirname(__file__)) + "/../../keys/"

def sort_condition(node_info):
    # ["a=1", "b=1", "default"]
    if len(node_info) <= 0:
        return

    node_info_ = sorted([node for node in node_info if node != default_node])
    if len(node_info) > len(node_info_):
        node_info_.append(default_node)

    for idx, v in enumerate(node_info_):
        node_info[idx] = v

    return node_info

