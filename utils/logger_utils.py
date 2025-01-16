import logging
from logging.handlers import TimedRotatingFileHandler


class CustomLogger(logging.Logger):
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
    __init__(self, name, log_to_console=True, log_to_file=True, max_bytes=32 * 1024 * 1024, backup_count=5,
              log_level=logging.INFO)
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

    def _configure_logger(self):
        """
        Configures the logger by adding both a console handler and a rotating file handler.

        This method is called automatically during initialization to ensure the logger
        is configured with appropriate handlers (console and file).
        """
        # Clear any existing handlers
        if self.hasHandlers():
            self.handlers.clear()

        # Set up the console handler (if enabled)
        if self.log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self._get_formatter())
            self.addHandler(console_handler)

        # Set up the rotating file handler (if enabled)
        if self.log_to_file:
            file_handler = TimedRotatingFileHandler(
                filename=self.log_file,
                encoding="utf-8",
                when=self.when,
                backupCount=self.backup_count,
            )
            file_handler.setFormatter(self._get_formatter())
            self.addHandler(file_handler)

    def _get_formatter(self):
        """
        Returns the default log message formatter.

        Returns
        -------
        logging.Formatter
            The formatter for the log message.
        """
        return logging.Formatter(
            "[{asctime}] [{levelname:6}] <{name}> {filename}:{lineno} ~ {message}",
            "%Y-%m-%d %H:%M:%S",
            style="{",
        )

    def set_level(self, level):
        """
        Sets the log level for the logger.

        Parameters
        ----------
        level : int
            The logging level to set (e.g., logging.DEBUG, logging.INFO).
        """
        self.setLevel(level)

    def add_custom_handler(self, handler):
        """
        Adds a custom logging handler to the logger.

        Parameters
        ----------
        handler : logging.Handler
            The custom logging handler to add (e.g., logging.FileHandler, logging.SMTPHandler).
        """
        handler.setFormatter(self._get_formatter())
        self.addHandler(handler)

    def get_logger(self):
        """
        Returns the configured logger instance.

        Returns
        -------
        logging.Logger
            The logger instance that has been configured with the appropriate handlers.
        """
        return self
