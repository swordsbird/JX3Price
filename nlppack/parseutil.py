import re
import math

multi_red = '四五六七八九十猴鸡羊猪狗'
multi_gold = '一代|猴|狐|苏|蝶|喵|高考|考|鸡|国|倒闭|狗|破晓|龙女|中秋|玫瑰|猪|丝路|珊瑚|兔|月兔|马尾'
multi_box = '伞|刀|咕|唐|喵|歌|毒|狗|猪|猫|白|秃|粉|糖|红|花|蓝|貂|青|鸡|黑|明教|蓬莱|藏剑'
multi_red_all_re = re.compile('([' + multi_red + ']{2,})红')
multi_gold_all_re = re.compile('([' + multi_gold + ']{2,})金')
multi_box_all_re = re.compile('([' + multi_box + ']{2,})盒[子?]')
multi_red_re = re.compile('([' + multi_red + '])')
multi_gold_re = re.compile('(' + multi_gold + ')')
multi_box_re = re.compile('(' + multi_box + ')')
ch_number_re = re.compile('(十一|[一二三四五六七八九十1-9])万([一二三四五六七八九1-9])?(?!花)')
ch_number_map = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5',
                 '六': '6', '七': '7', '八': '8', '九': '9', '十': '10', '十一': '11', '': '',
                 '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                 '6': '6', '7': '7', '8': '8', '9': '9'}
pointed_num_re = re.compile('(\d+\.\d+)w')
gen_number_re = re.compile('([一|二|三|四]{2,})代')
gen_old_re = re.compile('(老(?:蓝中秋|粉中秋|七夕|中秋|花朝|.花朝|元宵|重阳))')
gen_new_re = re.compile('(新(?:七夕|中秋|.中秋|花朝|.花朝|元宵|重阳))')
gen_re = re.compile('(([一二三四]代){2,}(七夕|重阳|元宵|.?花朝|.?中秋))')
start_re = re.compile('\$[^\s^【]*')
rent_re = re.compile('(出租|已租|\d{3}月)')

def parseNum(x):
    i = len(x)
    base = 1
    if 'k' in x:
        i = x.index('k')
        base = 1000
    if 'q' in x:
        i = x.index('q')
        base = 1000
    if 'w' in x:
        i = x.index('w')
        base = 10000
    tail = 0
    if i + 1 < len(x):
        tail = float(x[i + 1:])
        if tail != 0:
            while tail * 10 < base:
                tail = tail * 10
    try:
        ret = (float(x[:i]) if i > 0 else 1) * base + tail
    except:
        print(x, x[:i])
        return 1
    return ret

def parse2(x):
    for y in ch_number_re.findall(x):
        z = 'w'.join((ch_number_map[i] for i in y))
        x = x.replace('万'.join(y), z)
    for y in gen_old_re.findall(x):
        z = '一代' + y[1:]
        x = x.replace(y, z)
    for y in gen_new_re.findall(x):
        z = '二代' + y[1:]
        x = x.replace(y, z)
    for y in gen_number_re.findall(x):
        z = '代'.join(y)
        x = x.replace(y, z)
    for y in gen_re.findall(x):
        z = ''
        for i in range(0, len(y[0]) - len(y[2]), 2):
            z += y[0][i:i+2] + y[2]
        x = x.replace(y[0], z)
    for y in multi_red_all_re.findall(x):
        z = '红'.join(multi_red_re.findall(y))
        x = x.replace(y, z)
    for y in multi_gold_all_re.findall(x):
        z = '金'.join(multi_gold_re.findall(y))
        x = x.replace(y, z)
    for y in multi_box_all_re.findall(x):
        z = '盒子'.join(multi_box_re.findall(y))
        x = x.replace(y, z)
    for y in pointed_num_re.findall(x):
        z = str(math.floor(float(y) * 10000))
        x = x.replace(y + 'w', z)
    return x


def parse(x, dirty = False):
    x = x.lower()
    if dirty:
        x = '$' + x
        m = re.match(start_re, x)
        if m != None:
            x = x[m.span()[1]:]
        if len(rent_re.findall(x)) > 0:
            return ''
    x = re.sub('[•:：\s]', '', x)
    x = re.sub('[/◆●*★（）【】\\·、\[\]←=\*★。#\?·]', ' ', x)
    if dirty:
        x = re.sub('菀之Q3278806652←4063', '', x)
        x = re.sub('五七万专售', '', x)
    x = re.sub('q+\d{4,}', ' ', x)
    x = re.sub('[kq]\d{4,}', ' ', x)
    x = re.sub('100[^橙]{0,3}橙武', '100橙武', x)
    x = re.sub('100级[^橙]{0,2}大橙武', '100橙武', x)
    x = re.sub('100[^c]{0,3}cw', '100橙武', x)
    x = re.sub('100[^玄]{0,3}玄晶', '100玄晶', x)
    x = re.sub('100[^大]{0,3}大铁', '100玄晶', x)
    x = re.sub('岁宴\d+', '', x)
    x = re.sub('\d{7,}', ' ', x)
    x = re.sub('电五', '电五 ', x)
    x = re.sub('电一', '电一 ', x)
    x = re.sub('\s{2,}', ' ', x)
    x = re.sub('se', '色', x)
    x = re.sub('jio', '脚', x)
    x = re.sub('xiao', '小', x)
    x = re.sub('6e', '六翼', x)
    x = re.sub('61盒', '六一盒', x)
    x = re.sub('螺母', '罗姆', x)
    x = re.sub('不期', '不欺', x)
    x = re.sub('精灵', '金陵', x)
    x = re.sub('裁火莲', '栽火莲', x)
    x = re.sub('(猴红|九红|猪金|狐金|朱金|破晓金|端午金){1,}头像', '头像', x)
    x = re.sub('叽', '鸡', x)
    if dirty:
        x = re.sub('49盒', '雪月交晖', x)
        x = re.sub('资.历', '资历', x)
        x = re.sub('披.风', '披风', x)
        x = re.sub('小.姐', '小姐', x)
        x = re.sub('免定金接代售公司实体经营百万流量推广', ' ', x)
        x = re.sub('\d+k免定', ' ', x)
    x = re.sub('情r枕|qr枕|qrz', '情人枕', x)
    x = re.sub('二代.狐狸毛披风', '二代狐狸毛', x)
    x = parse2(x)
    return x

def get_prefix(cuts, r):
    sc = {}
    pc = {}
    other = set(('双色', '双', '三色', '四色', '全色', '下架'))
    rs = set(r)
    for cut in cuts:
        start = 0
        for i in range(start, len(cut) - 1):
            k = cut[i - 1] + cut[i]
            if cut[i] in rs and cut[i - 1] not in other:
                if k not in sc: sc[k] = 0
                sc[k] += 1
            if cut[i - 1] in rs and cut[i] not in other:
                if k not in pc: pc[k] = 0
                pc[k] += 1
    pw = [[x, pc[x]] for x in pc]
    sw = [[x, sc[x]] for x in sc]
    pw.sort(key = lambda x:-x[1])
    sw.sort(key = lambda x:-x[1])
    print(pw[:5] + sw[:5])
