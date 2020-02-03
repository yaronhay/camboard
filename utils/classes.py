class PointHolder:
    def __init__(self):
        self.__paths = list()
        self.__path = list()

    @property
    def paths(self):
        return self.__paths + [self.__path]

    def add_to_path(self, point):
        self.__path.append(point)

    def clear_path(self):
        self.__path = list()

    def finish_path(self):
        self.__paths.append(self.__path)
        self.clear_path()

    @property
    def path_len(self):
        return len(self.__path)

    def clear(self):
        self.__paths = list()
        self.clear_path()