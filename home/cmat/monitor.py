import pyinotify
from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent
import os
from PyQt4 import QtCore

class DirMonitor:
	def __init__(self, wdir, filesList):
		self.watchedDir = wdir
		self.adder = Adder(filesList)
		self.wdd = None
		self.wm = None
		self.mask = ''
		self.notifier = None

	def start(self):
		self.wm = WatchManager()
		self.notifier = ThreadedNotifier(self.wm, self.adder)
		self.notifier.start()
		self.mask = pyinotify.IN_MOVED_TO | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO
		self.wdd = self.wm.add_watch(self.watchedDir, self.mask, rec=True)

	def stop(self):
		self.notifier.stop()

	def resetWatched(self):
		self.wm.rm_watch(self.wdd.values(), rec=True)

	def addWatched(self, w):
		#remove all watched now
		self.wdd = self.wm.add_watch(w, self.mask, rec=True)






class Adder(ProcessEvent):
	def __init__(self, flist):
		self.flist = flist

	def process_default(self, event):
		if event.mask == pyinotify.IN_CLOSE_WRITE or event.mask == pyinotify.IN_CREATE or event.mask == pyinotify.IN_MOVED_TO:
			self.flist.filesStartedLoading.emit(False)
			self.flist.registerFile(None, QtCore.QString(event.pathname))
			self.flist.filesFinishedLoading.emit(True)
			print event.pathname
		else:
			print "Other event", event.mask
	# def process_IN_CREATE(self, event):
	# 	print "Create: %s" %  os.path.join(event.path, event.name)

	# def process_IN_DELETE(self, event):
	# 	print "Remove: %s" %  os.path.join(event.path, event.name)


# dm = DirMonitor('/home/accts/img22/Desktop/HWs/CS490/cmat_project/cmat/cmat-test')
# dm.start()
# print 'Monitor has started...'