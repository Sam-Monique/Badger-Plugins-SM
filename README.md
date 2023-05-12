# A collection of Badger Plugins and Intructions made by Sam for SECAR and COSY 

## Setting Up Badger 

First we need to install badger using `pip install badger-opt`. There are other ways to download or setup a badger enviroment in the links below.

Then, we need some plugins. We can either clone this repo and use the plugin directory above, or we can find the plugins from some place else.

Once badger is installed and a pathway is set. Type the command `badger` into your terminal. This will prompt you to set some paths. For the database, logbook, and archive roots,
make three new directories in a prefered spot. These are just to save information about routines that have been run. The plugin root needs to be the directory above, or another directory with plugins. 

To list all of the configuration keys. Use the command `badger config`. To then change a specfic key or path, use `badger config KEY`

## Some Useful Commands

| Command | Description |
| --- | ---- |
| badger | gives badger metadata, run this initially to configure badger |
| badger -ga | Launches badger GUI |
| badger algo | lists installed algorithms |
| badger algo ALGO | get configs of an algorithm |
|badger env | lists installed badger environments |
| badger env ENV | get configs of an environment | 
| badger routine | lists all routines |
| badger routine ROUTINE | gives details of a routine |
|badger run  -a ALGO_NAME [-ap ALGO_PARAMS] -e ENV_NAME [-ep ENV_PARAMS] -c ROUTINE_CONFIG [-s SAVE_NAME] -y [-v [{0,1,2}]]  | runs and saves a new routine |
| badger routine ROUTINE -r -y | Runs a saved routine |
| badger -h | badger help |
| badger config | list all configurations |
| badger config KEY | config KEY in the configuration list |

For the command `badger run`. `-ap` and `-ep` are optional and only change preexisting parameters. `-y` runs the routine without asking for confirmation, and `-v` is the verbose level

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

In the `__init__.py` file we have to substaintiate and subclass that includes the methods we need to define our optimization problem. In the `configs.yaml` for the Environment, it is important to note that if you are using an interface, it needs to specfied within this configuration file. 

## How to Run a Routine
