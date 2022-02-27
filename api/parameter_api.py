import logging
import nginx
from datetime import datetime, timedelta

from api.base import BaseAPI
from uuid import uuid4
from core.settings_utils import settings
from models import Parameter, ApiErrorCode, ApiParameter, Category, Function, SiteParameter, EventParameter, HttpParameter, LocationParameter, ParameterOptionsField, ParameterVariable, ParameterType, ServerParameter, UpstreamParameter
from mongoengine.queryset.visitor import Q


logger = logging.getLogger(__name__)

model_map = {
    'category': {
        "model": Category
    },
    'function': {
        "model": Function
    },
    'parameter_type': {
        "model": ParameterType
    },
    'parameter': {
        "model": Parameter
    },
    'api_parameter': {
        "model": ApiParameter,
        "is_parameter": True # 是否属于引用属性
    },
    'site_parameter': {
        "model": SiteParameter,
        "is_parameter": True
    },
    'event_parameter': {
        "model": EventParameter,
        "is_parameter": True
    },
    'http_parameter': {
        "model": HttpParameter,
        "is_parameter": True
    },
    'location_parameter': {
        "model": LocationParameter,
        "is_parameter": True
    },
    'parameter_variable': {
        "model": ParameterVariable,
    },
    'server_parameter': {
        "model": ServerParameter,
        "is_parameter": True
    },
    'upstream_parameter': {
        "model": UpstreamParameter,
        "is_parameter": True
    }
}


class ListAPI(BaseAPI):

    def parse_url_args(self, args, kwargs):
        self.modelCls = model_map[args[0]]['model']
        self.is_parameter = model_map[args[0]].get('is_parameter', False)

    def api(self, params):
        print(params)
        page = params.get("page", 1)
        pagesize = params.get("pagesize", 10)
        query_args = Q(is_enable=True) 
        keyword = params.get("keyword", "")
        if keyword:
            query_args = query_args & Q(key__contains=params.keyword)
        count, total_page, records = self.modelCls.paginate(page, pagesize, query_args)
        data = []
        records = records.order_by('id')
        for item in records:
            item_dct = item.to_dict()
            data.append(item_dct)

        if self.is_parameter is True:
            for item in data:
                parameter = Parameter.get_first(key=item['key'], is_enable=True)
                if parameter:
                    item['_parameter'] = parameter.to_dict()

        pageData =  {
            'data': data,
            'total': count,
            'total_page': total_page,
            'pagesize': pagesize,
            'page': page
        }
        pageData['keyword'] = keyword
        return pageData


class GetAPI(BaseAPI):

    def parse_url_args(self, args, kwargs):
        self.modelCls = model_map[args[0]]['model']
        self.is_parameter = model_map[args[0]].get('is_parameter', False)

    def api(self, params):
        entity = None
        parameter = None
        if params.get('id'):
            entity = self.modelCls.get_first(id=params.id, is_enable=True)
        elif params.get('key'):
            entity = self.modelCls.get_first(key=params.key, is_enable=True)
        else:
            self.fail(code=-1, message='id_or_key_required')
            return
        if not entity:
            self.fail(code=-1, message='entity_not_found')
            return
        if self.is_parameter is True:
            parameter = Parameter.get_first(key=entity.key, is_enable=True)
        data = {
            "entity": entity.to_dict(),
        }
        if parameter is not None:
            data.update(_parameter=parameter)
        return data


fields_exclude = ['id', '_cls', 'is_import', 'is_enable', 'create_at', 'update_at', 'status']

class CreateAPI(BaseAPI):

    def parse_url_args(self, args, kwargs):
        self.modelCls = model_map[args[0]]['model']
        self.is_parameter = model_map[args[0]].get('is_parameter', False)

    def api(self, params):
        now = datetime.now()
        fields = {
            "update_at": now,
            "create_at": now
        }
        for field in self.modelCls._fields.keys():
            if field not in fields_exclude:
                fields[field] = params.entity.get(field, '')
        entity = self.modelCls(**fields)
        entity.save()
        return {
            "entity": entity.to_dict()
        }

class UpdateAPI(BaseAPI):

    def parse_url_args(self, args, kwargs):
        self.modelCls = model_map[args[0]]['model']
        self.is_parameter = model_map[args[0]].get('is_parameter', False)

    def api(self, params):
        print(params)
        now = datetime.now()
        entity = None
        if params.get('id'):
            entity = self.modelCls.get_first(id=params.id, is_enable=True)
        elif params.get('key'):
            entity = self.modelCls.get_first(key=params.key, is_enable=True)
        else:
            self.fail(code=-1, message='id_or_key_required')
            return
        if not entity:
            self.fail(code=-1, message='entity_not_found')
            return
        
        for field in dict(params.entity).keys():
            if field not in fields_exclude:
                if field != 'options':
                    value = params.entity.get(field, '')
                else:
                    print('****')
                    print(value)
                    value = params.entity.get(field, [])
                    value = [ParameterOptionsField(**v.to_dict()) for v in value]
                setattr(entity, field, value)
        entity.update_at = now
        entity.save()
        return {
            "entity": entity.to_dict()
        }

class DeleteAPI(BaseAPI):

    def parse_url_args(self, args, kwargs):
        self.modelCls = model_map[args[0]]['model']
        self.is_parameter = model_map[args[0]].get('is_parameter', False)

    def api(self, params):
        now = datetime.now()
        entity = None
        if params.get('id'):
            entity = self.modelCls.get_first(id=params.id, is_enable=True)
        elif params.get('key'):
            entity = self.modelCls.get_first(key=params.key, is_enable=True)
        else:
            self.fail(code=-1, message='id_or_key_required')
            return

        entity.update_at = now
        entity.is_enable = False
        entity.save()
        return {
            "id": str(entity.id)
        }
