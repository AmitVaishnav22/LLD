from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4
    FATAL = 5

    def isGreaterThanOrEqualTo(self, other):
        return self.value >= other.value

class LogMessage:
    def __init__(self,level,LoggerName,message):
        self.timestamp = datetime.now()
        self.level = level
        self.LoggerName = LoggerName
        self.message = message
    def getTimestamp(self):
        return self.timestamp
    def getLevel(self):
        return self.level
    def getLoggerName(self):
        return self.LoggerName
    def getMessage(self):
        return self.message

class LogFormatter(ABC):
    @abstractmethod
    def format(self, logMessage):
        pass

class SimpleLogFormatter(LogFormatter):
    def format(self, logMessage):
        return f"{logMessage.getTimestamp()} - {logMessage.getLevel().name} - {logMessage.getLoggerName()} - {logMessage.getMessage()}"

class LogAppender(ABC):
    @abstractmethod
    def append(self, logMessage):
        pass
    @abstractmethod
    def setFormatter(self, formatter):
        pass
    @abstractmethod
    def getFormatter(self):
        pass
    @abstractmethod
    def close(self):
        pass

class ConsoleLogAppender(LogAppender):
    def __init__(self):
        self.formatter = SimpleLogFormatter()
    def append(self, logMessage):
        formattedMessage = self.formatter.format(logMessage)
        print(formattedMessage)
    def setFormatter(self, formatter):
        self.formatter = formatter
    def getFormatter(self):
        return self.formatter
    def close(self):
        pass

class FileLogAppender(LogAppender):
    def __init__(self, filePath):
        self.filePath = filePath
        self.formatter = SimpleLogFormatter()
        self.file = open(filePath, 'a')
    def append(self, logMessage):
        formattedMessage = self.formatter.format(logMessage)
        self.file.write(formattedMessage + '\n')
    def setFormatter(self, formatter):
        self.formatter = formatter
    def getFormatter(self):
        return self.formatter
    def close(self):
        self.file.close()

class Logger:
    def __init__(self,name,parent):
        self.name=name
        self.parent=parent
        self.appenders=[]
        self.level=None
        self.setadditivity=True
    
    def setLevel(self,level):
        self.level=level
    
    def addAppender(self,appender):
        self.appenders.append(appender)
    
    def getAppenders(self):
        return self.appenders
    
    def setAdditivity(self, additivity):
        self.setadditivity = additivity
    
    def getEffectiveLevel(self):
        if self.level is not None:
            return self.level
        elif self.parent is not None:
            return self.parent.getEffectiveLevel()
        else:
            return LogLevel.DEBUG
        
    def log(self, level, message):
        effectiveLevel = self.getEffectiveLevel()
        if level.isGreaterThanOrEqualTo(effectiveLevel):
            logMessage = LogMessage(level, self.name, message)
            for appender in self.appenders:
                appender.append(logMessage)
            self.callAppenders(logMessage)
        
    def callAppenders(self, logMessage):
        if self.appenders:
            LogManager.getInstance().callAppenders(logMessage, self.appenders)
        if self.setadditivity and self.parent is not None:
            self.parent.callAppenders(logMessage)
    
    def debug(self, message):
        self.log(LogLevel.DEBUG, message)
    
    def info(self, message):
        self.log(LogLevel.INFO, message)
    
    def warn(self, message):
        self.log(LogLevel.WARN, message)
    
    def error(self, message):
        self.log(LogLevel.ERROR, message)
    
    def fatal(self, message):
        self.log(LogLevel.FATAL, message)

class LogManager:
    _instance=None
    @staticmethod
    def getInstance():
        if LogManager._instance is None:
            LogManager._instance = LogManager()
        return LogManager._instance
    
    def __init__(self):
        self.loggers={}
        self.rootLogger=Logger("root", None)
        self.loggers["root"]=self.rootLogger

    def getLogger(self, name):
        if name in self.loggers:
            return self.loggers[name]
        self.loggers[name]=self.createLogger(name)
        return self.loggers[name]
    def createLogger(self, name):
        if name=="root":
            return self.rootLogger
        lastDotIndex = name.rfind('.')
        parentName = name[:lastDotIndex] if lastDotIndex != -1 else "root"
        parent=self.getLogger(parentName)
        logger=Logger(name, parent)
        return logger
    
    def getRootLogger(self):
        return self.rootLogger
    
    def shutdown(self):
        all_appenders=set()
        for logger in self.loggers.values():
            for appender in logger.getAppenders():
                all_appenders.add(appender)
        for appender in all_appenders:
            appender.close()
    def callAppenders(self, logMessage, appenders):
        for appender in appenders:
            appender.append(logMessage)
    

class LoggingSystem:
    @staticmethod
    def main():
        logManager = LogManager.getInstance()
        rootLogger = logManager.getRootLogger()
        rootLogger.setLevel(LogLevel.INFO)

        rootLogger.addAppender(ConsoleLogAppender())

        print("Logging with root logger:")
        main_logger = logManager.getLogger("com.example.Main")
        main_logger.debug("This is a debug message")
        main_logger.info("This is an info message")
        main_logger.warn("This is a warning message")
        main_logger.error("This is an error message")
        main_logger.fatal("This is a fatal message")
        print("\nLogging with file appender:")
        fileAppender = FileLogAppender("app.log")
        main_logger.addAppender(fileAppender)
        main_logger.info("This message should go to both console and file")
        logManager.shutdown()

if __name__ == "__main__":
    LoggingSystem.main()