# CAMBOARD Project

The CAMBOARD project was created as part of the Project Lab in Bar Ilan University.
CAMBOARD was created by Yaron Hay and with cooperation HILMA tech.

## Repository Structure

- **BoardShots** Contains some examples of screenshots of the board during its use.
- **calibration** Contains methods of calibration:
  - Point cropping calibration uses the user's mouse to select a list of consecutive points that create a cropping polygon.
  - Rectangle cropping calibration uses the user's mouse to select a rectangle for cropping.
- **conf** Contains some examples for configuration files that were in actual use.
- **core** Contains the main source files of CAMBOARD:
- **img** Contains 
- **experiments** Contains experiments with openCV which are not a part of CAMBOARD's source code.
- **utils** Contains some utilities used throughout the project.

### CAMBOARD Core Components 
In the core directory there are the following components: 
- core_algorithm.py : The board's operation code that controls how the board reacts to different events. 
-