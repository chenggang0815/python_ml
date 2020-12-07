# coding=utf-8
import tensorflow as tf

# 第一个是参数名称，第二个参数是默认值，第三个是参数描述
tf.app.flags.DEFINE_string('str_name', 'def_v_1', "descrip1")
tf.app.flags.DEFINE_integer('int_name', 10, "descript2")
tf.app.flags.DEFINE_boolean('bool_name', False, "descript3")

FLAGS = tf.app.flags.FLAGS


# 必须带参数，否则：'TypeError: main() takes no arguments (1 given)';  main的参数名随意定义，无要求
def main(_):
    print(FLAGS.str_name)
    print(FLAGS.int_name)
    print(FLAGS.bool_name)


if __name__ == '__main__':
    tf.app.run()
    # 执行main函数

'''
import sys
 
from absl import app
from absl import flags
from absl import logging
 
#设置参数，第一个是参数名称，第二个是参数默认值，无默认值可取None，第三个是参数解释
flags.DEFINE_string('str_1', 'hello',
                    'Input a string.')
flags.DEFINE_string('str_2', 'world',
                    'Input a string.')
 
flags.DEFINE_integer('num_1', 0,
                     'Input a integer.')
flags.DEFINE_integer('num_2', 0,
                     'Input a integer.')
 
FLAGS = flags.FLAGS
 
def main(argv=()):
    del argv
    #打印时间，以及Python版本号
    version = sys.version_info
    logging.info('Running under Python {0[0]}.{0[1]}.{0[2]}'.format(version))
 
    str3 = FLAGS.str_1 + FLAGS.str_2  #计算输入两个字符串的和-拼接字符串
    print(str3)
    c = FLAGS.num_1 * FLAGS.num_2   #计算输入两个整数的积
    print(c)
 
# 如果当前是从其它模块调用的该模块程序，则不会运行main函数！
# 而如果就是直接运行的该模块程序，则会运行main函数。
if __name__ == '__main__':
    flags.mark_flag_as_required('str_1')
    flags.mark_flag_as_required('str_2')
    flags.mark_flag_as_required('num_1')
    flags.mark_flag_as_required('num_2')
    # 执行程序中main函数，并解析命令行参数！
    app.run(main)
'''
