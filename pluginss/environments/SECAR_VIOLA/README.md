# Read me for SECAR Optimization of Steering

This environment is built to mimimize the overall steering on SECAR by any combination of bending elements at any viewer position using a user selected combination of any quadruples. As well as return the center of the beam back to a current position.

## Tools 

### EPICS Interface

This environment utilizes the epics interface that comes with badger to set and get magnet values of both quadruples and dipoles.

### Viola Viewer Analysis

Currently, in order for the viewer image analysis to work properly, you need to be on U1PC1. Login to Fernando's user account, open the application Viola. Note first you may have to get into position the viewer being selected using . After the viewer is in place, select the viewer in Viola and make sure the correct image is in place. Adjust the threshold and background as necessary. Once Viola is setup, select preferences at the upper left hand corner, select the bottom most tab. Open this up and copy the location of the dump file in the `np.memmap()` function, this is the first argument. Then run the file named `badger_viola.py`, use the command `python /user/e20008/sam/badger_viola/badger_viola.py location` where location is the the location of the dump file you just copied. This file constantly reads the data and saves it in a text file. Once the routine you are running is done, you will need to interupt this program.  

### setup.py

This environment uses two methods from the `setup.py` file. The first method, `CycleMagnet()` is used to cycle a given magnet, usually a dipole. The second method is `SaveIm()` used to save an image with a given tunename at a specific viewer. 

## Environmental Paramters

### What They Are

`tunename`

This is the tunename that the images will be saved with, this is defaulted to an empty string.

`quad_config`

This is the name of the `config.yaml` file for the quadruple configuration for a specfic routine. The value for this key should the path to the file. If this parameter is no given, there will be an error before you try to start the routine. 

`viewer`

This is the name of the viewer being looked at for this routine. Ex, `D1564`

`optimal_viewer_position`

The optimal viewer position parameter is only needed for the `RETURN_POSITION` observation. This is the optimal x position on the viewer you want the centroid of the beam to return to. 

`viewer_size`

The size of the viewer is needed if the beam is lost. If the beam is lost, the steering is set to the size of the viewer. This could be rid of, if a dictionary of viewer size values were correlated to each viewer.

`optional_transmission`

This is an optional key value. The value that should be given id the initial total number of counts determined by viola. If this is its default value, 0, then the initial transmission is found using the intial quad configruation for the first iteration.

`transmisison_tolerance`

This is the transmission tolerance of the steering. If the transmission, current number of total counts over the initial amount of total counts is less than the transmission tolerance, the steering is set to the size of the viewer. The reason this is done is to give a high weight to iterations that send the beam off the viewer. The beam not being on the viewer may cause the centroid found by Viola to be in an arbitrary position, so if the beam is lost, we just say it is the size of the viewer. This indicates high steering and "tells" the algorithm this is a bad value. This value is defaulted to 0.60. 


### How to Change Them

When you need to change these paramters, there is two ways to do this depending on how you are running badger. If you are running badger from the command line, creating a routine, after specifying the environment, use the flag `-ep` followed with a dictionary the specfies the changes from the defauly parameters. For example

```
-ep "{"tunename": "sample, "quad_config": "config.yaml", "viewer": "D1564", "viewer_size": 0.05}"
```

This only overides the parameters you specified here, it does not for example change `transmission_tolerance` which would still be set to `0.60`

In the GUI, changing these values is pretty straight forward, all you do is edit the value next to the key name in the text box.

## Environment Methods

This notes any revelvant information or changes about any methods.

`_set_var()`

Note about this method, there is a condition in this method that if the set value is greater than that of the current, then the magnet is cycled using the method `CycleMagnet`

`image_analysis()`

This method takes in no arguments, It returns the information found in the `viola.txt` file created by the `badger_viola.py` file that is from the dump file created by Viola. there is a sleep timer here so there is some time between changing the quads and doing the image analysis. The value may need to be changed depending on how long it takes. 

`steer()`

This function takes in no arguments and returns the value of the total steering by each quad. This function does however rely on relevant environmental paramters. The function first sets each quad to its initial value, given by the config file. If the intial transmission is not the defined, hence it is the first interation, the image analysis is done and the current total number of counts is set as the initial transmission. An image is a saved and a total is intitalized. For each quad, while the other quads are at their intial values, the quad is set to the bounds of its range, the image analysis is done, and an image is take for both the high and low value. The x centroid and total counts are noted, the steering or `x_diff` is set to the difference between the positions of the two centriods. If the either of these two transmissions are less than the transmission tolerance, `x_diff` is set to the viewer size. The square of `x_diff` is then added to the total, this then done for each magnet, the `total` is then returned.

## Objective Descriptions

`STEERING`

This returns the value given by the `steer()` method. The goal is to minimize this value for a given combination of quads, dipoles, and viewer locations. 

`RETURN_POSITION`

This objective returns the difference between the postion on the viewer and an optimal position selected by the user given by the environment parameters. The goal is to minimize this value to return the centriod of the beam back to a postion on the viewer, hence the name.

`X_CENTRIOD`

Although defined as an objective, this value is just the x centroid of the beam and is defined here so you can use it as a state and observe what it is for the initial quad configurations at each interation. This value at the optimal solution of mimized steering is what you would use as the optimal position for the `RETURN_POSITION` objective.

## Quad Configuration File Instructions

The file needs to have the extension `.yaml` and the path to the file needs to be specified as the `quad_config` environment parameter. An example of what this would look like
```
Q3:
  range:
    - 0.9
    - 1.1
  initial:
      1.0
Q4:
  range:
    - 0.9
    - 1.1
  initial: 
      1.0
Q5:
  range:
    - 0.9
    - 1.1
  initial: 
      1.0
```