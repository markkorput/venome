import logging
# from evento import Event

class LinesFile:
    def __init__(self, path=None, loop=False, autoOpen=True, verbose=False):
        self.path = path
        self.loop = loop

        self.file = None

        # last read frame info
        self.lastFrame = None
        self.lastFrameIndex = -1

        # events
        # self.loopEvent = Event()

        self.logger = logging.getLogger(__name__)
        if verbose:
            self.logger.setLevel(logging.DEBUG)

        if autoOpen:
            self.open()

    def __del__(self):
        self.close()

    def open(self):
        if self.file:
            self.close()

        try:
            if not self.path:
                self.logger.warn('no file path')
            else:
                self.file = open(self.path, 'r')
                # self.csvreader = csv.reader(self.file)
                self.logger.debug("csv frames file opened: %s" % self.path)
                self.lastFrame = None
                self.lastFrameIndex = -1
        except:
            self.logger.warn("could not open csv frames file: %s" % self.path)
            self.file = None

    def rewind(self):
        if self.file:
            self.file.seek(0)

    def close(self):
        if self.file:
            self.file.close()
            self.file = None
            self.logger.debug("csv frames file closed")

    def setLoop(self, loop):
        self.loop = loop

    def nextLine(self):
        while(True):
            line = self.file.readline()

            if not line:
                if not self.loop:
                    return None

                self.file.seek(0)
                self.lastFrameIndex = -1

                # self.loopEvent(self)
                self.loop = False # to avoid endless loop for empty files
                result = self.nextLine()
                self.loop = True # restore
                return result

            line = line.strip()

            # skip comments (break and return only when not a comment)
            if not line.startswith('#'):
                break

        self.lastFrame = line
        self.lastFrameIndex += 1
        return line
