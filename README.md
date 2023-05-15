# A collection of Badger Plugins and Intructions made by Sam for SECAR and COSY 

# In PROGRESSSS

## Setting Up Badger 

First we need to install badger using `pip install badger-opt`. There are other ways to download or setup a badger enviroment in the links below.

Then, we need some plugins. We can either clone this repo and use the plugin directory above, or we can find the plugins from some place else.

Once badger is installed and a pathway is set. Type the command `badger` into your terminal. This will prompt you to set some paths. For the database, logbook, and archive roots, make three new directories in a prefered spot. These are just to save information about routines that have been run. The plugin root needs to be the directory above, or another directory with plugins. 

To list all of the configuration keys. Use the command `badger config`. To then change a specfic key or path, use `badger config KEY`, and follow the prompts.

## General Description of Badger

Badger is a multidimensional optimizer. Badger uses a plugin system to run optimization routines. The user selects an algorithm, an environment, and some configuration, which variables to tweek and objectives to optimize. This is called a routine. You can save these routines in badger and run them again either in the command line or the GUI. Badger already comes with some algorithms already premade, all a user then needs to do is define an environment, described below. Badger is simple to use and offers interfaces to interact with external machines through channels such as using pyepics. 

## Brief Overview of Plugin Types

### Algorithms

This type of plugin specfies the algorithm being used to evaulate the optimization problem. There are a lot of algorithm pluggins alread in this repo and others you will find. The extentsion `xopt` allows for more options as well. It is possible to create your own algorithm plugin and may be useful, but it is not nesscary to use badger. 

### Environments

Environments are where you set up the optimization problem. This is where you define your variables that you will be tuning, and the objectives that will be optimized. You can also define additional parameters and the bounds of your tuning variables. Environments are the most important part of badger, and what makes badger easy to use. One badger environment could be used to solve an optimization problem imaginable, but choosing what problems to solve in what environment is an important part in making badger easy to use for someone who is not as familiar with badger.

### Interfaces

Interfaces allow for easy code reuse when interacting with an external machine when dealing with non-analytical problems with badger. For example, there is interface for `pyepics`, this makes it extremely simple to set up an environment where you have to set and get pv channels. Interfaces are there so you do not have to rewrite code for every environment, but simply can use the same code again when defining a new problem. 

## How to Set Up Environments and Interfaces

First off, for any plugin there needs to be a specfic file structure. In the directory that is the plugin roots. The file structure would look like this. Where this directory is within the respective plugin type folder.

```
| --<PLUGIN_ID>
    |-- __init.py__
    |-- configs.yaml
    |-- README.md 
```

Examples of these are within the plugin directory



### Setting Up and Environment

In the `__init__.py` file, we have to substaintiate a subclass that includes the methods we need to define our optimization problem. In the `configs.yaml` for the Environment, it is important to note that if you are using an interface, it needs to specfied within this configuration file. 

#### Methods

Let's discuss some of the methods used in the `__init__.py` file.

 `__init__()`
 
it is typically useful if you are doing an analytical problem, to make a dictionary with keys and initial values. If using an interface, usually there is some way to set up what the pv's are or how the variables you define interact with the environment.

`list_vars()`

A static method that return the variable names in a list

`list_obese()` 

A static method that return the observation names in a list

`get_default_parameters()`

Set up our default parameters, usually None, but in a case where we want to change a value for an individual routine, it can be very useful. We can call these values by using the keys with the dictionary `self.params`.

`_get_vrange()`

Set the variable ranges, can either set the same variable range for all variables, or use a dictionary to set different ranges for each variable, if this method is not defined, it is defaulted to a variable range of [0,1]. 

`_get_var()`

Method to define when given the name of a variable how to return its current value,either through a dictionary or a pv.

`_set_var()` 

Method to define when given the name of a variable, and a new value how to set the new value, either through a dictionary or a pv.

`_get_obs()`. 

This is how you define what the different objectives are that will be optimized. It should take in an objective name and return the value of that current objective. 


Using just those methods, we can create an environment. For the sake of simplicity, it is easiest just to copy the outline of this type of file from one of the examples. See documentation about a more in depth walkthrough of creating an environment. 

### Creating an Interface

You may not have to set up an interface with Badger because most likely, it already exist. There already exists an interface for epics with badger, and I have made an interface that interacts with COSY. It is still however useful to know how to create one; compared to creating an algorithm it is much simpler. 


#### Interface Methods
It only requires three methods,

`get_default_params()`

Returns the default parameters of the interface, usually and defaulted to None

`get_value()`

Takes in a channel name and returns the value of the pv

`set_value()` 

Takes in a channel name and a value and sets that channel to that value.

To call these methods in an environment use `self.interface.selected_method()` where `selected_method()` is one of the three methods above. Again note the interface has to be specified in the configuration file for the environment. All this does is prevents one having to rewrite how to set and get values from external machines. 

## How to Run a Routine

It is first necessary to explain what a routine means in Badger. A routine is where you pick what algorithm, what environment and the configuration. The configurations can either be passed in the command line as a `.yaml` file or selected in the GUI. The configuration consist of what variables you are tuning and their ranges, what objectives you are optimising, constraints put on certain objective, and what states you want to observe. How is this different that what you defined in the environment? This allows you to hand pick what variables you want for a specfic routine, or what objectives you want to match together. This again is about striking a balance between having the right amount of components in an environment. We can also change the algorithm paramters and the environment parameters when creating a routine. 

### Running a Routine from the Command Line

To find routines that already exist. Use the command

```
badger routine
```

To then get details about the configurations of a routine use the command

```
badger rountine ROUTINE
```

where `ROUTINE` is the routine name

Then to run that routine use the command

```
badger routine ROUTINE -r [-y] [-v [{0,1,2}]]
```

With the option of the -y to run it without confirmation and -v for the verbosity level.
0 being not printing any values, 1 being printing the optimal solutions, and 2 being printing all interations
 
To run and save a new routine use the command

```
`badger run  -a ALGO_NAME [-ap ALGO_PARAMS] -e ENV_NAME [-ep ENV_PARAMS] -c ROUTINE_CONFIG [-s SAVE_NAME] [-y] [-v [{0,1,2}]]
```

With ALGO_NAME and ENV_NAME the name of the specified algorithm and environment. ALGO_PARAMS and ENV_PARAMS being a dictionary like `"{"key":value}"` written into the command line. A routine configuration file which will be shown below. -s if you want to save with a name, and the other two flags

#### Routine Configuration Files

To run a new routine from the command line, you need to pass in a configuration file that determines the variables, objectives, constraints and states.

An example woule look like this

```
variables:
  - x1:
    - -4.0
    - 1.0
  - x2:
    - 0.0
    - 5.0
objectives:
  - y1: MINIMIZE
constraints:
  - y2:
    - LESS_THAN
    - 5
states:
  - y3

```
We set `x1` from [-4.0,1.0], `x2` from [0.0,5.0]. Define an objective of minimizing `y1`. A constraint on `y2` of being less than 5. Observe the state of `y3`

Note the other options for objective is `MAXIMIZE`. The other options for constraints are `EQUAL_TO` and `GREATER_THAN`.


### Running a Routine in Badger's GUI

![image](/doc_images/badger_doc_1.png)

## Some Useful Commands

| Command | Description |
| --- | ---- |
| `badger` | gives badger metadata, run this initially to configure badger |
| `badger -ga` | Launches badger GUI |
| `badger algo` | lists installed algorithms |
| `badger algo ALGO` | get configs of an algorithm |
| `badger env` | lists installed badger environments |
| `badger env ENV` | get configs of an environment | 
| `badger routine` | lists all routines |
| `badger routine ROUTINE` | gives details of a routine |
| `badger run  -a ALGO_NAME [-ap ALGO_PARAMS] -e ENV_NAME [-ep ENV_PARAMS] -c ROUTINE_CONFIG [-s SAVE_NAME] [-y] [-v [{0,1,2}]]`  | runs and saves a new routine |
| `badger routine ROUTINE -r [-y]` | Runs a saved routine |
| `badger -h` | badger help |
| `badger config` | list all configurations |
| `badger config KEY` | config KEY in the configuration list |


## Helpful Links / Other Repos

[Badger Github](https://slac-ml.github.io/Badger/)

[Documentation](https://slac-ml.github.io/Badger/docs)

[Badger hands on session Github](https://github.com/SLAC-ML/Badger-Handson)