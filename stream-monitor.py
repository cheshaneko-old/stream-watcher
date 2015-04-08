#!/usr/bin/env python

from apscheduler.schedulers.background import BlockingScheduler
import requests
import requests.packages.urllib3.contrib.pyopenssl
import logging



class StreamMonitor:
    LOG_FILE = "monitor.log" 
    STREAM_INFO_URL = "https://api.twitch.tv/kraken/streams/{channel}"
    SUCCESS_STATUS = 200
    TIME_INTERVAL = 10

    def __init__(self, channel, callBack):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("stream-monitor")
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        hdlr = logging.FileHandler(self.LOG_FILE)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        hdlr.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.addHandler(hdlr)

        self.callBack = callBack
        self.channel = channel

        self.sched = BlockingScheduler(timezone="UTC")
    
    def __checkLive(self):
        r = requests.get(self.STREAM_INFO_URL.format(channel = self.channel))
        if self.SUCCESS_STATUS != r.status_code:
            errorMsg = "Channel \"{channel} \" not found".format(channel = self.channel)
            self.logger.error(errorMsg)
            raise Exception(errorMsg)
        json = r.json()
        if ("stream" in json) and (json["stream"] != None):
            self.logger.debug("Channel \"{channel} \" is on".format(channel = self.channel))
            return True
        else:
            self.logger.debug("Channel \"{channel} \" is off".format(channel = self.channel))
            return False

    def __monitor(self):
        if self.__checkLive():
            self.sched.remove_all_jobs()
            self.callBack(self.channel)

    def start(self):
        self.sched.add_job(self.__monitor, trigger='interval', seconds = self.TIME_INTERVAL)
        self.sched.start()

def f(x):
    print("Call")
    print(x)

def main():
    s = StreamMonitor("dreadztv", f)
    s.start()
    print("Block?")

if __name__ == "__main__":
    main()
