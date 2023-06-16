import torch
from preprocessors import *
from KeyboardNet import KeyboardNet
import numpy as np

# ameのshapeは(-1, SENTENCE_LENGTH)
def ame_to_english(ames_list:list, model_outputs):
    result_list = []
    model_outputs = model_outputs.view(len(ames_list), len(ames_list[0]), -1)
    for ames, outputs in zip(ames_list, model_outputs):
        for a, o in zip(ames, outputs):
            if a not in [1, 2, 3, 4, 5, 6, 7, 8]:
                result_list.append(ame_to_possible_chars(a)[0])
            else:
                ame = torch.argmax(o)
                result_list.append(ame_to_possible_chars(a)[ame])
    return result_list


def english_to_result_list(sentence:str, model_name):
    SENTENCE_LENGTH = 32
    _, ames = datapipe_to_char_and_ame([" " + sentence], SENTENCE_LENGTH=SENTENCE_LENGTH)
    model = KeyboardNet(SENTENCE_LENGTH=SENTENCE_LENGTH, mlp_hidden_layers=120, num_class=8)
    model.load_state_dict(torch.load(model_name))
    model.eval()

    attention_masks = [[1 if a > 0 else 0 for a in fragment_ames] for fragment_ames in ames]
    output = model(torch.tensor(ames), torch.tensor(attention_masks))

    result_list = ame_to_english(ames_list=ames, model_outputs=output)
    return result_list

def english_to_english(sentence:str, model_name):
    result_list = english_to_result_list(sentence=sentence, model_name=model_name)

    text = ""
    for char in result_list:
        if char == "<sp>" or char == "<sep>":
            text += " "
        elif len(char) == 1:
            text+= char

    return text

input_text = "this is the best model of the one row keyboards."
model_name = "best_model_accuracy_0.7202258110046387"
print(english_to_english(sentence=input_text, model_name=model_name))