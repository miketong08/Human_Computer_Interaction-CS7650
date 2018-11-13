import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
sns.set_context('paper')


CSV_PATH = './Survey_Results_111018.csv' # CSV response format from http://peersurvey.cc.gatech.edu

df = pd.read_csv(CSV_PATH, index_col='response')

qual = [1, 2, 3, 5, 6, 7]

df_qual = df[['Q' + str(i) for i in qual]]


def add_text(ax, nums):
    '''Adds value counts above ax bars with given num counts
    :param ax: seaborn axes object
    :param nums: list of labels for the axes bars
    
    :return: none
    '''
    for i,p in enumerate(ax.patches):
        ax.text(p.get_x() + p.get_width()/2.,
                p.get_height() + 0.1,
                nums[i],
                ha='center')

for c in df_qual.columns:  
    counts = df_qual[c].value_counts()
    ax = sns.barplot(x=counts.index, y=counts)
    ax.set(ylabel='Counts', title='{} Responses'.format(c))
    add_text(ax, counts.values)
    ax.get_figure().savefig('./Figures/{}_responses'.format(c))
    plt.show()    