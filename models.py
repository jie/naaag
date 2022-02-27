import datetime
from tokenize import String
from typing import List
# from typing import Dict, List
from mongoengine.queryset.visitor import Q
from core.base_model import BaseDocument
from mongoengine import EmbeddedDocument
from mongoengine import StringField, FloatField, IntField, ListField, DictField, BooleanField
from mongoengine import ReferenceField, EmbeddedDocumentField, GenericEmbeddedDocumentField
from mongoengine import DateTimeField



class ApiErrorCode(BaseDocument):

    meta = {
        'db_alias': 'naaag',
        'collection': 'api_error_code'
    }

    key = StringField(max_length=10)
    required = BooleanField(default=False)
    message = StringField(max_length=255)


class ApiParameter(BaseDocument):

    meta = {
        'db_alias': 'naaag',
        'collection': 'api_parameter'
    }

    key = StringField(max_length=255)
    required = BooleanField(default=False)

class Category(BaseDocument):

    meta = {
        'db_alias': 'naaag',
        'collection': 'category'
    }

    key = StringField(max_length=255)
    required = BooleanField(default=False)


class FunctionKeysField(EmbeddedDocument):
    key = StringField(max_length=255)
    value = StringField(max_length=255)
    variables = ListField(default=[])


class Function(BaseDocument):

    meta = {
        'db_alias': 'naaag',
        'collection': 'function'
    }

    key = StringField(max_length=255)
    required = BooleanField(default=False)
    category = StringField(max_length=255)
    name = StringField(max_length=255)
    keys = ListField(EmbeddedDocumentField(FunctionKeysField), default=[])


class SiteParameter(BaseDocument):

    meta = {
        'db_alias': 'naaag',
        'collection': 'site_parameter'
    }

    key = StringField(max_length=255)
    required = BooleanField(default=False)


class EventParameter(BaseDocument):
    meta = {
        'db_alias': 'naaag',
        'collection': 'event_parameter'
    }

    key = StringField(max_length=255)
    required = BooleanField(default=False)


class HttpParameter(BaseDocument):

    meta = {
        'db_alias': 'naaag',
        'collection': 'http_parameter'
    }

    key = StringField(max_length=255)
    required = BooleanField(default=False)


class LocationParameter(BaseDocument):

    meta = {
        'db_alias': 'naaag',
        'collection': 'location_parameter'
    }

    key = StringField(max_length=255)
    required = BooleanField(default=False)

class ParameterVariable(BaseDocument):
    meta = {
        'db_alias': 'naaag',
        'collection': 'parameter_variable'
    }

    key = StringField(max_length=255)
    required = BooleanField(default=False)


class ParameterType(BaseDocument):
    meta = {
        'db_alias': 'naaag',
        'collection': 'parameter_type'
    }

    key = StringField(max_length=255)
    required = BooleanField(default=False)

class ParameterOptionsField(EmbeddedDocument):

    remark = StringField(max_length=255, default="")
    remark_en = StringField(max_length=255, default="")
    value = StringField(max_length=255)
    variables = ListField(default=[])


class Parameter(BaseDocument):

    meta = {
        'db_alias': 'naaag',
        'collection': 'parameter'
    }

    key = StringField(unique=True, max_length=255)
    type = StringField(max_length=255)
    options = ListField(EmbeddedDocumentField(ParameterOptionsField), default=[])
    default = StringField(max_length=255)
    category = StringField(max_length=255)
    multiple = BooleanField(default=False)


class ServerParameter(BaseDocument):

    meta = {
        'db_alias': 'naaag',
        'collection': 'server_parameter'
    }

    key = StringField(max_length=255)
    required = BooleanField(default=False)

class UpstreamParameter(BaseDocument):

    meta = {
        'db_alias': 'naaag',
        'collection': 'upstream_parameter'
    }

    key = StringField(max_length=255)
    required = BooleanField(default=False)




class User(BaseDocument):
    meta = {
        'db_alias': 'naaag',
        'collection': 'user'
    }

    email = StringField(max_length=255)


class ApiBackend(BaseDocument):
    meta = {
        'db_alias': 'naaag',
        'collection': 'api_sbackend'
    }

    uid = StringField(unique=True, max_length=255)
    name = StringField(max_length=255)
    desc = StringField(max_length=255)
    configs = ListField(default=[])
    user = ReferenceField('User')


class ApiLocation(BaseDocument):
    meta = {
        'db_alias': 'naaag',
        'collection': 'api_location'
    }
    uid = StringField(unique=True, max_length=255)
    name = StringField(max_length=255)
    desc = StringField(max_length=255)
    configs = ListField(default=[])
    user = ReferenceField('User')


class ApiServer(BaseDocument):
    meta = {
        'db_alias': 'naaag',
        'collection': 'api_server'
    }
    uid = StringField(unique=True, max_length=255)
    name = StringField(max_length=255)
    desc = StringField(max_length=255)
    configs = ListField(default=[])
    user = ReferenceField('User')


class ApiSite(BaseDocument):
    meta = {
        'db_alias': 'naaag',
        'collection': 'api_site'
    }
    uid = StringField(unique=True, max_length=255)
    name = StringField(max_length=255)
    desc = StringField(max_length=255)
    configs = ListField(default=[])
    user = ReferenceField('User')


class ApiGateway(BaseDocument):
    meta = {
        'db_alias': 'naaag',
        'collection': 'api_gateway'
    }

    uid = StringField(unique=True, max_length=255)
    name = StringField(max_length=255)
    desc = StringField(max_length=255)
    configs = ListField(default=[])
    user = ReferenceField('User')
