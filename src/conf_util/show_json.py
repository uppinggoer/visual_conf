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

def gen_show_json(json_value):
    def make_tree(conf_dict, children):
        if conf_dict.get(common.leaf_value):
            children.append({
                "name": conf_dict[common.leaf_value], 
                "symbol":'rect', 
                "symbolSize":30, 
                "label": {"rotate": 0, "align": "center", "fontSize": 10,},
            })
            return
        
        for key in common.sort_condition(conf_dict.keys()):
            traces = {
                "name":key, 
                "children":[],
                "symbolSize":10, 
                "label": {"rotate": 0, "align": "center", "fontSize": 10},
            }
            make_tree(conf_dict[key], traces["children"])
            children.append(traces)

    traces = {"name":"", "children":[]}
    make_tree(copy.deepcopy(json_value), traces["children"])
    return traces

if __name__ == '__main__':
    key = "demo"
    write_show_conf(key, gen_show_json(read_conf(key)))
