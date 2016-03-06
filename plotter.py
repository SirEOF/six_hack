#!/bin/env/python

import matplotlib.pyplot as plt
import random
"""
given a number of days, generate a spending report with categories and send the png to the bot
"""

# The slices will be ordered and plotted counter-clockwise.
labels = ['groceries', 'entertainment', 'books', 'shopping']
b = random.randint(2, 98)
a = random.randint(1, b - 1)
c = random.randint(b + 1, 99)
percents = [a, b - a, c - b, 100 - c]
print percents

colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
explode = (0, 0, 0, 0)  # explode a slice if required

plt.pie(percents, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=False)
        
#draw a circle at the center of pie to make it look like a donut
centre_circle = plt.Circle((0,0),0.75,color='black', fc='white',linewidth=1.25)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)


# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
fig_name = 'foo{}'.format(random.randint(1,1000000000000))
#fig.savefig(fig_name, dpi=300)

max_per = max(percents)
to_watch = labels[percents.index(max_per)]

print fig_name, (max_per, to_watch)
return "you should watch your spending on {}".format(to_watch)
#return fig_name, (max_per, to_watch)
