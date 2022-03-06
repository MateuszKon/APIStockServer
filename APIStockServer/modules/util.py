import os


def get_environ(var_name):
    value = os.environ.get(var_name)
    if value:
        return value
    else:
        raise KeyError(f"{var_name} environment variable is not defined!")


def get_environ_file_path(var_name, root_path=None):
    """
    Get environment variable which contains path to file.
    :param var_name: name of environment variable
    :param root_path: optional root path, if it is allowed to put path in environment variable as relative path to root
    :return: path from env variable or path concatenated to root_path if path is not absolut but relative to root_path
    """
    path = get_environ(var_name)
    if not os.path.isfile(path):
        tmp_path = os.path.join(root_path, path)
        if os.path.isfile(tmp_path) and root_path is not None:
            path = tmp_path
        else:
            raise KeyError(f"{var_name} environment variable is not a absolute nor relative path to file! "
                           f"Generated path from variable: '{path}' and '{tmp_path}'")
    return path
