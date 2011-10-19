import pyfann import libfann

def TestOnData(self, nn, testdata):
    ann = libfann.neural_net()
    ann.create_from_file(nn)

    data = libfann.read_train_from_file(testdata)
    fann_reset_MSE(ann)
    fann_test_data(ann, data)
    print "Mean Squared Error: " + str(fann_get_MSE(ann))


def TrainOnData(self, filename, output):
    connection_rate = 1
    learning_rate = 0.7

    #inputNodes = # Some coooool number
    #hiddenNodes = inputNodes * 2
    #outputNodes = 1
    
    desired_error = 0.0001
    max_iterations = 100000
    iterations_between_reports = 1000

    ann = libfann.neural_net()
    ann.create_sparse_array(connection_rate, (inputNodes, hiddenNodes, outputNodes))
    ann.set_learning_rate(learning_rate)
    ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)

    ann.train_on_file(filename, max_iterations, iterations_between_reports, desired_error)

    ann.save(output)

TrainOnData("data","NeuralNetwork.out")
TestOnData("NeuralNetwork.out", "TestData")