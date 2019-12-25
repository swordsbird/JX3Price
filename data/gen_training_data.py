import pymongo
import numpy as np
import math
import random
import sys
sys.path.append('.')
sys.path.append('..')
from data.item_feature import item_weight, reserved_items, fix_pairs, addition_pairs, random_change_weight, body_penalty

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["paopao"]

merge_category = ['cl7', 'cln', 'other', 'cloak']

items = mydb['items'].find({ 'index': { '$gte': 0}})
items = [x for x in items]
category = dict([[x['name'], x['type']] for x in items])
father = dict([[x['name'], x.get('father', '')] for x in items])
items.sort(key = lambda x: int(x['index']))
new_items = []
item_index = {}

for x in items:
    n = x['name']
    if n in category and n in father and category[n] in merge_category:
        if father[n] not in item_index:
            item_index[father[n]] = len(new_items)
            new_items.append({ 'name': father[n], 'index': len(new_items), 'include': []})
        new_items[item_index[father[n]]]['include'].append(x['index'])
    else:
        new_items.append({ 'name': n, 'index': len(new_items), 'include': [x['index']]})

reserved_set = set(reserved_items)
origin_index = dict([[x['name'], x['index']] for x in items])
typed_index = {}
for x in items:
    if x['type'] not in typed_index:
        typed_index[x['type']] = []
    typed_index[x['type']].append(x['name'])

new_fix_pairs = []
for p in fix_pairs:
    x = origin_index[p[0]]
    y = [[k['index'], max(0.005, k['stat']['mean'])] for k in items if k['type'] in p[1] and k['name'] not in reserved_set]
    z = [k['index'] for k in items if k['type'] in p[1] or ('-' + k['type']) in p[1]]
    total = sum([k[1] for k in y])
    y.sort(key = lambda k: k[1], reverse = True)
    for i in range(1, len(y)):
        y[i][1] += y[i - 1][1]
    for i in range(0, len(y)):
        #y[i][1] = (i + 1) / len(y)
        y[i][1] /= total
    new_fix_pairs.append((x, z, y))
fix_pairs = new_fix_pairs

addition_set = set([x[0] for x in addition_pairs])
for p in addition_pairs:
    new_items.append({ 'name': p[0], 'type': 'syn', 'index': len(new_items), 'include': [origin_index[x] for x in p[1]]})

def check_dims(v):
    r = v[:]
    for p in fix_pairs:
        s = r[p[0]]
        for i in p[1]:
            s -= r[i]
        if s == 0: continue
        order = p[2]
        k = s * 2
        while s > 0 and k > 0:
            rd = random.random()
            i = 0
            while i < len(order) and order[i][1] < rd:
                i += 1
            if i < len(order) and r[order[i][0]] == 0:
                r[order[i][0]] = 1
                s -= 1
            k -= 1
    r[origin_index['五甲']] = 0
    return r

def expand_dims(v, dirty = False):
    v = check_dims(v)
    r = []
    for x in new_items:
        t = 0
        for i in x['include']:
            t += v[i]
        r.append(t)
    for i in range(len(r) - 1, 0, -1):
        if new_items[i]['name'] not in addition_set: break
        r[i] = 1 if r[i] == 0 else 0
    return r

def normalize(v, body):
    items = [x for x in train_items if x['body'] == body]
    r = v
    for x in items:
        i = int(x['index'])
        std = x['std']
        mean = x['mean']
        if i < len(r):
            if mean != 0:
                if mean < 0.05: mean = 0.05
                r[i] = (float(r[i]) - std) / mean * x['weight']
            else:
                r[i] = 0
    return r

def get_price(p, body):
    v = [x for x in train_items if x['body'] == body and x['name'] == 'price']
    x = v[0]
    std = x['std']
    mean = x['mean']
    return p * mean + std

if __name__ == '__main__':
    bodys = items[2:6]
    bodys = [x['name'] for x in bodys][1:]
    for body in bodys:
        mydb['train_datas'].delete_many({ 'body': body })
        mydb['train_items'].delete_many({ 'body': body })
    for body in bodys:
        train_items = []
        for k in new_items:
            train_items.append({ 'name': k['name'], 'weight': item_weight[body].get(k['name'], 1), 'index': len(train_items), 'body': body })
        items = mydb['infos'].find({ 'body': body, 'price' : { '$gte' : 1800, '$lte': 150000 }, 'timestamp' : { '$gt' : 1575176104501 }})
        _items = [
            { 'price' : x['price'], 'name': x['name'], 'school' : x['school'], 'v': x['v'], 'url': x['url'], 'body': x['body'] }
            for x in items
        ]

        items_by_school = {}
        for x in _items:
            if x['school'] not in items_by_school:
                items_by_school[x['school']] = []
            items_by_school[x['school']].append(x)
        maxn = max([len(items_by_school[s]) for s in items_by_school])
        maxn = int(maxn * 2)

        items = []
        random_change_options = [x for x in random_change_weight]
        for school in items_by_school:
            n = len(items_by_school[school])
            m = int(n * min(max(maxn / n, 2), 6))
            if school == '凌雪':
                m = 0
            for k in range(m):
                selected = random.randint(0, n - 1)
                x = items_by_school[school][selected]
                price = x['price']
                body = x['body']
                pd = 0
                dlimit = min(price * 0.2, 2000) * random.uniform(0.5, 1)
                v = x['v'][:]
                while pd < dlimit:
                    i = random.randint(0, len(random_change_options) - 1)
                    i = random_change_options[i]
                    j = origin_index[i]
                    v[j] += 1
                    delta = random.uniform(0.6, 1.4) * random_change_weight[i] * body_penalty[body]
                    price += delta
                    pd += delta
                if price < 3000:
                    cw = random.randint(0, 10)
                else:
                    cw = random.randint(0, 18)
                if cw <= 1 and school != '凌雪' and v[origin_index['九天逍遥散']] == 0:
                    if cw == 0 and v[origin_index['100级橙武']] == 0:
                        v[origin_index['100级橙武']] = 1
                        delta = random.uniform(0.9, 1.1) * math.sqrt(body_penalty[body]) * 7500
                        price += delta
                    elif cw == 1 and v[origin_index['100级玄晶']] == 0:
                        v[origin_index['100级玄晶']] = 1
                        delta = random.uniform(0.9, 1.1) * math.sqrt(body_penalty[body]) * 5000
                        price += delta

                items.append({'price' : price, 'name': x['name'], 'school' : school, 'v': v, 'url': x['url'], 'body': body})

        for x in _items:
            items.append(x)

        print(body)
        print(len(items))
        print(sum([x['price'] for x in items]))

        for i in range(len(items)):
            x = items[i]
            x['v'] = expand_dims(x['v'], dirty = True) + [x['price']]

        train_items.append({ 'name': 'price', 'index': len(train_items), 'weight': 1, 'body': x['body'], 'type': 'price' })
        keyword_n = len(train_items)

        for i in range(0, keyword_n):
            v = np.array([x['v'][i] for x in items])
            vp = np.array([x['price'] for x in items if x['v'][i] > 0])
            std = np.std(v)
            mean = np.mean(v)
            if len(vp) > 0:
                std_p = np.std(vp)
                mean_p = np.mean(vp)
                min_p = np.min(vp)
            else:
                std_p = 0
                mean_p = 0
                min_p = 0
            train_items[i]['std'] = std
            train_items[i]['mean'] = mean
            train_items[i]['price_std'] = std_p
            train_items[i]['price_mean'] = mean_p
            train_items[i]['price_min'] = min_p

        for x in items:
            x['v'] = normalize(x['v'], body)

        mydb['train_items'].insert_many(train_items)
        mydb['train_datas'].insert_many(items)
else:
    train_items = mydb['train_items'].find()
    train_items = [x for x in train_items]
