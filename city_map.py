# city_map.py

class CityMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
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

    def place_construction_site(self, project, x, y) -> bool:
        """嘗試在地圖上規劃一片施工地"""
        width, height = project.size
        
        if not self._is_within_bounds(x, y, width, height):
            print("錯誤：規劃地點超出地圖邊界！")
            return False
        
        if self._is_overlapping(x, y, width, height):
            print("錯誤：此處已有其他規劃！")
            return False

        # 放置施工鷹架，我們用 '#' 作為標記
        for i in range(height):
            for j in range(width):
                self.grid[y + i][x + j] = '#'
        
        project.set_position(x, y)
        print(f"'{project.name}' 的工地已成功規劃在 ({x},{y})！")
        return True

    # --- 新增：將工地正式變為建築的方法 ---
    def finalize_building(self, building):
        """專案完工，將鷹架替換為建築"""
        if not building.coordinates:
            print("錯誤：此建築沒有座標，無法完工。")
            return
            
        x, y = building.coordinates
        width, height = building.size
        building_char = building.category[0].upper()

        for i in range(height):
            for j in range(width):
                self.grid[y + i][x + j] = building_char
        
        self.placed_buildings.append(building)