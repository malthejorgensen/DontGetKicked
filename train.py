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
    
    testData = libfann.training_data()
    testData.read_train_from_file(testdata)
    #print trainingData.length_train_data()
    ann.reset_MSE()

    if args.full:
        #print ann.run(testData.get_input())
        #print testData.num_data
        #print testData.num_input
        #print testData.num_output
        inputs = testData.get_input()
        outputs = testData.get_output()

        missed_goodbuys = 0
        missed_badbuys = 0
        correct_goodbuys = 0
        correct_badbuys = 0

        print "#Row\tCorrect\tCalc\tFail"

        for i in xrange(len(inputs)):
            nn_out = ann.run(inputs[i])[0]
            c_out = outputs[i][0]
            s = ' '
            if c_out == 1.0 and nn_out < 0.8:
                s = 'B'
                missed_badbuys += 1
            if c_out == 0.0 and nn_out >= 0.8:
                s = 'G'
                missed_goodbuys += 1
            if c_out == 1.0 and nn_out >= 0.8:
                correct_badbuys += 1
            if c_out == 0.0 and nn_out < 0.8:
                correct_goodbuys += 1
            
            print "%5u\t%1.3f\t%1.3f\t%s" % (i+1, outputs[i][0], ann.run(inputs[i])[0], s)
        print "Missed %u bad buys of %u (%2.1f%%)" % (missed_badbuys, correct_badbuys+missed_badbuys,
                                                    float(missed_badbuys)/(correct_badbuys+missed_badbuys)*100)
        print "Missed %u good buys of %u (%2.1f%%)" % (missed_goodbuys, correct_goodbuys+missed_goodbuys,
                                                     float(missed_goodbuys)/(correct_goodbuys+missed_goodbuys)*100)
    else:
        ann.test_data(testData)
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
