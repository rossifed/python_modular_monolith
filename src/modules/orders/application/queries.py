from shared.queries.abstractions import Query


class OrderQuery(Query):
    def __init__(self, name: str):
        self.name = name
