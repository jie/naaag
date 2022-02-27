import logging
from uuid import uuid4
from datetime import datetime, timedelta
from .base import BaseAPI
from tornado.web import RequestHandler
from models import ApiGateway
from mongoengine.queryset.visitor import Q
logger = logging.getLogger(__name__)
errcode_default = "892"



class TestAPI(RequestHandler):

    def post(self, name):
        logger.info("bnan:%s" % name)
        self.finish("ok")


fields_exclude = ['id', '_cls', 'is_import', 'is_enable', 'create_at', 'update_at', 'status']

class CreateAPI(BaseAPI):

    def parse_url_args(self, args, kwargs):
        self.modelCls = ApiGateway

    def api(self, params):
        now = datetime.now()
        fields = {
            "update_at": now,
            "create_at": now
        }
        if not params.entity.get("name"):
            self.fail(code=-1, message='name_required')
            return
        entity = params.entity.to_dict()
        entity.update(uid=uuid4().hex)
        for field in self.modelCls._fields.keys():
            if field not in fields_exclude:
                if field != 'configs':
                    fields[field] = entity.get(field, '')
                else:
                    fields[field] = entity.get(field, [])
        entity = self.modelCls(**fields)
        entity.save()
        return {
            "entity": entity.to_dict()
        }


class ListAPI(BaseAPI):

    def parse_url_args(self, args, kwargs):
        self.modelCls = ApiGateway

    def api(self, params):
        print(params)
        page = params.get("page", 1)
        pagesize = params.get("pagesize", 10)
        query_args = Q(is_enable=True) 
        keyword = params.get("keyword", "")
        if keyword:
            query_args = query_args & Q(name__contains=params.keyword)
        count, total_page, records = self.modelCls.paginate(page, pagesize, query_args)
        data = []
        records = records.order_by('id')
        for item in records:
            item_dct = item.to_dict()
            data.append(item_dct)

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
        self.modelCls = ApiGateway

    def api(self, params):
        entity = None
        if params.get('id'):
            entity = self.modelCls.get_first(id=params.id, is_enable=True)
        elif params.get('uid'):
            entity = self.modelCls.get_first(uid=params.uid, is_enable=True)
        else:
            self.fail(code=-1, message='id_or_uid_required')
            return
        if not entity:
            self.fail(code=-1, message='entity_not_found')
            return
        data = {
            "entity": entity.to_dict(),
        }
        return data
