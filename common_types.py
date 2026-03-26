from enum import StrEnum
from abc import ABC, abstractmethod
from typing import Protocol
from copy import deepcopy
from collections.abc import Sequence

class Action(StrEnum):
    PLANT = "p"
    WATER = "w"
    HARVEST = "h"
    NEXT_DAY = "n"
    GRID_STATUS = "g"

class ACCrops(StrEnum):
    TURNIP = "turnip"

class PVZCrops(StrEnum):
    SUNFLOWER = "sunflower"
    MARIGOLD = "marigold"

type grid_land = Sequence[Sequence[CropType | None]]

class CropType(ABC):
    def __init__(self, cost: int, days: int, value: int, sprites: tuple[str, str]) -> None:
        super().__init__()
        self._cost = cost
        self._days_to_grow = days
        self._harvest_value = value
        self._sprites = sprites

        self._age = 0
        self._is_grown = False
        self._is_watered = False
        self._water_history: list[bool] = []

    @property
    def cost(self): return self._cost

    @property
    def days_to_grow(self): return self._days_to_grow

    @property
    def harvest_value(self): return self._harvest_value

    @property
    def age(self): return self._age

    @property
    def is_grown(self): return self._is_grown

    @property
    def is_watered(self): return self._is_watered

    @abstractmethod
    def was_watered_on_k(self, k: int):
        ...

    def grow(self):
        self.__update_history()
        if self._is_watered:
            self._age += 1
            self._is_watered = False
        if self._age == self._days_to_grow:
            self._is_grown = True

    def __update_history(self):
        self._water_history.append(self._is_watered)

    def water(self):
        if not self._is_watered:
            self._is_watered = True

    def __str__(self) -> str:
        growing, grown = self._sprites
        return (grown if self._is_grown else growing)

class Turnip(CropType):
    def __init__(self):
        super().__init__(300, 2, 500, ("t", "T"))

    def was_watered_on_k(self, k: int):
        pass

class Sunflower(CropType):
    def __init__(self):
        super().__init__(25, 1, 50, ("s", "S"))

    def was_watered_on_k(self, k: int):
        pass

class Marigold(CropType):
    def __init__(self):
        super().__init__(50, 2, 150, ("m", "M"))

    def was_watered_on_k(self, k: int):
        pass


class SeedPacketMode(Protocol):
    _pesos: int
    _grid: grid_land

    @property
    def pesos(self) -> int: ...

    @property
    def grid(self) -> grid_land: ...

    def valid_crops(self) -> list[str]: ...

    def make_crop(self, crop: str) -> CropType: ...

class AnimalCrossing:
    def __init__(self) -> None:
        self._pesos = 1000
        self._grid: grid_land = [[None] * 5 for _ in range(5)]
    
    @property
    def pesos(self) -> int: return self._pesos

    @property
    def grid(self) -> grid_land: return deepcopy(self._grid)

    def valid_crops(self) -> list[str]:
        return [crop for crop in ACCrops]
    
    def make_crop(self, crop: str) -> CropType:
        match ACCrops(crop):
            case ACCrops.TURNIP:
                return Turnip()

class PlantsVSZombies:
    def __init__(self) -> None:
        self._pesos = 100
        self._grid: grid_land = [[None] * 9 for _ in range(5)]
    
    @property
    def pesos(self) -> int: return self._pesos

    @property
    def grid(self) -> grid_land: return deepcopy(self._grid)

    def valid_crops(self) -> list[str]:
        return [crop for crop in PVZCrops]
    
    def make_crop(self, crop: str) -> CropType:
        match PVZCrops(crop):
            case PVZCrops.SUNFLOWER:
                return Sunflower()
            case PVZCrops.MARIGOLD:
                return Marigold()


class WateringCan(Protocol):
    def aoe(self, i: int, j: int, grid: list[list[CropType | None]]) -> list[tuple[int, int]]: ...

class Basic:
    def aoe(self, i: int, j: int, grid: list[list[CropType | None]]) -> list[tuple[int, int]]:
        return [(i, j)]

class Steel:
    def aoe(self, i: int, j: int, grid: list[list[CropType | None]]) -> list[tuple[int, int]]:
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)]
        affected = [(i, j)]
        for di, dj in dir:
            ni = i + di
            nj = j + dj
            if 0 <= ni <= len(grid) and 0 <= nj < len(grid[0]):
                affected.append((ni, nj))
        return affected

packets: dict[str, type[SeedPacketMode]] = {
    "ac": AnimalCrossing,
    "pvz": PlantsVSZombies,
}
def make_packet(packet: str) -> SeedPacketMode:
    return packets[packet]()

water: dict[str, type[WateringCan]] = {
    "basic": Basic,
    "steel": Steel
}
def make_water(water_type: str) -> WateringCan:
    return water[water_type]()
