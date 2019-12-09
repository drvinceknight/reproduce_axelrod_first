# Reproduce Axelrod's first tournament.

Run Axelrod's 1st tournament with a number of potential seeds to try and get the
same results.

## Installation of dependencies

This installs the required dependencies:

    $ conda env create -f environment.yml

Activate the environment:

    $ conda activate reproduce_axelrod_first

This installs the particular Axelrod version needed from the git hash:

    $ pip install git+git://github.com/Axelrod-Python/Axelrod.git@36e82a24ec50dc5b4015d07e443a9eb3fc900272

## Run the experiments

    $ python main.py

## See a quick summary of the data

    $ python main.py --summarise
