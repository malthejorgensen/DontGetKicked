import numpy as np
import datetime
import time

import argparse

parser = argparse.ArgumentParser(description='Load training and process data.')
parser.add_argument('--force-load', action='store_true', help='Force loading of data. (Forces creation of a new tempfile)')
parser.add_argument('--temp-file', default='data.temp', help='File for storing loaded data. (Speeds up load time)')
parser.add_argument('--train-file', default='train.data', help='File for saving FANN training data.')

args = parser.parse_args()

"""
#This would be for N.loadtext
layout = {
	'names':   ('RefId',	'IsBadBuy',	'PurchDate',	'Auction',	'VehYear',	'VehicleAge',	'Make',		'Model',	'Trim',		'SubModel',	'Color',	'Transmission',	'WheelTypeID',	'WheelType',	'VehOdo',	'Nationality',	'Size',		'TopThreeAmericanName',	'MMRAcquisitionAuctionAveragePrice',	'MMRAcquisitionAuctionCleanPrice',	'MMRAcquisitionRetailAveragePrice',	'MMRAcquisitonRetailCleanPrice',	'MMRCurrentAuctionAveragePrice',	'MMRCurrentAuctionCleanPrice',	'MMRCurrentRetailAveragePrice',	'MMRCurrentRetailCleanPrice',	'PRIMEUNIT',	'AUCGUART',	'BYRNO',	'VNZIP1',	'VNST',		'VehBCost',	'IsOnlineSale',	'WarrantyCost'),
	'formats': ('int32',	'S10',	'S10',		'S10',	'int32',	'int32',		'S10',	'S10',	'S10', 	'S10',	'S10',	'S10',		'int32',		'S10',		'int32',	'S10',		'S10',	'S10',				'int32',								'int32',							'int32',							'int32',							'int32',							'int32',						'int32',						'int32',						'S10',		'S10',	'int32',	'int32',	'S10',	'int32',	'S10',		'int32')
}
#N.loadtxt('training.csv', delimiter=',', dtype=layout)
l = []
for i in xrange(len(layout['names'])):
	l.append( (layout['names'][i],layout['formats'][i]) )
print l
"""

colnames = ['RefId', 'IsBadBuy', 'PurchDate', 'Auction', 'VehYear', 'VehicleAge', 'Make',  'Model', 'Trim',  'SubModel', 'Color', 'Transmission', 'WheelTypeID', 'WheelType', 'VehOdo', 'Nationality', 'Size',  'TopThreeAmericanName', 'MMRAcquisitionAuctionAveragePrice', 'MMRAcquisitionAuctionCleanPrice', 'MMRAcquisitionRetailAveragePrice', 'MMRAcquisitonRetailCleanPrice', 'MMRCurrentAuctionAveragePrice', 'MMRCurrentAuctionCleanPrice', 'MMRCurrentRetailAveragePrice', 'MMRCurrentRetailCleanPrice', 'PRIMEUNIT', 'AUCGUART', 'BYRNO', 'VNZIP1', 'VNST',  'VehBCost', 'IsOnlineSale', 'WarrantyCost']

datatypes = [
		('RefId', 'int32'),
		('IsBadBuy', 'i1'),
		('PurchDate', 'int64'),
		('Auction', 'S10'),
		('VehYear', 'int64'),
		('VehicleAge', 'int32'),
		('Make', 'S10'),
		('Model', 'S10'),
		('Trim', 'S10'),
		('SubModel', 'S10'),
		('Color', 'S10'),
		('Transmission', 'S10'),
		('WheelTypeID', 'int32'),
		('WheelType', 'S10'),
		('VehOdo', 'int32'),
		('Nationality', 'S10'),
		('Size', 'S10'),
		('TopThreeAmericanName', 'S10'),
		('MMRAcquisitionAuctionAveragePrice', 'int32'),
		('MMRAcquisitionAuctionCleanPrice', 'int32'),
		('MMRAcquisitionRetailAveragePrice', 'int32'),
		('MMRAcquisitonRetailCleanPrice', 'int32'),
		('MMRCurrentAuctionAveragePrice', 'int32'),
		('MMRCurrentAuctionCleanPrice', 'int32'),
		('MMRCurrentRetailAveragePrice', 'int32'),
		('MMRCurrentRetailCleanPrice', 'int32'),
		('PRIMEUNIT', 'S10'),
		('AUCGUART', 'S10'),
		('BYRNO', 'int32'),
		('VNZIP1', 'int32'),
		('VNST', 'S10'),
		('VehBCost', 'int32'),
		('IsOnlineSale', 'S10'),
		('WarrantyCost', 'int32')
	]


def date_to_timestamp(s):
	if s == 'NULL':
		print 'Holy Balony'
		return 0
	d = s.split('/')
	return time.mktime(datetime.date(int(d[2]), int(d[0]), int(d[1])).timetuple())


import os, marshal
from operator import itemgetter

if not os.path.exists(args.temp_file) or args.force_load:
	data = np.genfromtxt('training.csv',
						 delimiter=',',
						 names=colnames, skip_header=1, # Auto: 'names=True,'
						 dtype=datatypes, # Auto: 'dtype=None,'
						 missing_values='NULL',
						 converters={'PurchDate': date_to_timestamp},
						 skip_footer=70000)
						 #converters={'PurchDate': np.datetime64})
						 #usemask=True)
	data.tofile(args.temp_file)
	np.save(args.temp_file, data)
else:
	#data = np.rec.fromfile(args.temp_file, formats=map(itemgetter(1), datatypes))
	data = np.rec.fromfile(args.temp_file, names=colnames, dtype=datatypes)
	#data = np.load(args.temp_file + '.npy')

datalength = len(data)

options = {}

neurondata = []
neuron_dict = {}

from heapq import nlargest

for name, datatype in datatypes:
	if name in options:
		option = options['name']
	else:
		option = 10

	if option == 'Skip':
		continue

	# dealing with strings
	if datatype == 'S10':
		# get the different values that this column can have
		values = np.unique(data[name])

		value_counts = {}

		# get number of occurences of each value
		for value in values:
			value_counts[value] = (data[name]==value).sum()

		# we select the top 10 values to become our neurons
		if option == 'All':
			selected_values = sorted(value_counts.iteritems(), key=itemgetter(1), reverse=True)
		else:
			selected_values = nlargest(option, value_counts.iteritems(), itemgetter(1))
		count = len(selected_values)
		
		neurons = []
		for i in range(count):
			neurons.append('0 '*i + '1' + ' 0'*(count-i))
		
		neuron_dict[name] = dict(zip(map(itemgetter(0), selected_values), neurons))
		neuron_dict[name][None] = '0 '*count + '1'

		print neuron_dict[name]

'''
	if datatype == 'int32':
		dmin = data[name].min()
		dmax = data[name].max()
		print name
		print dmin, dmax
'''

lines = []
for r in xrange(datalength):

	line = []

	for cname in colnames:
		if dict(datatypes)[cname] != 'S10':
			continue
		
		if data[r][cname] in neuron_dict[cname]: 
			line.append(neuron_dict[cname][data[r][cname]])
		else:
			line.append(neuron_dict[cname][None])
		
	lines.append(' '.join(line)+'\n')
	lines.append(str(data[r]['IsBadBuy'])+'\n')
			
open(args.train_file, 'w').writelines(lines)

#print data[data['WarrantyCost']>2000]['RefId']

"""

from pyfann import libfann

connection_rate = 1
learning_rate = 0.7
num_input = 2
num_neurons_hidden = 4
num_output = 1

desired_error = 0.0001
max_iterations = 100000
iterations_between_reports = 1000

ann = libfann.neural_net()
ann.create_sparse_array(connection_rate, (num_input, num_neurons_hidden, num_output))
ann.set_learning_rate(learning_rate)
ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)

ann.train_on_file("../../examples/xor.data", max_iterations, iterations_between_reports, desired_error)

ann.save("nets/xor_float.net")
"""