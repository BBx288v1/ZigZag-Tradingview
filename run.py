from tvDatafeed import TvDatafeed, Interval
import zigzig
import pandas as pd

def findNum(dfx, value):
    listDate = list(dfx.keys())
    for d in range(len(dfx)):
        if dfx[d]==value:
            #print(listDate[d])
            return listDate[d]

tv = TvDatafeed()

df = tv.get_hist(symbol='BTCUSDTPERP',exchange='BINANCE',interval=Interval.in_15_minute,n_bars=10000, extended_session=True)




print(df)

dataOut={
    "PEAK":[],
    "Time1":[],
    "Price1":[],
    "VALLEY":[],
    "Time2":[],
    "Price2":[],
}


hist = df
lenData=len(df)
listDate = list(df.low.keys())
for (i_h, p_h),(i_l, p_l) in zigzig.zigzag(hist['high'], hist['low'],depth=2,dev_threshold=1):
    time1=listDate[i_h*-1-1]
    time2=listDate[i_l*-1-1]
    print(f'PEAK Index: {i_h}, Time:{time1}, price: {p_h}, VALLEY Index: {i_l}, Time:{time2}, price: {p_l}')
    dataOut["PEAK"].append(i_h)
    dataOut["Time1"].append(time1)
    dataOut["Price1"].append(p_h)
    dataOut["VALLEY"].append(i_l)
    dataOut["Time2"].append(time2)
    dataOut["Price2"].append(p_l)
df = pd.DataFrame(dataOut)
df.to_csv('result.csv', index=False)
