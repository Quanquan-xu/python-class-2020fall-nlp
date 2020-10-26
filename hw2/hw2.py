from nltk.metrics import *
import pandas as pd
import numpy as np
import  os,sys
import argparse

def init_files(auto=True):
    files = ["1476382.male.33.Publishing.Gemini.xml","470861.male.27.indUnk.Cancer.xml","780903.male.25.Student.Aquarius.xml"]
    sentences = []
    positions = []
    for file in files:
        content = open(file, "rt", encoding='latin1')
        text = content.read()
        contents = text.split("<post>")
        posts = list(map(lambda x: x.split("</post>")[0].strip(), contents[1:]))
        posts = list(filter(lambda x: len(x) > 0, posts))
        position = (np.arange(len(posts))+1).astype(str)
        position = list(map(lambda x: file + "-" + x, position))
        sentences.extend(posts)
        positions.extend(position)
    sentences = list(filter(lambda x: len(x) > 0, sentences))
    length = list(map(lambda x: len(x.replace('\n','').replace('\t','')), sentences))
    max_length = max(length)
    min_length = min(length)
    size = len(length)
    # ser = pd.Series(length)
    # ser = ser.sort_values(ascending=True)
    # print(ser)
    # sys.exit()
    if auto and os.path.exists("max_distance_candidates.csv") and os.path.exists("min_distance_candidates.csv"):
        df1 = pd.read_csv('max_distance_candidates.csv')
        df2 = pd.read_csv('min_distance_candidates.csv')
    else:
        min_distance_set = np.arange(size*size).reshape((size, size)).astype(float)
        max_distance_set = np.arange(size*size).reshape((size, size)).astype(float)

        for i in range(0,size):
            for j in range(0,size):
                if i > j:
                    min_distance_set[i][j] = np.NaN
                    max_distance_set[i][j] = np.NaN
                elif i == j:
                    min_distance_set[i][j] = np.NaN
                    max_distance_set[i][j] = np.NaN
                else:
                    min_distance_set[i][j] = abs(length[i]-length[j])
                    max_distance_set[i][j] = max(length[i], length[j])
        min_flatten = min_distance_set.flatten()
        max_flatten = max_distance_set.flatten()
        #sort_min_distance_set = np.sort(min_distance_set, axis=None)
        #sort_max_distance_set = np.sort(max_distance_set, axis=None)
        sort_min_distance_set = np.sort(min_flatten[~np.isnan(min_flatten)])
        sort_max_distance_set = np.sort(max_flatten[~np.isnan(max_flatten)])
        max_min_reference = sort_min_distance_set[-10]
        min_max_reference = sort_max_distance_set[0]

        max_distance_candidates = []
        min_distance_candidates = []

        for i in range(0,size):
            for j in range(0,size):
                _max = max_distance_set[i][j]
                _min = min_distance_set[i][j]
                if _max >= max_min_reference:
                    max_distance_candidates.append((i,j,-1,_min,_max))
                if _min <= min_max_reference:
                    min_distance_candidates.append((i,j,-1,_min,_max))
        df1 = pd.DataFrame(max_distance_candidates, columns= ['i' ,'j','distance','min', 'max'])
        df2 = pd.DataFrame(min_distance_candidates, columns= ['i' ,'j','distance','min', 'max'])
        df1 = df1.sort_values(by=['max','min'], ascending=False).astype(int)
        df2 = df2.sort_values(by=['min','max'], ascending=True).astype(int)
        df1.to_csv ('max_distance_candidates.csv', index = False, header=True)
        df2.to_csv ('min_distance_candidates.csv', index = False, header=True)
    return [sentences,positions,df1,df2]

def calculate_max_edit_distance(sentences,df, file_name):
    count = 0
    max_index = 0
    for index, row in df.iterrows():
        _distance = df.iloc[index]["distance"]
        if _distance < 0:
            print("index:", index)
            i_sentence = sentences[row["i"]].replace('\n','').replace('\t','')
            j_sentence = sentences[row["j"]].replace('\n','').replace('\t','')
            df.iloc[index]["distance"] = edit_distance(i_sentence,j_sentence)
            count += 1
        if count and not count % 2:
            df.to_csv (file_name, index = False, header=True)
        if index >=100:
            max_index = index
            df.to_csv (file_name, index = False, header=True)
            break
    return df[:max_index]
def calculate_min_edit_distance(sentences,df, file_name):
    count = 0
    max_index = 0
    for index, row in df.iterrows():
        _distance = df.iloc[index]["distance"]
        _min = df.iloc[index]["min"]
        if _distance < 0 and _min == 0:
            print("index:", index)
            i_sentence = sentences[row["i"]].replace('\n','').replace('\t','')
            j_sentence = sentences[row["j"]].replace('\n','').replace('\t','')
            df.iloc[index]["distance"] = edit_distance(i_sentence,j_sentence)
            count += 1
        if count and not count % 2:
            df.to_csv (file_name, index = False, header=True)
        if _min >= 1:
            df.to_csv (file_name, index = False, header=True)
            max_index = index
            break
    return df[:max_index]
parser = argparse.ArgumentParser(description='manual to edit distance')
parser.add_argument('--model', type=str, default="all")
args = parser.parse_args()
model = args.model
if model == 'all':
    parmaters = init_files()
    sentences = parmaters[0]
    positions = parmaters[1]
    df1 = parmaters[2]
    df2 = parmaters[3]
    calculate_edit_distance(df1,"max_distance_candidates.csv")
    calculate_edit_distance(df2,"min_distance_candidates.csv")
elif model == 'init':
    init_files(False)
elif model == 'max':
    print("Calculating max edit distance......")
    parmaters = init_files()
    sentences = parmaters[0]
    positions = parmaters[1]
    df1 = parmaters[2]
    df = calculate_max_edit_distance(sentences, df1,"max_distance_candidates.csv")
    df = df.sort_values(by='distance', ascending=False)
    index = 0
    print("\n\nTop 10 max edit distance....")
    for _, row in df.iterrows():
        i_sentence = sentences[row["i"]]
        i_position = positions[row['i']]
        j_sentence = sentences[row["j"]]
        j_position = positions[row['j']]
        distance = row["distance"]
        print("#"*30)
        print("Top", index+1)
        print("distance:", distance)
        print("i_sentence:",i_position,'\n', i_sentence)
        print("j_sentence:",j_position,'\n',j_sentence)
        print("\n\n\n")
        index +=1
        if index == 10:
            break
elif model == 'min':
    print("Calculating min edit distance......")
    parmaters = init_files()
    sentences = parmaters[0]
    positions = parmaters[1]
    df2 = parmaters[3]
    df = calculate_min_edit_distance(sentences, df2,"min_distance_candidates.csv")
    df = df.sort_values(by='distance')
    index = 0
    print("\n\nTop 10 min edit distance....")
    for _, row in df.iterrows():
        i_sentence = sentences[row["i"]]
        i_position = positions[row['i']]
        j_sentence = sentences[row["j"]]
        j_position = positions[row['j']]
        distance = row["distance"]
        print("#"*30)
        print("Top", index+1)
        print("distance:", distance)
        print("i_sentence:",i_position,'\n', i_sentence)
        print("j_sentence:",j_position,'\n',j_sentence)
        print("\n\n\n")
        index +=1
        if index == 10:
            break
else:
    print("Please input valid model keyword")
