import logging
from django.conf import settings
from datetime import datetime

class ErrorLogger(object):
    def __init__(self):
            # Create the Logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)

        # Create the Handler for logging data to a file
        date  = datetime.strftime(datetime.now(),'%d_%m_%Y')
        logger_handler = logging.FileHandler(settings.BASE_DIR+'/log/'+date+'.log')
        logger_handler.setLevel(logging.ERROR)

        # Create a Formatter for formatting the log messages
        logger_formatter = logging.Formatter('%(asctime)s - %(pathname)s - %(lineno)d - %(module)s - %(funcName)s - %(levelname)s - %(message)s - %(user)s - %(details)s')

        # Add the Formatter to the Handler
        logger_handler.setFormatter(logger_formatter)

        # Add the Handler to the Logger
        self.logger.addHandler(logger_handler)

   # def log_error(self,str_msg,dct_error,int_critical=0):
   #     #dct_error = {'user' : str(request.user.id),'line No': str(exc_tb.tb_lineno) }
   #     self.logger.error(e, extra=dct_error)
   #     send_mail()
