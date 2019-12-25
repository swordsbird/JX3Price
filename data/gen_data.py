import csv
import json
import pymongo
import math
import numpy as np
import sys
sys.path.append(".")
sys.path.append("..")
from nlppack.word_cut import parse

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["paopao"]

words = mydb['dicts'].find()
words = [x for x in words]
word_map = dict([[x['name'], x['alias']] for x in words])
items = mydb['items'].find()
items = [x for x in items]
types = list(set([x['type'] for x in items]))
abbr = {}
for x in items:
    if x['type'] not in abbr:
        abbr[x['type']] = x['abbrtype']

typed_item_index = dict([[t, [x['index'] for x in items if x['type'] == t]] for t in types])
special_group = '红金白黑'

item_index = dict([[x['name'], x['index']] for x in items])
item_limit = dict([[x['name'], x.get('limit', 1)] for x in items])
item_type = dict([[x['name'], x['type']] for x in items])
item_tag = dict([[x['name'], x.get('tag', '')] for x in items])
item_set = set([x['name'] for x in items])
items = [x for x in items if x['index'] >= 0]

v_limit = [item_limit[x['name']] for x in items]
accounts = mydb['accounts'].find()


def find_index(x):
    if x in special_group:
        x = x + '发'
    return item_index.get(x, -1)


accounts = [x for x in accounts]


def achievePointF(x):
    if x > 0 and x < 10:
        x *= 10000
    elif x == -1 and x < 1000:
        x = 30000
    return x


def extract_vector(s, text, dirty=False):
    x = []
    enable_cl5 = True
    last = ''
    for i in s:
        if type(i) == float or type(i) == int:
            x.append(i)
        elif i == '':
            pass
        else:
            if ('复刻' in i or '下架' in i):
                enable_cl5 = False
            elif '五限' in i:
                enable_cl5 = True
            if i[0] == '-':
                x.append(i)
            else:
                if i in word_map:
                    has_cl5 = False
                    for j in word_map[i]:
                        if item_type.get(j, '') == 'cl5':
                            has_cl5 = True
                    if has_cl5:
                        if enable_cl5:
                            x += [j for j in word_map[i]
                                  if item_type.get(j, '') == 'cl5']
                        else:
                            x += [j for j in word_map[i]
                                  if item_type.get(j, '') != 'cl5']
                    else:
                        for j in word_map[i]:
                            x.append(j)
        last = i
    price = -1
    # trim head
    for i in range(len(x)):
        if type(x[i]) == float or type(x[i]) == str and x[i] != '' and x[i][0] != '-':
            x = x[i:]
            break
    forward_range = 12
    backward_range = 5
    school = None
    body = None
    # find school & body
    z = x[:forward_range]
    if len(x) > forward_range:
        delta = len(x) - forward_range
        if delta > backward_range:
            delta = backward_range
        z.append('')
        for i in range(0, delta):
            z.append(x[-i - 1])
    pindex = -1
    for i in range(len(z)):
        if (type(z[i]) == float and (i > 0 and price == -1 and 'body' in item_type.get(z[i - 1], '') and
                                     (i + 1 == len(z) or z[i + 1] != '资历' or i + 2 < len(z) and type(z[i + 2]) == float and z[i + 2] > 10000))):
            price = z[i]
            pindex = i
    for i in range(len(z)):
        if (type(z[i]) == float and (i > 0 and price == -1 and i + 1 < len(z) and 'school' in item_type.get(z[i + 1], '') and
                                     (i == 0 or z[i - 1] != '资历' or i > 1 and type(z[i - 2]) == float and z[i - 2] > 10000))):
            price = z[i]
            pindex = i
        elif type(z[i]) == str:
            if body == None and 'body' in item_type.get(z[i], ''):
                body = z[i]
            elif school == None and 'school' in item_type.get(z[i], ''):
                school = z[i]
    if price < 100:
        for i in range(len(z)):
            if type(z[i]) == float and z[i] >= 100:
                if i == 0 or z[i - 1] != '资历':
                    if i + 1 == len(z) or z[i + 1] != '资历':
                        price = z[i]
                        pindex = i
                        break
    #print(body, school, price, x)
    if dirty:
        if body == None or school == None or price == -1 or '月租' in text or '已租' in text or price < 200 or s[0] == '出租':
            return None, None, None, None
    # remove price info
    if pindex != -1:
        if pindex > forward_range:
            pindex = forward_range - pindex
        x[pindex] = ''
    v = [0] * len(items)
    last_type = ''
    last_item_type = ''
    last_info = ''
    last_val = ''
    last_colors = ''
    left = []
    i = 0
    while i < len(x):
        curr_item_type = item_type.get(x[i], '')
        curr_type = type(x[i])
        curr_info = item_tag.get(x[i], '')
        curr_val = x[i]
        if curr_type == float:
            if 'cnt' == last_item_type and (last_info == 'prefix' or last_info == 'both'):
                if find_index(last_val) != -1:
                    k = find_index(last_val)
                    if curr_val < v_limit[k] * 2:
                        v[k] = curr_val
                curr_item_type = ''
            last_colors = ''
        else:
            if last_type == float:
                if 'cnt' == curr_item_type and (curr_info == 'suffix' or curr_info == 'both'):
                    if find_index(curr_val) != -1:
                        k = find_index(curr_val)
                        if last_val < v_limit[k] * 2:
                            v[k] = last_val
                    curr_item_type = ''
                elif curr_val not in item_set and len(curr_val) >= 2 and curr_val[1] in special_group and last_val < 50:
                    if find_index(curr_val[1]) != -1:
                        k = find_index(curr_val[1])
                        if last_val < v_limit[k] * 2:
                            v[k] = last_val
                    if len(curr_val) > 2 and curr_val[2:] in item_set:
                        x[i] = curr_val[2:]
                        continue
                elif curr_val in item_set:
                    k = find_index(curr_val)
                    if k != -1:
                        v[k] += 1

            elif curr_type == str and 'cnt' not in curr_item_type and curr_val in item_set:
                k = find_index(curr_val)
                if k != -1:
                    if last_colors == '':
                        v[k] += 1
                    else:
                        if item_type.get(curr_val[0], '') in '白黑金红蓝紫绿黄粉':
                            colors = last_colors + curr_val[0]
                            for c in colors:
                                for t in word_map.get(c + curr_val[1:], []):
                                    k = find_index(t)
                                    if k != -1:
                                        v[k] += 1
                        else:
                            v[k] += len(last_colors)
            elif 'cnt' not in curr_item_type:
                # left.append(curr_val)
                pass
            flag = True
            for k in curr_val:
                if 'color' not in item_type.get(k, ''):
                    flag = False
                    break
            if flag:
                last_colors = last_colors + curr_val
            else:
                last_colors = ''
        last_info = curr_info
        last_item_type = curr_item_type
        last_type = curr_type
        last_val = curr_val
        i += 1
    v[item_index['资历']] = achievePointF(v[item_index['资历']])
    for i in range(len(v)):
        if v[i] > v_limit[i]:
            v[i] = v_limit[i]
    if v[item_index['资历']] >= 90000:
        v[item_index['资历金']] = 1
    if v[item_index['资历']] >= 100000:
        v[item_index['资历红']] = 1
    if v[item_index['盒子']] == 0:
        v[item_index['盒子']] = sum(
            [v[i] for i in typed_item_index['box'] + typed_item_index['boxn']])
    cnt_terms = ['cl5', 'cln', 'cloak', 'adv', 'rhair', 'ghair', 'pat']
    for term in cnt_terms:
        tsum = sum([v[i] for i in typed_item_index[term]])
        if v[item_index[abbr[term]]] == 0:
            v[item_index[abbr[term]]] = tsum
    if v[item_index['限量']] == 0:
        v[item_index['限量']] = sum([v[i] for i in typed_item_index['cl6']]) + sum(
            [v[i] for i in typed_item_index['cl7']]) + v[item_index['五限']] + v[item_index['盒子']]
    if dirty:
        if sum([v[i] for i in typed_item_index['school']]) >= 2 and sum([v[i] for i in typed_item_index['body']]) >= 2:
            return None, None, None, None
    for i in typed_item_index['school']:
        v[i] = 0
    for i in typed_item_index['body']:
        v[i] = 0
    v[item_index[school]] = 1
    v[item_index[body]] = 1
    for i in range(len(v)):
        if v[i] > v_limit[i]:
            v[i] = v_limit[i]
    #    if i in hiddenset:
    #        v[i] = 0
    return price, school, body, v


def check_vector(v):
    v[item_index['资历']] = achievePointF(v[item_index['资历']])
    for i in range(len(v)):
        if v[i] > v_limit[i]:
            v[i] = v_limit[i]
    if v[item_index['盒子']] == 0:
        v[item_index['盒子']] = sum(
            [v[i] for i in typed_item_index['box'] + typed_item_index['boxn']])
    cnt_terms = ['cl5', 'cln', 'cloak', 'adv', 'rhair', 'ghair', 'pat']
    for term in cnt_terms:
        tsum = sum([v[i] for i in typed_item_index[term]])
        if v[item_index[abbr[term]]] == 0:
            v[item_index[abbr[term]]] = tsum
    if v[item_index['限量']] == 0:
        v[item_index['限量']] = sum([v[i] for i in typed_item_index['cl6']]) + sum(
            [v[i] for i in typed_item_index['cl7']]) + v[item_index['五限']] + v[item_index['盒子']]
    for i in range(len(v)):
        if v[i] > v_limit[i]:
            v[i] = v_limit[i]
    return v


def set_school(v, school):
    for i in typed_item_index['school']:
        v[i] = 0
    v[item_index[school]] = 1


def set_body(v, body):
    for i in typed_item_index['body']:
        v[i] = 0
    v[item_index[body]] = 1


def extract(text, dirty=False):
    s = parse(text, dirty)
    r1, r2, r3, r4 = extract_vector(s, text, dirty)
    return s, (r1, r2, r3, r4)


if __name__ == '__main__':
    people = []
    headerset = set()
    existitems = mydb['infos'].find()
    existitems = [x['url'] for x in existitems]
    urlset = set(existitems)

    history_v = {}
    v_count = []
    for i in range(len(items)):
        v_count.append([])
    total = 0
    duplicate = 0
    frequent = [0] * len(items)
    counter = 0
    for it in accounts:
        counter += 1
        content = it['unparsed']['content']
        if it['url'] in urlset or content[:64] in headerset:
            duplicate += 1
            continue
        headerset.add(content[:64])
        urlset.add(it['url'])

        _, (p, s, b, v) = extract(content, dirty=True)
        if v == None:
            duplicate += 1
            continue

        flag = False
        np_v = np.array(v)
        vk = str(int(p)) + s + b
        vsum = np.sum(np_v)
        for w in history_v.get(vk, []):
            delta = np.sum(np.abs(w - np_v))
            if delta == 0 or delta <= 2 and vsum > 50:
                flag = True
        if flag:
            duplicate += 1
            continue
        else:
            if vk not in history_v:
                history_v[vk] = []
            history_v[vk].append(np_v)

        for i in range(len(v)):
            v_count[i].append(v[i])
        people.append({
            'v': v, 'timestamp': it['timestamp'], 'url': it['url'],
            'qq': it['qq'], 'body': b, 'school': s, 'price': p, 'name': it['name']
        })
        for i in range(len(v)):
            if v[i] > 0.5:
                frequent[i] += 1
        if len(people) > 100:
            mydb['infos'].insert_many(people)
            total += len(people)
            print(total, 'items have been inserted, ',
                  duplicate, ' duplicate items.')
            people = []

    frequent = [[items[i]['name'], frequent[i]] for i in range(len(items))]
    frequent.sort(key=lambda x: -x[1])
    mydb['infos'].insert_many(people)

    for i in range(len(v_count)):
        stat = {
            'std': float(np.std(v_count[i])),
            'mean': float(np.mean(v_count[i])),
            'min': float(np.min(v_count[i])),
            'max': float(np.max(v_count[i]))
        }
        mydb['items'].update_one({'index': i}, {'$set': {'stat': stat } })
