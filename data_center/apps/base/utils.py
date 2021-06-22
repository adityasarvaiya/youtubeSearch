import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidTokenError
)

JWT_SUCCESS = 'SUCCESS'
JWT_EXPIRED = 'EXPIRED'
JWT_INVALID = 'INVALID'


class CustomEnumMeta(type):
    """
    Meta class to ChoiceEnum class
    """
    def __new__(cls, clsname, bases, clsdict):
        obj = super().__new__(cls, clsname, bases, clsdict)
        obj.__values__ = []
        obj.__keys__ = []
        for key, val in vars(obj).items():
            if not key.startswith("__"):
                obj.__values__.append(val)
                obj.__keys__.append(key)
        obj.keys = lambda: obj.__keys__
        obj.values = lambda: obj.__values__
        obj._index = 0
        return obj

    def __getitem__(cls, key):
        return getattr(cls, key)

    def __iter__(cls):
        return zip(cls.__values__, cls.__keys__)

    def __next__(cls):
        if len(cls.__values__) >= cls._index:
            cls._index = 0
            raise StopIteration
        res = (cls.__values__[cls._index], cls.__keys__[cls._index])
        cls._index = cls._index + 1
        return res


class ConstantEnum(metaclass=CustomEnumMeta):
    """
    Inheriting this class will provide below operations on the derived class
    1. list(DerivedClass) -> list down all the class attributes and their values
    2. DerivedClass.attribute -> return the string representation of attribute value
    3. DerivedClass['enum'] -> return the string representation of attribute value
    4. 'attribute' in DerivedClass -> existence check for given attribute
    """
