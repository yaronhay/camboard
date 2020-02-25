class PointHolder:
    def __init__(self):
        self.__paths = list()
        self.__path = list()
        self.color = (0, 0, 0)

    @property
    def paths(self):
        return self.__paths + [{
            'points': self.__path,
            'color': self.color
        }]

    def add_to_path(self, point):
        if len(self.__path) == 0 or point != self.__path[-1]:
            self.__path.append(point)

    def clear_path(self):
        self.__path = list()

    def finish_path(self):
        self.__paths.append({
            'points': self.__path,
            'color': self.color
        })
        self.clear_path()

    def remove_path(self, path):
        self.__path.remove(path)

    @property
    def path_len(self):
        return len(self.__path)

    def clear(self):
        self.__paths = list()
        self.clear_path()

    def remove_paths(self, paths):
        for path in paths:
            if path in self.__paths:
                self.__paths.remove(path)
