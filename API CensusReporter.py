import urllib.request, json
import json,urllib.request
import pandas as pd
import numpy as np
import requests


def flatten_json(nested_json):
    """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out




#to add a key value pair, you first determine which variable you want
#you then find which table it is in https://censusreporter.org/topics/table-codes/
#then, you add the index to look4part2
#the indexs should line up


#example: i want number of males
#1) i find the table number (B01001)
#1b) i add a new key ('Male population') and a new value ('B01001') to arr1
#2) next, i see which column number holds the male numbers
#3) if you visit https://censusreporter.org/tables/B01001/, you can see column numbers
#4) the first column index is total population and the second column index is male population
#5) since male population is the second column, i will append 002 to look4part2

df = pd.read_excel('Book1.xlsx')

cbid = df['censusBlockId']
final=[]
for i in cbid:
    if not np.isnan(i): 
        arr1 = {'Population':'B01003','Median Age':'B01002','Male':'B01001','Female':'B01001','Per capita income':'B19301','Median Household Income':'B19013','Persons Below Poverty Line':'B17001'}
        look4part2 = ['001','001','002','026','001','001','002']


        ind=0
        temphold=[i]
        for j in arr1:
            data = urllib.request.urlopen("https://api.censusreporter.org/1.0/data/show/latest?table_ids="+arr1[j]+"&geo_ids=14000US"+str(int(np.floor(i/10000)))).read()
            output = json.loads(data)
            output2 = flatten_json(output)
            look4this='estimate_'+arr1[j]+look4part2[ind]
            ind+=1
            index = [idx for idx, s in enumerate(list(output2.keys())) if look4this in s][0]

           # print('\n')
            #print(output2)
            #print(output2[list(output2.keys())[index]])
            temphold.append(output2[list(output2.keys())[index]])
        final.append(temphold)
arr1 = ['Census Block ID','Population','Median Age','Male','Female','Per capita income','Median Household Income','Persons Below Poverty Line']

df=pd.DataFrame(final,columns=arr1)
df.to_excel('done.xlsx',index=False)


