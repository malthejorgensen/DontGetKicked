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

## load.py
The main file. Loads the training data and transforms it into training data for FANN.


## zipcodes.py
Move along -- nothing to see here...

## states.py
Move along -- nothing to see here...