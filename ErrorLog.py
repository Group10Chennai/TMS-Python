import logging
#import logging.handlers
#import apiupdate
def get_logger(name):
    #log_format = '%(asctime)s  %(name)8s  %(levelname)5s  %(message)s'
    log_format = '%(asctime)s#:#%(levelname)s#:#%(message)s#'
    #logging.basicConfig(level=logging.DEBUG,format=log_format,filename='/home/pi/Documents/TMS-Git/log/dev.log',filemode='a')
    #console = logging.StreamHandler()
    #logging.basicConfig(level=logging.DEBUG,format=log_format)
    console = logging.handlers.RotatingFileHandler(filename='/home/pi/Documents/TMS-Git/log/BLE_Error.log',mode='a',maxBytes=50000,backupCount=30)   #create multiple log files once the size reached  
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    #return getlogger(name)
    return logging.getLogger(name)

def get_logger1(name):
    #log_format = '%(asctime)s  %(name)8s  %(levelname)5s  %(message)s'
    log_format = '%(asctime)s#:#%(levelname)s#:#%(message)s#'
    #logging.basicConfig(level=logging.DEBUG,format=log_format,filename='/home/pi/Documents/TMS-Git/log/dev.log',filemode='a')
    #console = logging.StreamHandler()
    #logging.basicConfig(level=logging.ERROR,format=log_format)
    console = logging.handlers.RotatingFileHandler(filename='/home/pi/Documents/TMS-Git/log1/SENSOR_Error.log',mode='a',maxBytes=50000,backupCount=30)   #create multiple log files once the size reached  
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)

    return logging.getLogger(name)



