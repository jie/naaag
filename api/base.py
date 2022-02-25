import json
import logging
import os
import nginx
from core.api_base import APIHandler, SessionAPI
from datetime import datetime
from core.settings_utils import settings
logger = logging.getLogger(__name__)

logger.info('settings.settings_data:%s' % settings.settings_data)
class BaseAPI(APIHandler):

    @property
    def _now(self):
        return datetime.now()

    @property
    def redis(self):
        return self.application.settings["redis"]

    def _get_user_id(self):
        return None

    @property
    def nginx_site_path(self):
        logger.info(settings.settings_data)
        return os.path.join(settings.SD_NGINX_PATH, settings.SD_NGINX_CONF)

    def get_nginx_config(self, filename):
        return nginx.loadf(os.path.join(self.nginx_site_path, filename))

    def save_nginx_config(self, nginx_conf, filename):
        path = os.path.join(self.nginx_site_path, filename)
        nginx.dumpf(nginx_conf, path)

class UserSessionAPI(SessionAPI):

    @property
    def redis(self):
        return self.application.settings["redis"]

    @property
    def configs(self):
        return self.application.settings["configs"]

    def get_current_user(self):
        if not self.sessionid:
            return None

        if not self.current_session:
            return None
        return self.current_session.user

    @property
    def current_session(self):
        return None

    @property
    def sessionid(self):
        return self.request.headers.get("sessionid", None)

    @property
    def userid(self):
        return str(self.current_user.id)


class BaseAdminAPI(BaseAPI):
    pass