# -*- coding: utf-8 -*-
import os
import json
import copy

import common

def gen_mid_json(json_value, condition_list):
    def make_tree(conf_dict, children, traces):
        if conf_dict.get(common.leaf_value):
            common.sort_condition(children, condition_list)
            children.append(conf_dict[common.leaf_value])
            traces.append(children)
            return

        for k_, v_ in conf_dict.items():
            children_ = copy.deepcopy(children)
            children_.append(k_)
            make_tree(v_, children_, traces)

    traces = []
    make_tree(copy.deepcopy(json_value), [], traces)
    return traces

def mid_to_json(tree_nodes):
    json_value = {} 
    for trace in tree_nodes:
        sub_dict_ = json_value
        for node in trace[:-1]:
            sub_dict_ = common.safe_get_dict_value(sub_dict_, node, {})
        sub_dict_[common.default_node] = {common.leaf_value: trace[-1]} 
    common.fix_default_value(json_value)
    return json_value

if __name__ == '__main__':
    key = "demo"
    file_path = common.key_conf_path + key + ".json"
    json_value = json.loads(file(file_path).read())
    condition_list = ["b", "m", "a"]
    traces = gen_mid_json(json_value, condition_list)
    json_value = mid_to_json(traces)
    import show_json
    show_json.write_show_conf("demo", show_json.gen_show_json(json_value, condition_list))
