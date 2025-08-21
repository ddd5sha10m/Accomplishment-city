# main.py

from city import City
from project import Project
import datetime

# 等級設定
# key: 等級
# value: (該等級積木上限, 升到下一級所需的建築總數)
# 等級設定
LEVEL_CONFIG = {
    1: {'max_tasks': 5, 'buildings_to_level_up': 3, 'wip_limit': 2},
    2: {'max_tasks': 8, 'buildings_to_level_up': 7, 'wip_limit': 3},
    3: {'max_tasks': 12, 'buildings_to_level_up': 12, 'wip_limit': 4},
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
        # --- 修改：在主選單顯示目前專案數量與上限 ---
        current_wip_limit = LEVEL_CONFIG.get(my_city.architect_level, {}).get('wip_limit', 2)
        current_max_tasks = LEVEL_CONFIG.get(my_city.architect_level, {}).get('max_tasks', '無限制')
        
        print(f"\n=== 建築師工作台 (等級: {my_city.architect_level} | 專案: {len(projects)}/{current_wip_limit} | 積木上限: {current_max_tasks}) ===")
        print("1. 建立新專案與任務 (開始規劃新建築)")
        print("2. 編輯專案任務 (調整積木)")
        print("3. 完成任務 (開始堆砌積木)")
        print("4. 查看所有專案進度")
        print("5. 查看我的城市")
        print("6. 離開")
        
        choice = input("請選擇你的下一步行動 (1-6): ")

        if choice == '1':
            if len(projects) >= current_wip_limit:
                print("\n** 你的工作台已經滿了！ **")
                print("專注是通往偉大成就的捷徑。請先完成一項進行中的專案，來為新的靈感騰出空間。")
                continue # 中斷此次操作，返回主選單
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


        elif choice == '2': # 編輯專案任務
            if not projects:
                print("目前沒有任何專案可供編輯。")
                continue
            
            print("\n--- 選擇要編輯的專案 ---")
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

            # --- 進入該專案的「編輯工作台」迴圈 ---
            while True:
                print(f"\n--- 編輯專案: {chosen_project.name} ---")
                if not chosen_project.tasks:
                    print("此專案目前沒有任何積木。")
                else:
                    for i, task in enumerate(chosen_project.tasks):
                        print(f"{i+1}. {task}")
                
                print("\n--- 編輯選項 ---")
                print("1. 新增積木")
                print("2. 修改積木描述")
                print("3. 設定/修改積木期限")
                print("4. 刪除積木")
                print("b. 返回主選單")
                
                edit_choice = input("請選擇操作: ")

                if edit_choice == '1': # 新增
                    task_limit = LEVEL_CONFIG.get(my_city.architect_level, {}).get('max_tasks', float('inf'))
                    if len(chosen_project.tasks) >= task_limit:
                        print(f"無法新增，已達到等級 {my_city.architect_level} 的積木上限 ({task_limit}塊)。")
                        continue
                    
                    desc = input("輸入新積木的描述: ")
                    chosen_project.add_task(desc)

                elif edit_choice == '2': # 修改描述
                    try:
                        t_idx = int(input("選擇要修改的積木編號: ")) - 1
                        new_desc = input("輸入新的描述: ")
                        chosen_project.tasks[t_idx].edit(new_description=new_desc)
                    except (ValueError, IndexError):
                        print("無效的選擇或輸入。")

                elif edit_choice == '3': # 修改期限
                    try:
                        t_idx = int(input("選擇要設定期限的積木編號: ")) - 1
                        date_str = input("輸入期限 (格式 YYYY-MM-DD)，或留空來清除期限: ")
                        if not date_str:
                             chosen_project.tasks[t_idx].edit(new_due_date=None)
                        else:
                            new_due_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                            chosen_project.tasks[t_idx].edit(new_due_date=new_due_date)
                    except (ValueError, IndexError):
                        print("無效的選擇或日期格式錯誤。")
                
                elif edit_choice == '4': # 刪除
                    try:
                        t_idx = int(input("選擇要刪除的積木編號: ")) - 1
                        removed_task = chosen_project.tasks.pop(t_idx)
                        print(f"積木 '{removed_task.description}' 已被刪除。")
                    except (ValueError, IndexError):
                        print("無效的選擇。")

                elif edit_choice.lower() == 'b':
                    break # 跳出編輯迴圈
                else:
                    print("無效的選項。")

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
                        chosen_project.touch()

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

        elif choice == '4': # 查看所有專案進度
            if not projects:
                print("目前沒有任何進行中的專案。")
            else:
                print("\n--- 所有專案進度 ---")
                today = datetime.date.today()
                for project in projects:
                    # --- 新增：計算營火狀態 ---
                    days_idle = (today - project.last_updated_date).days
                    if days_idle < 3:
                        campfire_emoji = "🔥"
                    elif 3 <= days_idle <= 7:
                        campfire_emoji = "...🔥"
                    else:
                        campfire_emoji = "🧊"
                    
                    print(f"{campfire_emoji} {project}")

        elif choice == '5':
            my_city.display()

        elif choice == '6':
            print("感謝你的辛勤工作，建築師！期待下次再見。")
            break
            
        else:
            print("無效的輸入，請重新選擇。")

if __name__ == "__main__":
    main()