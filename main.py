# main.py

from city import City
from project import Project

def main():
    """
    「成就之城」主程式
    """
    print("--- 歡迎來到「成就之城」，偉大的建築師！ ---")
    city_name = input("首先，請為你的城市命名: ")
    my_city = City(city_name)
    print(f"美好的開始！'{my_city.name}' 期待你的建設。")

    projects = [] # 用來存放所有進行中的專案

    while True:
        print("\n=== 建築師工作台 ===")
        print("1. 建立新專案 (開始規劃新建築)")
        print("2. 為專案新增任務 (準備積木)")
        print("3. 完成任務 (開始堆砌積木)")
        print("4. 查看所有專案進度")
        print("5. 查看我的城市")
        print("6. 離開")
        
        choice = input("請選擇你的下一步行動 (1-6): ")

        if choice == '1':
            project_name = input("請輸入新專案的名稱: ")
            new_project = Project(project_name)
            projects.append(new_project)
            print(f"專案 '{project_name}' 已建立！")

        elif choice == '2':
            if not projects:
                print("目前沒有任何專案，請先建立一個。")
                continue
            for i, p in enumerate(projects):
                print(f"{i+1}. {p.name}")
            p_choice = int(input("請選擇要新增任務的專案編號: ")) - 1
            if 0 <= p_choice < len(projects):
                task_desc = input("請輸入任務描述 (積木內容): ")
                projects[p_choice].add_task(task_desc)
            else:
                print("無效的選擇。")

        elif choice == '3':
            # 邏輯與 choice '2' 相似，先選擇專案
            if not projects:
                print("目前沒有任何專案。")
                continue
            for i, p in enumerate(projects):
                print(f"{i+1}. {p.name}")
            p_choice = int(input("請選擇要完成任務的專案編號: ")) - 1
            
            if 0 <= p_choice < len(projects):
                chosen_project = projects[p_choice]
                # 選擇該專案中未完成的任務
                pending_tasks = [t for t in chosen_project.tasks if t.status == 'pending']
                if not pending_tasks:
                    print("這個專案的所有任務都已完成！")
                    continue
                
                for i, t in enumerate(pending_tasks):
                    print(f"{i+1}. {t.description}")
                t_choice = int(input("請選擇要完成的任務編號: ")) - 1
                
                if 0 <= t_choice < len(pending_tasks):
                    task_to_complete = pending_tasks[t_choice]
                    task_to_complete.complete()

                    # ** 核心檢查機制 **
                    if chosen_project.is_complete():
                        my_city.add_building(chosen_project.name)
                        # 從進行中專案列表移除已完成的專案
                        projects.pop(p_choice)
                else:
                    print("無效的任務選擇。")
            else:
                print("無效的專案選擇。")

        elif choice == '4':
            if not projects:
                print("目前沒有任何進行中的專案。")
            else:
                for project in projects:
                    print(project) # 利用我們寫好的 __str__ 方法

        elif choice == '5':
            my_city.display()

        elif choice == '6':
            print("感謝你的辛勤工作，建築師！期待下次再見。")
            break
            
        else:
            print("無效的輸入，請重新選擇。")

# 確保這個檔案被直接執行時，才運行 main()
if __name__ == "__main__":
    main()