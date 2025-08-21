# project.py

# 我們需要從 task.py 檔案中導入 Task 類別
from task import Task
import datetime
class Project:
    """
    代表一個專案或一個大目標，由多個小任務 (積木) 組成。

    屬性:
        name (str): 專案的名稱。
        tasks (list[Task]): 組成此專案的任務清單。
    """
    def __init__(self, name: str):
        self.name = name
        self.tasks = []

    def add_task(self, description: str, due_date: datetime.date = None):
        """
        為這個專案新增一個任務 (積木)。

        參數:
            description (str): 任務的描述。
            due_date (date, optional): 任務的期限. Defaults to None.
        """
        new_task = Task(description, due_date) # 將 due_date 傳遞給 Task
        self.tasks.append(new_task)
        print(f"專案 '{self.name}' -> 已新增積木: '{description}'")

    def is_complete(self) -> bool:
        """
        檢查專案中的所有任務是否都已完成。

        回傳:
            bool: 如果所有任務都完成，則為 True，否則為 False。
        """
        # 如果任務清單是空的，也算未完成
        if not self.tasks:
            return False
        
        for task in self.tasks:
            if task.status == 'pending':
                return False  # 只要有一個任務未完成，專案就未完成
        return True # 所有任務都完成了

    def __str__(self) -> str:
        """回傳專案的字串表示，包含其所有任務的狀態。"""
        # 計算完成度
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task.status == 'completed')
        
        # 建立專案標題和進度條
        header = f"--- 專案: {self.name} (進度: {completed_tasks}/{total_tasks}) ---\n"
        
        # 將每個任務的字串表示串接起來
        tasks_str = "\n".join(str(task) for task in self.tasks)
        
        return header + tasks_str