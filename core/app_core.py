import os
import tornado
import tornado.web
# import jinja2
# from .jinja_loader import Jinja2Loader


class CoreApplication(tornado.web.Application):

    def __init__(self, handlers=None, default_host="", transforms=None, **settings):
        # template_path = settings.get('template_path')
        # if template_path:
        #     jinja2_env = jinja2.Environment(
        #         loader=jinja2.FileSystemLoader(template_path), autoescape=False)
        #     jinja2_env.add_extension('jinja2.ext.do')
        #     jinja2_loader = Jinja2Loader(jinja2_env)
        #     settings.update(template_loader=jinja2_loader)
        super(CoreApplication, self).__init__(
            handlers, default_host, transforms, **settings)


class AppCore(object):

    def __init__(self, name, config, routes, port,
                 settings, autoreload=False, debug=True, cookie_secret=None, prefix="SD_"):

        self.name = name
        self.config = config
        self.routes = routes
        self.port = port
        self.autoreload = autoreload
        self.debug = debug
        self.settings = settings
        self.cookie_secret = cookie_secret
        self.prefix = prefix
        self.init_services()
    
    def init_services(self):
        self.application = self.make_app()
        self.application.settings["configs"] = self.config
        if self.getSetting("REDIS_HOST"):
            self.application.settings['redis'] = self.config.redis
    
    def drop_services(self):
        pass

    def getSetting(self, name):
        return getattr(self.settings, '%s%s' % (self.prefix, name), '')

    def make_app(self):
        if getattr(self, 'application', None):
            return self.application

        if self.getSetting('DEPLOY') == 'production':
            settings = {
                'autoreload': False,
                'debug': False
            }
        else:
            settings = {
                'autoreload': True,
                'debug': True
            }
        if self.cookie_secret:
            settings['cookie_secret'] = self.cookie_secret

        self.application = CoreApplication(self.routes, **settings)
        return self.application

    def start(self):
        if self.getSetting('DEPLOY') == 'production':
            self.application.listen(self.getSetting('PORT'), xheaders=True)
            print('@starting development: %s' % self.getSetting('PORT'))
        else:
            os.environ["SD_MONGODB"] = "user_service,mongodb://localhost:27017/user_service"
            self.config.update_configs()
            self.application.listen(self.port, xheaders=True)
            print('@starting development: %s' % self.port)
        tornado.ioloop.IOLoop.instance().start()