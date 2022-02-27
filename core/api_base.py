import json
import logging
import tornado
import addict
import functools
from .errcode import ErrorCode
from json import JSONEncoder
from tornado.web import RequestHandler
from tornado.web import HTTPError
from datetime import datetime, date


logger = logging.getLogger(__name__)


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            self.fail(code=ErrorCode.unauthorized, message="session_required")
        else:
            return method(self, *args, **kwargs)

    return wrapper


class ApiJsonEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(obj, date):
                return obj.strftime("%Y-%m-%d")
            iterable = iter(obj)
        except TypeError as e:
            print(type(obj))
            logger.warn(e)
        else:
            print(4)
            return list(iterable)
        return JSONEncoder.default(self, obj)


class APIError(Exception):
    code = "-10000"


class BaseMixin(object):
    def dumpjson(self, response):
        return json.dumps(response, cls=ApiJsonEncoder)

    def _get_msg_by_language(self, language, message):
        if not hasattr(self, "LANGUAGE_MAP"):
            return ""
        return (
            self.LANGUAGE_MAP[language][message]
            if self.LANGUAGE_MAP.get(language)
            and self.LANGUAGE_MAP[language].get(message)
            else message
        )

    def output(self, response, **kwargs):
        self._chunk = self.dumpjson(response)
        if not kwargs.get("content_type"):
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(self._chunk)
        self.finish()

    def success(self, message="ok", **kwargs):
        response = {"code": ErrorCode.success, "message": message, "data": kwargs}
        response["enmsg"] = self._get_msg_by_language("en-US", message)
        response["cnmsg"] = self._get_msg_by_language("zh-CN", message)
        self.output(response)


class BaseAPIHandler(RequestHandler, BaseMixin):

    ERR_PREFIX = None

    def fail(self, code, message, status_code=200, **kwargs):
        logger.info(
            "status_code: %s, message: %s, kwargs: %s" % (status_code, message, kwargs)
        )
        if status_code != 200:
            self.set_status(status_code)
            self.set_header("system_error_format", "json")

        errcode = code
        if getattr(self, "ERR_PREFIX", None):
            errcode = self.ERR_PREFIX + errcode

        response = {"code": errcode, "message": message, "data": kwargs}
        response["enmsg"] = self._get_msg_by_language("en-US", message)
        response["cnmsg"] = self._get_msg_by_language("zh-CN", message)
        self.output(response)

    def info(self, status_code=200, **kwargs):
        logger.info("status_code: %s, kwargs: %s" % (status_code, kwargs))
        self.set_status(status_code)
        self.output(kwargs)

    def get_current_user(self):
        userid = self.request.headers.get("userid")
        if not userid:
            return

        return userid

    @property
    def userid(self):
        return self.current_user


class APIHandler(BaseAPIHandler):
    required_params = []

    def api(self, params):
        return {}

    def parse_params(self):
        return (
            addict.Dict(tornado.escape.json_decode(self.request.body))
            if self.request.body
            else addict.Dict({})
        )

    def validate_params(self, params):
        """
        params validate success return True value jump to finish
        else return None
        """
        return True, ""

    def validate_required_params(self, params):
        for item in self.required_params:
            if not params.get(item):
                return False, "%s_required" % item
        return True, "ok"

    def parse_url_args(self, args, kwargs):
        pass

    def post(self, *args, **kwargs):
        self.parse_url_args(args, kwargs)
        params = self.parse_params()
        result, message = self.validate_required_params(params)
        if result is False:
            self.fail(code=ErrorCode.arguments_error, message=message)
            return
        result, message = self.validate_params(params)
        if result is False:
            self.fail(code=ErrorCode.arguments_error, message=message)
            return
        data = self.api(params)
        if not self._finished:
            self.success(**data if data else {})


class SessionAPI(APIHandler):
    @authenticated
    def post(self, *args, **kwargs):
        if self._finished:
            return
        super(SessionAPI, self).post(*args, **kwargs)

