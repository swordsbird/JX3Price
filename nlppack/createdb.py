import re
import pymongo
import json
from findpath import nlppath

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["paopao"]

f = open(nlppath('rawdata.txt'), 'r')
text = f.read()
f.close()
re1 = re.compile('\[[^\]]+\]')
re2 = re.compile('\([^\)]+\)')
re3 = re.compile('\{[^\}]+\}')
re4 = re.compile('<[^>]+>')
v = re1.findall(text)
v = [v[i][1:-1] for i in range(len(v)) if i == v.index(v[i])]
w = re4.findall(text)
w = [x[1:-1] for x in w]
category = {}
for x in w:
    s = x.split(',')
    t = s[0]
    if t not in category:
        category[t] = []
    category[t].append(s[1:])

al = re3.findall(text)
al = [x[1:-2] for x in al if '(' in x]
alias = {}
for x in al:
    [p, s] = x.split('(')
    alias[s] = [y for y in p.split('/')]

items = []
father = {}
box = [x for x in v if '礼盒' in x]
bb = [x for x in v if '礼包' in x]
rh = [x for x in v if '红发' in x or ('红' == x[0] and len(x) <= 4)]
gh = [x for x in v if '金发' in x or ('金' == x[0] and len(x) <= 4)]
s = set(box + bb + rh + gh)
box = [re.sub('礼盒', '', x) for x in box]
bb = [x[:-2] for x in bb]
rh = [x if '·' not in x else x[x.index('·') + 1:] for x in rh]
gh = [x if '·' not in x else x[x.index('·') + 1:] for x in gh]
v = [x for x in v if x not in s]
co = [x for x in v if len(x) >= 8 or len(
    x) == 7 and '·' in x and x.index('·') == 3 or x in ['玉振天音', '夜烬无声', '雪啸刚风', '天火之眼', '熔金烈风']]
pat = [x for x in v if '挂宠' in x or x in ['雪凤·杰克', '玄凤·鹦歌', '黑凤·护国']]
v = [x for x in v if x not in co + pat]
cl = [x for x in v if '·' in x]
excl7 = ['幽舞华芳', '明镜高悬', '雪月交晖', '任侠河山']
excln = ['金罗姆', '望月']
exbox = ['斩夜无常', '虞渊引梦', '霜岱应元', '日月无心', '云中雪霁', '碧海云仙', '浮屠明音', '陌上窈窕',
         '剑歌惊月', '染墨千秋', '碧翎叠云', '北望天狼', '天穹掠影', '云锦梦华', '九阙天影', '盘龙凤舞']
skip_set = set(['沧海间', '贺华岁', '飒西风', '夜隐仙'])
cl5_set = set([x[:x.index('·')] for x in cl[:32]])
cl_cnt = {}
name_set = set()
abbr_set = set()
counter = 0
clothes = []
for x in cl:
    [p, s] = x.split('·')
    if p not in cl_cnt:
        cl_cnt[p] = 0
    cl_cnt[p] += 1

for k in ['rhair', 'ghair']:
    for x in category[k]:
        for y in x:
            items.append([y, x[0]])
        clothes.append([x[0], x[0], k])
        father[x[0]] = x[0]

items.append(['红发全', '_'.join([x[0] for x in category['rhair']])])
items.append(['红全', '_'.join([x[0] for x in category['rhair']])])
items.append(['全红', '_'.join([x[0] for x in category['rhair']])])
items.append(['金发全', '_'.join([x[0] for x in category['ghair']])])
items.append(['金全', '_'.join([x[0] for x in category['ghair']])])
items.append(['全金', '_'.join([x[0] for x in category['ghair']])])

abbrs = {}
counter = 0
special_items = {
    'cloak': ['情人枕'],
    'cln': ['烟花套'],
}

skip_fa_name = set(['榆塞'])

for x in cl:
    [p, s] = x.split('·')
    fa = p
    name = x
    abbr = p
    if x in alias:
        name = alias[x][0]
        abbr = name[1:]
        if len(abbr) == 1:
            abbr = p
        elif len(abbr) > 3:
            abbr = name[2:]
    if counter >= 100 and (p in cl5_set or cl_cnt[p] == 2):
        if len(fa) == 4:
            fa = '复刻' + fa[:2]
        else:
            fa = '复刻' + fa
        if len(name) < 4:
            name = '复刻' + name
    elif x in alias and counter >= 100 and len(name) >= 3:
        if name[1:] not in skip_fa_name:
            fa = name[1:]
    # disambiguation
    if len(p) >= 3 and p not in skip_set:
        if x not in alias:
            abbr = p[:2]
            name = p[:2] + s
        items.append([p[:2] + s, name])
    elif x not in alias:
        name = p + s
    if x in alias:
        for y in alias[x]:
            if y != s:
                items.append([y, name])
    if abbr not in abbrs:
        abbrs[abbr] = []
    abbrs[abbr].append(name)
    items.append([p + s, name])
    if len(s) >= 2:
        items.append([s, name])
    if counter < 32:
        clothes.append([name, x, 'cl5'])
    elif counter < 56:
        clothes.append([name, x, 'cl6'])
    elif '复刻' not in fa:
        clothes.append([name, x, 'cl7'])
    else:
        clothes.append([name, x, 'cln'])
    father[name] = fa
    counter += 1

counter = 0
for k in abbrs:
    if counter < 16 or len(abbrs[k]) == 2:
        items.append(['双色' + k, '_'.join(abbrs[k])])
        items.append(['双' + k, '_'.join(abbrs[k])])
    elif len(abbrs[k]) > 2:
        items.append(['双色' + k, '_'.join(abbrs[k][:2])])
        items.append(['双' + k, '_'.join(abbrs[k][:2])])
        for i in range(3, len(abbrs[k]) + 1):
            items.append(['三四五六'[i - 3] + '色' + k, '_'.join(abbrs[k][:i])])
        items.append(['全色' + k, '_'.join(abbrs[k])])
    items.append([k, abbrs[k][-1]])
    counter += 1

cl += excl7
for x in excl7:
    name = x
    if x in alias:
        name = alias[x][0]
        items.append([name, name])
    items.append([x, name])
    if len(x) >= 4:
        items.append([x[:2], name])
    clothes.append([name, x, 'cl7'])
    father[name] = name

for x in excln:
    name = x
    if x in alias:
        name = alias[x][0]
        items.append([name, name])
    items.append([x, name])
    if len(x) >= 4:
        items.append([x[:2], name])
    clothes.append([name, x, 'cln'])
    father[name] = name

v = [x for x in v if x not in cl]

for x in box:
    fa = x
    name = x
    boxtype = 'boxn'
    if x in alias:
        name = alias[x][0]
        fa = name
    if '·' in x:
        [p, s] = x.split('·')
        if x not in alias:
            fa = p
        if x not in alias:
            name = p + s
            if len(name) >= 6:
                name = p[:2] + s
    elif len(x) >= 4:
        if x in exbox:
            boxtype = 'box'
        items.append([p[:2] + s, name, fa])
    if x in alias:
        first = True
        for y in alias[x]:
            items.append([y, name])
            if (len(y) > 3 or len(y) == 3 and first) and y[-1] == '盒':
                items.append([y[:-1], name])
            if y[-1] == '盒':
                items.append([y + '子', name])
            first = False
    items.append([re.sub('·', '', x), name])
    clothes.append([name, x, boxtype])
    father[name] = fa

for k in special_items:
    for x in special_items[k]:
        items.append([x, x])
        clothes.append([x, x, k])
        father[x] = x

reserve_cloaks = ['情人枕', '六周年龙', '孔雀', '六翼', '特效粉金鱼', '狐狸毛', '钰瓣', '天辉', '暗夜', '长歌干', '喵萝干', '狄仁杰黑', '狄仁杰白', '一代黄', '一代白', '一代粉', '一代黑', '一代红', '一代紫',
                  '二代粉', '二代蓝', '二代白', '二代紫', '二代红', '二代黑', '羽毛', '黑白荷花', '粉牡丹', '画卷', '狼头', '燕子',
                  '黑竹笋', '凤凰蛋', '白莲花', '蓝扇子', '大蝴蝶', '丛云凋雪', '顺毛干', '小兔子',
                  '小绿', '粉短', '业火劫', '九天玄影', '白狐裘', '黑狐裘']

for x in co:
    fa = x
    name = x
    if x in alias:
        name = alias[x][0]
        fa = name
    if '·' in x:
        [p, s] = x.split('·')
        if x not in alias:
            fa = p
            name = s
        items.append([s, name])
        category['stop'].append([p])
    if x in alias:
        for y in alias[x]:
            items.append([y, name])
    if '·' not in x:
        items.append([re.sub('·', '', x), name])
    clothes.append([name, x, 'cloak'])
    if fa in reserve_cloaks:
        father[name] = fa
    else:
        father[name] = '普通披风'

for x in pat:
    fa = x
    name = x
    if x in alias:
        name = alias[x][0]
        fa = name
    if '·' in x:
        [p, s] = x.split('·')
        if x not in alias:
            fa = s
            name = s
        items.append([s, name])
    if x in alias:
        for y in alias[x]:
            items.append([y, name])
    items.append([re.sub('·', '', x), name])
    clothes.append([name, x, 'pat'])
    father[name] = fa

v = [[x] if x not in alias else [x] + alias[x] for x in v]
category['other'] += v
for k in ['adv', 'school', 'body', 'stype']:
    for x in category[k]:
        for y in x:
            items.append([y, x[0]])
        clothes.append([x[0], x[0], k])
        father[x[0]] = x[0]

reserve_items = [
    '脚气马', '劲足赤兔', '瘸腿赤兔', '踏炎', '里飞沙', '可刀', '三内', '二内', '济世菩萨', '黑龙斩铁', '夜幕星河', '九霄', '舞云飞', '白虎仔',
    '九天逍遥散', '珠盏映粉蕊', '焰归', '业火封狼', '开明参虎', '星河清梦', '银月金虹', '狼烽夜宴', '金影绝风', '火眼白蹄', '月伴晨星',
    '招募椅子', '100级橙武', '100级玄晶', '西宫胃宿', '弦歌落曲', '如意金箍', '狼绒绒', '兔团团']

for x in category['other']:
    for y in x:
        items.append([y, x[0]])
    clothes.append([x[0], x[0], 'other'])
    if x[0] in reserve_items:
        father[x[0]] = x[0]
    else:
        father[x[0]] = '普通挂件'

for x in category['reserve']:
    for y in x:
        items.append([y, y])
        father[y] = ''
        clothes.append([y, y, 'reserve'])

for x in category['stop']:
    for y in x:
        items.append([y, ''])

for x in category['cnt']:
    for y in x[2:]:
        items.append([y, x[2]])

new_items = []
item_index = {}
for x in items:
    if x[0] in item_index:
        if x[0] not in ['寒江', '空山', '雪月'] and x[1] != '':
            new_items[item_index[x[0]]][1] += '_' + x[1]
    else:
        item_index[x[0]] = len(new_items)
        new_items.append(x)
items = new_items

data = []
for x in items:
    data.append({'name': x[0], 'alias': x[1].split('_')})
mydb['dicts'].delete_many({})
mydb['dicts'].insert_many(data)

abbr = {
    'stype': '点月',
    'body': '体型',
    'school': '门派',
    'rhair': '红发',
    'ghair': '金发',
    'cl5': '五限',
    'cl6': '六限',
    'cl7': '限时',
    'cln': '复刻',
    'cloak': '披风',
    'box': '包身盒子',
    'boxn': '普通盒子',
    'pat': '挂宠',
    'adv': '奇遇',
    'other': '其他',
    'cnt': '统计',
    'server': '区服',
}
type_order = ['stype', 'body', 'school', 'rhair', 'ghair', 'cl5', 'cl6', 'cl7', 'cln',
              'cloak', 'box', 'boxn', 'pat', 'adv', 'other', 'cnt', 'reserve']
type_index = dict([[type_order[i], i] for i in range(len(type_order))])
data = []

f = open(nlppath('props.csv'), 'r')
propdate = {}
propprice = {}
for y in f:
    x = re.sub('\s', '', y).split(',')
    propdate[x[0]] = x[1]
    propprice[x[0]] = int(x[2])

default_price0_by_type = {
    'cl5': 200,
    'cl6': 280,
    'cl7': 280,
    'cln': 200,
    'box': 888,
    'boxn': 520,
    'rhair': 380,
    'ghair': 280,
    'cloak': 688,
    'pat': 388
}
default_price0_by_name = {
    '下架': 200,
    '拓印': 240,
    '白发': 200,
    '黑发': 100
}

for x in clothes:
    if x[1] in propdate:
        release_date = propdate[x[1]]
        price = propprice[x[1]]
    elif x[1] + '礼盒' in propdate:
        release_date = propdate[x[1] + '礼盒']
        price = propprice[x[1] + '礼盒']
    else:
        release_date = '2020/12/12'
        price = 0
    price0 = default_price0_by_type.get(x[2], 0)
    data.append({
        'name': x[0],
        'fullname': x[1],
        'type': x[2],
        'price': price,
        'price0': price0,
        'release_date': release_date,
        'father': father.get(x[0], '')
    })

for x in category['cnt']:
    price = 0
    price0 = default_price0_by_name.get(x[0], 0)
    data.append({
        'name': x[2],
        'type': 'cnt',
        'price': price,
        'price0': price0,
        'fullname': x[2],
        'limit': int(x[1]),
        'tag': x[0]
    })

data.sort(key=lambda x: type_index.get(x['type'], 100))
for i in range(len(data)):
    data[i]['abbrtype']=abbr.get(data[i]['type'], '')
    if data[i]['type'] == 'reserve':
        data[i]['index']=-1
    else:
        data[i]['index']=i

# mydb['items'].delete_many({})
# mydb['items'].insert_many(data)
for x in data:
    mydb['items'].update_one(
        {'name': x['name']},
        {"$set": {
            "release_date": x.get('release_date', '2020/12/12'),
            "price": x.get('price', 0),
            "price0": x.get('price0', 0)
            }
        }
    )
