# -*- coding: utf-8 -*-
import os
import json
import copy

# https://blog.csdn.net/qq_17034717/article/details/81942059
# class _const:
#     class ConstError(TypeError):pass
#     def __setattr__(self,name,value):
#         if name in self.__dict__:
#             raise self.ConstError("Can't rebind const (%s)" %name)
#         self.__dict__[name]=value
        
# import sys
# sys.modules[__name__]=_const()

leaf_value = "__value"
default_node = "default"
key_conf_path = os.path.abspath(os.path.dirname(__file__)) + "/../../keys/"

condition_conflict = "条件冲突"
unvaile_append_nodes = "子树不合法"

class ConditionSymble:
    assignment = "="
    negate = "!="
    assgin_set = "in"
    negate_set = "not-in"
    
    codintion_or = "||"
    codintion_and = "&&"
    set_join_op = ","

    @staticmethod
    def get_all_symble():
        return {
            ConditionSymble.assignment,
            ConditionSymble.negate,
            ConditionSymble.assgin_set,
            ConditionSymble.negate_set,
        }

    @staticmethod
    def _gen_negate_map(origin_sub_cons):
        negate_map = {}
        for idx, c in enumerate(origin_sub_cons):
            negate_map[idx] = {}
            for con in split_condition(c):
                c_pair = ConditionSymble.split_negate_condition(con)
                if len(c_pair) >= 2:
                    negate_map[idx][c_pair[0]] = c_pair[1]
                    continue

                c_pair = ConditionSymble.split_negate_set_condition(con)
                if len(c_pair) >= 2:
                    negate_map[idx][c_pair[0]] = c_pair[1]
                    continue
        return negate_map

    @staticmethod
    def _other_list_negates(negate_map, cur_idx):
        negates = {}
        for idx, v in negate_map.items():
            if idx == cur_idx:
                continue
            for k,v in v.items():
                negates[k] = negates.get(k, ",") + v
        return {k:",".join({i for i in v.split(",") if i}) for k,v in negates.items()}

    @staticmethod
    def split_or_condition(con):
        origin_sub_cons = ConditionSymble._do_split_condition(con, ConditionSymble.codintion_or)
        negate_map = ConditionSymble._gen_negate_map(origin_sub_cons)

        sub_cons = []
        for idx, con in enumerate(origin_sub_cons):
            negates = ConditionSymble._other_list_negates(negate_map, idx)
            for k, v in negates.items():
                sub_cons.append(k + ConditionSymble.assgin_set + v + ConditionSymble.codintion_and + con)
        sub_cons.extend(origin_sub_cons)
        return sub_cons

    @staticmethod
    def check_negate(con):
        if len(ConditionSymble.split_negate_condition(con)) >= 2:
            return True
        if len(ConditionSymble.split_negate_set_condition(con)) >= 2:
            return True


    @staticmethod
    def split_assignment_condition(con):
        c_pair = ConditionSymble._do_split_condition(con, ConditionSymble.assignment)
        assert len(c_pair) == 2, "not assignment"
        return c_pair

    @staticmethod
    def split_negate_condition(con):
        c_pair = ConditionSymble._do_split_condition(con, ConditionSymble.negate)
        assert len(c_pair) <= 2, "error !="
        return c_pair

    @staticmethod
    def split_set_condition(con):
        c_pair = ConditionSymble._do_split_condition(con, ConditionSymble.assgin_set)
        assert len(c_pair) <= 2, "error in"
        return c_pair

    @staticmethod
    def split_negate_set_condition(con):
        c_pair = ConditionSymble._do_split_condition(con, ConditionSymble.negate_set)
        assert len(c_pair) <= 2, "error no-in"
        return c_pair

    @staticmethod
    def _do_split_condition(con, symble):
        if not con:
            return []
        c_pair = con.split(symble)
        return [i.strip() for i in c_pair]
    
def remove_default_condition(condition):
    return [c for c in condition if c != default_node]

def make_cmp_fun(condition_list):
    condition_map = {v:idx for idx, v in enumerate(condition_list)}
    def cmp_fun(x, y):
        idx = condition_map.get(x.split(ConditionSymble.assignment)[0], 100000)
        idy = condition_map.get(y.split(ConditionSymble.assignment)[0], 100000)
        if idx == idy:
            return cmp(x, y)
        return idx - idy
    return cmp_fun

def sort_condition(node_info, condition_list):
    # ["a=1", "b=1", "default"]
    if len(node_info) <= 0:
        return
 
 
    node_info_ = sorted([node for node in node_info if node != default_node], cmp=make_cmp_fun(condition_list))
    if len(node_info) > len(node_info_):
        node_info_.append(default_node)

    for idx, v in enumerate(node_info_):
        node_info[idx] = v

    return node_info

def join_condition(conditions):
    return ConditionSymble.codintion_and.join(conditions)

def split_condition(conditions):
    if not conditions:
        return []
    return conditions.split(ConditionSymble.codintion_and)

def safe_get_dict_value(dict_, key_, default_):
    v_ = dict_.get(key_, default_)
    dict_[key_] = v_
    return dict_[key_]

def cut_by_default_value(json_value):
    def do_cut_default_value(dict_):
        if dict_.get(leaf_value):
            return

        default_value = dict_[default_node]
        for k_, v_ in dict_.items():
            if k_ != default_node and v_ == default_value:
                del dict_[k_]
                continue
            do_cut_default_value(v_)

    do_cut_default_value(json_value)
    return json_value

def fix_default_value(json_value):
    def do_fix_default_value(dict_):
        while dict_.keys() == [default_node]:
            default_node_ = dict_[default_node]
            del dict_[default_node]
            for k, v in default_node_.items():
                dict_[k] = v

        if dict_.get(leaf_value) != None:
            return

        for v in dict_.values():
            do_fix_default_value(v)

    do_fix_default_value(json_value)
    return json_value

def fill_default_value(json_value):
    def do_fill_default_value(dict_, value_):
        if dict_.get(leaf_value):
            return

        if not dict_.get(default_node):
            dict_[default_node] = {leaf_value: value_}

        for v in dict_.values():
            do_fill_default_value(v, dict_[default_node])

    do_fill_default_value(json_value, json_value[default_node])
    return json_value

if __name__ == '__main__':
    cond = "a!=1&&c!=1||b!=1&&d!=1||m!=1&&n!=1"
    print ConditionSymble.split_or_condition(cond)