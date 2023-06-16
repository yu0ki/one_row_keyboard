# １単語をascii_mod_encodeに変換
def char_to_ame(char:str):
    # padは0
    if char == "<pad>":
        return 0

    # clsは10
    if char == "<cls>":
        return 10

    # sepは11
    if char == "<sep>":
        return 11

    # スペースだけ9
    if char == "<sp>":
        return 9
    
    # そうでない場合は、ASCII(2進)の下３桁
    try:
        mod = ord(char) % 8 
    except:
        print(char)

    if mod == 0:
        ame = 8
    else:
        ame = mod
    return ame


# 1sentenceをascii_mod_encodeのリストに変換
def sentence_to_ames(sentence:str):
    s_split = sentence_to_chars(sentence)
    ames = []
    # 特殊文字の変換
    for char in s_split:
        ames.append(char_to_ame(char))
    return ames
# print(sentence_to_ames("I am a student of Kyoto University."))


# 文章を一文字ずつにバラして、スペースを特殊トークン<sp>に置き換える
def sentence_to_chars(sentence:str):
    chars = []
    for char in list(sentence):
        if char == " ":
            chars.append("<sp>")
        else:
            chars.append(char)
    return chars

# AMEを受け取って、可能な文字一覧を返す
ascii_list = [(i, chr(i)) for i in range(32, 65)] + [(i, chr(i)) for i in range(95, 127)]
def ame_to_possible_chars(ame:int):
    if ame == 9:
        return ["<sp>"]

    if ame == 10:
        return ["<cls>"]
    
    if ame == 11:
        return ["<sep>"]
    
    if ame == 0:
        return ["<pad>"]

    chars = []
    if ame == 8:
        for (i, c) in ascii_list:
            if i % 8 == 0:
                chars.append(c)
    else:
        for (i, c) in ascii_list:
            if i % 8 == ame:
                chars.append(c)
    if " " in chars:
        chars.remove(" ")

    return chars
for i in range(0, 12):
    print(ame_to_possible_chars(i))


def char_to_classid(char:str):
    if char == "<sp>" or char == "<pad>" or char == "<sep>" or char == "<cls>":
        return 0
    
    char = char.lower()
    ame = char_to_ame(char)
    possible_chars = ame_to_possible_chars(ame)
    try:
        return possible_chars.index(char)
    except:
        # 対応外のやつはとりあえず0で返す
        # print("this is not in classid list ", char)
        return 0


def datapipe_to_char_and_ame(dataset, SENTENCE_LENGTH):
    chars = []
    ames = []
    for d in dataset:
        d = d[1:].replace('\n', '').replace("<unk>", "")

        # asciiコード0~127までで表せないものは削除
        d = ''.join(char for char in d if ord(char) < 128)

        if d == "":
            continue

        # 先頭が=のデータを削除
        if d[0] == "=":
            continue

        # ascii_mod_encodeのリストに変換
        encoded_d = sentence_to_ames(d)
        # dを分割
        d_split = sentence_to_chars(d)
        # print(len(encoded_d), len(d_split))


        # words, amesにデータ追加
        sent_ln = SENTENCE_LENGTH - 2
        while len(encoded_d) > sent_ln:
            # リスト中の一番最後の<sp>で分割
            try:
                last_index = sent_ln - d_split[:sent_ln][::-1].index("<sp>") - 1
            except ValueError:
                # <sp>が存在しない場合
                last_index = sent_ln

            ames.append([10] + encoded_d[:last_index] + [11] + [0 for _ in range(sent_ln - last_index)])
            chars.append(["<cls>"] + d_split[:last_index] + ["<sep>"] + ["<pad>" for _ in range(sent_ln - last_index)])
            encoded_d = encoded_d[last_index + 1:]
            d_split = d_split[last_index + 1:]

        
        # paddingは0
        if len(encoded_d) > 0:
            # <cls>と<sep>を追加
            # それぞれ10と11を割り当てる
            encoded_d = [10] + encoded_d + [11]
            encoded_d += [0 for _ in range(SENTENCE_LENGTH - len(encoded_d))]
            ames.append(encoded_d)

            d_split = ["<cls>"] + d_split + ["<sep>"]
            d_split += ["<pad>" for _ in range(SENTENCE_LENGTH  - len(d_split))]
            chars.append(d_split)
    
    return chars, ames
