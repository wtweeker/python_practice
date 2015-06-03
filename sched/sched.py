from datetime import datetime
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler

each = 20

def tick():
    print('Tick! The time is: %s' % datetime.now())
    global total
    global start
    global end
    left = total - end
    if left == 0:
        start = 0
        end = 0
        left = total
    
    if left < each:
        end = total
    else:
        end = start + each
        
    print("start: {0}, end: {1}".format(start, end))
    for i in range(start, end):
        print('i: {0}'.format(i))
    start = end


if __name__ == '__main__':
    total = 27
    start = 0
    end = 0
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # Not strictly necessary if daemonic mode is enabled but should be done if possible
