# city_map.py

class CityMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # 創建一個二維列表作為網格，'.' 代表空地
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
        # 用來存放已放置的建築物物件
        self.placed_buildings = []

    def display(self):
        """在終端機中印出整個城市地圖"""
        print("\n" + " " * 4 + "".join([f"{i:<2}" for i in range(self.width)])) # 印出 X 座標軸
        print(" " * 3 + "+" + "-" * (self.width * 2) + "+")
        for y in range(self.height):
            # 印出 Y 座標軸 和 地圖內容
            print(f"{y:<2} | {' '.join(self.grid[y])} |")
        print(" " * 3 + "+" + "-" * (self.width * 2) + "+")

    def _is_within_bounds(self, x, y, width, height):
        """檢查建築是否超出地圖邊界"""
        return 0 <= x and (x + width) <= self.width and 0 <= y and (y + height) <= self.height

    def _is_overlapping(self, x, y, width, height):
        """檢查該區域是否已被佔用"""
        for i in range(height):
            for j in range(width):
                if self.grid[y + i][x + j] != '.':
                    return True
        return False

    def place_building(self, building, x, y) -> bool:
        """嘗試將建築放置在地圖上"""
        width, height = building.size
        
        if not self._is_within_bounds(x, y, width, height):
            print("錯誤：建築超出地圖邊界！")
            return False
        
        if self._is_overlapping(x, y, width, height):
            print("錯誤：此處已被其他建築佔用！")
            return False

        # 放置建築
        building_char = building.category[0].upper() # 用分類的第一個字母當作圖標
        for i in range(height):
            for j in range(width):
                self.grid[y + i][x + j] = building_char
        
        building.set_position(x, y)
        self.placed_buildings.append(building)
        return True