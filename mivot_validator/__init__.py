import sys, os, tempfile
from mivot_validator.logger_setup import LoggerSetup

logger = LoggerSetup.get_logger()
LoggerSetup.set_info_level()

logger.debug("mivot_validator package initialized")
