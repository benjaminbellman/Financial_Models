
import xlwings as xw
import pandas as pd
import numpy as np
from pandas_datareader import data


# Run main (recap)

def main():
    wb = xw.Book.caller()
    sheet = wb.sheets[0]
    sheet.range("A1").value = 123

    
    
#Importing Data from Web Api with Pandas/DataReader    
    
@xw.func
@xw.arg("symbols", expand = "right")
@xw.ret(expand = "table", index = True, header = True)
def getdata(symbols, startdate, enddate):
    df = data.DataReader(name = symbols, data_source = "yahoo",
                         start = startdate, end = enddate).Close
    return df



#Resampling Time Series Data with resample()

@xw.func
@xw.arg("data", pd.DataFrame, expand = "table", 
        index = True, header = True)
@xw.ret(expand = "table", index = True, header = True)
def resample(data, freq):
    return data.resample(freq).last().dropna()



# Calculating Stock Returns (Simple vs. Log)

@xw.func
@xw.arg("data", pd.DataFrame, expand = "table", 
        index = True, header = True)
@xw.ret(expand = "table", index = True, header = True)
def returns(data, log = False):
    if log == False:
        ret = data.pct_change().dropna()
    elif log == True:
        ret = np.log(data / data.shift(1)).dropna()
    return ret



# Summary Statistics with describe()

@xw.func
@xw.arg("returns", pd.DataFrame, expand = "table", 
        index = True, header = True)
@xw.ret(expand = "table", index = True, header = True)
def describe(returns):
    return returns.describe() 



# Correlation Matrix with corr()

@xw.func
@xw.arg("returns", pd.DataFrame, expand = "table",
        index = True, header = True)
@xw.ret(expand = "table", index = True, header = True)
def corr(returns):
    return returns.corr() 



# The Super UDF

@xw.func
@xw.arg("symbols", expand = "right")
@xw.ret(expand = "table", index = True, header = True)
def financial_data(symbols, startdate, enddate, 
                   freq, returns = False, log = False):
    prices = data.DataReader(name = symbols, data_source = "yahoo", 
                         start = startdate, end = enddate).Close
    prices = prices.resample(freq).last().dropna(how = "all")
    
    if returns == False:
        output = prices
    elif returns == True:
        if log == False:
            output = prices.pct_change().dropna(how = "all")
        elif log == True:
            output = np.log(prices / prices.shift(1)).dropna(how = "all")
    
    return output



# Merging Tables with pd.merge() 

@xw.func
@xw.arg("left", pd.DataFrame, expand = "table",
        index = True, header = True)
@xw.arg("right", pd.DataFrame, expand = "table",
        index = True, header = True)
@xw.ret(expand = "table", index = True, header = True)
def merge(left, right, how, merge_on):
    return pd.merge(left = left, right = right, how = how, on = merge_on) 


