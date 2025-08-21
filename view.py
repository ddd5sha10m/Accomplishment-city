# view.py

import tkinter as tk
from tkinter import Canvas, Frame, Label

COLOR_MAPPING = {
    ".": "#C2B280", "#": "#A9A9A9", "L": "#87CEEB", "S": "#FFD700",
    "H": "#90EE90", "C": "#FFA07A", "E": "#DDA0DD",
}

class CityView:
    def __init__(self, root):
        self.root = root
        self.root.title("成就之城")
        self.root.geometry("1000x720")
        self.cell_size = 32
        self._setup_layout()

    def _setup_layout(self):
        map_frame = Frame(self.root)
        map_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        sidebar_frame = Frame(self.root, width=250)
        sidebar_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # --- 修改：將元件儲存為 self 的屬性，方便外部存取 ---
        self.map_canvas = Canvas(map_frame, bg="#F5F5DC")
        self.map_canvas.pack(fill="both", expand=True)

        self.header_label = Label(sidebar_frame, text="", wraplength=240, justify="left", font=("Arial", 12, "bold"))
        self.header_label.pack(pady=5, fill="x")

        self.message_label = Label(sidebar_frame, text="歡迎來到成就之城！", wraplength=240, justify="left", font=("Arial", 11))
        self.message_label.pack(pady=10, fill="x")

        controls_frame = Frame(sidebar_frame)
        controls_frame.pack(pady=10, fill="x")
        
        # --- 修改：將按鈕也儲存為 self 的屬性 ---
        self.btn_create_project = self._create_button(controls_frame, "建立新專案 (規劃工地)")
        self.btn_complete_task = self._create_button(controls_frame, "完成任務 (推進工期)")
        self.btn_view_projects = self._create_button(controls_frame, "查看所有專案進度")
        self.btn_draw_inspiration = self._create_button(controls_frame, "抽取每日靈感")

    def _create_button(self, parent, text):
        """一個建立按鈕的輔助函式，父元件作為參數傳入"""
        btn = tk.Button(parent, text=text, font=("Arial", 11))
        btn.pack(pady=5, fill="x")
        return btn

    def draw_map(self, city_map):
        self.map_canvas.delete("all")
        for y, row in enumerate(city_map.grid):
            for x, cell_char in enumerate(row):
                x1, y1 = x * self.cell_size, y * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color_code = cell_char if cell_char in COLOR_MAPPING else city_map.grid[y][x][0].upper()
                color = COLOR_MAPPING.get(color_code, "white")
                self.map_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    # --- 新增：更新頂部狀態欄的方法 ---
    def update_header(self, level, project_count, wip_limit, vitality):
        header_text = f"等級: {level} | 專案: {project_count}/{wip_limit} | 活力: {vitality}"
        self.header_label.config(text=header_text)

    # --- 新增：更新訊息欄的方法 ---
    def show_message(self, message):
        self.message_label.config(text=message)