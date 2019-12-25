import csv
import jieba
import pymongo
import re
from findpath import nlppath
from parseutil import parse, parseNum

genset = set(('一代', '二代', '三代', '四代'))
number_re = re.compile('(\d+\.\d+|\d*)[wkq]?\d*')
id_re = re.compile('[a-z0-9]{3,}')

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["paopao"]

items = mydb['accounts'].find()
_items = [x['unparsed']['content'] for x in items]
items = [parse(x, dirty = True) for x in _items]
items = [x for x in items if x != '']
content = '\n'.join(items)

words = mydb['dicts'].find()
words = [x for x in words]
word_map = dict([[x['name'], x['alias']] for x in words])
allf = [x['name'] for x in words if len(x['name']) >= 1]
f = [x['name'] for x in words if len(x['name']) >= 2]

def mycut(x):
    x = jieba.cut(x)
    y = []
    z = []
    for i in x:
        if i not in genset:
            if len(z) == 0:
                y.append(i)
            else:
                for j in z:
                    y.append(j + i)
                z = []
        else:
            z.append(i)
    return y

words = [re.sub(r'\s', '', x.split(' ')[0]) for x in f]
ws = set(words)
allws = set(allf)
words = [x for x in ws]

edge = {}
degree = {}

for x in words:
    edge[x] = []
    degree[x] = 0

for x in words:
    for y in words:
        if x.count(y) > 0 and x != y:
            edge[x].append(y)
            degree[y] += 1

orders = [x for x in words if degree[x] == 0]
for i in range(len(words)):
    x = orders[i]
    for y in edge[x]:
        degree[y] -= 1
        if degree[y] == 0:
            orders.append(y)

f = open(nlppath('dict.txt'), 'w')
nw = []
for x in orders:
    cnt = content.count(x)
    if cnt == 0: continue
    nw.append([x, cnt + 5])
    content = re.sub(x, ' ', content)

nw.sort(key=lambda x: len(x[0]) * 100000 - x[1])
s = ''
for x in nw:
    s += x[0] + ' ' + str(x[1]) + '\n'

f.write(s)
f.close()

jieba.load_userdict(nlppath('dict.txt'))
content = '\n'.join(items)
cuts = [[y for y in mycut(x) if y != ' ' and y !=
         '' and y != '\n'] for x in items]

current = 0
total = 0
left = []
number = ''
for sentence in cuts:
    for i in sentence:
        if i in allws:
            current += len(i)
        else:
            m = re.match(number_re, i)
            if m != None and m.span()[1] == len(i):
                number = number + ', ' + i
            elif re.match(id_re, i) != None:
                continue
            else:
                left.append(i)
        total += len(i)

print('coverage rate: ', current * 1.0 / total)

cnt = {}

for i in left:
    if i not in cnt:
        cnt[i] = 0
    cnt[i] += 1

for i in words:
    if i in cnt:
        del cnt[i]

words = [[i, cnt[i]] for i in cnt]
words.sort(key=lambda x: -x[1])

