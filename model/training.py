from __future__ import absolute_import, division, print_function, unicode_literals
import pymongo
import pathlib
import seaborn as sns

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from sklearn import preprocessing
import json


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["paopao"]
keywords = mydb['train_items'].find({ 'body' : '萝莉' })
keywords = [{ 'std': x['std'], 'mean': x['mean'], 'name': x['name'], 'index': int(x['index'])} for x in keywords]
keywords.sort(key = lambda x: int(x['index']))

items = mydb['train_datas'].find({ 'body' : '萝莉' })
items = [
    { 'price' : x['price'], 'name': x['name'], 'school' : x['school'], 'v': x['v'], 'url': x['url'], 'body': x['body'] }
    for x in items
]
print(sum([x['price'] for x in items]))

keyword_n = len(keywords)

import random

candidates = {}
random.shuffle(items)
train_items = items[:int(len(items) / 5 * 4)]
test_items = items[int(len(items) / 5 * 4):]

for i in range(0, keyword_n - 1):
    candidates[keywords[i]['name']] = np.array([x['v'][i] for x in train_items]).astype('float64')

keywords_s = [x['name'] for x in keywords]
keywords_s = keywords_s[:-1]
df = pd.DataFrame(candidates, columns = keywords_s)

train_x = df[keywords_s]
train_y = np.array([x['v'][-1] for x in train_items]).astype('float64')

dataset = tf.data.Dataset.from_tensor_slices((df.values, train_y))
train_dataset = dataset.shuffle(len(df)).batch(100)


class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

def build_model():
    model = keras.Sequential([
    #layers.Dense(128, activation='relu', kernel_constraint=keras.constraints.NonNeg()),
    layers.Dense(1500, activation='relu',input_shape=[keyword_n - 1]),
    layers.Dense(512, activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dense(1)
    ])

    optimizer = keras.optimizers.Nadam()

    model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
    return model

model = build_model()
history = model.fit(train_dataset,
  epochs=200, verbose=0,
  callbacks=[PrintDot()])

std = keywords[-1]['std']
mean = keywords[-1]['mean']
tot = 0
test_x = [x['v'][:-1] for x in test_items]
test_y = [x['v'][-1] for x in test_items]
pred_y = model.predict(np.array(test_x))
pred_y = pred_y.flatten()
test_y = [x * mean + std for x in test_y]
pred_y = [x * mean + std for x in pred_y]
d_y = [(pred_y[i] - test_y[i]) / test_y[i] for i in range(len(test_y))]
d_y = [x if x > 0 else -x for x in d_y]
tot = sum(d_y)
print(tot / len(test_y))

for i in range(len(pred_y)):
    d = pred_y[i] - test_y[i]
    if d < 0: d = -d
    if d / test_y[i] < 1: continue
    item = mydb['accounts'].find_one({ 'url': test_items[i]['url'] })
    print(item['unparsed']['content'])
    s = ''
    v = test_items[i]['v']
    for j in range(len(v)):
        if v[j] > 0:
            s = s + keywords[j]['name'] + ', '
    print(s)
    print('expected', pred_y[i], 'actually', test_y[i])

model.save('萝莉.h5')
new_model.summary()

