#-*- coding: utf-8 -*-
# amber 20180312
import numpy as np
from numpy import nan
import pandas as pd
import sklearn
import random

def ReadData(csv):
    data=pd.read_csv(csv, names=["open","high","low","close"])
    return data

def MovingAverage(numpy_data,short_term, long_term):
    short_term_line=pd.Series(numpy_data['open']).rolling(window=short_term).mean()
    long_term_line=pd.Series(numpy_data['open']).rolling(window=long_term).mean()
    trading_line=np.sign(short_term_line-long_term_line)
    return(np.sign(trading_line-trading_line.shift(1)))

def TrainParameters(numpy_data):
    #default period
    short_term=8
    long_term=20
    trade=MovingAverage(numpy_data,short_term, long_term)
    ans=TrainReward(numpy_data, trade)
    #find better period
    test_times=35
    for i in range(0,test_times,1):
        x1=random.randint(5,10)
        x2=random.randint(12,20)
        trade=MovingAverage(numpy_data,x1, x2)
        now=TrainReward(numpy_data, trade)
        if now>ans:
            short_term=x1
            long_term=x2
            ans=now
    return(short_term, long_term)

def TrainReward(numpy_data,train_trade):
    paid = 0
    hold = 0
    maxDay=numpy_data.index.get_values().max()
    for i in range(0,maxDay,1):
        if pd.isnull(train_trade[i]):
            continue
        if i+1 == maxDay:
            if hold==1:#sold with close_price
                paid=paid+numpy_data["close"][i+1]
            elif hold==-1:
                paid=paid-numpy_data["close"][i+1]
            break
        if train_trade[i] == 0:
            continue
        elif train_trade[i] == 1:#next day, buy with open_price
            hold=hold+1
            paid=paid-numpy_data["open"][i+1]
        elif train_trade[i] == -1:#next day, sold with open_price
            hold=hold-1
            paid=paid+numpy_data["open"][i+1]
    return paid

def StrategyMake(numpy_data,predict_trade):
    strategy=[]
    maxDay=numpy_data.index.get_values().max()
    nowhold=0
    for i in numpy_data.index.values:
        if i == maxDay:
            break
        if pd.isnull(predict_trade[i]):
            strategy.append(0)
        if predict_trade[i] == 1:
            if nowhold==0:
                nowhold=1;
                strategy.append(1)
            else:
                strategy.append(0)
        elif predict_trade[i] == 0:
            strategy.append(0)
            continue
        elif predict_trade[i] == -1:
            if nowhold==1:
                nowhold=0;
                strategy.append(-1)
            else:
                strategy.append(0)
    return strategy

def StrategyReward(numpy_data,strategy):
    paid = 0
    hold = 0
    maxDay=numpy_data.index.get_values().max()
    for i in range(0,maxDay,1):
        if i+1 == maxDay:
            if hold==1:#sold with close_price
                paid=paid+numpy_data["close"][i+1]
            elif hold==-1:
                paid=paid-numpy_data["close"][i+1]
            break
        if strategy[i] == 0:
            continue
        elif strategy[i] == 1 and hold==0:#next day, buy with open_price
            hold=hold+1
            paid=paid-numpy_data["open"][i+1]
        elif strategy[i] == -1 and hold==1:#next day, sold with open_price
            hold=hold-1
            paid=paid+numpy_data["open"][i+1]
    return paid

if __name__ == '__main__':
    # You should not modify this part.
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                        default='training_data.csv',
                        help='input training data file name')
    parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')
    args = parser.parse_args()
        
    # The following part is an example.
    # You can modify it at will.

    training_data=ReadData(args.training)
    (predictshort_term, predictlong_term)=TrainParameters(training_data)
    
    testing_data=ReadData(args.testing)
    predict_trade=MovingAverage(testing_data,predictshort_term, predictlong_term)
    test_strategy=StrategyMake(testing_data, predict_trade)
    #print(predictshort_term," ",predictlong_term," ",StrategyReward(testing_data, test_strategy))
    np.savetxt('output.csv',test_strategy,fmt="%d")



