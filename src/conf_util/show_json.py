# -*- coding: utf-8 -*-
import os
import json
import copy
import common

def read_conf(key):
    json_value = json.loads(file(common.key_conf_path + key + ".json").read())
    return json_value

def write_show_conf(key, traces):
    file(common.key_conf_path + "." + key + ".js", "w").write("var data=" + json.dumps(traces))

def gen_show_json(json_value, condition_list=[]):
    def make_tree(conf_dict, condition_label, children):
        if conf_dict.get(common.leaf_value):
            # 可以优化下，同一个节点所有孩子值一样  化简展示
            #
            # old_value = "m1"
            # new_value = "m1a2"
            # res = make_append_tree("m=1", "a!=2", old_value, new_value)
            # condition_list = ["a", "m"]
            # res = middle_json.mid_to_json(middle_json.gen_mid_json(res, condition_list))
            # show_json.write_show_conf("demo", show_json.gen_show_json(res, condition_list))

            children.append({
                "id": common.leaf_value,
                "name": conf_dict[common.leaf_value], 
                "symbol":'rect', 
                "symbolSize":30, 
                "label": {"rotate": 0, "align": "center", "fontSize": 10,},
            })
            return
        
        for key in common.sort_condition(conf_dict.keys(), condition_list):
            condition_label_ = copy.deepcopy(condition_label)
            condition_label_.append(key)
            traces = {
                "name":key, 
                "id": common.join_condition(condition_label_),
                "children":[],
                "symbolSize":10, 
                "label": {"rotate": 0, "align": "center", "fontSize": 10},
            }
            make_tree(conf_dict[key], condition_label_, traces["children"])
            children.append(traces)

    traces = {"name":"", "children":[]}
    make_tree(copy.deepcopy(json_value), [], traces["children"])
    return traces

if __name__ == '__main__':
    key = "demo"
    write_show_conf(key, gen_show_json(read_conf(key)))
