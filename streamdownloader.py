#!/usr/bin/env python

from streammonitor import StreamMonitor

class StreamDownloader:
    def __init__(self, channels):
        self.streamMonitors = []
        for channel in channels:
            self.streamMonitors.append(StreamMonitor(channel, self.__download))

    def __download(self, channel):
        print(channel)
        
    def start(self):
        for monitor in self.streamMonitors:
            print("Running thread {channel}".format(channel=monitor.channel))
            monitor.start()
        for monitor in self.streamMonitors:
            monitor.join()


def main():
    s = StreamDownloader(["dreadztv", "nastjanastja"])
    s.start()

if __name__ == "__main__":
    main()

