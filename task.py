# task.py

import datetime

class Task:
    """
    代表一個待辦任務的類別。

    屬性:
        description (str): 任務的文字描述。
        status (str): 任務的狀態，'pending' (未完成) 或 'completed' (已完成)。
        creation_date (date): 任務的創建日期。
    """
    def __init__(self, description: str):
        """
        初始化一個新的 Task 物件。
        
        參數:
            description (str): 任務的描述。
        """
        self.description = description
        self.status = "pending"  # 初始狀態都是 'pending'
        self.creation_date = datetime.date.today()

    def complete(self):
        """將任務狀態標記為 'completed'。"""
        self.status = "completed"
        print(f"恭喜你！任務 '{self.description}' 已完成！")

    def __str__(self) -> str:
        """回傳任務的字串表示，方便列印。"""
        # 如果任務已完成，顯示 [x]，否則顯示 [ ]
        marker = 'x' if self.status == 'completed' else ' '
        return f"[{marker}] {self.description} (建立於: {self.creation_date})"