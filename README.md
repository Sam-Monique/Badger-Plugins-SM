# A collection of Badger Plugins and Intructions made by Sam for SECAR and COSY 

## Setting Up Badger 

First we need to install badger using `pip install badger-opt`. There are other ways to download or setup a badger enviroment in the links below.

Then, we need some plugins. We can either clone this repo and use the plugin directory above, or we can find the plugins from some place else.

Once badger is installed and a pathway is set. Type the command `badger` into your terminal. This will prompt you to set some paths. For the database, logbook, and archive roots,
make three new directories in a prefered spot. These are just to save information about routines that have been run. The plugin root needs to be the directory above, or another directory with plugins. 

To list all of the configuration keys. Use the command `badger config`. To then change a specfic key or path, use `badger config KEY`

## General Description of Badger

Badger uses a plugin system to run optimization routines. The user selects an algorithm, and environment, and some configuration, which variable to tweek and objectives to optimize. This is called a routine. You can save these routines in badger and run them again either in the command line or the GUI. 

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

Let's discuss some of the methods used in the `__init__.py` file. In the `__init__` method, it is typically useful if you are doing an analytical problem, to make a dictionary with keys and initial values. If using an interface, usually there is some way to set up what the pv's are or how the variables you define interact with the environment. The `list_vars` and `list_obese` are needed just to return a list of the names of each of the variables and objectives respectively. In the `get_default_parameters`, we set up our default parameters, usually None, but in a case where we want to change a value for an individual routine, it can be very useful. We can call these values by using the keys with the dictionary `self.params`. For the method `_get_vrange`, we set the variable ranges, we can either set the same variable range for all variables, or use a dictionary to set different ranges for each variable, if this method is not defined, it is defaulted to a variable range of [0,1]. The `_get_var` and `_set_var` is where we define how to get the current value of a variable and how we set a variable, either through a dictionary or a pv. Where most of the work is done in defining an environment, there is the `_get_obs`. This is where we define what the different objectives are that will be optimized. Using just those methods, we can create an environment. For the sake of simplicity, it is easiest just to copy the outline of this type of file from one of the examples.

### Creating an Interface

You may not have to set up an interface with Badger because most likely, it already exist. There already exists an interface for epics with badger, and I have made an interface that interacts with COSY. It is still however useful to know how to create one; compared to creating an algorithm it is much simpler. It only requires three methods, `get_default_params`, similar to before. As well as `get_value` and `set_value` where you define how to get and set a value based of a channel or variable name. All this does is prevents one having to rewrite how to set and get values from external machines. 

## How to Run a Routine

It is first necessary to explain what a routine means in Badger. A routine is where you pick what algorithm, what environment and the configuration. The configurations can either be passed in the command line as a `.yaml` file or selected in the GUI. The configuration consist of what variables you are tuning and their ranges, what objectives you are optimising, constraints put on certain objective, and what states you want to observe. How is this different that what you defined in the environment? This allows you to hand pick what variables you want for a specfic routine, or what objectives you want to match together. This again is about striking a balance between having the right amount of components in an environment. We can also change the algorithm paramters and the environment parameters when creating a routine. 

### Running a Routine from the Command Line



### Running a Routine in Badger's GUI

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
| `badger run  -a ALGO_NAME [-ap ALGO_PARAMS] -e ENV_NAME [-ep ENV_PARAMS] -c ROUTINE_CONFIG [-s SAVE_NAME] -y [-v [{0,1,2}]]`  | runs and saves a new routine |
| `badger routine ROUTINE -r -y` | Runs a saved routine |
| `badger -h` | badger help |
| `badger config` | list all configurations |
| `badger config KEY` | config KEY in the configuration list |

For the command `badger run`. `-ap` and `-ep` are optional and only change preexisting parameters. `-y` runs the routine without asking for confirmation, and `-v` is the verbose level

## Helpful Links/ Other Repos

[Badger Github](https://slac-ml.github.io/Badger/)

[Documentation](https://slac-ml.github.io/Badger/docs)

[Badger hands on session Github](https://github.com/SLAC-ML/Badger-Handson)