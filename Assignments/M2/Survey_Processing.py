import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
sns.set_context('paper')


CSV_PATH = './Survey_Responses.csv' # CSV response format from http://peersurvey.cc.gatech.edu

df = pd.read_csv(CSV_PATH, index_col='response')
qual = ['Q1', 'Q4', 'Q6', 'Q8', 'Q11']

# Q4 and Q6 use semicolons to split response values. e.g. work;personal;other
Q4_col = ['Q4_Work', 'Q4_Academic', 'Q4_Personal', 'Q4_Other']
Q4_resp = ['Work', 'Academic', 'Personal', 'Other']

Q6_col = ['Q6_Email', 'Q6_Calendar', 'Q6_Groups', 'Q6_Tasks', 'Q6_Notes', 'Q6_Meetings']
Q6_resp = ['Email', 'Calendar', 'Groups', 'Tasks', 'Notes', 'Meetings']

df_qual = df[qual]
df_qual = pd.concat([df_qual, pd.DataFrame(columns=Q4_col+Q6_col)], axis=1)

for i,v in df.iterrows():
    for col,resp in zip(Q4_col, Q4_resp): df_qual.loc[i, col] = v['Q4'].split(';').count(resp)
    for col,resp in zip(Q6_col, Q6_resp): df_qual.loc[i, col] = v['Q6'].split(';').count(resp)

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
     
# Age range
Q1_counts = df_qual['Q1'].value_counts()
ax = sns.barplot(x=Q1_counts.index, y=Q1_counts)
ax.set(ylabel='Counts', title='Q1 Responses')
add_text(ax, Q1_counts.values)
ax.get_figure().savefig('./Figures/Q1_responses')
plt.show()

# What is your primary use for Outlook?
Q4_counts = df_qual[Q4_col].sum()
Q4_counts.index = Q4_resp
ax = sns.barplot(x=Q4_counts.index, y=Q4_counts)
ax.set(ylabel='Counts', title='Q4 Responses')
add_text(ax, Q4_counts.values)
ax.get_figure().savefig('./Figures/Q4_responses')
plt.show()

# Which features do you utilize in Outlook?
Q6_counts = df_qual[Q6_col].sum()
Q6_counts.index = Q6_resp
ax = sns.barplot(x=Q6_counts.index, y=Q6_counts)
ax.set(ylabel='Counts', title='Q6 Responses')
add_text(ax, Q6_counts.values)
ax.get_figure().savefig('./Figures/Q6_responses')
plt.show()

# Is Outlook your preferred application?
Q8_counts = df_qual['Q8'].value_counts()
ax = sns.barplot(x=Q8_counts.index, y=Q8_counts)
ax.set(ylabel='Counts', title='Q8 Responses')
add_text(ax, Q8_counts.values)
ax.get_figure().savefig('./Figures/Q8_responses')
plt.show()

# I'm content with Outlook.
Q11_counts = df_qual['Q11'].value_counts()
ax = sns.barplot(x=Q11_counts.index, y=Q11_counts)
ax.set(xlabel='Increasing Satisfaction', ylabel='Counts', title='Q11 Responses')
add_text(ax, Q11_counts.sort_index().values)
ax.get_figure().savefig('./Figures/Q11_responses')
plt.show()

# Q7 google / gmail usage
keyword_count = 0
gmail_count = 0
google_cal_count = 0
for resp in df['Q7'].values.astype('str'):
    if resp.lower().find('google') != -1 or resp.lower().find('gmail') != -1:
        keyword_count += 1
    if resp.lower().find('gmail') != -1:
        gmail_count += 1
    if resp.lower().find('google cal') != -1:
        google_cal_count += 1

print('\n~~~~~')
print("For Q7, Google is referred to {} times.".format(keyword_count))
print("For Q7, Gmail is referred to {} times.".format(gmail_count))
print("For Q7, Google Calendar is referred to {} times.".format(google_cal_count))
