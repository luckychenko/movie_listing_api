
import sys
import logging

logger = logging.getLogger(__name__)

# formatter
formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(message)s'
)

# handler
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')

# stream formatter
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# log handler
logger.handlers = [stream_handler, file_handler]

logger.setLevel(logging.INFO) 