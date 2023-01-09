import numpy as np
import re
import warnings
import bz2
from gensim.models import KeyedVectors# gensim用来加载预训练词向量
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import pkuseg
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Bidirectional
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.model_selection import train_test_split
warnings.filterwarnings("ignore")

#导入词向量
with open("./embeddings/sgns.weibo.bigram", 'wb') as new_file, open("./embeddings/sgns.weibo.bigram.bz2", 'rb') as file:
    decompressor = bz2.BZ2Decompressor()
    for data in iter(lambda : file.read(100 * 1024), b''):
        new_file.write(decompressor.decompress(data))
cn_model = KeyedVectors.load_word2vec_format('./embeddings/sgns.weibo.bigram', binary=False, unicode_errors="ignore")

#读取文本
weibo = pd.read_csv('./data/all_data.txt',sep='\t', names=['is_not_rumor','content'],encoding='utf-8')
weibo = weibo.dropna()#删除缺失值
weibo.head()

content = weibo.content.values.tolist()
label=weibo.is_not_rumor.values.tolist()

#分词和tokenize
stopwords=pd.read_csv("./stopwords/stopwords.txt",index_col=False,sep="\t",quoting=3,names=['stopword'], encoding='utf-8')
stopwords = stopwords.stopword.values.tolist()#转为list形式

seg = pkuseg.pkuseg(model_name='web')  # 程序会自动下载所对应的细领域模型

train_tokens = []
for text in content:
    # 去掉标点
    text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "",text)
    # pkuseg分词
    cut_list = seg.cut(text)
    #去除停用词
    cut_list_clean=[]
    for word in cut_list:
        if word in stopwords:
            continue
        cut_list_clean.append(word)
    #索引化
    for i, word in enumerate(cut_list_clean): # enumerate()
        try:
            # 将词转换为索引index
            cut_list_clean[i] = cn_model.vocab[word].index
        except KeyError:
            # 如果词不在字典中，则输出0
            cut_list_clean[i] = 0
    train_tokens.append(cut_list_clean)

#索引长度标准化
num_tokens = [len(tokens) for tokens in train_tokens]
num_tokens = np.array(num_tokens)
max_tokens = np.mean(num_tokens) + 2 * np.std(num_tokens)
max_tokens = int(max_tokens)

#padding（填充）和truncating（修剪）
train_pad = pad_sequences(train_tokens, maxlen=max_tokens, padding='pre', truncating='pre')

num_words = 50000
embedding_dim=300
embedding_matrix = np.zeros((num_words, embedding_dim))
for i in range(num_words):
    embedding_matrix[i,:] = cn_model[cn_model.index2word[i]]#前50000个index对应的词的词向量
embedding_matrix = embedding_matrix.astype('float32')
np.sum(cn_model[cn_model.index2word[333]] == embedding_matrix[333] )
train_pad[train_pad>=num_words ] = 0
train_target = np.array(label)

# 90%的样本用来训练，剩余10%用来测试
X_train, X_test, y_train, y_test = train_test_split(train_pad, train_target, test_size=0.1, random_state=12)

#网络结构
model = Sequential()
model.add(Embedding(num_words, embedding_dim, weights=[embedding_matrix], input_length=max_tokens, trainable=False))
model.add(Bidirectional(LSTM(units=64, return_sequences=True)))
model.add(Bidirectional(LSTM(units=32, return_sequences=False)))
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
optimizer=Adam(lr=1e-3)

import os
# 建立一个权重的存储点
checkpoint_save_path="./checkpoint/rumor_LSTM.ckpt"
if os.path.exists(checkpoint_save_path+'.index'):
    print('----------load the model----------')
    model.load_weights(checkpoint_save_path)
checkpoint = ModelCheckpoint(filepath=checkpoint_save_path, monitor='val_loss', verbose=1, save_weights_only=True, save_best_only=True)
earlystopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1)
lr_reduction = ReduceLROnPlateau(monitor='val_loss', factor=0.1, min_lr=1e-8, patience=0, verbose=1)
callbacks = [earlystopping, lr_reduction]
model.compile(optimizer=optimizer,loss='binary_crossentropy', metrics=['accuracy'])

#训练模型
model.fit(X_train, y_train,validation_split=0.1,epochs=20,batch_size=128,callbacks=callbacks)
# model1.fit(X_train, y_train,validation_split=0.1,epochs=20,batch_size=128,callbacks=callbacks)

#对测试集进行预测
result = model.evaluate(X_test, y_test)
print('Accuracy:{0:.2%}'.format(result[1]))

#下面用训练好的模型对微博言论进行测试
#用model实例测试text_list中的文字
def predict_rumor_LSTM(text,label):
    print(text)
    # 去标点
    text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "",text)
    # 分词
    cut = seg.cut(text)
    #去除停用词
    cut_clean=[]
    for word in cut:
        if word in stopwords:
            continue
        cut_clean.append(word)
    # tokenize
    for i, word in enumerate(cut_clean):
        try:
            cut_clean[i] = cn_model.vocab[word].index
            if cut_clean[i] >= 50000:
                cut_clean[i] = 0
        except KeyError:
            cut_clean[i] = 0
    # padding
    tokens_pad = pad_sequences([cut_clean], maxlen=max_tokens, padding='pre', truncating='pre')
    # 预测
    dic={0:'谣言',1:'非谣言'}
    result = model.predict(x=tokens_pad)
    coef = result[0][0]
    if coef >= 0.5:
        print('实际是'+dic[label],'预测是非谣言','output=%.2f'%coef)
    else:
        print('实际是'+dic[label],'预测是谣言','output=%.2f'%coef)
    print('---------------------------------------------')

test_list = [
    '新闻发言人施毅陆军大校表示，东部战区近期在台岛周边海空域组织诸军兵种部队系列联合军事行动，成功完成各项任务，有效检验了部队一体化联合作战能力。战区部队将紧盯台海形势变化，持续开展练兵备战，常态组织台海方向战备警巡，坚决捍卫国家主权和领土完整。',
    '近日，山东德州。一女子报警称其坐公交车时被一70多岁老人猥亵。该老人故意坐到女孩身边，不断触碰女孩胳膊、肋部和大腿，女子掏出手机冷静录下视频证据。后老人下车逃跑，公交车司机也一同下车追了出去并报警。',
    '上海一名31岁外卖小哥胡先生，长期不喝白水喝饮料，近日突发尿毒症，医院连发三道病危通知。',
]
test_label=[1,0,0]
for i in range(len(test_list)):
    predict_rumor_LSTM(test_list[i],test_label[i])
