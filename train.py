import argparse

parser = argparse.ArgumentParser(description='Train and test neural network on generated training and test data.')

parser.add_argument('--network-file', default='networks/default.net', help='File where FANN neural network is stored.')

parser.add_argument('--train-file', default='data/train.dat', help='File where FANN training data is stored.')

parser.add_argument('--test', action='store_true', help='Test neural network (instead of training it).')
parser.add_argument('--full', action='store_true', help='Fully test of neural network (print result for all test input).')
parser.add_argument('--test-file', default='data/test.dat', help='File where FANN test data is stored.')

parser.add_argument('--neural-config', default='standard', help='Which config (number of neurons in hidden layer etc.) to use. The files are stored in config/learnneurons/')


#parser.add_argument('--skip-header', default=0, type=int, help='Skip this number of lines from beginning of file.')
#parser.add_argument('--skip-footer', default=0, type=int, help='Skip this number of lines from end of file.')
#parser.add_argument('--range', default='0,2000', help='The range of data rows to be output to the file ("START,END").')

args = parser.parse_args()


from pyfann import libfann

def TestOnData(nn, testdata):
    ann = libfann.neural_net()
    ann.create_from_file(nn)
    
    trainingData = libfann.training_data()
    trainingData.read_train_from_file(testdata)
    #print trainingData.length_train_data()
    ann.reset_MSE()
    ann.test_data(trainingData)
    print "Bit Fail: " + str(ann.get_bit_fail())
    print "Mean Squared Error: " + str(ann.get_MSE())


def TrainOnData(filename, output):
    conf = __import__("config.learnneurons.%s" % args.neural_config, globals(), locals(), ['*'])

    inputNodes = int(open(filename).readline().split()[1])
    outputNodes = int(open(filename).readline().split()[2])

    ann = libfann.neural_net()
    ann.create_sparse_array(conf.connection_rate, (inputNodes, conf.hiddenNodes, outputNodes))
    ann.set_learning_rate(conf.learning_rate)
    ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)

    ann.train_on_file(filename, conf.max_iterations, conf.iterations_between_reports, conf.desired_error)

    ann.save(output)

if args.test:
    TestOnData(args.network_file, args.test_file)
else:
    TrainOnData(args.train_file, args.network_file)
