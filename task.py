# task.py

import datetime

class Task:
    """
    代表一個待辦任務的類別。

    屬性:
        description (str): 任務的文字描述。
        status (str): 任務的狀態，'pending' (未完成) 或 'completed' (已完成)。
        creation_date (date): 任務的創建日期。
        due_date (date | None): 任務的期限，可選。
    """
    def __init__(self, description: str, due_date: datetime.date = None):
        """
        初始化一個新的 Task 物件。
        
        參數:
            description (str): 任務的描述。
            due_date (date, optional): 任務的期限. Defaults to None.
        """
        self.description = description
        self.status = "pending"
        self.creation_date = datetime.date.today()
        self.due_date = due_date

    def complete(self):
        """將任務狀態標記為 'completed'。"""
        self.status = "completed"
        print(f"恭喜你！任務 '{self.description}' 已完成！")

    def edit(self, new_description: str = None, new_due_date: datetime.date = None):
        """
        編輯任務的描述或期限。
        """
        if new_description:
            self.description = new_description
        if new_due_date is not None: # 允許將日期設為空
            self.due_date = new_due_date
        print("任務已更新！")

    def __str__(self) -> str:
        """回傳任務的字串表示，方便列印。"""
        marker = 'x' if self.status == 'completed' else ' '
        # 如果有設定期限，就顯示出來
        due_date_str = f" (期限: {self.due_date})" if self.due_date else ""
        return f"[{marker}] {self.description}{due_date_str}"