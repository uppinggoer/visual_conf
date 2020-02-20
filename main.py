# -*- coding: utf-8 -*-
import os
import json
import copy

node_id = "__node_id"
left_value = "__value"
key_conf_path = os.path.abspath(os.path.dirname(__file__)) + "/keys/"

def gen_mid_json(key):
    def make_tree(conf_dict, children, traces):
        conf_dict[node_id] = 0
        del conf_dict[node_id]
        if conf_dict.get(left_value):
            children.append("value=" + conf_dict[left_value])
            traces.append(children)
            return
        
        for key in [i[0] for i in sorted(conf_dict.items(), key=lambda x:x[1][node_id])]:
            children_ = copy.deepcopy(children)
            children_.append(key)
            make_tree(conf_dict[key], children_, traces)

    json_value = json.loads(file(key_conf_path + key + ".json").read())
    traces = []
    make_tree(copy.deepcopy(json_value), [], traces)
    return traces

def mid_to_json(json_value):
    print json.dumps(json_value)
    pass

def gen_show_json(key):
    def make_tree(conf_dict, children):
        conf_dict[node_id] = 0
        del conf_dict[node_id]
        if conf_dict.get(left_value):
            children.append({
                "name": conf_dict[left_value], 
                "symbol":'rect', 
                "symbolSize":30, 
                "label": {"rotate": 0, "align": "center", "fontSize": 10,},
            })
            return
        
        for key in [i[0] for i in sorted(conf_dict.items(), key=lambda x:x[1][node_id])]:
            traces = {
                "name":key, 
                "children":[],
                "symbolSize":10, 
                "label": {"rotate": 0, "align": "center", "fontSize": 10},
            }
            make_tree(conf_dict[key], traces["children"])
            children.append(traces)

    json_value = json.loads(file(key_conf_path + key + ".json").read())
    traces = {"name":"", "children":[]}
    make_tree(copy.deepcopy(json_value), traces["children"])

    file(key_conf_path + "." + key + ".js", "w").write("var data=" + json.dumps(traces))
    return json.dumps(traces)

def test_mid_json():
    key = "demo"
    traces = gen_mid_json(key)
    mid_file = key_conf_path + "." + key + ".mid.json"
    file(mid_file, "w").write(json.dumps(traces))
    json_value = json.loads(file(mid_file).read())
    mid_to_json(json_value)

if __name__ == '__main__':
    gen_show_json("demo")
    test_mid_json()
