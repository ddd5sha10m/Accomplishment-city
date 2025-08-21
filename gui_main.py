# gui_main.py

import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button, Entry, OptionMenu, StringVar, Checkbutton, BooleanVar
from view import CityView
from main1 import load_game, save_game, CATEGORIES, LEVEL_CONFIG, check_for_level_up, check_for_milestones
from project import Project

class Game:
    """管理遊戲狀態"""
    def __init__(self):
        self.city, self.projects = load_game()
        if self.city is None:
            messagebox.showerror("錯誤", "找不到存檔檔案 'savegame.dat'。請先運行文字版 main.py 建立一個城市並儲存。")
            exit()

    def save(self):
        save_game(self.city, self.projects)

class AppController:
    """應用程式的總指揮官 (Controller)"""
    def __init__(self, game: Game, view: CityView):
        self.game = game
        self.view = view
        self.placement_mode = False
        self.project_to_place = None

        self._bind_buttons()
        self.view.map_canvas.bind("<Button-1>", self.on_map_click)
        self.update_view()

    def _bind_buttons(self):
        """將 View 中的按鈕與 Controller 的方法連結起來"""
        self.view.btn_create_project.config(command=self.prompt_create_project)
        self.view.btn_complete_task.config(command=self.prompt_select_project_to_work_on)

    def update_view(self):
        """全面更新所有視覺元件"""
        self.view.draw_map(self.game.city.map)
        wip_limit = LEVEL_CONFIG.get(self.game.city.architect_level, {}).get('wip_limit', 2)
        self.view.update_header(self.game.city.architect_level, len(self.game.projects), wip_limit, self.game.city.total_vitality)

    def prompt_create_project(self):
        # (此方法與上一版完全相同，不變)
        wip_limit = LEVEL_CONFIG.get(self.game.city.architect_level, {}).get('wip_limit', 2)
        if len(self.game.projects) >= wip_limit:
            messagebox.showinfo("提示", "你的工作台已經滿了！請先完成一項專案來騰出空間。")
            return
        dialog = Toplevel(self.view.root)
        dialog.title("建立新專案")
        Label(dialog, text="選擇分類:").pack(padx=10, pady=5)
        cat_list = list(CATEGORIES.keys())
        category_var = StringVar(dialog); category_var.set(cat_list[0])
        OptionMenu(dialog, category_var, *cat_list).pack(padx=10, pady=5)
        Label(dialog, text="專案名稱:").pack(padx=10, pady=5)
        name_entry = Entry(dialog, width=30); name_entry.pack(padx=10, pady=5)
        def on_submit():
            name = name_entry.get()
            category = category_var.get()
            if not name:
                messagebox.showerror("錯誤", "專案名稱不可為空！", parent=dialog)
                return
            category_info = CATEGORIES[category]
            self.project_to_place = Project(name, category, category_info['size'])
            self.project_to_place.vitality_points = category_info['points']
            self.placement_mode = True
            self.view.show_message(f"進入放置模式！\n請在地圖上點擊左上角，為 '{name}' ({category_info['size'][0]}x{category_info['size'][1]}) 規劃工地。")
            dialog.destroy()
        Button(dialog, text="下一步：選擇地點", command=on_submit).pack(padx=10, pady=10)

    def on_map_click(self, event):
        # (此方法與上一版完全相同，不變)
        if not self.placement_mode: return
        grid_x = event.x // self.view.cell_size
        grid_y = event.y // self.view.cell_size
        if self.game.city.start_project_site(self.project_to_place, grid_x, grid_y):
            self.game.projects.append(self.project_to_place)
            self.view.show_message(f"專案 '{self.project_to_place.name}' 已在 ({grid_x},{grid_y}) 開工！")
            self.placement_mode = False
            self.project_to_place = None
            self.update_view()
        else:
            messagebox.showerror("放置失敗", "該地點無效或已被佔用，請重新選擇。")

    def prompt_select_project_to_work_on(self):
        # (此方法與上一版完全相同，不變，只是 Listbox 被移除了)
        if not self.game.projects:
            messagebox.showinfo("提示", "目前沒有任何進行中的專案。")
            return
        dialog = Toplevel(self.view.root)
        dialog.title("選擇專案")
        Label(dialog, text="請選擇要推進工期的專案:").pack(padx=10, pady=10)
        
        # 使用 OptionMenu (下拉選單) 來選擇專案
        project_names = [p.name for p in self.game.projects]
        project_var = StringVar(dialog)
        if project_names:
            project_var.set(project_names[0])
        OptionMenu(dialog, project_var, *project_names).pack(padx=10, pady=10)

        def on_select():
            selected_name = project_var.get()
            # 根據選擇的名字找到對應的專案物件和索引
            chosen_project = None
            project_index = -1
            for i, p in enumerate(self.game.projects):
                if p.name == selected_name:
                    chosen_project = p
                    project_index = i
                    break
            
            if chosen_project:
                dialog.destroy()
                self.prompt_select_task_to_complete(chosen_project, project_index)

        Button(dialog, text="選擇任務", command=on_select).pack(padx=10, pady=10)

    # --- 核心修改：將「完成任務」的第二步改為勾選模式 ---
    def prompt_select_task_to_complete(self, chosen_project, project_index):
        """彈出視窗，用複選框顯示待辦任務"""
        pending_tasks = [t for t in chosen_project.tasks if t.status == 'pending']

        if not pending_tasks:
            messagebox.showinfo("完成", f"專案 '{chosen_project.name}' 的所有任務都已完成！", parent=self.view.root)
            return

        dialog = Toplevel(self.view.root)
        dialog.title(f"完成任務: {chosen_project.name}")

        Label(dialog, text="請勾選所有已完成的任務 (積木):").pack(padx=10, pady=10)

        # 創建一個列表來存放 BooleanVar 和對應的 task 物件
        task_vars = []
        for task in pending_tasks:
            var = BooleanVar()
            cb = Checkbutton(dialog, text=task.description, variable=var, anchor='w')
            cb.pack(padx=20, pady=2, fill='x')
            task_vars.append((var, task)) # 將變數和任務本身綁定在一起

        def on_complete():
            completed_count = 0
            for var, task in task_vars:
                if var.get(): # 檢查核取方塊是否被勾選
                    task.complete()
                    completed_count += 1
            
            if completed_count > 0:
                chosen_project.touch() # 只要有進度，就更新營火
                self.view.show_message(f"完成了 {completed_count} 個任務！")
            
            # 在所有勾選的任務都處理完畢後，再檢查專案是否竣工
            if chosen_project.is_complete():
                self.view.show_message(f"專案 '{chosen_project.name}' 即將完工！")
                self.game.city.complete_project_site(chosen_project)
                self.game.projects.pop(project_index)
                check_for_level_up(self.game.city)
                check_for_milestones(self.game.city)
            
            dialog.destroy()
            self.update_view() # 無論如何都要刷新畫面

        Button(dialog, text="完成勾選的任務", command=on_complete).pack(padx=10, pady=10)

def main():
    root = tk.Tk()
    game = Game()
    view = CityView(root)
    controller = AppController(game, view)
    
    def on_closing():
        if messagebox.askokcancel("退出", "確定要退出並儲存進度嗎？"):
            controller.game.save()
            root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

if __name__ == "__main__":
    main()