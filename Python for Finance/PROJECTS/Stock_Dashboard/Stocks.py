
# ## Running with Run main

# In[35]:


import xlwings as xw
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data 
import seaborn as sns
from statsmodels.formula.api import ols
plt.style.use("seaborn")


def main():
    
    #connect
    wb = xw.Book.caller()
    
    #define sheets
    db_s = wb.sheets[0]
    prices_s = wb.sheets[1]
    
    #read values
    symbol = db_s.range("C7").value
    start = db_s.range("F7").value
    end = db_s.range("I7").value
    benchmark = db_s.range("K20").value
    freq = db_s.range("K39").value
    
    #load stock data and create df
    df = data.DataReader(name = [symbol, benchmark], data_source = "yahoo",
                         start = start, end = end).Close
    df.rename(columns = {benchmark:benchmark.replace("^", "")}, inplace = True)
    df.rename(columns = {symbol: symbol.split(".")[0]}, inplace = True)
    
    benchmark = benchmark.replace("^", "")
    symbol = symbol.split(".")[0]

    
    df.dropna(inplace= True)
    
    #create chart 
    chart = plt.figure(figsize = (19, 8))
    df[symbol].plot(fontsize = 15)
    plt.title(symbol, fontsize = 20)
    plt.xlabel("Date", fontsize = 15)
    plt.ylabel("Stock Price", fontsize = 15)
    db_s.pictures.add(chart, name = "Chart", update = True, 
                      left = db_s.range("C8").left, 
                      top = db_s.range("C8").top,
                      scale = 0.47)
    
    #calculate and write metrics
    first = df.iloc[0,0]
    high = df.iloc[:, 0].max()
    low = df.iloc[:, 0].min()
    last = df.iloc[-1, 0]
    total_change = last / first - 1
    db_s.range("H12").options(transpose = True).value = [first, high, low, last, total_change]
    
    #create chart2
    norm = df.div(df.iloc[0]).mul(100)
    chart2 = plt.figure(figsize = (19, 8))
    norm[symbol].plot(fontsize = 15)
    norm[benchmark].plot(fontsize = 15)
    plt.title(symbol + " vs. " + benchmark, fontsize = 20)
    plt.xlabel("Date", fontsize = 15)
    plt.ylabel("Normalized Price (Base 100)", fontsize = 15)
    plt.legend(fontsize = 20)
    db_s.pictures.add(chart2, name = "Chart2", update = True, 
                      left = db_s.range("C21").left, 
                      top = db_s.range("C21").top + 10,
                      scale = 0.46)
    
    #calculate returns
    ret  = df.resample(freq).last().dropna().pct_change().dropna()
   
    #create chart3
    chart3 = plt.figure(figsize = (12.5, 10))
    sns.regplot(data = ret, x = benchmark, y = symbol)
    plt.title(symbol + " vs. " + benchmark, fontsize = 20)
    plt.xlabel(benchmark + " Returns", fontsize = 15)
    plt.ylabel(symbol + " Returns", fontsize = 15)
    db_s.pictures.add(chart3, name = "Chart3", update = True, 
                      left = db_s.range("C40").left, 
                      top = db_s.range("C40").top,
                      scale = 0.47)
    
    #Linear Regression
    model = ols(symbol + "~" + benchmark, data = ret)
    results = model.fit()
    
    #calculate & write Regression Statistics
    obs = len(ret)
    corr_coef = ret.corr().iloc[0,1]
    beta = results.params[1]
    r_sq = results.rsquared
    t_stat = results.tvalues[1]
    p_value = results.pvalues[1]
    conf_left = results.conf_int().iloc[1,0]
    conf_right = results.conf_int().iloc[1,1]
    interc = results.params[0]
    
    regr_list = [obs, corr_coef, beta, r_sq, t_stat, 
                 p_value, conf_left, conf_right, interc]
    db_s.range("K41").options(transpose = True).value = regr_list
    
    #write raw data
    prices_s.range("A1").expand().clear_contents()
    prices_s.range("A1").value = df







