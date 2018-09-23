## DSAI Hw2- BooleanSearch

## Command
```
 python3 main.py
```
## Loading Data
```
data=pd.read_csv(args.source, names=['index','title'])
query=open(args.query,'r',encoding='UTF-8')
```

## Data Processing

### MakeKeywordList
First, using list structure to store total keywords in query data.
then, initializing the  keyword_dictionary, it is a dictionary structure with multiple value each key.

```
def MakeKeywordList(query_data, keyword_list,keyword_dictionary):
    for line in query_data:
    line=line.split()
    for i in range(0,len(line),2):
        if line[i] not in keyword_dictionary.keys():
            keyword_list.append(line[i])
            keyword_dictionary.setdefault(line[i], [])
```

### MakeKeywordDictionary
In the  keyword_dictionary, key is the keyword from query data, which value is the index number of the title from in source data.
if the key is the substring of the string of the title, then recording the index number as its value.

```
def MakeKeywordDictionary(data, keyword_list, keyword_dictionary):
    list_length=len(keyword_list)
    for number in data['index']:
        line = data['title'][number-1]
        for i in range(0,list_length,1):
            if keyword_list[i] in line:
                keyword_dictionary[keyword_list[i]].append(number)
```

## Search
In seaching, time complexity of dictionary is better than list, we can find the key and its value  quickly, and the data structure of the value is a list.
For getting intersection, union and difference between two list quickly, we use the set( ) method to improve efficiency.

```
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
```

## Writing Data

```
def WriteAnswer(answer_data):
    f=open(args.output, mode='wt', encoding='utf-8',newline='')
    for line in answer_data:
        answer=str(line).strip('[').strip(']').replace(', ',',')
        f.write(answer)
        if(line!=answer_data[-1]):
            f.write("\n")
```

## Requirements
```
pandas==0.21.1
```

