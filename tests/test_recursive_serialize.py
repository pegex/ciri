import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')  # noqa

from ciri.fields import Boolean, Float, String, List, Schema as SubSchema, SelfReference
from ciri.core import Schema, PolySchema, SchemaOptions
from ciri.exception import ValidationError
from ciri.registry import schema_registry

import pytest

"""
SCHEMAS
"""

class ExpiresSchema(Schema):
    expires_on = Float()

class ItemSchema(Schema):
    class Meta:
        pre_serialize = ['get_computed']

    def get_computed(self, data, schema=None, context=None):
        if data.get('expires'):
            if isinstance(data['expires'], dict):
                print("Pre_serialize is dict")
            if isinstance(data['expires'], Expires):
                print("Pre_serialize is object")
        return data

    expires = SubSchema(ExpiresSchema)

class RefSchema(Schema):
    item = SubSchema(ItemSchema)


"""
MOCK CLASSES
"""
class Expires:

    def __init__(self):
        self.expires_on = 123;

class Item:
    def __init__(self):
        self.expires = Expires()

class ItemRef:
    def __init__(self):
        self.item = Item()

def test_nested_preserialize():
    normal_obj = Item()
    normal_schema = ItemSchema()
    normal_schema.serialize(normal_obj)
    # output: Pre_serialize is object

    recurse_obj = ItemRef()
    recurse_schema = RefSchema()
    recurse_schema.serialize(recurse_obj)
    # output: Pre_serialize is dict

    assert False
