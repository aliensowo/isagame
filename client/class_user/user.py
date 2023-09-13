from server.errors.errors_user import InventoryFullError, InventoryElementNotEnough


class User:
    _inventory_len = 25
    _inventory = {}
    _speed = 5
    _power = 1
    _level = 0

    def get_inventory(self):
        return self._inventory

    def put_to_inventory(self, element: str, count: int) -> bool:
        if element in self._inventory.keys():
            self._inventory[element] += count
        else:
            if len(self._inventory) < self._inventory_len:
                self._inventory[element] = count
            else:
                raise InventoryFullError
        return True

    def get_from_inventory(self, element: str, count: int):
        if element in self._inventory.keys():
            if self._inventory[element] >= count:
                self._inventory[element] -= count
                return {element: count}
        raise InventoryElementNotEnough

