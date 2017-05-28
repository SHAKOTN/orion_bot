from importlib import import_module


def import_string(dotted_path):
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = "{} wrong module path".format(dotted_path)
        raise ImportError(msg)

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "{}" does not define a "{}" attribute/class'.format(
            module_path, class_name
        )
        raise ImportError(msg)
