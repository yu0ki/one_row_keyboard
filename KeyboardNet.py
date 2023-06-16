import torch
import torch.nn as nn
from transformers import BertConfig
from transformers import BertModel
torch.backends.cudnn.benchmark = True
torch.backends.cuda.max_split_size_mb = 0

class KeyboardNet(nn.Module):
    def __init__(self, SENTENCE_LENGTH, mlp_hidden_layers, num_class):
        super(KeyboardNet, self).__init__()
        # https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html
        # とりあえず全部デフォ値
        # self.transformer = nn.Transformer(d_model=SENTENCE_LENGTH)
        # BERTの設定を定義
        self.bert_config = BertConfig(
            vocab_size=12,
            hidden_size=768, # bertの最終層出力の次元数
            num_attention_heads=12,
            num_hidden_layers=6,
            intermediate_size=3072,
            max_position_embeddings=512,
        )
        self.bert_encoder = BertModel(self.bert_config)
        self.classification_dropout = nn.Dropout(0.2)

        # inputの数字(ame)によって入力する線形層の位置を変える
        self.linear1 = nn.Linear(self.bert_config.hidden_size * SENTENCE_LENGTH, mlp_hidden_layers * SENTENCE_LENGTH)

        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.2)
        self.linear2 = nn.Linear(mlp_hidden_layers * SENTENCE_LENGTH, num_class * SENTENCE_LENGTH)
        # self.softmax = nn.Softmax(dim=1)

        self.SENTENCE_LENGTH = SENTENCE_LENGTH
    
    def forward(self, input_datas, attention_masks):
        bert_output = self.bert_encoder(input_datas, attention_masks)["last_hidden_state"].view(-1, self.bert_config.hidden_size  * self.SENTENCE_LENGTH)
        cl_drouput = self.classification_dropout(bert_output)
        linear_output = self.linear1(cl_drouput)
        relu_output = self.relu1(linear_output)
        dropout_output = self.dropout1(relu_output)
        linear2_output = self.linear2(dropout_output)
        return linear2_output
