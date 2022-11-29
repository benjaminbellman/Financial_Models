#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xlwings as xw


# In[ ]:


def main():
    wb = xw.Book.caller()
    sheet = wb.sheets[0]
    sheet.rangge("A2").value ="This is easy"

