## Created this file in src/mcqgenerator after finishing 
###experimenting in jupyter notebook 

##purpose of this file is to log everything we code 
### We will define a logging obbject in this file, and 
### import into all of our project files 

## Logging will allow for us to know our history about 
### what we've done 

import logging 
import os 
from datetime import datetime

##create log file: 
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

##in the above, we are basically collecting the current time 
### (datetime.now()) and formatting it in the way we want to (strftime method)

##create a specific path for the log file (sldo creates a new folder to keep the logs)
log_path = os.path.join(os.getcwd(), 'logs')

os.makedirs(log_path, exist_ok= True)

#inside our new folder, I will create the new log file 
LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

##create logging object 
logging.basicConfig(level = logging.INFO, ##defines at what level you wan to log information
        ##at INFO level, it will capture all the information in the INFO level AND above (nothing below this level-- see python logger docs for more info)
        filename = LOG_FILEPATH,
        format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s")


