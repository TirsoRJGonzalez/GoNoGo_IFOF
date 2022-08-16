# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:33:44 2021

@author: tirso

"""

import os, time
import pandas as pd
import seaborn as sns; sns.set_style('white'); sns.set_context('paper')
from scipy.stats import pearsonr, zscore
import matplotlib.pyplot as plt

timestamp = time.strftime("%Y%m%d_%H%M%S")

# create output dirs
outdirs = ['Figures','Stats_Results_Correls']
for d in outdirs:
    if not os.path.isdir(d):
        os.makedirs(d)

# load data
df = pd.read_csv('data.csv')

# define analyses to do:
# Analysis 1 - Main: 4 task variables by 2 (left) IFOF strength variables
# Analysis 2 - Hemispheric differences: 4 task variables by 2 hemispheric differences in IFOF strength
# Analysis 3 - Task contrasts: 3 task contrasts by 2 (left) IFOF strength variables
analyses = {1:
            {'beh':['Tirso_GONOGO_Offline_Word_Eff_zscore', 'Tirso_GONOGO_Offline_Pic_Eff_zscore', 
                    'Tirso_GONOGO_Offline_Easy_Eff_zscore', 'Tirso_GONOGO_Offline_Hard_Eff_zscore'],
             'conn':['IFOFdorsalLEFT','IFOFventralLEFT']
             },
            2:
             {'beh':['Tirso_GONOGO_Offline_Word_Eff_zscore', 'Tirso_GONOGO_Offline_Pic_Eff_zscore', 
                     'Tirso_GONOGO_Offline_Easy_Eff_zscore', 'Tirso_GONOGO_Offline_Hard_Eff_zscore'],
              'conn': ['Dorsal_LminR', 'Ventral_LminR']
              },
            3:
            {'beh':['Word_min_Pic', 'Hard_min_Easy', 'Semantic_min_Perceptual'],
             'conn':['IFOFdorsalLEFT','IFOFventralLEFT']
             }
            }
            
    
# iterate over each analysis defined, getting the Pearson r for each pair of
# correlations of interest, and plotting them
for analysis in analyses:
    # set empty lists we'll need to construct the output df reporting correlations
    IDs = []
    rs = []
    ps = []

    # format variables to load
    beh = analyses[analysis]['beh']
    conn = analyses[analysis]['conn']
    
    # if it's a contrast, impute the outliers
    if '_min_' in beh[0]:
        for b in beh:
            temp = zscore(df[b])
            temp[temp > 2.1] = 2.1
            temp[temp < -2.1] = -2.1
            df[b] = temp
            
    # set the colours according to the dorsal/ventral distinction
    for c in conn:
        if 'dorsal' in c or 'Dorsal' in c:
            color = 'purple'
        elif 'ventral' in c or 'Ventral' in c:
            color = 'blue'
            
        for b in beh:
            # get Pearson r and do the scatterplot
            r,p = pearsonr(df[b],df[c])
            ax = sns.regplot(x=b, y=c, data=df,color=color)
            
            # format plot
            ax.set_xlabel('')
            ax.set_yticklabels('')
            ax.set_ylabel('')
            ax.tick_params(labelsize=15)
            print(c, b)
            print(r, p)
            
            # append values to lists to construct the output dfs
            ID = ' '.join([c,b])
            IDs.append(ID)
            rs.append(r)
            ps.append(p)
            plt.savefig(r'Figures\%s_by_%s.png'%(b,c), transparent=True)
            plt.show()
        
    # construct output df with Pearson r and p values and save it
    df2 = pd.DataFrame({'ID':IDs,'r':rs,'p':ps})
    df2.to_csv('Stats_Results_Correls\Correls_Analysis{}_{}.csv'.format(analysis,timestamp),index=False)
    