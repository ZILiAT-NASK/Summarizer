# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/Summarizer/LICENSE

import logging
import os
import sys


libs_dir = os.path.dirname(os.path.abspath(__file__))
txt_dir = os.path.abspath(os.path.join(libs_dir, '../../../data/txt'))
meta_dir = os.path.abspath(os.path.join(libs_dir, '../../../data/meta'))
out_dir = os.path.abspath(os.path.join(libs_dir, '../../../data/out/txt'))
log_dir = os.path.abspath(os.path.join(libs_dir, '../../../data/log'))
nltk_data_dir = os.path.abspath(os.path.join(libs_dir, '../../../data/nltk_data'))


def file_iterator():
    for dirpath, dirnames, filenames in os.walk(txt_dir):
        for counter, filename in enumerate([fn for fn in filenames if fn.lower().endswith('.txt')]):
            fp_in = os.path.join(dirpath, filename)
            fp_out = os.path.join(dirpath.replace(txt_dir, out_dir), filename.replace('.txt', r'_{}.txt'))
            yield fp_in, fp_out


def get_stopwords_file():
    return os.path.join(libs_dir, 'stopwords.txt')


def get_logger(file: str, name: str, overwrite=False) -> logging.Logger:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    log_file = os.path.join(log_dir, f'{file}_debug.log')
    if overwrite and os.path.exists(log_file):
        os.unlink(log_file)
    fhd = logging.FileHandler(log_file, encoding='utf-8')
    fhd.setLevel(logging.DEBUG)
    fhd.setFormatter(formatter)

    log_file = os.path.join(log_dir, f'{file}_info.log')
    if overwrite and os.path.exists(log_file):
        os.unlink(log_file)
    fhi = logging.FileHandler(log_file, encoding='utf-8')
    fhi.setLevel(logging.INFO)
    fhi.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(fhd)
    logger.addHandler(fhi)
    return logger
