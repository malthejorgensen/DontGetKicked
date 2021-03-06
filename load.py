import numpy as np
import datetime
import time

import argparse

parser = argparse.ArgumentParser(description='Load training and process data.')
parser.add_argument('--force-load', action='store_true', help='Force loading of data. (Forces creation of a new tempfile)')
parser.add_argument('--temp-file', default='temp/data.tmp', help='File for storing loaded data. (Speeds up load time)')

parser.add_argument('--train-file', default='data/train.dat', help='File for saving FANN training data.')

parser.add_argument('--test-data', action='store_true', help='Generate and save FANN test data to "data/test.dat". (No training data will be saved)')
parser.add_argument('--test-file', default='', help='Generate and save FANN test data to specified file . (No training data will be saved)')

parser.add_argument('--skip-header', default=0, type=int, help='Skip this number of lines from beginning of file.')
parser.add_argument('--skip-footer', default=0, type=int, help='Skip this number of lines from end of file.')

parser.add_argument('--data-mapping', default='default', help='Change mapping from data to input neurons (/config/datamapping/default.py)')

parser.add_argument('--range', default='1,2000', help='The range of data rows to be output to the file ("START,END").')

args = parser.parse_args()

# parse '--range' argument
r_start, r_end = 0, 0
if args.range.lower() != 'all' and args.range.lower() != 'full':
    r_start, r_end = map(int, args.range.split(','))

if args.test_data and args.test_file == '':
    args.test_file = 'data/test.dat'
elif args.test_file != '':
    args.test_data = True

# load datamapping from config file (e.g. config/datamapping/skipalot.py)
dm = __import__("config.datamapping.%s" % args.data_mapping, globals(), locals(), ['*'])
colnames = dm.colnames
datatypes = map(lambda n: (n, dm.data_options[n][0]), colnames)
options = dict(map(lambda (n, (_, o)): (n, o), dm.data_options.items()))

# convert datestring (MM/DD/YYYY) to unix timestamp
def date_to_timestamp(s):
    if s == 'NULL':
        print 'Holy Balony'
        return 0
    d = s.split('/')
    return time.mktime(datetime.date(int(d[2]), int(d[0]), int(d[1])).timetuple())


import os, marshal
from operator import itemgetter

# load data and save to cachefile
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
    # load from cache
    data = np.rec.fromfile(args.temp_file, names=colnames, dtype=datatypes)

    #data = np.rec.fromfile(args.temp_file, formats=map(itemgetter(1), datatypes))
    #data = np.load(args.temp_file + '.npy')

datalength = len(data)
if args.range.lower() == 'all' or args.range.lower() == 'full':
    r_start = 1
    r_end = datalength

# convert values (strings and ints) to neuron inputs
neurondata = []
neuron_count = 0
neuron_dict = {}
neuron_descriptions = {}
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
        if option != 'All' and option >= len(values)-1:
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
        
        
        neurons = []
        for i in range(count):
            if option == 'All':
                minus = 1
            else:
                minus = 0
            neurons.append('0 '*i + '1' + ' 0'*(count-i-minus))
        
        
        neuron_dict[name] = dict(zip(map(itemgetter(0), selected_values), neurons))
        for v in map(itemgetter(0), selected_values):
            neuron_count += 1
            neuron_descriptions[neuron_count] = (name, v)


        if option != 'All':
            neuron_dict[name][None] = '0 '*count + '1'
            neuron_count += 1
            neuron_descriptions[neuron_count] = (name, '*Other*')

    if datatype[0:3] == 'int':
        if option == 'Decimal':
            neuron_count += 1
            neuron_descriptions[neuron_count] = (name, 'Decimal')
            continue
        else:
            dmin = data[name].min()
            dmax = data[name].max()
            dinterval = np.linspace(dmin, dmax, num=option+1)
            int_intervals[name] = dinterval

            for i in xrange(1, len(dinterval)):
                neuron_count += 1
                neuron_descriptions[neuron_count] = (name, '%u - %u' % (dinterval[i-1], dinterval[i]))



# generate file output
lines = []

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

s = str(neuron_descriptions).replace('), ', '),\n    ')
s = s.replace('{','{\n    ')
s = s.replace('}','\n}')
open(out_file + '.conf.py', 'w').write('neuron_names = ' + s)
