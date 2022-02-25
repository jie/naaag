import logging
import nginx
from datetime import datetime, timedelta

from .base import BaseAPI, UserSessionAPI
from uuid import uuid4
from core.settings_utils import settings

logger = logging.getLogger(__name__)


errcode_default = "892"


class CreateAPI(UserSessionAPI):

    required_params = ["name"]

    def api(self, params):
        pass


class UpdateAPI(UserSessionAPI):

    required_params = ["name"]

    def api(self, params):
        pass
    


class DeleteAPI(UserSessionAPI):

    def api(self, params):
        pass
    

class GetAPI(BaseAPI):

    required_params = ["server_block"]

    def api(self, params):
        server_path = '/opt/homebrew/etc/nginx/servers/%s' % params.server_block
        logger.info(server_path)
        server_block = nginx.loadf(server_path)
        logger.info(server_block.filter('Upstream'))
        logger.info(server_block.filter('Upstream')[0].as_dict)
        self.get_nginx_config_file(params.server_block)
        # logger.info(server_block.children)
        # logger.info(server_block.server.children)
        # logger.info(server_block.as_dict.keys())
        # logger.info(server_block.as_dict["conf"])

        # for item in server_block.as_dict["conf"]:
        #     logger.info(item)