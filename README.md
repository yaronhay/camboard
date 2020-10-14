# CAMBOARD Project

The CAMBOARD project was created as part of the Project Lab in Bar Ilan University.
CAMBOARD was created by Yaron Hay and in cooperation with HILMA tech.

The CAMBOARD project won second place in the [2020 project competition](https://land.cbl.co.il/biu/innovation_and_beyond/) (Hebrew) in the Computer Science Department at Bar-Ilan University, and appeared in the [Maariv Online](https://m.maariv.co.il/business/tech/Article-793734?utm_source=whatsapp) newspaper (Hebrew). 
The presentation movie that entered the project competition is in [YouTube](https://www.youtube.com/watch?v=TDGpc5-Swkk) (Hebrew). 
## Repository Structure

- **BoardShots** Contains some examples of screenshots of the board during its use.
- **calibration** Contains methods of calibration:
  - Point cropping calibration uses the user's mouse to select a list of consecutive points that create a cropping polygon.
  - Rectangle cropping calibration uses the user's mouse to select a rectangle for cropping.
- **conf** Contains some examples for configuration files that were in actual use.
- **core** Contains the main source files of CAMBOARD SmartBoard
- **img** Contains board background images
- **profiling** Python profiling file
- **tutorial** Contains a presentation (English) and a tutorial movie on how to use the board (in Hebrew)
- **experiments** Contains experiments with openCV which are not a part of CAMBOARD's source code.
- **utils** Contains some utilities used throughout the project.

### CAMBOARD Core Components 
In the core directory there are the following components: 
- core_algorithm.py : The board's operation code that controls how the board reacts to different events. 
- detector.py: Detects pen presence and pen movement on the board
- display.py: Displays the shapes on the board
- email.sh: A macOS AppleScript that sends an email using the macOS default email app
- main.py: Initializes the system

## Starting the system
The run.sh script executes the main.py python file that is at the root of the project directory.
The first command line argument is the action that is to be executed. You may read the main.py file to understand the available actions.
Use the following actions to use the system:

### Configuration
Configuration is exported to a configuration file using the *conf* action. Use the command used is
```run.sh conf <conf id> <conf action>```  
When conf id is the configuration file id and conf action is the action to be performed.
#### Cameras Calibration
Use the *bcalib* conf action:  
```run.sh conf <conf id> bcalib <front camera id> <top camera id>```  
The camera id's are integers used to identify video captures in openCV.

#### Menu Calibration
Use the *mcalib* conf action:  
```run.sh conf <conf id> bcalib <front camera id>```  
The camera id is an integer used to identify video captures in openCV.

### Using the board
Use the *track* conf action:  
```run.sh track <conf id> <front camera id> <top camera id>```  
The camera id's are integers used to identify video captures in openCV.
