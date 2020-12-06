import tensorflow as tf
import numpy as np
import time
import os

# 生成样本数据
x = np.random.randn(10000, 1)
y = 0.03 * x + 0.8

# 定义模型参数
Weights = tf.Variable(tf.random_normal([1], seed=1, stddev=1), name='Weights')
bias = tf.Variable(tf.random_normal([1], seed=1, stddev=1), name='bias')

xx = tf.placeholder(tf.float32, shape=(None, 1), name='xx')
yy = tf.placeholder(tf.float32, shape=(None, 1), name='yy')

# 线性模型
y_predict = tf.add(Weights * xx, bias, name='predict')

# 损失函数
loss = tf.reduce_mean(tf.square(yy - y_predict))

# 优化方法
optimizer = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

with tf.Session() as sess:
    init_var = tf.global_variables_initializer()
    sess.run(init_var)
    version = str(int(time.time()))
    builder = tf.saved_model.builder.SavedModelBuilder(os.path.join('saved_model', version))
    print('before training, variable is %s,%s' % (sess.run(Weights), sess.run(bias)))
    for i in (range(5000)):

        sess.run(optimizer, feed_dict={xx: [x[i]], yy: [y[i]]})

        if (i + 1) % 1000 == 0:
            print(sess.run(loss, feed_dict={xx: [x[i]], yy: [y[i]]}))

    # 构建 signature
    signature = tf.saved_model.build_signature_def(
        # 获取输入输出的信息（shape,dtype等），在部署服务后请求带来的数据会喂到inputs中，服务吐的结果会以outputs的形式返回
        inputs={"input": tf.saved_model.utils.build_tensor_info(xx)},  # 获取输入tensor的信息，这个字典可以有多个key-value对
        outputs={"output": tf.saved_model.utils.build_tensor_info(y_predict)},  # 获取输出tensor的信息，这个字典可以有多个key-value对
        method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME  # 就是'tensorflow/serving/predict'
    )
    builder.add_meta_graph_and_variables(sess, ['test'], signature_def_map={"serving_default": signature})
    builder.save()
    print('after training, variable is %s,%s' % (sess.run(Weights), sess.run(bias)))
    
"""
saved_model_dir = "./saved_model/1607274900"

with tf.Session() as sess:
    # tf.saved_model.tag_constants.SERVING == "serve"，这里load时的tags需要和保存时的tags一致
    meta_graph_def = tf.saved_model.loader.load(sess, tags=["test"], export_dir=saved_model_dir)
    signature = meta_graph_def.signature_def
    print(signature)  # signature 内包含了保存模型时，signature_def_map 的信息

    check_input = sess.graph.get_tensor_by_name("Weights:0")
    print(sess.run(check_input))
"""