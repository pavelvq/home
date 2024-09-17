import psutil, time

def waitforclose(pid):
    while True:
        if not psutil.pid_exists(pid):
            break
        time.sleep(1)