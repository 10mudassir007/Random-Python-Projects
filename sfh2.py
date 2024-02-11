import numpy as np
import pandas as pd

print("Squad")
'''
squad = {'name' : ['Nathan', 'Dex','Jyn','Tower','Briggs'], 
'class' : ['Engineer','Mercenary','Sniper','Juggernaut','General'],
'Signature Weapon':['M416','RPG','BARETTA','R870','DUAL MAGNUM']}


#squad1 = np.array([['Briggs','General','Dual Magnum'],
['Nathan','Engineer','M416'],
['Dex','Mercenary','RPG'],
['Tower','Juggernaut','R870'],
['Jyn','Sniper','Baretta']]).reshape(5,3)
'''
squad2 = np.array([['Briggs','Nathan','Dex','Tower','Jyn'],
['General','Engineer','Mercenary','Juggernaut','Sniper'],
['Dual Magnum','M416','RPG','R870','Baretta']]).reshape(3,5)

dataframe = pd.DataFrame(squad2,['Name','Class','Weapon'],[1,2,3,4,5])

print(dataframe)