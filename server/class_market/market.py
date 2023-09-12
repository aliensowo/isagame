from typing import Dict
from server.db.db_queries import Queries


class Market:

    stock: Dict[str, Dict[int, int]]  # {name: cost: count}

    def __init__(self):
        self.db = Queries()
        self.stock = {}

    def add_to_stock(self, element: str, cost: int, count: int):
        query_rows = self.db.sql_select(
            "select count(*) from Market where element = '{}' and cost = {}".format(element, cost)
        )
        if query_rows[0][0] > 0:
            self.db.sql_insert(
                "UPDATE Market SET count = count + {} where element = '{}' and cost = {}".format(
                    count, element, cost
                ),
            )
        else:
            self.db.sql_insert(
                'INSERT INTO Market (element, cost, count) VALUES (?, ?, ?)',
                (element, cost, count),
            )

    def get_stock(self):
        query_rows = self.db.sql_select("select element, cost, count from Market")
        return self.pack_query_to_stock(query_rows)

    @staticmethod
    def pack_query_to_stock(query_rows: list):
        stock = {}
        for row in query_rows:
            if row[0] in stock.keys():
                if row[1] not in stock[row[0]].keys():
                    stock[row[0]][row[1]] = row[2]
            else:
                stock[row[0]] = {row[1]: row[2]}
        return stock

    @staticmethod
    def _sort_stock(dictionary: dict):
        return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}

    def __sort_stock(self):
        for element, value in self.stock.items():
            self.stock[element] = self._sort_stock(value)

    def buy_from_stock(self, element: str, cost: int, count: int) -> bool:
        query_rows = self.db.sql_select(
            "select element, cost, count from Market where element = '{}' and cost = {}".format(element, cost)
        )
        if len(query_rows[0][0]) > 0:
            stock = self.pack_query_to_stock(query_rows)
            print(stock)
            print(list(stock[element].values())[0])
            if list(stock[element].values())[0] >= count:
                self.db.sql_insert(
                    "UPDATE Market SET count = count - {} where element = '{}' and cost = {}".format(
                        count, element, cost
                    ),
                )
                return True
        return False
