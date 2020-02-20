# -*- coding: utf-8 -*-
import os
import json
import copy

import common

def gen_mid_json(json_value):
    def make_tree(conf_dict, children, traces):
        if conf_dict.get(common.leaf_value):
            common.sort_condition(children)
            children.append("value=" + conf_dict[common.leaf_value])
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
    def safe_get_dict_value(dict_, key_, default_):
        v_ = dict_.get(key_, default_)
        dict_[key_] = v_
        return dict_[key_]

    json_value = {} 
    for trace in tree_nodes:
        sub_dict_ = json_value
        for node in trace[:-1]:
            sub_dict_ = safe_get_dict_value(sub_dict_, node, {})
        sub_dict_[common.leaf_value] = trace[-1] 
    print json.dumps(tree_nodes)
    print json.dumps(json_value)
    pass

if __name__ == '__main__':
    key = "demo"
    json_value = json.loads(file(common.key_conf_path + key + ".json").read())
    traces = gen_mid_json(json_value)
    mid_file = common.key_conf_path + "." + key + ".mid.json"
    file(mid_file, "w").write(json.dumps(traces))
    json_value = json.loads(file(mid_file).read())
    mid_to_json(json_value)
