def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def update_connection_decorator(func):
    def wrapper(self, *args, **kwargs):
        self.updateConnection()
        return func(self, *args, **kwargs)

    return wrapper
