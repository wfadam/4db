import tensorflow as tf
import numpy as np
from random import shuffle
 
train_input = ['{0:010b}'.format(i) for i in range(2**10)]
shuffle(train_input)
train_input = [map(int,i) for i in train_input]
ti  = []
for i in train_input:
    temp_list = []
    for j in i:
            temp_list.append([j])
    ti.append(np.array(temp_list))
train_input = ti
#print(train_input)	#a8w4db

train_output = []
for i in train_input:
    count = 0
    for j in i:
        if j[0] == 1:
            count+=1
    temp_list = ([0]*11)
    temp_list[count]=1
    train_output.append(temp_list)
#print(train_output)	#a8w4db


NUM_EXAMPLES = 400
test_input = train_input[NUM_EXAMPLES:]
test_output = train_output[NUM_EXAMPLES:] #everything beyond NUM_EXAMPLES
 
train_input = train_input[:NUM_EXAMPLES]
train_output = train_output[:NUM_EXAMPLES] #till NUM_EXAMPLES

#a8w4db--
#for inData, outData in zip(train_input, train_output):
#	print("%s -> %s\n" % (inData, outData))
#--


data = tf.placeholder(tf.float32, [None, 10,1])
target = tf.placeholder(tf.float32, [None, 11])

num_hidden = 8
cell = tf.contrib.rnn.core_rnn_cell.LSTMCell(num_hidden,state_is_tuple=True)
val, state = tf.nn.dynamic_rnn(cell, data, dtype=tf.float32)
val = tf.transpose(val, [1, 0, 2])
last = tf.gather(val, int(val.get_shape()[0]) - 1)

weight = tf.Variable(tf.truncated_normal([num_hidden, int(target.get_shape()[1])]))
bias = tf.Variable(tf.constant(0.1, shape=[target.get_shape()[1]]))
#bias = tf.Variable(tf.truncated_normal([target.get_shape()[1]]))#a8w4db
prediction = tf.nn.softmax(tf.matmul(last, weight) + bias)
cross_entropy = -tf.reduce_sum(target * tf.log(tf.clip_by_value(prediction,1e-10,1.0)))

optimizer = tf.train.AdamOptimizer()
minimize = optimizer.minimize(cross_entropy)

mistakes = tf.not_equal(tf.argmax(target, 1), tf.argmax(prediction, 1))
error = tf.reduce_mean(tf.cast(mistakes, tf.float32))

init_op = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init_op)

batch_size = 4
no_of_batches = int(len(train_input)/batch_size)
epoch = 500
for i in range(epoch):
    ptr = 0
    for j in range(no_of_batches):
        inp, out = train_input[ptr:ptr+batch_size], train_output[ptr:ptr+batch_size]
        ptr+=batch_size
        sess.run(minimize,{data: inp, target: out})
    if i%100 == 99:
        incorrect = sess.run(error,{data: test_input, target: test_output})
        print('Epoch {:2d} error {:3.1f}%'.format(i + 1, 100 * incorrect))
incorrect = sess.run(error,{data: test_input, target: test_output})
print('Epoch {:2d} error {:3.1f}%'.format(i + 1, 100 * incorrect))
sess.close()

