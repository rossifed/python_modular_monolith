from shared.queries.abstractions import Query


class HelloQuery(Query):
    def __init__(self, name: str):
        self.name = name
