def autosave(method):
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        if hasattr(self, "repository") and self.repository:
            self.repository.save(self)
        return result
    return wrapper
