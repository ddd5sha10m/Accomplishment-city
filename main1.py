# main.py

import datetime
import random
import pickle # --- 新增：導入 pickle 模組 ---
from city import City
from project import Project
from building import Landmark

# (CATEGORIES, LEVEL_CONFIG, VITALITY_MILESTONES 等設定檔保持不變)
CATEGORIES = {
    "生活": {"points": 10, "size": (2, 2), "inspirations": ["整理桌面5分鐘", "繳納一份帳單", "為植物澆水"]},
    "學習": {"points": 20, "size": (3, 2), "inspirations": ["閱讀一篇文章", "學習一個新單字", "看一段教學影片"]},
    "健康": {"points": 15, "size": (3, 3), "inspirations": ["到戶外散步15分鐘", "做一組伸展運動", "喝一杯溫開水"]},
    "創作": {"points": 25, "size": (2, 3), "inspirations": ["寫下今天的一個想法", "畫一個簡單的塗鴉"]},
    "娛樂": {"points": 12, "size": (4, 2), "inspirations": ["看一集喜歡的劇", "聽一張完整的專輯"]},
}
LEVEL_CONFIG = {
    1: {'max_tasks': 5, 'buildings_to_level_up': 3, 'wip_limit': 2},
    2: {'max_tasks': 8, 'buildings_to_level_up': 7, 'wip_limit': 3},
    3: {'max_tasks': 12, 'buildings_to_level_up': 12, 'wip_limit': 4},
}
VITALITY_MILESTONES = {
    100: Landmark("初心噴泉", "紀念你踏出第一步的勇氣"),
    300: Landmark("毅力鐘樓", "你的堅持，連時間都為之動容"),
    800: Landmark("成就紀念碑", "這座城市因你的努力而閃耀"),
}

# --- 新增：儲存遊戲的函式 ---
def save_game(city, projects, filename="savegame.dat"):
    """將城市和專案物件儲存到檔案中"""
    try:
        with open(filename, "wb") as f: # 'wb' 表示二進位寫入模式
            game_state = {
                'city': city,
                'projects': projects
            }
            pickle.dump(game_state, f)
            print("遊戲進度已儲存！")
    except Exception as e:
        print(f"儲存失敗：{e}")

# --- 新增：讀取遊戲的函式 ---
def load_game(filename="savegame.dat"):
    """從檔案中讀取城市和專案物件"""
    try:
        with open(filename, "rb") as f: # 'rb' 表示二進位讀取模式
            game_state = pickle.load(f)
            return game_state['city'], game_state['projects']
    except FileNotFoundError:
        print("找不到存檔檔案，將開始一個新遊戲。")
        return None, None
    except Exception as e:
        print(f"讀取失敗：{e}")
        return None, None

def check_for_level_up(city: City):
    current_level = city.architect_level
    if current_level not in LEVEL_CONFIG: return
    buildings_count = len(city.map.placed_buildings)
    required_buildings = LEVEL_CONFIG[current_level]['buildings_to_level_up']
    if buildings_count >= required_buildings:
        city.level_up()

def check_for_milestones(city: City):
    unlocked_landmarks = [lm.name for lm in city.landmarks]
    for vitality_goal, landmark in VITALITY_MILESTONES.items():
        if city.total_vitality >= vitality_goal and landmark.name not in unlocked_landmarks:
            city.add_landmark(landmark)

def main():
    """「成就之城」主程式"""
    
    # --- 修改：程式啟動時，先嘗試讀取存檔 ---
    my_city, projects = load_game()
    
    if my_city is None:
        # 如果沒有存檔，才執行全新的初始化流程
        print("--- 歡迎來到「成就之城」，偉大的建築師！ ---")
        city_name = input("首先，請為你的城市命名: ")
        my_city = City(city_name)
        projects = []
        print(f"美好的開始！'{my_city.name}' 期待你的建設。")
    else:
        # 如果成功讀取，就歡迎回來
        print(f"--- 歡迎回來，{my_city.name} 的偉大建築師！ ---")

    while True:
        # (主迴圈內的所有邏輯，包括選單和選項1-7的實作，都保持不變)
        # ...
        current_wip_limit = LEVEL_CONFIG.get(my_city.architect_level, {}).get('wip_limit', 2)
        
        print(f"\n=== 建築師工作台 (等級: {my_city.architect_level} | 專案: {len(projects)}/{current_wip_limit} | 活力: {my_city.total_vitality}) ===")
        print("1. 建立新專案 (規劃工地)")
        print("2. 完成任務 (推進工期)")
        print("3. 查看所有專案進度")
        print("4. 查看我的城市")
        print("5. 抽取每日靈感")
        print("6. 編輯專案任務 (開發中)")
        print("7. 離開")
        
        choice = input("請選擇你的下一步行動: ")

        if choice == '1':
            # ... (此處所有邏輯與上一版相同)
            if len(projects) >= current_wip_limit:
                print("\n** 你的工作台已經滿了！ **\n專注是通往偉大成就的捷徑。請先完成一項進行中的專案，來為新的靈感騰出空間。")
                continue
            print("\n--- 選擇專案分類 ---")
            cat_list = list(CATEGORIES.keys())
            for i, cat in enumerate(cat_list): print(f"{i+1}. {cat}")
            try:
                cat_choice = int(input("請選擇分類編號: ")) - 1
                if not (0 <= cat_choice < len(cat_list)): print("無效的選擇。"); continue
                chosen_category = cat_list[cat_choice]
            except ValueError: print("請輸入數字。"); continue
            project_name = input(f"請為這個 '{chosen_category}' 專案命名: ")
            category_info = CATEGORIES[chosen_category]
            new_project = Project(project_name, chosen_category, category_info['size'])
            new_project.vitality_points = category_info['points']
            print(f"\n--- 規劃工地 ---")
            print(f"你即將為新專案 '{new_project.name}' {new_project.size[0]}x{new_project.size[1]} 規劃一片土地。")
            site_placed = False
            while not site_placed:
                my_city.map.display()
                coord_input = input("請輸入工地左上角座標 (格式: x,y)，或輸入 'b' 取消規劃: ")
                if coord_input.lower() == 'b': print("已取消專案規劃。"); break
                try:
                    x_str, y_str = coord_input.split(',')
                    x, y = int(x_str.strip()), int(y_str.strip())
                    if my_city.start_project_site(new_project, x, y): site_placed = True
                except ValueError: print("座標格式錯誤，請輸入如 '3,4' 的格式。")
            if not site_placed: continue
            task_limit = LEVEL_CONFIG.get(my_city.architect_level, {}).get('max_tasks', float('inf'))
            print(f"工地規劃完畢！現在為 '{project_name}' 新增任務 (積木上限: {task_limit})。")
            print("輸入任務內容後按 Enter，輸入 '完成' 或 'done' 結束新增。")
            while len(new_project.tasks) < task_limit:
                task_desc = input(f"新增積木 ({len(new_project.tasks)+1}/{task_limit}): ")
                if task_desc.lower() in ['完成', 'done']: break
                new_project.add_task(task_desc)
            projects.append(new_project)
            print(f"專案 '{project_name}' 已正式開工！")

        elif choice == '2':
            # ... (此處所有邏輯與上一版相同)
            if not projects: print("目前沒有任何專案。"); continue
            print("\n--- 選擇要執行的專案 ---")
            for i, p in enumerate(projects): print(f"{i+1}. {p.name}")
            try:
                p_choice = int(input(f"請選擇專案編號 (1-{len(projects)}): ")) - 1
                if not (0 <= p_choice < len(projects)): print("無效的選擇。"); continue
            except ValueError: print("請輸入數字。"); continue
            chosen_project = projects[p_choice]
            while True:
                pending_tasks = [t for t in chosen_project.tasks if t.status == 'pending']
                if not pending_tasks: print(f"\n專案 '{chosen_project.name}' 的所有積木都已堆砌完畢！"); break
                print(f"\n--- 專案: {chosen_project.name} (未完成積木) ---")
                for i, t in enumerate(pending_tasks): print(f"{i+1}. {t.description}")
                t_choice_str = input(f"請選擇要完成的任務編號 (1-{len(pending_tasks)})，或輸入 'b' 返回: ")
                if t_choice_str.lower() == 'b': break
                try:
                    t_choice = int(t_choice_str) - 1
                    if 0 <= t_choice < len(pending_tasks):
                        task_to_complete = pending_tasks[t_choice]
                        task_to_complete.complete()
                        chosen_project.touch()
                        if chosen_project.is_complete():
                            my_city.complete_project_site(chosen_project)
                            projects.pop(p_choice)
                            check_for_level_up(my_city)
                            check_for_milestones(my_city)
                            break
                    else: print("無效的任務選擇。")
                except ValueError: print("請輸入數字或 'b'。")
        
        elif choice == '3':
            # ... (此處所有邏輯與上一版相同)
            if not projects: print("目前沒有任何進行中的專案。"); continue
            print("\n--- 所有專案進度 ---")
            today = datetime.date.today()
            for project in projects:
                days_idle = (today - project.last_updated_date).days
                if days_idle < 3: campfire_emoji = "🔥"
                elif 3 <= days_idle <= 7: campfire_emoji = "...🔥"
                else: campfire_emoji = "🧊"
                print(f"{campfire_emoji} {project}")

        elif choice == '4':
            # ... (此處所有邏輯與上一版相同)
            my_city.display()
        
        elif choice == '5':
            # ... (此處所有邏輯與上一版相同)
            print("\n--- 每日靈感 ---")
            random_category = random.choice(list(CATEGORIES.keys()))
            random_inspiration = random.choice(CATEGORIES[random_category]['inspirations'])
            print(f"分類：{random_category}")
            print(f"靈感：「{random_inspiration}」")
            action = input("要將這個靈感變成一個新專案嗎？ (y/n): ")
            if action.lower() == 'y':
                if len(projects) >= current_wip_limit:
                    print("\n** 你的工作台已經滿了！ **\n請先完成一項專案，才能將靈感付諸實踐喔。")
                else:
                    print("\n請注意：靈感專案也需要在地圖上規劃工地。")
                    category_info = CATEGORIES[random_category]
                    new_project = Project(random_inspiration, random_category, category_info['size'])
                    new_project.vitality_points = category_info['points']
                    site_placed = False
                    while not site_placed:
                         my_city.map.display()
                         coord_input = input(f"為 '{random_inspiration}' 規劃工地 (格式: x,y): ")
                         try:
                            x, y = map(int, coord_input.split(','))
                            if my_city.start_project_site(new_project, x, y): site_placed = True
                         except ValueError: print("格式錯誤。")
                    new_project.add_task(random_inspiration)
                    projects.append(new_project)
                    print(f"已建立並規劃新專案：'{random_inspiration}' [{random_category}]！")

        elif choice == '6':
            print("\n(此功能仍在規劃中，敬請期待！)")
        
        elif choice == '7':
            # --- 修改：在離開前，儲存遊戲 ---
            save_game(my_city, projects)
            print("感謝你的辛勤工作，建築師！期待下次再見。")
            break
        else:
            print("無效的輸入，請重新選擇。")

if __name__ == "__main__":
    main()