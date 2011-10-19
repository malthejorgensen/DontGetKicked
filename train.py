import argparse

parser = argparse.ArgumentParser(description='Train and test neural network on generated training and test data.')

parser.add_argument('--network-file', default='brain.neuralnet', help='File where FANN neural network is stored.')

parser.add_argument('--train-file', default='train.data', help='File where FANN training data is stored.')

parser.add_argument('--test', action='store_true', help='Test neural network (instead of training it).')
parser.add_argument('--test-file', default='test.data', help='File where FANN test data is stored.')

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
    connection_rate = 1
    learning_rate = 0.7

    inputNodes = 99
    hiddenNodes = inputNodes * 2
    outputNodes = 1
    
    desired_error = 0.0001
    max_iterations = 1000
    iterations_between_reports = 10

    ann = libfann.neural_net()
    ann.create_sparse_array(connection_rate, (inputNodes, hiddenNodes, outputNodes))
    ann.set_learning_rate(learning_rate)
    ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)

    ann.train_on_file(filename, max_iterations, iterations_between_reports, desired_error)

    ann.save(output)

if args.test:
    TestOnData(args.network_file, args.test_file)
else:
    TrainOnData(args.train_file, args.network_file)
