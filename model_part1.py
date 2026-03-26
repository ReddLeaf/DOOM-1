from common_types import SeedPacketMode, WateringCan, CropType


class TCModel1:
    def __init__(self, seed_packet_mode: SeedPacketMode, watering_can: WateringCan) -> None:
        self._seed_packet_mode = seed_packet_mode
        self._watering_can = watering_can
        
        self._pesos = self._seed_packet_mode.pesos
        self._grid: list[list[CropType | None]] = [list(inner) for inner in self._seed_packet_mode.grid]
        self._day = 1

    @property
    def day(self): return self._day
    
    @property
    def pesos(self): return self._pesos
    
    @property
    def grid(self): return self._grid

    @property
    def valid_crops(self): return self._seed_packet_mode.valid_crops()
    
    def inbounds(self, i: int, j: int):
        return 0 <= i < len(self._grid) and 0 <= j < len(self._grid[0])
    
    def plant(self, crop: str, i: int, j: int) -> bool:
        mode = self._seed_packet_mode
        crop_type = mode.make_crop(crop)
        if not self.inbounds(i, j):
            return False
        if self.grid[i][j] is not None:
            return False
        if crop_type.cost > self._pesos:
            return False
        
        self._pesos -= crop_type.cost
        self._grid[i][j] = crop_type
        return True

    def water(self, i: int, j: int) -> bool:
        if not self.inbounds(i, j):
            return False
        
        for r, c in self._watering_can.aoe(i, j, self._grid):
            cell = self._grid[r][c]
            if cell is not None:
                cell.water()
        return True

    def harvest(self) -> bool:
        success = False
        for i in range(len(self._grid)):
            for j in range(len(self.grid[0])):
                cell = self._grid[i][j]
                if cell is not None and cell.is_grown:
                    self._pesos += cell.harvest_value
                    cell = None
                    success = True
        return success
    
    def next_day(self):
        for i in range(len(self._grid)):
            for j in range(len(self.grid[0])):
                cell = self._grid[i][j]
                if cell is not None:
                    cell.grow()
        self._day += 1
