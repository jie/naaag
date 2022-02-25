import logging
import nginx
from datetime import datetime, timedelta
from .base import BaseAPI, UserSessionAPI

logger = logging.getLogger(__name__)
errcode_default = "892"


class Mixin(object):

    def get_server(self, site, server_name):
        for server in site.servers:
            server_data = server.as_dict
            values = list(server_data.values())[0]
            logger.info("values:%s" % values)
            if values[0].get("#") and server_name == values[0]["#"]:
                return server
        return None

    def get_location(self, server, location_name):
        location = None
        for item in server.filter('Location'):
            location_data = item.as_dict
            keys = location_data.keys()
            first = list(location_data.values())[0][0]
            if first.get("#") and location_name == first['#']:
                location = location_data 
            elif ('location %s' % location_name) == list(keys)[0]:
                location = location_data 
        return location


class CreateAPI(BaseAPI, Mixin):

    required_params = ["site", "server_name", "location_name"]

    def api(self, params):
        location_name = params.location_name
        locations = params.locations
        site = self.get_nginx_config(params.site)
        server = self.get_server(params.server_name)
        if not server:
            self.fail(code=errcode_default, message="server_not_found")
            return
        location = self.get_location(server, location_name)
        if location:
            self.fail(code=-1, message='location_exists')
            return
        _locations = []
        for item in locations:
            data = item.to_dict()
            item_data = list(data.items())
            _locations.append(
                nginx.Key(item_data[0][0], item_data[0][1])
            )
        
        nginx_location = nginx.location(location_name, *_locations)
        site.add(nginx_location)
        self.save_nginx_config(site, params.site)
        return {
            "locations": nginx_location.as_dict
        }


class UpdateAPI(BaseAPI, Mixin):

    required_params = ["site"]

    def api(self, params):
        location_name = params.location_name
        locations = params.locations

        site = self.get_nginx_config(params.site)
        location = self.get_location(site, location_name)
        if not location:
            self.fail(code=-1, message='location_not_exists')
            return
        _locations = []
        for item in locations:
            data = item.to_dict()
            item_data = list(data.items())
            _locations.append(
                nginx.Key(item_data[0][0], item_data[0][1])
            )
        location.children = _locations
        self.save_nginx_config(site, params.site)
        return {
            "locations": location.as_dict
        }


class DeleteAPI(BaseAPI, Mixin):

    required_params = ["site"]

    def api(self, params):
        location_name = params.location_name
        location = params.location or []
        site = self.get_nginx_config(params.site)
        location = self.get_location(site, location_name)
        site.children.remove(location)
        self.save_nginx_config(site, params.site)



class ListAPI(BaseAPI, Mixin):

    required_params = ["site"]

    def api(self, params):
        site = self.get_nginx_config(params.site)
        server = self.get_server(site, params.server_name)
        if not server:
            self.fail(code=errcode_default, message="server_not_found")
            return

        locations = []
        for location in server.filter('Location'):
            location_data = location.as_dict
            values = list(location_data.values())[0]
            keys = list(location_data.keys())[0]
            if values[0].get("#"):
                locations.append({
                    "name": values[0]["#"],
                    "data": location.as_dict
                })
            else:
                _keys = keys.split(" ")
                locations.append({
                    "name": _keys[len(_keys) - 1],
                    "data": location.as_dict
                })

        return {
            "locations": locations
        }


class GetAPI(BaseAPI, Mixin):

    required_params = ["site"]

    def api(self, params):
        site = self.get_nginx_config(params.site)
        server = self.get_server(site, params.server_name)
        if not server:
            self.fail(code=errcode_default, message="server_not_found")
            return
        location_name = params.location_name
        location = self.get_location(server, location_name)
        return {
            "location": location
        }