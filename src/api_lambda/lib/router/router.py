class Router:
    def __init__(self, default_route):
        self.routes = {}
        self.default_route = default_route

    def set(self, path, method, target):
        self.routes[f"{path}-{method}"] = target

    def get(self, path: str, method: str):
        try:
            route = self.routes[f"{path}-{method}"]
        except KeyError:
            route = self.default_route
        return route
