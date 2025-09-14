import os, logging, datetime, sys

global errorOutputs
global parent_dir
errorOutputs = []
parent_dir = sys.path[0].split('appfiles')[0]

def getDatetime():
    global date_Ymd
    global date_YmdHMS
    date_Ymd = datetime.datetime.now().strftime("%Y_%m_%d")
    date_YmdHMS = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    return date_Ymd, date_YmdHMS

def getTime():
    currentTime = datetime.datetime.now().strftime("%H:%M:%S")
    return currentTime

def initLogFile(dir_name, type):
    if os.path.isdir(parent_dir + "logfiles\\" + dir_name + "\\" + date_Ymd) == True:
        logfile_name = parent_dir + "logfiles\\" + dir_name + "\\" + date_Ymd + "\\" + dir_name + "_logfile_" + date_YmdHMS + ".log"
        if type == 'INFO':
            logging.basicConfig(filename=logfile_name, level=logging.INFO, force=True)
        elif type == 'ERROR':
            logging.basicConfig(filename=logfile_name, level=logging.ERROR, force=True)
    else:
        if os.path.isdir(parent_dir + "logfiles\\" + dir_name + "") == True:
            os.mkdir(parent_dir + "logfiles\\" + dir_name + "\\" + date_Ymd)
        elif os.path.isdir(parent_dir + "logfiles\\") == True:
            os.mkdir(parent_dir + "logfiles\\" + dir_name + "")
            os.mkdir(parent_dir + "logfiles\\" + dir_name + "\\" + date_Ymd)
        else:
            os.mkdir(parent_dir + "logfiles")
            os.mkdir(parent_dir + "logfiles\\" + dir_name + "")
            os.mkdir(parent_dir + "logfiles\\" + dir_name + "\\" + date_Ymd)
        logfile_name = parent_dir + "logfiles\\" + dir_name + "\\" + date_Ymd + "\\" + dir_name + "_logfile_" + date_YmdHMS + ".log"
        
        if type == 'INFO':
            logging.basicConfig(filename=logfile_name, level=logging.INFO, force=True)
        elif type == 'ERROR':
            logging.basicConfig(filename=logfile_name, level=logging.ERROR, force=True)

def handleInfo(info_msg, dir_name):
    initLogFile(dir_name, 'INFO')
    if '\n' in info_msg:                        # This removes newlines from logfiles. This is done for UI purposes. You can edit the original info_msg to show it to the user in
        info_msg = info_msg.replace('\n', '')   # a more readable format. Meanwhile, a newline breaks the look of a logfile. The same check is done in handleError().
    if dir_name == 'app':
        line = dir_name + ".py: " + info_msg + ' (' + getTime() + ')'
    elif dir_name == 'TFG':
        line = dir_name + "_alloy_ratios.py: " + info_msg + ' (' + getTime() + ')'
    print(line)
    logging.info(line)

def handleError(err_msg, dir_name):
    initLogFile(dir_name, 'ERROR')
    if '\n' in err_msg:
        err_msg = err_msg.replace('\n', '')
    line = dir_name + "_alloy_ratios.py: " + err_msg + ' (' + getTime() + ')'
    print(line)
    logging.error(line)
    gatherErrorOutputs(line)

def gatherErrorOutputs(line):
    errorOutputs.append(line)

getDatetime()