# main.py

from city import City
from project import Project

# 等級設定
# key: 等級
# value: (該等級積木上限, 升到下一級所需的建築總數)
LEVEL_CONFIG = {
    1: {'max_tasks': 5, 'buildings_to_level_up': 3},
    2: {'max_tasks': 8, 'buildings_to_level_up': 7},
    3: {'max_tasks': 12, 'buildings_to_level_up': 12},
    # 可以繼續往上加
}

def check_for_level_up(city: City):
    """檢查是否滿足升級條件"""
    current_level = city.architect_level
    # 如果當前等級不在設定中，表示已滿級
    if current_level not in LEVEL_CONFIG:
        return

    buildings_count = len(city.buildings)
    required_buildings = LEVEL_CONFIG[current_level]['buildings_to_level_up']
    
    if buildings_count >= required_buildings:
        city.level_up()

def main():
    """
    「成就之城」主程式
    """
    print("--- 歡迎來到「成就之城」，偉大的建築師！ ---")
    city_name = input("首先，請為你的城市命名: ")
    my_city = City(city_name)
    print(f"美好的開始！'{my_city.name}' 期待你的建設。")

    projects = []

    while True:
        current_max_tasks = LEVEL_CONFIG.get(my_city.architect_level, {}).get('max_tasks', '無限制')
        print(f"\n=== 建築師工作台 (等級: {my_city.architect_level} | 積木上限: {current_max_tasks}) ===")
        print("1. 建立新專案與任務 (開始規劃新建築)")
        print("2. 編輯專案任務 (調整積木)")
        print("3. 完成任務 (開始堆砌積木)")
        print("4. 查看所有專案進度")
        print("5. 查看我的城市")
        print("6. 離開")
        
        choice = input("請選擇你的下一步行動 (1-6): ")

        if choice == '1':
            project_name = input("請輸入新專案的名稱: ")
            new_project = Project(project_name)
            
            # --- 新的流暢化任務新增流程 ---
            print(f"專案 '{project_name}' 已建立！現在開始為它新增任務 (積木)。")
            print("輸入任務內容後按 Enter，輸入 '完成' 或 'done' 結束新增。")
            
            task_limit = LEVEL_CONFIG.get(my_city.architect_level, {}).get('max_tasks', float('inf'))

            while len(new_project.tasks) < task_limit:
                task_desc = input(f"新增積木 ({len(new_project.tasks)+1}/{task_limit}): ")
                if task_desc.lower() in ['完成', 'done']:
                    break
                new_project.add_task(task_desc)
            
            if len(new_project.tasks) >= task_limit:
                print(f"已達到等級 {my_city.architect_level} 的積木上限 ({task_limit}塊)。")

            projects.append(new_project)
            print(f"專案 '{project_name}' 規劃完畢！")


        elif choice == '2': # 原本的 "新增任務" 改為 "編輯"
            if not projects:
                print("目前沒有任何專案可供編輯。")
                continue
            # ... (此處邏輯與舊版的 choice '2' 相同，用於後續彈性調整，此處省略以保持簡潔)
            print("功能開發中... (此處可加入新增/刪除/修改任務的邏輯)")

        elif choice == '3':
            if not projects:
                print("目前沒有任何專案。")
                continue
            
            print("\n--- 選擇要執行的專案 ---")
            for i, p in enumerate(projects):
                print(f"{i+1}. {p.name}")
            
            try:
                p_choice = int(input(f"請選擇專案編號 (1-{len(projects)}): ")) - 1
                if not (0 <= p_choice < len(projects)):
                    print("無效的選擇。")
                    continue
            except ValueError:
                print("請輸入數字。")
                continue

            chosen_project = projects[p_choice]

            # --- 進入該專案的「連續任務完成」迴圈 ---
            while True:
                # 每次迴圈都重新獲取未完成的任務列表
                pending_tasks = [t for t in chosen_project.tasks if t.status == 'pending']

                # 如果沒有未完成的任務了，就自動跳出
                if not pending_tasks:
                    print(f"\n專案 '{chosen_project.name}' 的所有積木都已堆砌完畢！")
                    break

                print(f"\n--- 專案: {chosen_project.name} (未完成積木) ---")
                for i, t in enumerate(pending_tasks):
                    print(f"{i+1}. {t.description}")
                print("---------------------------------")
                
                t_choice_str = input(f"請選擇要完成的任務編號 (1-{len(pending_tasks)})，或輸入 'b' 返回主選單: ")

                if t_choice_str.lower() == 'b':
                    print("返回主選單...")
                    break # 跳出這個專案的任務迴圈

                try:
                    t_choice = int(t_choice_str) - 1
                    if 0 <= t_choice < len(pending_tasks):
                        task_to_complete = pending_tasks[t_choice]
                        task_to_complete.complete()

                        # ** 核心檢查機制 **
                        # 檢查整個專案是否因為這次的任務完成而全部完成
                        if chosen_project.is_complete():
                            my_city.add_building(chosen_project.name)
                            projects.pop(p_choice) # 從進行中專案列表移除
                            check_for_level_up(my_city) # 檢查升級
                            break # 專案已完成，自動跳出迴圈
                    else:
                        print("無效的任務選擇。")
                except ValueError:
                    print("請輸入數字或 'b'。")

        elif choice == '4':
            if not projects:
                print("目前沒有任何進行中的專案。")
            else:
                for project in projects:
                    print(project)

        elif choice == '5':
            my_city.display()

        elif choice == '6':
            print("感謝你的辛勤工作，建築師！期待下次再見。")
            break
            
        else:
            print("無效的輸入，請重新選擇。")

if __name__ == "__main__":
    main()