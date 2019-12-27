from __future__ import absolute_import, division, print_function, unicode_literals
from tensorflow import keras
import numpy as np
import json
import time
import pymongo
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_compress import Compress
import tensorflow as tf
import sys
sys.path.append("..")
from data.gen_data import extract, set_body, set_school, check_vector
from data.gen_training_data import expand_dims, get_price, normalize
from data.item_feature import type_penalty, school_penalty, body_penalty

model_path = '../model/'
model = {}

compress = Compress()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["paopao"]

items = mydb['items'].find({'index': {'$gte': 0}})
items = [{
    'name': x['name'],
    'type': x['abbrtype'],
    'fullname': x.get('fullname', ''),
    'date': x.get('release_date', ''),
    'price': x.get('price', 0),
    'price0': x.get('price0', 0),
    'index': int(x['index']),
    'mean': float(x.get('stat', {}).get('mean', 0))
} for x in items]
items.sort(key=lambda x: int(x['index']))
item_price = np.array([x['price'] * type_penalty.get(x['type'], 0.7) for x in items])
keyword_map = dict([x['name'], x['index']] for x in items)

app = Flask(__name__, static_folder='./dist/',
            template_folder="./dist/", static_url_path='')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
compress.init_app(app)


class Model:
    @staticmethod
    def loadmodel(name):
        return keras.models.load_model(model_path + name + '.h5')

    def __init__(self, name):
        self.graph = tf.get_default_graph()
        with self.graph.as_default():
            self.session = tf.Session(graph=self.graph)
            with self.session.as_default():
                self.model = self.loadmodel(name)

    def predict(self, X):
        with self.graph.as_default():
            with self.session.as_default():
                return self.model.predict(X)


models = {}
bodys = ['成女', '萝莉', '成男', '正太']
for i in bodys:
    models[i] = Model(i)

@app.route('/api/querydb/', methods=['POST'])
def querydb():
    args = request.form
    print(args)
    start_date = request.args.get('start_date', 0)
    end_date = request.args.get('end_date', 2000000000000)
    min_price = request.args.get('min_price', 1)
    max_price = request.args.get('max_price', 999999)
    query = {
        'price': {'$gte': int(min_price), '$lte': int(max_price)},
        'timestamp': {'$gte': int(start_date), '$lte': int(end_date)},
    }
    body = request.args.get('body', None)
    school = request.args.get('school', None)
    if body != None:
        query['body'] = body
    if school != None:
        query['school'] = school

    schools = mydb['schools'].find()
    schools = [x['name'] for x in schools]

    items = mydb['infos'].find(query)
    items = [
        {'price': x['price'], 'school': x['school'],
            'v': x['v'], 'url': x['url']}
        for x in items
    ]

    return json.dumps(items)


@app.route('/api/queryaccount/', methods=['POST'])
def queryaccount():
    start_time = time.time()
    args = json.loads(request.get_data(as_text=True))
    text = args.get('text', '')
    v = args.get('v', [])
    if text != '':
        words, (price, school, body, v) = extract(text)
    else:
        words = []
        v = check_vector(v)

    sc = args.get('school', '')
    if sc != '':
        school = sc
        set_school(v, school)

    bd = args.get('body', '')
    if bd != '':
        body = bd
        set_body(v, body)
    
    if body == None or school == None or body == '' or school == '':
        return json.dumps({'status': 'failed'})

    p = -1
    if body in models:
        p0 = np.array(v) * item_price * body_penalty.get(body, 1) * school_penalty.get(school, 1)
        if p0 < 2000:
            p = p0
        else:
            tv = expand_dims(v)
            tv = normalize(tv, body)
            model = models[body]
            p = model.predict(np.array([tv]))
            p = get_price(p, body)
            p = float(p[0][0])
    end_time = time.time()
    print('time cost: ', (end_time - start_time) * 1000)
    return json.dumps({'status': 'success', 'price': p, 'text': words, 'v': v, 'school': school, 'body': body})
    #except:
    #    return json.dumps({'status': 'failed'})

@app.route('/api/items/', methods=['GET'])
def get_items():
    return {'items': items}

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/text')
def main1():
    return render_template('index.html')

@app.route('/customize')
def main2():
    return render_template('index.html')

@app.route('/history')
def main3():
    return render_template('index.html')

@app.route('/analysis')
def main4():
    return render_template('index.html')
