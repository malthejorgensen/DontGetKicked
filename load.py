import numpy as np
import datetime
import time

import argparse

parser = argparse.ArgumentParser(description='Load training and process data.')
parser.add_argument('--force-load', action='store_true', help='Force loading of data. (Forces creation of a new tempfile)')
parser.add_argument('--temp-file', default='data.temp', help='File for storing loaded data. (Speeds up load time)')

parser.add_argument('--train-file', default='train.data', help='File for saving FANN training data.')

parser.add_argument('--test-data', action='store_true', help='Save FANN test data (instead of training data).')
parser.add_argument('--test-file', default='test.data', help='File for saving FANN test data.')

parser.add_argument('--skip-header', default=0, type=int, help='Skip this number of lines from beginning of file.')
parser.add_argument('--skip-footer', default=0, type=int, help='Skip this number of lines from end of file.')

parser.add_argument('--range', default='0,2000', help='The range of data rows to be output to the file ("START,END").')

args = parser.parse_args()

r_start, r_end = 0, 0
if args.range != 'all':
    r_start, r_end = map(int, args.range.split(','))

'''
strlen = 30
strtype = np.dtype('S' + str(strlen))
#strtype = 'S' + str(strlen)
'''

"""
#This would be for N.loadtext
layout = {
    'names':   ('RefId',    'IsBadBuy', 'PurchDate',    'Auction',  'VehYear',  'VehicleAge',   'Make',     'Model',    'Trim',     'SubModel', 'Color',    'Transmission', 'WheelTypeID',  'WheelType',    'VehOdo',   'Nationality',  'Size',     'TopThreeAmericanName', 'MMRAcquisitionAuctionAveragePrice',    'MMRAcquisitionAuctionCleanPrice',  'MMRAcquisitionRetailAveragePrice', 'MMRAcquisitonRetailCleanPrice',    'MMRCurrentAuctionAveragePrice',    'MMRCurrentAuctionCleanPrice',  'MMRCurrentRetailAveragePrice', 'MMRCurrentRetailCleanPrice',   'PRIMEUNIT',    'AUCGUART', 'BYRNO',    'VNZIP1',   'VNST',     'VehBCost', 'IsOnlineSale', 'WarrantyCost'),
    'formats': ('int32',    'S10',  'S10',      'S10',  'int32',    'int32',        'S10',  'S10',  'S10',  'S10',  'S10',  'S10',      'int32',        'S10',      'int32',    'S10',      'S10',  'S10',              'int32',                                'int32',                            'int32',                            'int32',                            'int32',                            'int32',                        'int32',                        'int32',                        'S10',      'S10',  'int32',    'int32',    'S10',  'int32',    'S10',      'int32')
}
#N.loadtxt('training.csv', delimiter=',', dtype=layout)
l = []
for i in xrange(len(layout['names'])):
    l.append( (layout['names'][i],layout['formats'][i]) )
print l
"""

from config.datatypes.standard import *


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
                         names=colnames, skip_header=1+args.skip_header, # Auto: 'names=True,'
                         dtype=datatypes, # Auto: 'dtype=None,'
                         missing_values='NULL',
                         converters={'PurchDate': date_to_timestamp},
                         skip_footer=args.skip_footer)
                         #converters={'PurchDate': np.datetime64})
                         #usemask=True)
    data.tofile(args.temp_file)
    np.save(args.temp_file, data)
else:
    #data = np.rec.fromfile(args.temp_file, formats=map(itemgetter(1), datatypes))
    data = np.rec.fromfile(args.temp_file, names=colnames, dtype=datatypes)
    #data = np.load(args.temp_file + '.npy')

datalength = len(data)
if args.range == 'all':
    r_start = 1
    r_end = datalength

# load options from config file (config/skipalot.py)
from config.neurons.standard import *

neurondata = []
neuron_count = 0
neuron_dict = {}
int_intervals = {}

from heapq import nlargest

for name, datatype in datatypes:
    if name in options:
        option = options[name]
    else:
        option = 10

    if option == 'Skip':
        continue

    # dealing with strings
    if datatype == 'S10':
        # get the different values that this column can have
        values = np.unique(data[name])

        # if we have selected more values than are actually present (in data)
        if option != 'All' and option >= len(values):
            option = 'All'

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
        neuron_count += count
        
        neurons = []
        for i in range(count):
            if option == 'All':
                minus = 1
            else:
                minus = 0
            neurons.append('0 '*i + '1' + ' 0'*(count-i-minus))
        
        
        neuron_dict[name] = dict(zip(map(itemgetter(0), selected_values), neurons))
        if option != 'All':
            neuron_dict[name][None] = '0 '*count + '1'

        print neuron_dict[name]

    if datatype[0:3] == 'int':
        if option == 'Decimal':
            neuron_count += 1
            continue
        else:
            neuron_count += option

            dmin = data[name].min()
            dmax = data[name].max()
            dinterval = np.linspace(dmin, dmax, num=option+1)
            int_intervals[name] = dinterval
            print name
            print dmin, dmax
            print dinterval


lines = []

print r_start
for r in xrange(r_start-1, r_end-1):

    line = []

    for cname in colnames:
        if options[cname] == 'Skip':
            continue
        
        if dict(datatypes)[cname] == 'S10':
            if data[r][cname] in neuron_dict[cname]: 
                line.append(neuron_dict[cname][data[r][cname]])
            else:
                line.append(neuron_dict[cname][None])
        if dict(datatypes)[cname][0:3] == 'int':
            if options[cname] == 'Decimal':
                line.append(str(data[r][cname]))
            else:
                c = len(int_intervals[cname]) - 1
                for i in range(1, len(int_intervals[cname])):
                    if int_intervals[cname][i-1] <= data[r][cname] <= int_intervals[cname][i]:
                        #line.append(str(data[r][cname]))
                        line.append('0 '*(i-1) + '1' + ' 0'*(c-i))
                        break

            
    lines.append(' '.join(line)+'\n')
    lines.append(str(data[r]['IsBadBuy'])+'\n')

out_file = args.train_file
if args.test_data:
    out_file = args.test_file

s = "%u %u %u\n" % (r_end - r_start, neuron_count, 1)
open(out_file, 'w').write(s)
open(out_file, 'a').writelines(lines)

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