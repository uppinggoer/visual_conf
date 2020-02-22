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
    common.fix_default_value(json_value)
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

def _merge_node(origin_tree_, append_tree_):
    for k, sub_tree in append_tree_.items():
        sub_dict_ = common.safe_get_dict_value(origin_tree_, k, {})
        if sub_tree.get(common.leaf_value):
            assert sub_dict_.keys() in [[], [common.leaf_value]], common.unvaile_append_nodes
            sub_dict_[common.leaf_value] = sub_tree[common.leaf_value]
            continue

        if sub_dict_.get(common.leaf_value):
            t_ = sub_dict_[common.leaf_value]
            del sub_dict_[common.leaf_value]
            # default 值发生变化 ！！！！
            sub_dict_[common.default_node] = {common.leaf_value: t_}

        _merge_node(sub_dict_, sub_tree)

def insert_node(origin_tree, append_tree, old_value):
    _merge_node(origin_tree, append_tree)
    common.fill_default_value(origin_tree, old_value)
    common.fix_default_value(origin_tree)
    return origin_tree

if __name__ == '__main__':
    key = "demo"
    file_path = common.key_conf_path + key + ".json"
    json_value = json.loads(file(file_path).read())
    # print json.dumps(json_value)
    condition_list = ["b", "m", "a"]
    traces = gen_mid_json(json_value, condition_list)
    json_value = mid_to_json(traces)
    import show_json
    show_json.write_show_conf("demo", show_json.gen_show_json(json_value, condition_list))
    # insert_node({}, {}, 0)
