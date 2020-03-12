import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

df = pd.DataFrame()

# generated 20 data files
data_list = []

# for x in range(1, 11):
	#df = df.append(pd.read_csv('pkl/{}_denoised.csv'.format(x), index_col=0))
	#df = df.append(pd.read_csv('pkl/{}_denoised_trained.csv'.format(x), index_col=0))

#data_mean_denoised = df.groupby(level=0).mean()
#data_mean_denoised.to_csv('data_mean_denoised.csv')
# data_mean_denoised_trained = df.groupby(level=0).mean()
# data_mean_denoised_trained.to_csv('data_mean_denoised.csv')

# df = pd.DataFrame()

# for x in range(1, 11):
	#df = df.append(pd.read_csv('pkl/{}_noisy.csv'.format(x), index_col=0))
	#df = df.append(pd.read_csv('pkl/{}_noisy_trained.csv'.format(x), index_col=0))

# data_mean_noisy = df.groupby(level=0).mean()
# data_mean_noisy.to_csv('data_mean_noisy.csv')
# data_mean_noisy_trained = df.groupby(level=0).mean()
# data_mean_noisy_trained.to_csv('data_mean_noisy.csv')

data_mean_denoised = pd.read_csv('data_mean_denoised.csv', index_col=0)
data_mean_noisy = pd.read_csv('data_mean_noisy.csv', index_col=0)
data_mean_denoised_trained = pd.read_csv('data_mean_denoised_trained.csv', index_col=0)
data_mean_noisy_trained = pd.read_csv('data_mean_noisy_trained.csv', index_col=0)

# makes line graph 
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

plt.plot([int(x) for x in list(data_mean_noisy.columns)], data_mean_noisy.iloc[0], color='k', linewidth=1, marker='s', mfc='k', ms=8, clip_on=False, zorder=100)
plt.plot([int(x) for x in list(data_mean_denoised.columns)], data_mean_denoised.iloc[0], color='k', linewidth=1, marker='o', mfc='b', ms=8, clip_on=False, zorder=100)
plt.plot([int(x) for x in list(data_mean_noisy_trained.columns)], data_mean_noisy_trained.iloc[0], color='k', linewidth=1, marker='o', mfc='y', ms=8, clip_on=False, zorder=100)
plt.plot([int(x) for x in list(data_mean_denoised_trained.columns)], data_mean_denoised_trained.iloc[0], color='k', linewidth=1, marker='o', mfc='g', ms=8, clip_on=False, zorder=100)

ax.set_xlim(-20, 30)
ax.set_ylim(0.27, 0.9)
ax.set_zorder(-5)

plt.setp(ax.spines.values(), linewidth=2)
plt.grid(True)
plt.axhline(y=0.26, color='k', linestyle='--')

plt.xticks(range(-20, 33, 5))
plt.yticks(np.arange(0.25, 0.95, 0.05))
plt.xlabel('TIR (dB)')
plt.ylabel('PER')
plt.legend(('Base Performance', 'Denoised Performance', 'Trained Performance', 'Denoised/Trained Performance'), loc='upper right')
ax.set_title('Comparison of Denoising and Training Performance', fontdict={'fontsize': 10, 'fontweight': 'medium'})
plt.savefig('line_graph_all.png')

##################################################################################################

# make improvement bar graphs

# denoising_improvement = data_mean_denoised - data_mean_noisy
# training_improvement = data_mean_noisy_trained - data_mean_noisy
# denoising_training_improvement = data_mean_denoised_trained - data_mean_noisy

#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
#ax.yaxis.grid()

#ax.set_ylim(-0.25, 0.25)
#ax.set_zorder(-1)

#plt.setp(ax.spines.values(), linewidth=2)
#plt.xlabel('TIR (dB)')
#plt.xticks(range(-20, 33, 5))
#plt.ylabel('Relative PER change')
#plt.yticks(np.arange(-0.25, 0.3, 0.05))
#plt.axhline(y=0, color='k', label='')

# change this to each of the 3 improvement lists to make graph
#y = denoising_improvement
#y = training_improvement
#y = denoising_training_improvement

#improve = y.iloc[0] < 0
#worsen = y.iloc[0] > 0

#ax.bar([int(x) for x in list(data_mean_denoised.columns[improve])], y.iloc[0][improve], color='b', zorder=100, width=1.5)
#ax.bar([int(x) for x in list(data_mean_denoised.columns[worsen])], y.iloc[0][worsen], color='r', zorder=100, width=1.5)

#custom_lines = [Patch(facecolor='b', edgecolor='b'),
#                Patch(facecolor='r', edgecolor='r')]
#ax.legend(custom_lines, ['Improvement', 'Worsened'], loc='upper left')

#ax.set_title('Denoising/No Training on Model Performance')
#plt.savefig('denoising_improvement_clean.png')

#ax.set_title('No Denoising/Training on Model Performance')
#plt.savefig('training_improvement_denoised.png')

#ax.set_title('Denoising/Training on Model Performance')
#plt.savefig('denoising_improvement_trained.png')