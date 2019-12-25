# JX3Price
A project for account price estimation of Jianxia3. 一个剑网3游戏账号价格估计的项目.

[Miemie Price Estimation Project 咩咩估价](http://jx3.in)

### 咩咩估价是作者初次使用tensorflow训练人工神经网络的游戏之作，整个工程流程包括：

数据爬虫，使用Node.js和正则表达式单线程抓取；

文本预处理，使用规则列表生成游戏道具数据库和同义词词库，统计词库单词出现的词频（使用拓扑排序进行粗粒度的单词消歧）；

数据处理， 基于分词、预定义规则和正则表达式，进行账号文本向量化；

模型训练，使用Tensorflow，模型为三层神经元的MLP回归模型；

模型调用，使用Flask搭建服务器；

网页访问，使用Vuetify实现网页，使用fontmin消减版的自定义字体。

如有预测结果不甚理想，请君笑之。

### 1. dataspider 数据爬虫
咩咩估价从代售阁和盆栽蹲号收集了一个月以来的13万条账号记录，从中去除无效和重复账号后，剩余44387条账号记录。

数据爬虫部分使用Node.js实现。为了防止高频率的数据抓取被目标服务器拒绝，爬虫使用单线程处理。

抓取的数据将存储在MongoDB中，请先安装MongoDB。

|文件|描述|
|----|----|
|dataspider/spider.mjs|账号信息爬虫|

使用方法

```
cd dataspider
npm run spider
```

### 2. nlppack 文本预处理
咩咩估价使用结巴分词进行中文分词处理。由于外观名称和通常的汉语词语差距较大，需要提前生成外观词库和外观同义词标注。

|文件|描述|
|----|----|
|nlppack/createdb.py|生成外观词库和外观同义词标注|
|nlppack/gen_dict.py|生成词频统计|


```
python3 nlppack/createdb.py
python3 nlppack/gen_dict.py
```

### 3. data 数据处理
|文件|描述|
|----|----|
|data/gen_data.py|游戏账号向量化|
|data/gen_training_data.py|生成训练数据|

```
python3 data/gen_data.py
python3 data/gen_training_data.py
```

### 4. model 模型训练


|文件|描述|
|----|----|
|model/training.py|使用keras的简单多层感知机，代码为训练萝莉的样例，可以自行修改|
```
python3 model/training.py
```

### 5. server 估价模型部署和服务器

|文件|描述|
|----|----|
|sserver/app.py|使用Flask的简单Restful服务器|

```
cd server
flask run
```
### 6. miemie 估价器网页前端

```
cd miemie
npm run build
```

## Q&A 问题解答

### 1. 为什么我加了红年轮/ 脚气马/ 里飞沙价格反而变低了呢？
咩咩估价只能获取大致的价格范围，不会特别精确，毕竟是人工智能模型（通俗地说）自动算的……我也不知道人工智障是怎么想的！目前还是娱乐为主

### 2. 为什么我的白板号都能有2000块？
因为2000以下的号，和2000以上的号，价格构成比例差别很大。在几百元、一千元这个级别的选手，装备、拓印占了比较大的比重，而这些在当前的咩咩估价里面没有做很多的考虑。

为了追求更高的准确度，当前的咩咩估价抛弃了2000元以下的账号数据，只参考了2000元以上的账号数据，所以会出现这种“白板号都有2000块的现象”。

### 3. 咩咩估价是怎么计算的呢？
有一只咩咩在网线后面，收到消息，进行估价，返回结果。（划掉） 咩咩估价使用了人工神经网络作为数值工具，没有过多地人为干扰，预测结果都是人工智障的学习成果。

### 4. 咩咩估价从哪里学习账号价格信息呢？
咩咩估价从代售阁和盆栽蹲号收集了一个月以来的13万条账号记录，从中去除无效和重复账号后，剩余44387条账号记录，其中70%超过2000元。咩咩从这里学习估价知识。

## ABOUT
The Miemie Price Estimation Project is the author's first try to use tensorflow to train artificial neural networks. The whole engineering process includes:

Data crawler, using Node.js and regular expression single-thread crawling;

Text preprocessing, using rule list to generate game props database and synonym thesaurus, counting the word frequency of thesaurus words (using topological sorting for coarse-grained word disambiguation);

In data processing, account text vectorization is carried out based on word segmentation, predefined rules and regular expressions.

Model training, using Tensorflow, model as MLP regression model of three-layer neurons;

Model call, using Flask to build the server;

Web page access, using Vuetify to achieve web pages, using fontmin subtractive version of the custom font.

If the forecast result is not very satisfactory, please laugh at it.

### 1. dataspider
The Miemie Price Estimation Project collects the data from j3dh.com and paopaox.com. 130000 account records have been collected over the past month, and after invalid and duplicate accounts have been removed, there are 44387 account records left.

The data crawler part is implemented using Node.js. In order to prevent high-frequency data fetching from being rejected by the target server, the crawler uses single-threaded processing.

The crawled data will be stored in mongodb, so please install mongodb first.

Usage

```
cd dataspider
npm run spider
```

### 2. nlppack
The Miemie Price Estimation Project uses the Jieba Library for Chinese text segmentation. As there is a big gap between the game prop name and the common Chinese words, it is necessary to generate the game prop name thesaurus and the game prop name synonym tagging first.

|file|description|
|----|----|
|nlppack/createdb.py|to generate the game prop name thesaurus and the game prop name synonym tagging|
|nlppack/gen_dict.py|Generate word frequency statistics|

```
python3 nlppack/createdb.py
python3 nlppack/gen_dict.py
```

### 3. data

TODO
```
python3 data/gen_data.py
python3 data/gen_training_data.py
```

### 4. model

```
python3 mode/training.py
```

### 5. server
```
cd server
flask run
```
### 6. miemie
```
cd miemie
npm run build
```
