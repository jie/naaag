
import fire
from core.app_utils import AppConfig

config = AppConfig()



class WebServer(object):

    def start(self, port=None):
        from core.app_core import AppCore
        from routes import routes
        micro_service = AppCore(
            'TORNADO_SERVER',
            config,
            routes,
            settings=config.settings,
            autoreload=port,
            debug=True,
            port=port,
            prefix=config.prefix
        )
        micro_service.start()

if __name__ == "__main__":
    fire.Fire(WebServer)

