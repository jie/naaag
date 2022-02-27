"""
Document class which provides some convenient methods
"""
from math import ceil
from datetime import datetime
from mongoengine.document import Document
from mongoengine import StringField, BooleanField, DateTimeField, DateTimeField


class FiltersRequiredErr(Exception):
    pass


class BaseDocument(Document):
    """Base Document
    """

    # !IMPORTANT! 允许继承
    meta = {
        'allow_inheritance': True,
        'abstract': True,
        'strict': False,
    }


    is_enable= BooleanField(required=True, default=True)
    status = StringField(required=True, default='1')
    remark = StringField(default='', length=255)
    remark_en = StringField(default='', length=255)
    create_at = DateTimeField(required=True, default=datetime.utcnow)
    update_at = DateTimeField(required=True, default=datetime.utcnow)
    is_import = BooleanField(required=True, default=False)


    @classmethod
    def create(cls, **kwargs):
        """
        Create a new document
        TODO: check if the filed exists
        """
        return cls(**kwargs).save()

    @classmethod
    def set_as_del(cls, **filters):
        """
        Set as deleted
        """
        if not filters:
            raise FiltersRequiredErr()
        return cls.objects(**filters).update(is_del=True)

    @classmethod
    def find_and_update(cls, filters, **kwargs):
        '''
        Query with filters and update all with kwargs
        @fitlers: a dict type query arguments
        @kwargs: update values
        return query count
        '''
        if not filters:
            raise FiltersRequiredErr()
        return cls.objects(**filters).update(**kwargs)

    @classmethod
    def find_and_update_one(cls, filters, **kwargs):
        '''
        Query with filters and update one with kwargs
        @fitlers: a dict type query arguments
        @kwargs: update values
        return query count
        '''
        if not filters:
            raise FiltersRequiredErr()
        return cls.objects(**filters).update_one(**kwargs)

    @classmethod
    def paginate(cls, page, pagesize, *args, **kwargs):
        """
        Query and paginate result
        return count, total_page, records
        """
        skip = (page - 1) * pagesize
        query = cls.objects(*args, **kwargs)

        # TODO check if count is need
        count = query.count()
        total_page = ceil(count / pagesize)

        records = query.skip(skip).limit(pagesize)
        if records:
            return (count, total_page, records)
        else:
            return (0, 0, records)

    @classmethod
    def query(cls, **filters):
        if not filters:
            raise FiltersRequiredErr()
        return cls.objects(**filters)

    @classmethod
    def get_by_id(cls, id):
        """Query record by id."""
        return cls.objects(id=id).first()

    @classmethod
    def get_first(cls, **filters):
        """Query one record"""
        if not filters:
            raise FiltersRequiredErr()
        return cls.objects(**filters).first()

    def to_dict(self, keys=None):
        """return json data of document
        """
        data = super().to_mongo().to_dict()
        data.pop('_id')
        data.pop('_cls')
        data.update(id=self.get_object_id())

        if not keys:
            return data

        res = {}
        for key in keys:
            if key in data.keys():
                res[key] = data.get(key)
        return res

    def get_object_id(self):
        return str(self.id)


