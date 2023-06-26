# A collection of Badger Plugins and Instructions made by Sam for SECAR and COSY


# In PROGRESSSS


## Setting Up Badger


First we need to install badger using


```
pip install badger-opt
```


 There are other ways to download or set up a badger environment in the links below.


Then, we need some plugins. We can either clone this repo and use the plugin directory above, or we can find the plugins from some place else.


Once badger is installed and a pathway is set. Type the command


```
badger
```


 into your terminal. This will prompt you to set some paths. For the database, logbook, and archive roots, make three new directories in a preferred spot. These are just to save information about routines that have been run. The plugin root needs to be the directory above, or another directory with plugins.


To list all of the configuration keys. Use the command


```
badger config
```


To then change a specific key or path, use


```
badger config KEY
```


 and follow the prompts.


## General Description of Badger


Badger is a multidimensional optimizer. Badger uses a plugin system to run optimization routines. The user selects an algorithm, an environment, and some configuration, which variables to tweak and objectives to optimize. This is called a routine. You can save these routines in badger and run them again either in the command line or the GUI. Badger already comes with some algorithms already premade, all a user then needs to do is define an environment, described below. Badger is simple to use and offers interfaces to interact with external machines through channels such as using pyepics.


## Brief Overview of Plugin Types


### Algorithms


This type of plugin specifies the algorithm being used to evaluate the optimization problem. There are a lot of algorithm plugins already in this repo and others you will find. The extension `xopt` allows for more options as well. It is possible to create your own algorithm plugin and may be useful, but it is not necessary to use badger.


### Environments


Environments are where you set up the optimization problem. This is where you define your variables that you will be tuning, and the objectives that will be optimized. You can also define additional parameters and the bounds of your tuning variables. Environments are the most important part of badger, and what makes badger easy to use. One badger environment could be used to solve an optimization problem imaginable, but choosing what problems to solve in what environment is an important part in making badger easy to use for someone who is not as familiar with badger.


### Interfaces


Interfaces allow for easy code reuse when interacting with an external machine when dealing with non-analytical problems with badger. For example, there is an interface for `pyepics`, this makes it extremely simple to set up an environment where you have to set and get pv channels. Interfaces are there so you do not have to rewrite code for every environment, but simply can use the same code again when defining a new problem.


## How to Set Up Plugins


First off, for any plugin there needs to be a specific file structure. In the directory that is the plugin roots. The file structure would look like this. Where this directory is within the respective plugin type folder.


```
| --<PLUGIN_ID>
    |-- __init.py__
    |-- configs.yaml
    |-- README.md
```


Examples of these are within the plugin directory



### Implementing an Algorithm into Badger

To build an algorithm plugin in badger, we use the file format above. In the `__init__.py` file, you define a function `optimize()` that has two inputs

`evaluate()`

Inputs: X (a 2-d array) or None. The points that the environment pluggin will be evaluated at. 

Return: Y, E, I, X. Y the observations, E the equality constraints, I the inequality constraints, and X the points evaluated at. If X is None, then Y, E, and I are returned as None and X is the initial/current state of the input variables. 

`params`

The algorithm parameters determined by the configuration files, typically itemgetter is used to unpack these. 

Import the relevant packages for your specific optimization, then write the optimization as you typically would when given a specific problem. Note that the bounds for each of the input variables in badger are normalized, so if the optimization requires inputs for bounds for each variable, make sure that they are set to [0,1]. You can also use `evaluate(None)` to get the initial input variables and dimensionality of the problem. It is also typically useful to create a new function inside the `optimize()` called `_evaluate()` that uses the `evaluate()` function, but defines in a way that the function uses the same input and output types that are required by the packages used to do the optimization. 

A configuration file also needs to be provided, this is where the default hyperparameters can be set, but also having the availiblity to change them through badger when making a new routine. This is mainly used for hyperparameters than may need tweaking, other hyperparameters can just be hardcoded into the `__init__.py` script. 


### Setting Up and Environment


In the `__init__.py` file, we have to substantiate a subclass that includes the methods we need to define our optimization problem. In the `configs.yaml` for the Environment, it is important to note that if you are using an interface, it needs to be specified within this configuration file.


#### Methods


Let's discuss some of the methods used in the `__init__.py` file.


 `__init__()`
 
It is typically useful if you are doing an analytical problem, to make a dictionary with keys and initial values. If using an interface, usually there is some way to set up what the pv's are or how the variables you define interact with the environment.


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


You may not have to set up an interface with Badger because most likely, it already exists. There already exists an interface for epics with badger, and I have made an interface that interacts with COSY. It is still however useful to know how to create one; compared to creating an algorithm it is much simpler.




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


It is first necessary to explain what a routine means in Badger. A routine is where you pick what algorithm, what environment and the configuration. The configurations can either be passed in the command line as a `.yaml` file or selected in the GUI. The configuration consists of what variables you are tuning and their ranges, what objectives you are optimizing, constraints put on certain objectives, and what states you want to observe. How is this different from what you defined in the environment? This allows you to hand pick what variables you want for a specific routine, or what objectives you want to match together. This again is about striking a balance between having the right amount of components in an environment. We can also change the algorithm parameters and the environment parameters when creating a routine.


### Running a Routine from the Command Line


To find routines that already exist. Use the command


```
badger routine
```


To then get details about the configurations of a routine use the command


```
badger routine ROUTINE
```


where `ROUTINE` is the routine name


Then to run that routine use the command


```
badger routine ROUTINE -r [-y] [-v [{0,1,2}]]
```


With the option of the -y to run it without confirmation and -v for the verbosity level.
0 being not printing any values, 1 being printing the optimal solutions, and 2 being printing all interactions
 
To run and save a new routine use the command


```
`badger run  -a ALGO_NAME [-ap ALGO_PARAMS] -e ENV_NAME [-ep ENV_PARAMS] -c ROUTINE_CONFIG [-s SAVE_NAME] [-y] [-v [{0,1,2}]]
```


With ALGO_NAME and ENV_NAME the name of the specified algorithm and environment. ALGO_PARAMS and ENV_PARAMS being a dictionary like `"{"key":value}"` written into the command line. A routine configuration file which will be shown below. -s if you want to save with a name, and the other two flags


#### Routine Configuration Files


To run a new routine from the command line, you need to pass in a configuration file that determines the variables, objectives, constraints and states.


An example would look like this


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


Note the other option for objective is `MAXIMIZE`. The other options for constraints are `EQUAL_TO` and `GREATER_THAN`.




### Running a Routine in Badger's GUI


#### Instructions


First, you need to open the GUI for badger. Use the command


```
badger -ga
```


When you first open badger you will see something like this


![image](/doc_images/badgerdoc1.png)




On the left side, it will be empty for now, but once you create and save a routine, they will appear where you can search through them. On the right side, is the 'Run Monitor', this is where the results of a routine are displayed. To start creating a new routine, click on 'Routine Editor'.


![image](/doc_images/badgerdoc2.png)


For the 'Metadata' section, all you need to do for now is give your routine a name. Usually badger provides a fun sounding animal name as a recommendation.


Next we need to choose an algorithm.


![image](/doc_images/badgerdoc3.png)


Use the drop down menu to select an algorithm. You can use the text box next to where it says 'Params' to change any hyperparameters. There is also an option to change the scaling.


Next scroll down to the 'Environment + VOCS' tab


![image](/doc_images/badgerdoc4.png)


Again, use the drop down menu to select which environment you wish to choose. In the box next to 'Params', you can change the environment parameters. In the 'Vars' tab you can select which variable to tune and change their ranges. In the 'Objs' tab, you can select which objectives to optimize and whether they are to be minimized or maximized.


![image](/doc_images/badgerdoc5.png)


You can also set your constraints and states you'd like to observe.


This part is the same as creating a configuration file except you use the GUI.


You can then save the routine, make sure to save it with a unique name different from other routines. You are then brought back to the 'Run Monitor'.


![image](/doc_images/badgerdoc6.png)


Then press run to run the routine. While the routine is running, you have the option to pause it, then resume it.


![image](/doc_images/badgerdoc7.png)


Once we have finished running, we can delete the run, logbook the run to the logbook directory, find the optimal solution, reset the variable back to their initial conditions, or set the variables to the optimal solution. The values for each run were printed to the command line, but they are also visible through the run monitor if you drag up the bottom bar.


![image](/doc_images/badgerdoc8.png)


Note that now in the left hand side, we can also see some of our other possible saved runs.


That is about all you need to know to be able to use Badger's GUI.


#### Notes


Badger's GUI has some flaws. When in the 'Routine Editor', be careful when scrolling because you can scroll through the algorithms or environments and crash badger. Badger does not also like editing a routine, it is best if you are going to change a routine, give it a new name and save it that way, this will save some annoyance trying to delete the old routine in the side window and trying to name it the same thing. Sometimes it will change what's in the 'Routine Editor'. The GUI is useful, but for running multiple routines in a row, it can be best to run badger from the command line, or have a python script run the command.


## Badger for SECAR


In this repository, there are a few environmental plugins for SECAR. As of now, the main one used to optimize the steerers is named `SECAR_VIOLA`. In its folder is a README file that contains the relevant information on how to use that environment. In the future, there will be an environment with the goal of optimizing multiple objectives, such as maximizing intensity or minimizing beam spot size, using a linear combination of quads based on the PCA. This would require integrating Faraday Cups into badger.


## A Very COSY - Badger






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
