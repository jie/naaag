import logging
from core.settings_utils import Settings
from core.redis_util import RedisUtils

logger = logging.getLogger(__name__)

class AppConfig(object):

    def __init__(self, prefix='SD_'):
        self.prefix = prefix
        self.settings = Settings()
        self.init_logger()
        self.init_redis()
    
    def update_configs(self):
        logger.info('configs updated')
        self.settings = Settings()
        self.init_logger()
        self.init_redis()
    
    def get_setting(self, name):
        att = None
        try:
            att = getattr(self.settings, '%s%s' % (self.prefix, name))
        except:
            pass
        return att

    def init_redis(self):
        if not self.get_setting('REDIS_HOST'):
            logger.warning("redis_setting_not_found")
            return
        import redis
        pool = redis.ConnectionPool(
            host=self.get_setting('REDIS_HOST'),
            port=int(self.get_setting('REDIS_PORT')),
            db=self.get_setting('REDIS_DB'),
            decode_responses=True
        )
        redis_service = RedisUtils(pool)
        redis_service.get_client()
        self.redis = redis_service

    def init_logger(self):
        pass
