import time



def timestr(secs_since_epoch):
    return time.strftime("%I:%M:%S %p", time.localtime(secs_since_epoch))

