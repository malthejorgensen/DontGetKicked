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

#TrainOnData("train.data","NeuralNetwork.out")
TestOnData("NeuralNetwork.out", "testdata")