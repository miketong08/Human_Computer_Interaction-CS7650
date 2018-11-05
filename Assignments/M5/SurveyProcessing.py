import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
DATA_DIR_qual = "./SurveyData.csv"
DATA_DIR_emp = "./Empirical_Data.xlsx"
OLD_DATA_DIR = "/Users/michaeltong/Documents/OMSCS/CS6750/Assignments/M2/Survey_Responses.csv"
# 1. What do you primarily use Outlook for?
# 2. Do you use folders to organize your emails?
# 4. Do you categorize everything or only specific emails?
# 5. Are you content with the folder system?
# 7. You can now send a message from a folder and all responses will return there, do you think this is helpful?

class qualitative(object):
    def __init__(self, DATA_DIR):
        self.DATA_DIR = DATA_DIR
        
    def add_text(self, ax, nums):
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
    
    def process(self):     
        df = pd.read_csv(self.DATA_DIR, index_col='response')
        cat_cols = df.columns[[0, 1, 3, 4, 6]]
        
        # Q1 counts    
        ans = {}
        for i, resp in df.loc[:, cat_cols[0]].iteritems():
            for resp_ in resp.split(';'):
                try:
                    ans[resp_] += 1
                except(KeyError):
                    ans[resp_] = 0
        
        f = sns.barplot(list(ans.keys()), list(ans.values()))
        f.set_title("Q1 Response Count")
        f.set_xlabel("Responses")
        f.set_ylabel("count")
        self.add_text(f, list(ans.values()))
        f.get_figure().savefig('./Figures/Q1_counts')
        plt.show()
        
        #Q2 through 7 counts
        for col in cat_cols[1:]:
            data = np.unique(df.loc[:, col].values, return_counts=True)
            data = [i[::-1] for i in data]
        #    f = sns.countplot(selection.values)
            f = sns.barplot(x=data[0], y=data[1])
            f.set_title("{} Response count".format(col))
            f.set_xlabel("Responses")
            self.add_text(f, data[1])
            f.get_figure().savefig('./Figures/{}_counts'.format(col))
            plt.show()

class Empirical(object):
    def __init__(self, DATA_DIR):
        self.DATA_DIR = DATA_DIR
        self.df = pd.read_excel(DATA_DIR)
        self.n_delta = list(map(lambda x: x.second, self.df[self.df['Method'] == 'N']['Delta']))
        self.o_delta = list(map(lambda x: x.second, self.df[self.df['Method'] == 'O']['Delta']))

    def process_plots(self):
        f = sns.countplot(self.n_delta)
        f.set_xlabel('Delta Value')
        f.set_title('Distribution of Delta Values for New Method')
        plt.show()
        f = sns.countplot(self.o_delta)
        f.set_xlabel('Delta Value')
        f.set_title('Distribution of Delta Values for Old Method')
        plt.show()
    
    def process_stats(self):
        print("\nt: {}\np: {}".format(ttest_ind(self.n_delta, self.o_delta)[0], ttest_ind(self.n_delta, self.o_delta)[1]))
        print('\nN_Mean: {}\nO_Mean: {:.2f}'.format(np.mean(self.n_delta), np.mean(self.o_delta)))
        print('\nN_Stdev: {:.3f}\nO_Stdev: {:.3f}'.format(np.std(self.n_delta), np.std(self.o_delta)))
        print('\nN_Median: {}\nO_Median: {}'.format(np.median(self.n_delta), np.median(self.o_delta)))
    
    def per_person_stats(self):
#        d = dict.fromkeys(emp.df['Person'].unique(), 
#                          dict.fromkeys(['N', 'O'], None).copy())
#                
#        
#        for k in d:
#            for e in ['N', 'O']:
#                d[k][e] = [i.second for i in self.df[(self.df['Person'] == k) & (self.df['Method'] == e)]['Delta']]
#            
#        self.d = d
#        
#        for k in d:
#            for e in ['N', 'O']:
#                if e == 'N':
#                    print('\nThe mean for person {0} with the new method is {1}'.format(k, np.mean(d[k][e])))
#                if e == 'O':
#                    print('The mean for person {0} with the old method is {1}'.format(k, np.mean(d[k][e])))
        
        n_values = []
        o_values = []
        for i in emp.df['Person'].unique():
            for j in ['N', 'O']:
                if j == 'N':
                    n_values.append([i.second for i in emp.df[(emp.df['Person'] == i) & (emp.df['Method'] == j)]['Delta']])
                if j =='O':
                    o_values.append([i.second for i in emp.df[(emp.df['Person'] == i) & (emp.df['Method'] == j)]['Delta']])
        self.n_values_pp = n_values
        self.o_values_pp = o_values    
        
        ids = emp.df['Person'].unique()
        n_means = np.mean(n_values, axis=1)
        o_means = np.mean(o_values, axis=1)
        
        df_temp = pd.DataFrame(ids, columns=['Person'])
        df_temp['New'] = n_means
        df_temp['Old'] = o_means
        df_temp_ = pd.melt(df_temp, id_vars='Person', var_name='Method', value_name='Value')
        
        f = sns.barplot(x='Person', y='Value', hue='Method', data=df_temp_)
        f.get_figure().savefig("./Figures/empirical_mean")
        f.set_title("Mean per Person by Experimental Method")
        plt.show()
        
        
        n_std = np.std(n_values, axis=1)
        o_std = np.std(o_values, axis=1)
        
        df_temp = pd.DataFrame(ids, columns=['Person'])
        df_temp['New'] = n_std
        df_temp['Old'] = o_std
        df_temp_ = pd.melt(df_temp, id_vars='Person', var_name='Method', value_name='Value')
        
        f = sns.barplot(x='Person', y='Value', hue='Method', data=df_temp_)
        f.get_figure().savefig("./Figures/empirical_std")
        f.set_title("Standard Deviation per Person by Experimental Method")
        plt.show()
        
#qual = qualitative(DATA_DIR_qual)
#qual.process()
emp = Empirical(DATA_DIR_emp)
emp.process_plots()
emp.process_stats()
emp.per_person_stats()