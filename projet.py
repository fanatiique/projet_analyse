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
from scipy.special import boxcox1p

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

print(data['Installs'].unique())
data['Installs'] = data['Installs'].apply(lambda x: str(x).replace(',',''))
data['Installs'] = data['Installs'].apply(lambda x: str(x).replace('+',''))
data['Installs'] = data['Installs'].apply(lambda x: int(x))
Sorted_value = sorted(list(data['Installs'].unique()))
print(data.describe())

skewness = data['Installs'].skew() 
data['Installs'] =  boxcox1p(data['Installs'], 0.25)



g = sns.catplot(x="Genres",y="Rating",data=data, kind="box", height = 10 ,
palette = "Set1")
g.set_xticklabels(rotation=90)

g = g.set_ylabels("Rating")
plt.title('Boxplot of Rating VS Category',size = 20)
#data['Installs'].replace(Sorted_value,range(0,len(Sorted_value),1), inplace = True )
g = sns.catplot(x="Installs",y="Rating",data=data, kind="box", height = 10 ,
palette = "Set1")
g.set_xticklabels(rotation=90)

plt.title('Boxplot of Rating VS Category',size = 20)
print(data['Price'].unique())

print(data.dtypes)
print(data['Reviews'].unique())
data['Reviews'] = data['Reviews'].apply(lambda x: int(x))
data['Type'] = data['Type'].apply(lambda x: str(x).replace('Free','0'))
data['Type'] = data['Type'].apply(lambda x: str(x).replace('Paid','1'))
data['Type'] = data['Type'].apply(lambda x: int(x))

data['Price'] = data['Price'].apply(lambda x: str(x).replace('$',''))
data['Price'] = data['Price'].apply(lambda x: float(x))


corr = data.corr()
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
f, ax = plt.subplots(figsize=(11, 9))
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

#data=pd.get_dummies(data['Content Rating'])
print (data['Type'].unique())
# Traitement de la variable Reviews
#
