class DataClass:
    def __init__(self, data: dict = dict()):
        for key in data:
            setattr(self, key, data[key])
