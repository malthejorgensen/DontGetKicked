import matplotlib.pyplot as plt
from load import *

states = np.unique(data['VNST'])

bad_buy_avg = []
#states = []
for state in states:
    avg = data[data['VNST']==state]['IsBadBuy'].mean()
    bad_buy_avg.append(avg)
    #print data[data['VNZIP1']==zip]['IsBadBuy'].mean()*100

    #if avg > 0.2:
    #   states.append((state, avg, len(data[data['VNST']==state])))

bar_pos = np.arange(len(states))*2

bars = plt.bar(bar_pos, bad_buy_avg)
for (state, bar) in zip(states, bars):
    height = bar.get_height()
    plt.text(bar.get_x()+bar.get_width()/2., 1.05*height, len(data[data['VNST']==state]),
            ha='center', va='bottom', rotation=90)


plt.xticks(bar_pos, states, rotation=90)

#print zips

plt.show()

'''
x = 'WarrantyCost'
y = 'VehicleAge'
plot.plot(data[x], data[y], 'bo', markersize=5, antialiased=True)
plot.xlabel(x)
plot.ylabel(y)
plot.draw()
plot.show()
'''