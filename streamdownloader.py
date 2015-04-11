#!/usr/bin/env python

from streammonitor import StreamMonitor

class StreamDownloader:
    def __init__(self, channels = []):
        self.streamMonitors = dict()
        for channel in channels:
            self.streamMonitors[channel] = StreamMonitor(channel, self.__download)

    def __download(self, channel):
        print(channel)
        
    def start(self):
        for channelKey, monitor in self.streamMonitors.iteritems():
            print("Running thread {channel}".format(channel=monitor.channel))
            monitor.start()
    
    def add(self, channel):
        if not channel in self.streamMonitors:
            self.streamMonitors[channel] = StreamMonitor(channel, self.__download)
            self.streamMonitors[channel].start()

    def delete(self, channel):
        if channel in self.streamMonitors:
            self.streamMonitors[channel].stop() 
            del self.streamMonitors[channel]
    
    def getChannelStatus(self, channel):
        if channel in self.streamMonitors:
            return self.streamMonitors[channel].getStatus()
        else:
            return 'unknow'

    def contain(self, channel):
        if channel in self.streamMonitors:
            return True
        else:
            return False 
