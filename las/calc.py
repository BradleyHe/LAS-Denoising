import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame()

# generated 20 data files
# data_list = []

# for x in range(1, 11):
# 	df = df.append(pd.read_csv('pkl/{}_denoised.csv'.format(x), index_col=0))

# data_mean_denoised = df.groupby(level=0).mean()
#data_mean_denoised.to_csv('data_mean_denoised.csv')

# df = pd.DataFrame()

# for x in range(1, 11):
# 	df = df.append(pd.read_csv('pkl/{}_noisy.csv'.format(x), index_col=0))

# data_mean_noisy = df.groupby(level=0).mean()
# data_mean_noisy.to_csv('data_mean_noisy.csv')

data_mean_denoised = pd.read_csv('data_mean_denoised.csv', index_col=0)
data_mean_noisy = pd.read_csv('data_mean_noisy.csv', index_col=0)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

plt.plot([int(x) for x in list(data_mean_denoised.columns)], data_mean_denoised.iloc[0], color='k', linewidth=1, marker='o', mfc='g', clip_on=False, zorder=100)
plt.plot([int(x) for x in list(data_mean_noisy.columns)], data_mean_noisy.iloc[0], color='k', linewidth=1, marker='s', mfc='b', clip_on=False, zorder=100)

ax.set_xlim(-20, 30)
ax.set_ylim(0.27, 0.9)
ax.set_zorder(-5)

plt.setp(ax.spines.values(), linewidth=2)
plt.grid(True)
plt.axhline(y=0.26, color='k', linestyle='--')

plt.xticks(range(-20, 33, 5))
plt.yticks(np.arange(0.25, 0.9, 0.05))
plt.xlabel('TIR (dB)')
plt.ylabel('PER')
plt.legend(('Denoised', 'Noisy', 'Optimal'), loc='upper right')
ax.set_title('Comparison of Noisy and Denoised Performance', fontdict={'fontsize': 10, 'fontweight': 'medium'})
plt.savefig('graph1' + '.pdf')