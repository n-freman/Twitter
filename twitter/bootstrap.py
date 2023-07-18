from .adapters import orm


def bootstrap():
    orm.start_mappers()
