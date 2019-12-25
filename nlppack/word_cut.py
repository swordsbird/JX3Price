import jieba
import re
import csv
from .findpath import nlppath
from . import parseutil
import pymongo

number_re = re.compile('(\d+\.\d+|\d*)[wkq]?\d*')
id_re = re.compile('[a-z0-9]{3,}')
empty_re = re.compile('\s+')
genset = set(('一代', '二代', '三代', '四代'))
jieba.load_userdict(nlppath('dict.txt'))
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["paopao"]
items = mydb['dicts'].find()
items = [x for x in items]
word_map = set([x['name'] for x in items])

def cut(x):
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

def parse(x, dirty = False):
    x = parseutil.parse(x, dirty)
    sentence = cut(x)
    ret = []
    for k in range(len(sentence)):
        i = sentence[k]
        if i != '' and i in word_map:
            ret.append(i)
        else:
            m = re.match(number_re, i)
            if m != None and (m.span()[1] >= 2 or m.span()[1] == len(i)):
                if i == 'k' or i == 'w' or i == 'q':
                    continue
                elif k + 1 < len(sentence) and (sentence[k + 1] == 'k' or sentence[k + 1] == 'w'):
                    sentence[k + 1] = i + sentence[k + 1]
                    continue
                ret.append(parseutil.parseNum(i[:m.span()[1]]))
            elif re.match(id_re, i) != None:
                continue
            elif i != '' and re.match(empty_re, i) == None:
                ret.append('-' + i)
    return ret
