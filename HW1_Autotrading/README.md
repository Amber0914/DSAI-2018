## DSAI H1- Autotrading

## Command
```
 python3 trader.py
```

## Loading Data
```
def ReadData(csv):
    data=pd.read_csv(csv, names=["open","high","low","close"])
    return data
```

## Moving Average, MA
A moving average (MA) is a statistic technique to get the trends in a dataset, and it is useful for predicting long-term trends.
With the long-term trends, it can help us decide when to buy/sell the stock.

* Formulation
```
N-days MovingAverage = N-days / N
```

* my MovingAverage function

    In this homework, the perfomance using open price is better than the performance using close price.

    We focus on the cross point on short_term_line and long_term_line, and that point help us decide when to buy/sell the stock( i.e. predict_trade )
    When short_term_line exceeds long_term_line, we buy a stock.
    When short_term_line falls below long_term_line, we sell a stock.

* note

    When using MovingAverage, we calculate the average price of the day with the data from  N-day before only. Therefore, when there is a cross point, we make buy/sell strategy immediately on that day. If there is no cross point, then our strategy is stay.

    When we get the cross point value, we convert it to 1, 0 ,-1 signal.
    
    If the signal is 1, we buy the stock.
    
    If the signal is -1, we sell the stock.
    
    If the signal is 0, we stay.

    Moreover, since the value for begining N-days is null value 'NaN',we use StrategyMake to rewrite our strategy and set 'NaN' as 0.

```
def MovingAverage(numpy_data,short_term, long_term):
    short_term_line=pd.Series(numpy_data['open']).rolling(window=short_term).mean()
    long_term_line=pd.Series(numpy_data['open']).rolling(window=long_term).mean()
    trading_line=np.sign(short_term_line-long_term_line)
    return(np.sign(trading_line-trading_line.shift(1)))
```

## Training period parameters
After observation, a good default setting is short_term=8 and long_term=20

To get the best setting, we test 35 times, and the best setting means we can get the most reward after training the data.

the range of short_term is  5≤ short_term ≤ 10.

the range of long_term is  12 ≤ long_term ≤ 20.

```
def TrainParameters(numpy_data):
    #default period
    short_term=8
    long_term=20
    trade=MovingAverage(numpy_data,short_term, long_term)
    ans=TrainReward(numpy_data, trade)
    #find better period
    test_times=20
    for i in range(0,test_times,1):
        x1=random.randint(7,10)
        x2=random.randint(30,35)
        trade=MovingAverage(numpy_data,x1, x2)
        now=TrainReward(numpy_data, trade)
        if now>ans:
            short_term=x1
            long_term=x2
            ans=now
    return(short_term, long_term)
```

## StrategyMake
After running MovingAverage, we can get the predict_trade, then rewrite our strategy.

If predict_trade is 1, we buy the stock.

If predict_trade is -1, we sell the stock.

If predict_trade is 0, we stay.

```
def StrategyMake(numpy_data,pridict_trade):
    strategy=[]
    maxDay=numpy_data.index.get_values().max()
    nowhold=0
    for i in numpy_data.index.values:
        if i == maxDay:
            break
        if pd.isnull(pridict_trade[i]):
            strategy.append(0)
        if pridict_trade[i] == 1:
            if nowhold==0:
                nowhold=1;
                strategy.append(1)
            else:
                strategy.append(0)
        elif pridict_trade[i] == 0:
            strategy.append(0)
            continue
        elif pridict_trade[i] == -1:
            if nowhold==1:
            nowhold=0;
            strategy.append(-1)
        else:
            strategy.append(0)
    return strategy
```

## Requirement
```
scikit-learn==0.19.1
numpy==1.13.3
pandas==0.21.1
scipy==1.0.0
```

