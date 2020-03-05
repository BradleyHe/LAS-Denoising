import torch
import yaml
from util.timit_dataset import create_dataloader
from model.las_model import Listener,Speller
from util.functions import batch_iterator
import numpy as np
from torch.autograd import Variable
import sys
import pandas as pd
from six.moves import cPickle
import os


def load_dataset(data_path,**kwargs):
    with open(data_path, 'rb') as cPickle_file:
        [X_test, y_test] = cPickle.load(cPickle_file)
    for data in [ X_test, y_test]:
        assert len(data) > 0
    return X_test, y_test

config_path = 'config/las_denoised_test_config.yaml'
tir = [-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]

conf = yaml.load(open(config_path,'r'))
os.makedirs('pkl', exist_ok=True)   

for category in ['noisy', 'denoised']:
    for num in range (1, 11):
        data = {}
        for ratio in tir:
            global_step = 0
            total = 0

            conf['meta_variable']['data_path'] = 'pkl/{}/timit_mfcc_39_{}_{}.pkl'.format(num, category, ratio)

            X_test, y_test = load_dataset(**conf['meta_variable'])
            test_set = create_dataloader(X_test, y_test, **conf['model_parameter'], **conf['training_parameter'], shuffle=False)

            listener = torch.load(conf['training_parameter']['pretrained_listener_path'], map_location=lambda storage, loc: storage)
            speller = torch.load(conf['training_parameter']['pretrained_speller_path'], map_location=lambda storage, loc: storage)
            optimizer = torch.optim.Adam([{'params':listener.parameters()}, {'params':speller.parameters()}], lr=conf['training_parameter']['learning_rate'])

            for batch_index,(batch_data,batch_label) in enumerate(test_set):
              batch_loss, batch_ler = batch_iterator(batch_data, batch_label, listener, speller, optimizer, 0, is_training=False, **conf['model_parameter'])
              total += np.array(batch_ler).mean()
              global_step += 1
              print('PER for {}: {}'.format(ratio, total / global_step), end='\r', flush=True)

            data[ratio] = [total / global_step]
            print()

            df = pd.DataFrame(data)
            df.to_csv('pkl/{}_{}_trained.csv'.format(num, category))
        df = pd.DataFrame(data)
        df.to_csv('pkl/{}_{}_trained.csv'.format(num, category))