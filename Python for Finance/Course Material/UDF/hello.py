
import xlwings as xw
import numpy as np
import pandas as pd

# run main (recap)

def main():
    wb = xw.Book.caller()
    sheet = wb.sheets[0]
    sheet.range("A8").value = [[1,2], [3,4], [5,6]]

# Simple Functions

@xw.func
def bonjour(name):
    return "Bonjour {}!".format(name)


@xw.func
@xw.arg("number", doc = "This is an integer or float")
def squareroot(number):
    """returns the square root of a number""" 
    return np.sqrt(number)


# Reading more complex function arguments

@xw.func
def total(data):
    return sum(data)


@xw.func
@xw.arg("data", ndim = 2)
def total2(data):
    return sum([sum(row) for row in data])


# numpy arrays

@xw.func
@xw.arg("data", np.array)
def total3(data):
    return data.sum()


#Many Outputs with Array Formulas

@xw.func
def randomnumb(mean, std, rows, columns):
    return np.random.normal(mean, std, (int(rows), int(columns)))


# Dynamic Arrays with the return decorator

@xw.func
@xw.ret(expand = "table")
def randomnumb2(mean, std, rows, columns):
    return np.random.normal(mean, std, (int(rows), int(columns)))


# Reading and writing DataFrames

@xw.func
@xw.arg("data", pd.DataFrame, index = False, header = False)
def dfsum(data):
    return data.sum().sum()


@xw.func
@xw.arg("data", pd.DataFrame, expand = "table", index = False, header = False)
def dfsum2(data):
    return data.sum().sum()


@xw.func
@xw.arg("data", pd.DataFrame, expand = "table", index = False, header = False)
@xw.ret(expand = "table")
def addone(data):
    return data.add(1)
