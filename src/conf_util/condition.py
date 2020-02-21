# -*- coding: utf-8 -*-
import os
import json
import copy

import copy
import common

OLD_condition = "O"    
NEW_condition = "N"    

def _join_sub_multi(subs_multi):
    # 详细 case 见 test/conf_util/test_condition.py
    # ? * new = new   old*old=old
    # [[('N', [a=1])], [('N', [b=2])]]   =>   [('N', [a=1, b=2])]
    def _do_join(subs_multi_):
        def _recursive_join(prefix, post_multi, traces, result):
            if prefix:
                traces.append(prefix)
            if not post_multi:
                result.append(traces)
                return
            for t_ in post_multi[0]:
                traces_ = copy.deepcopy(traces)
                _recursive_join(t_, post_multi[1:], traces_, result)
        result = []
        _recursive_join(None, subs_multi_, [], result)
        return result

    weight = {
        OLD_condition: 1000000000,
        NEW_condition: -1,
    }

    res = []
    for sub_mid_res in  _do_join(subs_multi):
        res_weight = sum([weight[c[0]] for c in sub_mid_res])
        if res_weight > 0:
            res.append((OLD_condition, [c[1] for c in sub_mid_res]))
        else:
            res.append((NEW_condition, [c[1] for c in sub_mid_res]))
    return res

def _analyze_condition(con):
    if not con:
        return []

    # 详细 case 见 test/conf_util/test_condition.py
    # 处理 b!=2    ===>   [('O', [b=2]), ("N", ["default"])]
    sub_pair = common.ConditionSymble.split_negate_condition(con)
    if len(sub_pair) == 2:
        return [
            (OLD_condition, common.ConditionSymble.assignment.join(sub_pair)),
            (NEW_condition, common.default_node)
        ]

    # 处理 b not-in 2,3,4
    # [('O', [b=2]),('O', [b=2]),('O', [b=2]), ("N", ["default"])]
    sub_pair = common.ConditionSymble.split_negate_set_condition(con)
    if len(sub_pair) == 2:
        c__ = [(NEW_condition, common.default_node)]
        for sub_v_ in sub_pair[1].split(common.ConditionSymble.set_join_op):
            c__.append((OLD_condition, sub_pair[0] + common.ConditionSymble.assignment + sub_v_))
        return c__

    # 处理 b in 2,3,4
    # [('N', [b=2]),('N', [b=2]),('N', [b=2])]
    sub_pair = common.ConditionSymble.split_set_condition(con)
    if len(sub_pair) == 2:
        c__ = []
        for sub_v_ in sub_pair[1].split(common.ConditionSymble.set_join_op):
            c__.append((NEW_condition, sub_pair[0] + common.ConditionSymble.assignment + sub_v_))
        return c__

    # 处理 b=2 ===> [('N', [b=2])]
    return [(NEW_condition, con)]

def _make_conditions(node_id, condition_string):
    # 前端提交的 condition_string 的 value base64处理，防冲突 && || = ……
    pre_condition = set(common.remove_default_condition(common.split_condition(node_id)))

    # negate
    conditions = set()
    for sub in common.ConditionSymble.split_or_condition(condition_string):
        sub_multi = [
            _analyze_condition(sub_) for sub_ in common.remove_default_condition(common.split_condition(sub))
        ]
        for c in _join_sub_multi(sub_multi):
            # c  ('O', [a=1, b=2])
            new_condition = copy.deepcopy(pre_condition)
            new_condition.update(c[1])

            c_temp_ = common.remove_default_condition(new_condition) 
            if (len(c_temp_) != len(new_condition)):
                new_condition = c_temp_[:]
                new_condition.append(common.default_node)
            assert len(c_temp_) == len({common.ConditionSymble.split_assignment_condition(c)[0] for c in c_temp_}), common.condition_conflict

            conditions.add((c[0], common.join_condition(new_condition)))

    return [(c[0], common.split_condition(c[1])) for c in conditions]
        
    # # assign
    # conditions = set()
    # for sub in sub_conditions:
    #     new_condition = copy.deepcopy(pre_condition)
    #     new_condition.update(common.remove_default_condition(common.split_condition(sub)))

    #     assert len(new_condition) == len({common.ConditionSymble.split_assignment_condition(c)[0] for c in new_condition}), common.condition_conflict

    #     new_condition = common.sort_condition(list(new_condition), [])
    #     conditions.add((NEW_condition, common.join_condition(new_condition)))

def _make_append_tree(old_value, conditions, new_value):
    # 详细 case 见 test/conf_util/test_condition.py
    def fill_default_value(dict_):
        if dict_.get(common.leaf_value):
            return

        for v in dict_.values():
            fill_default_value(v)

        if not dict_.get(common.default_node):
            dict_[common.default_node] = {common.leaf_value: old_value}

    json_value = {} 
    for con in conditions:
        sub_dict_ = json_value
        for sub_c in con[1]:
            sub_dict_ = common.safe_get_dict_value(sub_dict_, sub_c, {})
        sub_dict_[common.leaf_value] = new_value if con[0] == NEW_condition else old_value

    fill_default_value(json_value)
    common.fix_default_value(json_value)
    return json_value

def make_append_tree(node_id, condition_string, old_value, new_value):
    conditions = _make_conditions(node_id, condition_string)
    return _make_append_tree(old_value, conditions, new_value)


def insert_node():
    # 冲突丢弃
    pass

if __name__ == '__main__':
    old_value = "m1"
    new_value = "m1a2b2"
    res = make_append_tree("m=1", "a!=2||b=2", old_value, new_value)
    print json.dumps(res)
    # print res

    import show_json, middle_json
    condition_list = ["m", "a", "b"]
    res = middle_json.mid_to_json(middle_json.gen_mid_json(res, condition_list))
    show_json.write_show_conf("demo", show_json.gen_show_json(res, condition_list))
