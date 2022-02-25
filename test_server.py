import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self, name):
        self.write("Hello, world")

if __name__ == "__main__":
    application = tornado.web.Application([
        (r'/_gateway/(.*)$', MainHandler),
        (r"/", MainHandler),
    ])
    application.listen(9000)
    tornado.ioloop.IOLoop.current().start()