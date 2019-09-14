import numpy as np
import pandas as pd

from keras.layers import Input, Dense
from keras.models import Model, Sequential
from keras.layers import LeakyReLU
from keras.optimizers import Adam
from keras import backend as K
from keras.utils.vis_utils import plot_model
from keras.callbacks import LearningRateScheduler

from sklearn.metrics import mean_squared_error, mean_absolute_error

from tensorflow.python.client import device_lib

#Hyperparameters

N_LAYERS = 3
LAYER_SIZE = 64
ACTIVATION = 'tanh'
INPUT_SIZE = 46
OUTPUT_SIZE = 11
LEARNING_RATE = 0.01
BETA_1 = 0.9
BETA_2 = 0.999
EPSILON = 1e-08
LOSS_FUNCTION = 'binary_crossentropy'
EPOCHS = 100
EPOCHS_DROP = 5000
BATCH_SIZE = 128
DROP = 0.8

#Dataset processing

dataset = pd.read_csv('dataset.csv', delimiter = ",", engine = 'python')
dataset = dataset.dropna(axis=0, how='any')
train_X = dataset.values[:, :46]
train_Y = dataset.values[:, 46:]


#Neural Network Design
model =  Sequential()
model.add(Dense(LAYER_SIZE, input_dim = INPUT_SIZE, activation = ACTIVATION))
for i in range(N_LAYERS - 2):
        model.add(Dense(LAYER_SIZE, input_dim = INPUT_SIZE, activation = ACTIVATION))
model.add(Dense(OUTPUT_SIZE, activation = 'sigmoid'))


model.summary()
#plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=False)


#Training Procedure
def step_decay(epoch):
   initial_lrate = LEARNING_RATE
   drop = DROP
   epochs_drop = float(EPOCHS_DROP)
   lrate = initial_lrate * np.power(drop,  
           np.floor((1+epoch)/epochs_drop))
   return lrate

lrate = LearningRateScheduler(step_decay)

adam = Adam(lr=LEARNING_RATE, beta_1=BETA_1, beta_2=BETA_2, epsilon=EPSILON)
model.compile (loss = LOSS_FUNCTION, optimizer = adam, metrics = ['accuracy'])
history_callback = model.fit (train_X, train_Y, epochs = EPOCHS, batch_size = BATCH_SIZE, verbose = 2, callbacks=[lrate], validation_split=0.2)

#Save the model
print (K.get_session().graph)
model.save('marking_system_neural_network')
