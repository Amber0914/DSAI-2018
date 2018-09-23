#-*- coding: utf-8 -*-
# amber 20180312
import pandas as pd

def MakeKeywordList(query_data, keyword_list,keyword_dictionary):
    for line in query_data:
        line=line.split()
        for i in range(0,len(line),2):
            if line[i] not in keyword_dictionary.keys():
                keyword_list.append(line[i])
                keyword_dictionary.setdefault(line[i], [])

def MakeKeywordDictionary(data, keyword_list, keyword_dictionary):
    list_length=len(keyword_list)
    for number in data['index']:
        line = data['title'][number-1]
        for i in range(0,list_length,1):
            if keyword_list[i] in line:
                    keyword_dictionary[keyword_list[i]].append(number)

def Search(query_data, keyword_dictionary):
    query_data.seek(0)
    final_answer=[]
    for line in query_data:
        line=line.split()
        answer=keyword_dictionary[line[0]]
        if(line[1] == "and"):
            for i in range(2,len(line),2):
                pick=keyword_dictionary[line[i]]
                pick=set(pick)
                answer= [val for val in answer if val in pick]
        elif (line[1]== "not"):
            for i in range(2,len(line),2):
                pick=keyword_dictionary[line[i]]
                pick=set(pick)
                answer= [val for val in answer if val not in pick]
        elif(line[1]=="or"):
            for i in range(2,len(line),2):
                pick=keyword_dictionary[line[i]]
                answer=list(set(answer).union(pick))
            answer.sort()
        if len(answer) == 0:
            answer.append(0)
        final_answer.append(answer)
    return final_answer

def WriteAnswer(answer_data):
    f=open(args.output, mode='wt', encoding='utf-8',newline='')
    for line in answer_data:
        answer=str(line).strip('[').strip(']').replace(', ',',')
        f.write(answer)
        if(line!=answer_data[-1]):
            f.write("\n")

if __name__ == '__main__':
    # You should not modify this part.
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--source',
                        default='source.csv',
                        help='input source data file name')
    parser.add_argument('--query',
                        default='query.txt',
                        help='query file name')
    parser.add_argument('--output',
                        default='output.txt',
                        help='output file name')
    args = parser.parse_args()

    data=pd.read_csv(args.source, names=['index','title'])
    query=open(args.query,'r',encoding='UTF-8')

    keyword_list=[]
    keyword_dictionary={}

    MakeKeywordList(query, keyword_list, keyword_dictionary)
    MakeKeywordDictionary(data, keyword_list, keyword_dictionary)
    ans=Search(query, keyword_dictionary)
    WriteAnswer(ans)
