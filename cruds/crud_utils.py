from factory.core_instantiations import g as global_object


def get_url_param():
    if hasattr(global_object, 'url_parameter'):
        url_param = getattr(global_object, 'url_parameter', None)
        delattr(global_object, 'url_parameter')
        return url_param
    else:
        return None
