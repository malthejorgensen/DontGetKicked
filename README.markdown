# DontGetKicked
This is a project for the [Kaggle](http://kaggle.com) competition [Don't Get Kicked!](http://www.kaggle.com/c/DontGetKicked).

The project uses:

 * [Python](python.org) (tested with 2.6 and 2.7)
 * [numpy](http://numpy.org/) (tested with 1.6.1, _does not work with 1.5.1_)
 * [FANN](http://leenissen.dk/fann/wp/) (2.1.0)
 * [argparse](http://pypi.python.org/pypi/argparse) (tested with 1.1)
 * [matplotlib](http://matplotlib.sourceforge.net) (tested with 1.0.1)
	* only needed for: `zipcodes.py`, `states.py`


The project currently consists of the following files:

__Main files__

 * `load.py` Loads the training data and transforms it into training data for FANN. _(Step 1)_
 * `train.py`
 	* Trainer. Runs FANN on generated training data and generates neural network. _(Step 2)_
	* Tester. Runs generated neural network on generated testing data. _(Step 3)_

_Note_: Training data and testing data are basically the same (they have the same format),
        but it is recommended to have them in seperate files so you don't test on the same data you trained on.

__Auxiliary files__
 
 * `zipcodes.py` -- Plots the _IsBadBuy_ score for each zipcode.
 * `states.py` -- Plots the _IsBadBuy_ score for each state.

## Basic usage

1. Make training file (reads from `training.csv` outputs to `data/train.dat`)

        python load.py

2. Make test file (reads from `training.csv` outputs to `data/train.dat`)

        python load.py --test-data --range 2001,4000
   
   * The training data is by default made from line 1-2000 in `training.csv`, here we choose line 2001-4000
3. Train the neural network (reads from `data/train.dat` and outputs the neural network to `networks/default.net`)

        python train.py

4. Test the neural network (reads from `data/test.dat` using the neural network in `networks/default.net`)

        python train.py --test

## Advanced usage

1. Make training file (reads lines 5000-6000 from `training.csv` outputs to `data/minimal_train.dat`)
   
   The training file's input neurons is specified in `config/datamapping/minimal.py`

        python load.py --data-mapping minimal --range=5000,6000 --train-file 'data/minimal_train.dat'

2. Make test file (reads lines 3700-4700 from `training.csv` outputs to `data/minimal_train.dat`)
   
   The test file's input neurons is specified in `config/datamapping/minimal.py`

        python load.py --data-mapping minimal --range=3700,4700 --test-file 'data/minimal_test.dat'
   
3. Train the neural network (reads from `data/minimal_train.dat` and outputs the neural network to `networks/minimal.net`)
   
   The neural network's learning rate, hidden layer etc. is read from `config/learn/minimal.py`

        python train.py --train-file 'data/minimal_train.dat' --neural-config minimal --network-file 'networks/minimal.net'

4. Test the neural network (reads from `data/minimal_test.dat` using the neural network in `networks/minimal.net`)
   Also gives line-by-line output of the test results

        python train.py --test-file 'data/minimal_test.dat' --network-file 'networks/minimal.net' --full


## load.py
The main file. Loads the training data and transforms it into training data for FANN.


## zipcodes.py
Move along -- nothing to see here...

## states.py
Move along -- nothing to see here...