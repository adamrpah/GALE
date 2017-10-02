import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

#set the font
font = {'size'   : 12}
mpl.rc('font', **font)
inset_font_size = 22
#Start up seaborn
sns.set_context('talk')
sns.set_style({'font.family': 'sans-serif', 'font.sans-serif': 'Arial Narrow', 'font.size': 18})
#Create the fontdict for use in 
fontdict = {'size' : 22, 'weight':'bold'}

