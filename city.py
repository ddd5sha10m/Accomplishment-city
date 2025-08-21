# city.py

from building import Building

class City:
    """
    代表建築師的成就之城，是所有建築物的容器。

    屬性:
        name (str): 城市的名稱。
        buildings (list[Building]): 城市中所有建築物的清單。
    """
    def __init__(self, name: str):
        """
        初始化一個新的 City 物件。

        參數:
            name (str): 建築師為城市取的名字。
        """
        self.name = name
        self.buildings = []

    def add_building(self, project_name: str):
        """
        當一個專案完成時，在城市中新增一棟建築物。

        參數:
            project_name (str): 已完成專案的名稱。
        """
        new_building = Building(project_name)
        self.buildings.append(new_building)
        print(f"\n🎉 偉大的成就！一棟新的建築物 '{project_name}' 在 '{self.name}' 拔地而起！ 🎉")

    def display(self):
        """展示城市的樣貌和所有建築物。"""
        print(f"\n--- 歡迎來到你的城市: {self.name} ---")
        if not self.buildings:
            print("這裡還空空如也，讓我們開始建造第一棟建築吧！")
        else:
            print(f"城市中目前有 {len(self.buildings)} 棟建築物:")
            for building in self.buildings:
                print(f"  - {building}")
        print("----------------------------------------")