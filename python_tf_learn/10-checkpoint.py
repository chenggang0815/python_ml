# coding=utf-8
import tensorflow as tf
import numpy as np

# 生成样本数据
x = np.random.randn(10000, 1)
y = 0.03 * x + 0.8
# 定义模型参数
Weights = tf.Variable(tf.random_normal([1], seed=1, stddev=1), name='Weights')
bias = tf.Variable(tf.random_normal([1], seed=1, stddev=1), name='bias')
xx = tf.placeholder(tf.float32, shape=(None, 1), name='xx')
yy = tf.placeholder(tf.float32, shape=(None, 1), name='yy')
# 网络结构
y_predict = tf.add(Weights * xx, bias, name='predict')
# 损失函数
loss = tf.reduce_mean(tf.square(yy - y_predict))
# 优化方法
optimizer = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

with tf.Session() as sess:
    init_var = tf.global_variables_initializer()
    sess.run(init_var)
    saver = tf.train.Saver()
    print('before training, variable is %s,%s' % (sess.run(Weights), sess.run(bias)))
    for i in (range(10000)):
        sess.run(optimizer, feed_dict={xx: [x[i]], yy: [y[i]]})
        # 实现每1000步保存一次模型
        if (i + 1) % 1000 == 0:
            saver.save(sess, 'checkpoint/model.ckpt', global_step=i + 1)
            print("loss: {}".format(sess.run(loss, feed_dict={xx: [x[i]], yy: [y[i]]})))
    print('after training, variable is %s,%s' % (sess.run(Weights), sess.run(bias)))

"""
不需要重新定义好变量和网络结构
with tf.Session() as sess:
    saver = tf.train.import_meta_graph('checkpoint/model.ckpt-10000.meta')
    # saver.restore(sess, 'checkpoint/ckpt-10000')
    saver.restore(sess, tf.train.latest_checkpoint('checkpoint'))
    print("weight: {}".format(sess.run('Weights:0')))
    print("bias: {}".format(sess.run('bias:0')))
    # weight: [0.03000008]
    # bias: [0.79999954]
    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name("xx:0")
    feed_dict = {x: [[100.0], [200.0]]}

    y = graph.get_tensor_by_name("predict:0")
    print(sess.run(y, feed_dict))
    # [[3.8000073]
    # [6.8000154]]
"""

"""
# 需要提前重新定义好变量和网络结构
# 定义模型参数
w = tf.Variable([1.0], name='Weights')
bias = tf.Variable([1.0], name='bias')
x = tf.placeholder(tf.float32, shape=(None, 1), name='xx')
# 定义网络结构
y_predict = tf.add(w * x, bias, name='predict')

with tf.Session() as sess:
    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint('checkpoint'))
    print("weight: {}".format(sess.run(w)))
    print("bias: {}".format(sess.run(bias)))
    print("predict: {}".format(sess.run(y_predict, feed_dict={x: [[100.0], [200.0]]})))
    #predict: [[3.8000073],[6.8000154]]
"""
