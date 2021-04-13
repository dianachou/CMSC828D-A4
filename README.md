# CMSC828D A4: Evaluating the Performance of A3  

Name: Diana Chou    
Email: dchou4@umd.edu    
    
### Introduction  
#### _Fatal Police Shootings in the United States (2015-2020)_  
The original dataset is comprised of fatal police shootings in U.S. that occurred between January 2015 and June 2020. You will be interacting with a generated dataset of 10,000 tuples that uses the same attributes and distribution based on the original dataset. The data contains basic information about the people who were killed and factors relating the shooting event. For my dashboard, I decided to specifically focus on a person's race, gender, and age group, as well as the date it took place, where it occurred, signs of mental illness, if the suspect was fleeing, and if there was a body camera present to record the incident.    

### Pre-requisite  
1. Make sure you have pip3, python3, and psql installed. _The setup script will create the proper user (```cmsc828d```), database (```a3database```), and corresponding schemas and tables for you._  

### Set-up Instructions 
1. Navigate to the project directory folder: ```cmsc828d_a4_dchou/```
2. Run the ```setup.sh``` script: 
```bash
./setup.sh
```

### Launching the Interface
Run the following to start the experiment:
```bash
python3 ./server.py
```
If you see the following, then you have successfully connected to the database:
```bash 
Connecting to database
	->host='localhost' dbname='a3database' user='cmsc828d'
Connected!
```
Now, open the web page http://127.0.0.1:8000/ with any browser to run the dashboard.

### Notes
1. If you have any additional feedback on any part of this process (i.e. setting up the interface, interacting with the vis, etc.) , please include it in the last prompt on the google form labeled: "_Please provide any additional feedback here_"
2. **All tasks are to be performed on the A3 dashboard**. I will not be asking you to make observations on the A2 dashboard, but it is included in the setup so that you may interact with it if you are interested. 
   * You can access the A2 dashboard interface by visiting the page: http://127.0.0.1:8000/a2
   * If you have any feedback after interacting with both the A3 and A2 dashboards, please include it in the last prompt on the form as well.
3. For your convenience, there are buttons at the top right of the screen that can record when you start and end each task. _This information is important to understand how long each task took, so **please use these controls during the evaluation**._
  
### Tasks
Please fill out the following form to complete tasks and provide feedback: [[Form Link]](https://forms.gle/SLpYdX4v64Tan9bX9)<br>  
You will be asked to **perform 4 tasks** and **upload a user log file (logs.txt)** at the end of the evaluation.
  
If you have any questions, please feel free to reach out to me with any of the following methods:  
Email: dchou@umd.edu  
Phone: (240) 477-2994