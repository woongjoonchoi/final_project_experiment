import os

from datasets import load_dataset


def load_data(data_args):
    PATH = data_args.dataset_name
    datasets = load_dataset('csv', data_files={'train':os.path.join(PATH, 'train_small.csv'), 'validation': os.path.join(PATH, 'valid_small.csv')})
    print(datasets)