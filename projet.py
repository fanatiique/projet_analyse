#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 15:51:09 2019

@author: emilio
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # this is used for the plot the graph 
import seaborn as sns # used for plot interactive graph.

#
data = pd.read_csv("googleplaystore.csv")
dataType = data.dtypes
#


#On calcule le pourcentage de valeur null en fonction des variables
total = data.isnull().sum().sort_values(ascending=False)
percent = (data.isnull().sum()/data.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
data.dropna(how ='any', inplace = True)
desc = data.describe()
print(len(data[data.Size == 'Varies with device'])) # 1637 


# Plot de la distribution de notes
"""
g = sns.kdeplot(data.Rating, color="Red", shade = True)
g.set_xlabel("Notation")
g.set_ylabel("Fréquence")
plt.title('Distribution des notes',size = 20)
plt.savefig('rating_freq.png')
"""
# Traitement de la variable Size
# remplace par des nan (valeur null)
data['Size'].replace('Varies with device', np.nan, inplace = True )
# Les tailles sont exprimées en "[0-9]*M ou [0-9]*k 
# On les converties en int
data['Size'] = data['Size'].apply(lambda x: str(x).replace('Varies with device', 'NaN') if 'Varies with device' in str(x) else x)
data['Size'] = data['Size'].apply(lambda x: str(x).replace('M', '') if 'M' in str(x) else x)
data['Size'] = data['Size'].apply(lambda x: str(x).replace(',', '') if 'M' in str(x) else x)
data['Size'] = data['Size'].apply(lambda x: float(str(x).replace('k', '')) / 1000 if 'k' in str(x) else x)
data['Size'] = data['Size'].apply(lambda x: float(x))
data['Size'].fillna(data.groupby('Category')['Size'].transform('mean'),inplace = True)
# Plot de la variable Size
"""
ax = sns.kdeplot(data.Size, color="Blue", shade = True)
ax.set_xlabel("Taille")
ax.set_ylabel("Fréquence")
plt.title('Distribution des tailles d\'application',size = 20)
plt.savefig('size_freq2.png')
"""
# 
"""
g = sns.countplot(x="Category",data=data, palette = "Set1")
g.set_xticklabels(g.get_xticklabels(), rotation=90, ha="right")
g 
plt.title('Nombre d\'application pour chaque catégorie' ,size = 20)
plt.savefig('count_cat.png',bbox_inches='tight')
"""
reviews = data['Reviews']
test=pd.Series(reviews).unique()