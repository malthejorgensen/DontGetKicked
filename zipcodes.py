import matplotlib.pyplot as plt
from load import *

print np.unique(data['Auction'])
zipcodes = np.unique(data['VNZIP1'])


bad_buy_avg = []
zips = []
for zip in zipcodes:
	avg = data[data['VNZIP1']==zip]['IsBadBuy'].mean()
	bad_buy_avg.append(avg)
	#print data[data['VNZIP1']==zip]['IsBadBuy'].mean()*100

	if avg > 0.2:
		zips.append((zip, avg, len(data[data['VNZIP1']==zip])))

bar_pos = np.arange(len(zipcodes))

plt.bar(bar_pos, bad_buy_avg)

plt.xticks(bar_pos[::10], zipcodes[::10], rotation=90)

print zips

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