import numpy as np
import matplotlib as mpl
#mpl.use('pdf')
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
fontsize = 10
mpl.rcParams['axes.labelsize'] = fontsize
mpl.rcParams['xtick.labelsize'] = fontsize
mpl.rcParams['ytick.labelsize'] = fontsize
mpl.rcParams['legend.fontsize'] = fontsize

import matplotlib.mlab as mlab
import matplotlib.ticker as ticker

import scipy.stats as stats

import re
import pylab

class LogFormatterTeXExponent(pylab.LogFormatter, object):
    """Extends pylab.LogFormatter to use 
    tex notation for tick labels."""
    
    def __init__(self, *args, **kwargs):
        super(LogFormatterTeXExponent, 
              self).__init__(*args, **kwargs)
        
    def __call__(self, *args, **kwargs):
        """Wrap call to parent class with 
        change to tex notation."""
        label = super(LogFormatterTeXExponent, 
                      self).__call__(*args, **kwargs)
        label = re.sub(r'e(\S)0?(\d+)', 
                       r'\\times 10^{\1\2}', 
                       str(label))
        label = "$" + label + "$"
        return label

# width as measured in inkscape
scale = 1.0
ratio = 1.2#1.618
width = scale * 3.487
height = (width / ratio)

take_ln = False
moving_avg = True
window_size = 500

labels = [r'$\beta_1$ = 0.2',
          r'$\beta_1$ = 0.9',
          r'$\beta_1$ = 0.2, Batch Renorm',
          r'$\beta_1$ = 0.9, Batch Renorm',
          r'$\beta_1$ = 0.2, ReLU6']
file_nums = [3, 1, 5, 4, 6]
#file_nums = [i for i in range(3, 9)]
loc = "//flexo.ads.warwick.ac.uk/Shared41/Microscopy/Jeffrey-Ede/models/denoiser-multi-gpu-"
files = [loc+str(i)+"/log.npy" for i in file_nums]

datasets = [np.load(file) for file in files]

#trunc_fn = lambda data, max_len: data if data.size <= max_len else data[:max_len]
max_len = np.max([data.size for data in datasets])
#datasets = [trunc_fn(data, max_len) for data in datasets]

min_len = min([len(dataset) for dataset in datasets])

def moving_average(a, n=window_size):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

f = plt.figure(1)
ax = f.add_subplot(1,1,1)
for i, dataset in enumerate(datasets):
    losses = moving_average(np.array(dataset[0:min_len])) if moving_avg else np.array(dataset[0:min_len])
    #losses = np.log(losses) if take_ln else losses
    

    plt.plot(np.linspace(1, losses.size, losses.size), np.log10(losses), linewidth=1., label=labels[i])

plt.xlabel('Batches $\\times$10$^3$')
plt.ylabel('Log$_{{10}}$(MSE)')
plt.minorticks_on()
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_ticks_position('both')
#ax.set_x_ticks
plt.locator_params(axis='y', nbins=7)
ticks = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/1000.))
ax.xaxis.set_major_formatter(ticks)
#ticks = ticker.FuncFormatter(lambda x, pos: '$10^{{{0:g.4}}}$'.format(x/1000.))
#ax.yaxis.set_major_formatter(ticks)
#ax.set_yscale('log')
#ax.grid()
#plt.rc('font', family='serif', serif=['Times'])
#plt.rc('text', usetex=False)
#plt.rc('xtick', labelsize=8)
#plt.rc('ytick', labelsize=8)
#plt.rc('axes', labelsize=8)

plt.legend(loc='upper right', frameon=False)

f.subplots_adjust(wspace=0.18, hspace=0.18)
f.subplots_adjust(left=.00, bottom=.00, right=1., top=1.)

#ax.set_ylabel('Some Metric (in unit)')
#ax.set_xlabel('Something (in unit)')
#ax.set_xlim(0, 3*np.pi)

f.set_size_inches(width, height)

#plt.show()

f.savefig('plot_learning_curves.pdf', bbox_inches='tight')

