import logging
from logging.handlers import TimedRotatingFileHandler


class CustomLogger(logging.Logger):

    def __init__(
        self,
        name,
        log_to_console=True,
        log_to_file=True,
        log_file="default",
        log_level=logging.INFO,
    ):
        """
        Initializes the CustomLogger instance with provided parameters.

        Parameters
        ----------
        name : str
            The name of the logger instance (used to distinguish different loggers).
        log_to_console : bool
            Option boolean to enable/disable logging to console. Default is True.
        log_to_file : bool
            Option boolean to enable/disable logging to file. Default is True.
        log_level : int, optional
            The logging level (e.g., logging.DEBUG, logging.INFO, default is logging.INFO).
        """
        super().__init__(name)  # Initialize the base Logger class with the name
        self.name = name
        self.log_to_console = log_to_console
        self.log_to_file = log_to_file
        if log_file == "default":
            self.log_file = f"logs/{name}.log"  # Default log file path
        else:
            self.log_file = log_file  # Override
        self.when = "midnight"
        self.backup_count = 30
        self.log_level = log_level
        self.setLevel(log_level)  # Set the log level for the logger
        self._configure_logger()  # Configure the logger with handlers

    def console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._get_formatter())
        return console_handler

    def file_handler(self):
        file_handler = TimedRotatingFileHandler(
            filename=self.log_file,
            encoding="utf-8",
            when=self.when,
            backupCount=self.backup_count,
        )
        file_handler.setFormatter(self._get_formatter())
        return file_handler

    def set_level(self, level):
        self.setLevel(level)

    def add_custom_handler(self, handler):
        handler.setFormatter(self._get_formatter())
        self.addHandler(handler)

    def get_logger(self):
        return self

    def _get_formatter(self):
        return logging.Formatter(
            "[{asctime}] [{levelname:6}] <{name}> {filename}:{lineno} {message}",
            "%Y-%m-%d %H:%M:%S",
            style="{",
        )

    def _configure_logger(self):
        # Clear any existing handlers
        if self.hasHandlers():
            self.handlers.clear()

        # Set up the console handler (if enabled)
        if self.log_to_console:
            self.addHandler(self.console_handler())

        # Set up the rotating file handler (if enabled)
        if self.log_to_file:
            self.addHandler(self.file_handler())
