from torch.utils.data.dataset import TensorDataset
import torch
from torch.utils.data import Dataset
import numpy as np
from preprocessors import *

class AsciiModDataset(Dataset):
    def __init__(self, SENTENCE_LENGTH):
        # ファイルを読み込みモードで開く
        wiki_dataset = []
        with open('./dataset/wikitext-2/wiki.train.tokens', 'r') as file:
            # ファイルの内容を一行ずつ読み込む
            for line in file:
                # 読み込んだ行を処理する（例えば表示する）
                wiki_dataset.append(line)
        with open('./dataset/wikitext-2/wiki.valid.tokens', 'r') as file:
            # ファイルの内容を一行ずつ読み込む
            for line in file:
                # 読み込んだ行を処理する（例えば表示する）
                wiki_dataset.append(line)
        with open('./dataset/wikitext-2/wiki.test.tokens', 'r') as file:
            # ファイルの内容を一行ずつ読み込む
            for line in file:
                # 読み込んだ行を処理する（例えば表示する）
                wiki_dataset.append(line)

        # 文字とエンコードの組み合わせをひたすら組み合わせる
        chars, ames = datapipe_to_char_and_ame(wiki_dataset, SENTENCE_LENGTH)
        
        # idに変換
        char_class_list = [[char_to_classid(c) for c in cs] for cs in chars]
        ascii_mod_list = ames

        self.dataset = TensorDataset(torch.tensor(ascii_mod_list, dtype=torch.int64), torch.tensor(char_class_list, dtype=torch.int64))
        self.char_list = chars

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, index):
        return self.dataset[index]
    
    def get_char_and_dataset(self, index):
        return self.char_list[index], self.dataset[index]