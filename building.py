# building.py

import datetime
'''
class Building:
    """
    代表一座由完成的專案所建成的建築物。

    屬性:
        name (str): 建築物的名稱，事後可修改。
        completion_date (date): 建築物的建成日期。
    """
    def __init__(self, project_name: str):
        """
        初始化一個新的 Building 物件。

        參數:
            project_name (str): 作為建築物初始名稱的專案名稱。
        """
        self.name = project_name
        self.completion_date = datetime.date.today()

    def rename(self, new_name: str):
        """
        修改建築物的名稱。
        """
        self.name = new_name
        print(f"建築物 '{self.name}' 已更名為 '{new_name}'。")

    def __str__(self) -> str:
        """回傳建築物的字串表示。"""
        return f"建築物: {self.name} (建成於: {self.completion_date})"
'''
# building.py

class Building:
    # --- 修改：增加 size 和 coordinates 屬性 ---
    def __init__(self, project_name: str, category: str, vitality_points: int, size: tuple):
        self.name = project_name
        self.category = category
        self.vitality_points = vitality_points
        self.size = size  # --- 新增：尺寸，例如 (寬, 高) -> (2, 2)
        self.coordinates = None  # --- 新增：位置，初始為 None

    # --- 新增：設定建築位置的方法 ---
    def set_position(self, x: int, y: int):
        self.coordinates = (x, y)

    def rename(self, new_name: str):
        self.name = new_name
        print(f"建築物 '{self.name}' 已更名為 '{new_name}'。")

    def __str__(self) -> str:
        # --- 修改：顯示更豐富的資訊 ---
        pos_str = f" @ ({self.coordinates[0]},{self.coordinates[1]})" if self.coordinates else ""
        size_str = f"({self.size[0]}x{self.size[1]})"
        return f"建築物: {self.name} {size_str} [{self.category}]{pos_str}"

# --- 新增：一個專門給獎勵的地標類別 ---
class Landmark:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.unlock_date = datetime.date.today()

    def __str__(self) -> str:
        return f"🌟 地標: {self.name} - {self.description} (解鎖於: {self.unlock_date})"