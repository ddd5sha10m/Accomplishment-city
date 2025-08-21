# building.py

import datetime

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