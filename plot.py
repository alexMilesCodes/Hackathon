import pandas as pd
import scipy.stats as sts
import matplotlib.pyplot as plt


data = pd.read_csv('time-varied-HIP.csv')

off = 23
# Test for normality across the last year
lst_yr = data.loc[data['Abs Month'].isin(range(max(data['Abs Month'])-11-off, max(data['Abs Month'])+1-off))]

for col in lst_yr.columns[4:]:
    stat, p = sts.shapiro(lst_yr[col])
    print(str(col) + ' --- stat: ' + str(stat) + ' p: ' + str(p))

# Create a subset of data that contains all data before 2008
# Test for normality of each year-long window
# If a window can be considered normally distributed, perform a t-test with lst_yr
# If a window cannot be considered normally distributed, perform a Wilcoxon Signed-Rank Test with lst_yr
bfr_08 = data.loc[data['Year'].isin(range(min(data['Year']), 2008))]

starts = range(1, len(bfr_08['Date'])-10)
dates = data['Date'][:len(starts)]
pvals = pd.DataFrame({'Abs Month': starts, 'Start Date': dates})
pvals2 = pd.DataFrame({'Abs Month': starts, 'Start Date': dates})
pvals3 = pd.DataFrame({'Abs Month': starts, 'Start Date': dates})
for col in bfr_08.columns[4:]:
    temp = []
    temp2 = []
    temp3 = []
    for i in range(len(bfr_08['Date'])-11):
        stat, p = sts.shapiro(bfr_08[col][i:i+12])
        if p > 0.05:
            stat2, p2 = sts.ttest_rel(lst_yr[col], bfr_08[col][i:i+12])
            stat3, p3 = sts.pearsonr(lst_yr[col], bfr_08[col][i:i+12])
        else:
            stat2, p2 = sts.wilcoxon(lst_yr[col], bfr_08[col][i:i+12])
            stat3, p3 = sts.spearmanr(lst_yr[col], bfr_08[col][i:i+12])
        temp.append(p)
        temp2.append(p2)
        temp3.append(p3)
    pvals[col] = temp
    pvals2[col] = temp2
    pvals3[col] = temp3

pvals.to_csv('pvals.csv')
pvals2.to_csv('pvals2.csv')
pvals3.to_csv('pvals3.csv')

pvals3['Mean'] = pvals3[bfr_08.columns[4:]].mean(axis=1)
pvals3['Median'] = pvals3[bfr_08.columns[4:]].median(axis=1)

fig, ax = plt.subplots()
ax.plot(pvals3['Abs Month'], pvals3['Mean'], label='Mean')
ax.plot(pvals3['Abs Month'], pvals3['Median'], label='Median')
_ = plt.xlabel('x (starting month of year-long window)')
_ = plt.ylabel('average correlation coefficient')
# _ = plt.title('average correlation coefficients (median and mean) across several '
              # 'time-dependent variables (comparing [Nov 2020, Sept 2021] to [x, x + 11 months])')
_ = plt.legend()

ax.set_xticks(range(1, len(pvals['Abs Month'])+1, 24))
ax.set_xticklabels(['Jan 1995', 'Jan 1997', 'Jan 1999', 'Jan 2001', 'Jan 2003', 'Jan 2005', 'Jan 2007'])
ax.set(ylim=(0, 1))

plt.show()
