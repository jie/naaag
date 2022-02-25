import logging
import nginx
from datetime import datetime, timedelta
from .base import BaseAPI, UserSessionAPI

logger = logging.getLogger(__name__)
errcode_default = "892"


class Mixin(object):
    def get_upstream(self, site, upstream_name):
        upstream = None
        for item in site.filter('Upstream'):
            keys = item.as_dict.keys()
            for key in keys:
                if upstream_name in key:
                    upstream = item
                    break
        return upstream


class CreateAPI(BaseAPI, Mixin):

    required_params = ["site", "upstreams", "upstream_name"]

    def api(self, params):
        upstream_name = params.upstream_name
        upstreams = params.upstreams
        site = self.get_nginx_config(params.site)
        upstream = self.get_upstream(site, upstream_name)
        if upstream:
            self.fail(code=-1, message='upstream_exists')
            return
        _upstreams = []
        for item in upstreams:
            data = item.to_dict()
            item_data = list(data.items())
            _upstreams.append(
                nginx.Key(item_data[0][0], item_data[0][1])
            )
        
        nginx_upstream = nginx.Upstream(upstream_name, *_upstreams)
        site.add(nginx_upstream)
        self.save_nginx_config(site, params.site)
        return {
            "upstreams": nginx_upstream.as_dict
        }


class UpdateAPI(BaseAPI, Mixin):

    required_params = ["site"]

    def api(self, params):
        upstream_name = params.upstream_name
        upstreams = params.upstreams

        site = self.get_nginx_config(params.site)
        upstream = self.get_upstream(site, upstream_name)
        if not upstream:
            self.fail(code=-1, message='upstream_not_exists')
            return
        _upstreams = []
        for item in upstreams:
            data = item.to_dict()
            item_data = list(data.items())
            _upstreams.append(
                nginx.Key(item_data[0][0], item_data[0][1])
            )
        upstream.children = _upstreams
        self.save_nginx_config(site, params.site)
        return {
            "upstreams": upstream.as_dict
        }


class DeleteAPI(BaseAPI, Mixin):

    required_params = ["site"]

    def api(self, params):
        upstream_name = params.upstream_name
        upstream = params.upstream or []
        site = self.get_nginx_config(params.site)
        upstream = self.get_upstream(site, upstream_name)
        site.children.remove(upstream)
        self.save_nginx_config(site, params.site)


class GetAPI(BaseAPI):

    required_params = ["site"]

    def api(self, params):
        site = self.get_nginx_config(params.site)
        stream_name = params.stream_name or None
        upstreams = []
        for item in site.filter('Upstream'):
            if stream_name is None:
                upstreams.append(item.as_dict)
            else:
                keys = item.as_dict.keys()
                for key in keys:
                    if stream_name in key:
                        upstreams.append(item.as_dict)
                        break
        return {
            "upstreams": upstreams
        }