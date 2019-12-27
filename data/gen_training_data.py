import pymongo
import numpy as np
import math
import random
import sys
sys.path.append('.')
sys.path.append('..')
from data.item_feature import fix_pairs, random_change_weight, type_penalty, body_penalty

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["paopao"]

merge_category = ['cl7', 'cln', 'other', 'cloak']

items = mydb['items'].find({ 'index': { '$gte': 0}})
items = [x for x in items]
reserved_items = [x['name'] for x in items if x['price'] > x['price0']]
reserved_set = set(reserved_items)
expand_items = [x['index'] for x in items if x['price'] <= x['price0'] * 1.1 and x['abbrtype'] in type_penalty]

category = dict([[x['name'], x['type']] for x in items])
father = dict([[x['name'], x.get('father', '')] for x in items])
items.sort(key = lambda x: int(x['index']))
new_items = []
item_index = {}

base_prop_price = 200
base_price = 1000

for x in items:
    n = x['name']
    if n in category and n in father and category[n] in merge_category:
        if father[n] not in item_index:
            item_index[father[n]] = len(new_items)
            new_items.append({ 'name': father[n], 'index': len(new_items), 'include': [], 'max': 0, 'weight': 1})
        index = item_index[father[n]]
        new_items[index]['include'].append(x['index'])
        new_items[index]['max'] += x.get('stat', {}).get('max', 0)
        if x.get('price', 0) > 0 and x.get('price0', 0) > 0:
            new_items[index]['weight'] += x['price']
    else:
        new_items.append({
            'name': n, 'index': len(new_items),
            'include': [x['index']],
            'max': x.get('stat', {}).get('max', 0),
            'weight': 1
        })
        if x.get('price', 0) > 0 and x.get('price0', 0) > 0:
            new_items[-1]['weight'] = x['price']

for x in new_items:
    x['weight'] = (x['weight'] / base_prop_price) ** 0.4

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
    return r

def normalize(v, body):
    keys = [x for x in train_items if x['body'] == body]
    r = v
    for x in keys:
        i = int(x['index'])
        if i < len(r):
            if x['max'] == 0:
                r[i] = 0
            else:
                r[i] = r[i] / x['max'] * x['weight']
    return r

def get_price(p, body):
    v = [x for x in train_items if x['body'] == body and x['name'] == 'price']
    x = v[0]
    return p * x['max']

if __name__ == '__main__':
    bodys = items[2:6]
    bodys = [x['name'] for x in bodys]
    for body in bodys:
        mydb['train_datas'].delete_many({ 'body': body })
        mydb['train_items'].delete_many({ 'body': body })
    for body in bodys:
        train_items = []
        for k in new_items:
            train_items.append({ 'name': k['name'], 'weight': k['weight'], 'index': len(train_items), 'body': body, 'max': k['max']})
        data = mydb['infos'].find({ 'body': body, 'price' : { '$gte' : 1800, '$lte': 150000 }, 'timestamp' : { '$gt' : 1575176104501 }})
        _data = [
            { 'price' : x['price'], 'name': x['name'], 'school' : x['school'], 'v': x['v'], 'url': x['url'], 'body': x['body'] }
            for x in data
        ]

        data_by_school = {}
        for x in _data:
            if x['school'] not in data_by_school:
                data_by_school[x['school']] = []
            data_by_school[x['school']].append(x)
        maxn = max([len(data_by_school[s]) for s in data_by_school])
        maxn = int(maxn)

        data = []
        random_change_options = [x for x in random_change_weight]
        for school in data_by_school:
            n = len(data_by_school[school])
            m = int(n * min(max(maxn / n, 2), 4))
            if school == '凌雪':
                m = 0
            for k in range(m):
                selected = random.randint(0, n - 1)
                x = data_by_school[school][selected]
                price = x['price']
                body = x['body']
                pd = 0
                dlimit = min(price * 0.2, 2000) * random.uniform(0.5, 1)
                v = x['v'][:]
                if v[origin_index['九天逍遥散']] != 0:
                    continue
                expand_v = [x for x in expand_items if v[x] == 0]
                while pd < dlimit and len(expand_v) > 0:
                    rand = random.randint(0, len(expand_v) - 1)
                    i = expand_v[rand]
                    v[i] += 1
                    expand_v = expand_v[:rand] + expand_v[rand:]
                    typ = items[i]['abbrtype']
                    delta = random.uniform(0.8, 1.2) * type_penalty[typ] * body_penalty[body] * items[i]['price']
                    price += delta
                    pd += delta
                if price < 3000:
                    cw = random.randint(0, 10)
                else:
                    cw = random.randint(0, 20)
                if cw <= 1:
                    if cw == 0 and v[origin_index['100级橙武']] == 0:
                        v[origin_index['100级橙武']] = 1
                        delta = random.uniform(0.9, 1.1) * math.sqrt(body_penalty[body]) * 7000
                        price += delta
                    elif cw == 1 and v[origin_index['100级玄晶']] == 0:
                        v[origin_index['100级玄晶']] = 1
                        delta = random.uniform(0.9, 1.1) * math.sqrt(body_penalty[body]) * 4000
                        price += delta
                data.append({'price' : price, 'name': x['name'], 'school' : school, 'v': v, 'url': x['url'], 'body': body})

        for x in _data:
            data.append(x)

        print(body)
        print(len(data))
        print(sum([x['price'] for x in data]))

        for i in range(len(data)):
            x = data[i]
            x['v'] = expand_dims(x['v'], dirty = True) + [x['price']]

        train_items.append({ 'name': 'price', 'index': len(train_items), 'weight': 1, 'body': x['body'], 'type': 'price', 'max': base_price })
        keyword_n = len(train_items)

        for i in range(0, keyword_n):
            v = np.array([x['v'][i] for x in data])
            vp = np.array([x['price'] for x in data if x['v'][i] > 0])
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

        for x in data:
            x['v'] = normalize(x['v'], body)

        mydb['train_items'].insert_many(train_items)
        mydb['train_datas'].insert_many(data)
else:
    train_items = mydb['train_items'].find()
    train_items = [x for x in train_items]
