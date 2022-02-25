import logging
from datetime import datetime, timedelta
from .base import BaseAPI
from tornado.web import RequestHandler
logger = logging.getLogger(__name__)
errcode_default = "892"



class TestAPI(RequestHandler):

    def post(self, name):
        logger.info("bnan:%s" % name)
        self.finish("ok")