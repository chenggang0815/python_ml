# coding=utf-8
import tensorflow as tf

#https://zhuanlan.zhihu.com/p/128546377
saved_model_dir = "./saved_model/xx"

with tf.Session() as sess:
    # tf.saved_model.tag_constants.SERVING == "serve"，这里load时的tags需要和保存时的tags一致
    model = tf.saved_model.loader.load(sess, tags=["test"], export_dir=saved_model_dir)

    weight = sess.graph.get_tensor_by_name("Weights:0")
    print(sess.run(weight))

    # 从signature_def_map 可以拿到输入和输出的tensor name
    # 从meta_graph_def中取出SignatureDef对象; signature内包含了保存模型时，signature_def_map 的信息
    signature = model.signature_def

    # 从signature中找出具体输入输出的tensor name
    input_tensor_name = signature["serving_default"].inputs["input"].name
    output_tensor_name = signature["serving_default"].outputs["output"].name

    # 获取tensor 并inference
    x = sess.graph.get_tensor_by_name(input_tensor_name)
    y = sess.graph.get_tensor_by_name(output_tensor_name)

    print(sess.run(y, feed_dict={x: [[100], [200]]}))
    # 上述步骤不需要知道具体的tensor的name。只需要从事先定义好中的signature中获取input和output的value





