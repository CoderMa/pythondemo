class g_var(object):
    _global_dict = {}

    def set_dict(self, key, value):
        self._global_dict[key] = value

    def get_dict(self, key):
        return self._global_dict[key]

    def show_dict(self):
        return self._global_dict
