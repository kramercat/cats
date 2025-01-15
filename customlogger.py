import logging
from logging.handlers import RotatingFileHandler


class CustomLogger:
    """
    Custom logger class for managing logging configurations with console and file handlers.

    This class provides an easy-to-use interface to configure logging for different
    components of the bot or application, supporting log file rotation and custom log handlers.

    Attributes
    ----------
    name : str
        The name of the logger instance (used to distinguish different loggers).
    log_file : str
        Path to the log file for file logging. Defaults to 'default.log'.
    max_bytes : int
        Maximum size of the log file before it rotates (in bytes). Defaults to 32 MiB.
    backup_count : int
        Number of backup log files to keep. Defaults to 5.
    log_level : int
        The logging level (e.g., logging.DEBUG, logging.INFO). Defaults to logging.INFO.
    logger : logging.Logger
        The logging instance.

    Methods
    -------
    __init__(self, name, log_file='default.log', max_bytes=32 * 1024 * 1024, backup_count=5, log_level=logging.INFO)
        Initializes the CustomLogger instance with provided parameters.
    _configure_logger(self)
        Configures the logger with both console and rotating file handlers.
    _get_formatter(self)
        Returns the default formatter for the logger.
    set_level(self, level)
        Sets the log level for the logger.
    add_custom_handler(self, handler)
        Adds a custom logging handler to the logger.
    get_logger(self)
        Returns the configured logger instance.
    """

    def __init__(self, name,
                 log_to_console=True,
                 log_to_file=True,
                 max_bytes=32 * 1024 * 1024,
                 backup_count=5,
                 log_level=logging.INFO,
                 ):
        """
        Initializes the CustomLogger instance with provided parameters.

        Parameters
        ----------
        name : str
            The name of the logger instance (used to distinguish different loggers).
        log_to_console : bool
            Option boolean to disable logging to console.
        log_to_file : bool
            Option boolean to disable logging to file.
        max_bytes : int, optional
            Maximum size of the log file before it rotates (in bytes, default is 32 MiB).
        backup_count : int, optional
            Number of backup log files to keep (default is 5).
        log_level : int, optional
            The logging level (e.g., logging.DEBUG, logging.INFO, default is logging.INFO).
        """
        self.name = name
        self.log_to_console = log_to_console
        self.log_to_file = log_to_file
        self.log_file = f'logs/{name}.log'
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.log_level = log_level
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self._configure_logger()

    def _configure_logger(self):
        """
        Configures the logger by adding both a console handler and a rotating file handler.

        This method is called automatically during initialization to ensure the logger
        is configured with appropriate handlers (console and file).
        """
        # Clear any existing handlers
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Set up the console handler
        if self.log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self._get_formatter())
            self.logger.addHandler(console_handler)

        # Set up the rotating file handler
        if self.log_to_file:
            file_handler = RotatingFileHandler(
                filename=self.log_file,
                encoding='utf-8',
                maxBytes=self.max_bytes,
                backupCount=self.backup_count
            )
            file_handler.setFormatter(self._get_formatter())
            self.logger.addHandler(file_handler)

    def _get_formatter(self):
        return logging.Formatter(
            '[{asctime}] [{levelname:<8}] {name}: {message}',
            '%Y-%m-%d %H:%M:%S',
            style='{'
        )

    def set_level(self, level):
        self.logger.setLevel(level)

    def add_custom_handler(self, handler):
        handler.setFormatter(self._get_formatter())
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger
