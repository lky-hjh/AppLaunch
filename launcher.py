"""
🚀 一键软件启动器 v2 — 现代 Fluent 风格
功能：
  - 可视化增删改软件列表
  - 一键全部启动 / 单独启动
  - 搜索过滤
  - 配置自动保存到 apps.json
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import subprocess
import os
import sys
import threading
import webbrowser

# ─── 路径 ──────────────────────────────────────────────────────────────────
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apps.json")

# ─── 调色板 ────────────────────────────────────────────────────────────────
# 主色
BG_DEEP     = "#0f0f1a"       # 最底层背景
BG_SURFACE  = "#1a1a2e"       # 表面卡片背景
BG_CARD     = "#222240"       # 列表卡片
BG_HOVER    = "#2a2a50"       # 卡片悬停
ACCENT      = "#7c6af7"       # 紫色主色调
ACCENT_LIGHT= "#9d8dfa"
ACCENT2     = "#4a9eff"       # 蓝色辅助
SUCCESS     = "#34d399"       # 绿色
DANGER      = "#f87171"       # 红色
TEXT_PRIMARY = "#f0f0ff"
TEXT_SECONDARY = "#8888aa"
TEXT_MUTED  = "#555577"
BORDER      = "#2e2e50"

# 字体
FONT       = ("Microsoft YaHei UI", 10)
FONT_SM    = ("Microsoft YaHei UI", 9)
FONT_XS    = ("Microsoft YaHei UI", 8)
FONT_B     = ("Microsoft YaHei UI", 10, "bold")
FONT_TITLE = ("Microsoft YaHei UI", 14, "bold")
FONT_MONO  = ("Consolas", 9)

# 卡片图标颜色池
ICON_COLORS = [
    "#7c6af7", "#4a9eff", "#34d399", "#fbbf24", "#f87171",
    "#a78bfa", "#60a5fa", "#2dd4bf", "#f472b6", "#fb923c",
]


# ─── 工具函数 ──────────────────────────────────────────────────────────────
def load_apps():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def save_apps(apps):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(apps, f, ensure_ascii=False, indent=2)


def launch_app(path):
    """启动单个程序，成功返回 True，失败返回错误字符串"""
    # 相对路径解析为脚本所在目录
    if not os.path.isabs(path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, path)
    try:
        ext = os.path.splitext(path)[1].lower()
        if ext in (".bat", ".cmd"):
            subprocess.Popen(path, shell=True)
        elif ext == ".ps1":
            subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-File", path])
        elif ext == ".py":
            subprocess.Popen([sys.executable, path])
        elif path.startswith("http://") or path.startswith("https://"):
            webbrowser.open(path)
        else:
            os.startfile(path)
        return True
    except Exception as e:
        return str(e)


def get_initials(name):
    """取软件名首字母（英文取首字母，中文取前两个字）"""
    name = name.strip()
    if not name:
        return "?"
    en = ""
    cn = ""
    for ch in name:
        if ord(ch) < 128:
            en += ch
        else:
            cn += ch
    if cn:
        return cn[:2]
    return en[:2].upper() if en else "?"


def darken(hex_color, amount=25):
    """颜色加深"""
    try:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        r, g, b = max(0, r - amount), max(0, g - amount), max(0, b - amount)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


def lighten(hex_color, amount=25):
    """颜色变亮"""
    try:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        r, g, b = min(255, r + amount), min(255, g + amount), min(255, b + amount)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color


# ─── 自定义组件 ────────────────────────────────────────────────────────────
class RoundButton(tk.Canvas):
    """圆角按钮 (Canvas 绘制)"""
    def __init__(self, parent, text, command=None, bg=ACCENT, fg="white",
                 font=FONT, width=None, height=32, radius=8, **kwargs):
        super().__init__(parent, bg=BG_DEEP, highlightthickness=0, **kwargs)
        self.command = command
        self.bg = bg
        self.fg = fg
        self.font = font
        self.radius = radius
        self._disabled = False

        # 测量文字宽度
        self.text = text
        self.btn_width = width if width else len(text) * 9 + 24
        self.btn_height = height

        self.configure(width=self.btn_width, height=self.btn_height)
        self._draw(self.bg)

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _draw(self, color, outline=None):
        self.delete("all")
        r = self.radius
        w, h = self.btn_width, self.btn_height
        # 圆角矩形
        self.create_rounded_rect(1, 1, w - 1, h - 1, r, fill=color,
                                 outline=outline or color, width=1)
        # 文字
        self.create_text(w // 2, h // 2, text=self.text, fill=self.fg,
                         font=self.font, anchor="center")

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_enter(self, e):
        if not self._disabled:
            self._draw(lighten(self.bg))

    def _on_leave(self, e):
        if not self._disabled:
            self._draw(self.bg)

    def _on_click(self, e):
        if self.command and not self._disabled:
            self._draw(darken(self.bg))
            self.after(80, lambda: self._draw(self.bg))
            self.command()

    def set_disabled(self, disabled):
        self._disabled = disabled
        if disabled:
            self._draw("#333355", outline="#333355")
        else:
            self._draw(self.bg)


class IconCircle(tk.Canvas):
    """彩色圆形图标 (带首字母)"""
    def __init__(self, parent, text, color, size=40, **kwargs):
        super().__init__(parent, bg=BG_DEEP, highlightthickness=0,
                         width=size, height=size, **kwargs)
        self.size = size
        r = size // 2
        self.create_oval(2, 2, size - 2, size - 2, fill=color, outline="")
        self.create_text(r + 1, r + 1, text=get_initials(text),
                         fill="white", font=("Microsoft YaHei UI", size // 3, "bold"),
                         anchor="center")


# ─── 添加 / 编辑对话框 ──────────────────────────────────────────────────────
class AppDialog(tk.Toplevel):
    def __init__(self, parent, title="添加软件", data=None):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG_DEEP)
        self.resizable(False, False)
        self.result = None

        self.transient(parent)
        self.grab_set()

        w, h = 460, 260
        px, py = parent.winfo_rootx(), parent.winfo_rooty()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        self.geometry(f"{w}x{h}+{px + (pw - w) // 2}+{py + (ph - h) // 2}")

        # 控件构建完后必须 update 让窗口可见，否则 grab 会卡死
        self._build(data)
        self.update_idletasks()
        self.name_e.focus_set()
        self.wait_window()

    def _build(self, data):
        body = tk.Frame(self, bg=BG_DEEP, padx=24, pady=20)
        body.pack(fill="both", expand=True)

        # 名称行
        tk.Label(body, text="软件名称", bg=BG_DEEP, fg=TEXT_SECONDARY,
                 font=FONT_XS, anchor="w").pack(fill="x")
        self.name_var = tk.StringVar(value=data["name"] if data else "")
        self.name_e = tk.Entry(body, textvariable=self.name_var,
                                bg=BG_SURFACE, fg=TEXT_PRIMARY,
                                insertbackground=TEXT_PRIMARY, relief="flat",
                                font=FONT, bd=0, highlightthickness=1,
                                highlightbackground=BORDER, highlightcolor=ACCENT)
        self.name_e.pack(fill="x", pady=(2, 12), ipady=5, ipadx=6)

        # 路径行
        tk.Label(body, text="程序路径", bg=BG_DEEP, fg=TEXT_SECONDARY,
                 font=FONT_XS, anchor="w").pack(fill="x")
        path_frame = tk.Frame(body, bg=BG_DEEP)
        path_frame.pack(fill="x", pady=(2, 4))

        self.path_var = tk.StringVar(value=data["path"] if data else "")
        self.path_e = tk.Entry(path_frame, textvariable=self.path_var,
                                bg=BG_SURFACE, fg=TEXT_PRIMARY,
                                insertbackground=TEXT_PRIMARY, relief="flat",
                                font=FONT_MONO, bd=0, highlightthickness=1,
                                highlightbackground=BORDER, highlightcolor=ACCENT)
        self.path_e.pack(side="left", fill="x", expand=True, ipady=5, ipadx=6)

        browse_btn = RoundButton(path_frame, "浏览…", self._browse,
                                 ACCENT2, "white", FONT_SM, width=60, height=28, radius=6)
        browse_btn.pack(side="left", padx=(6, 0))

        # 提示
        tk.Label(body, text="支持 .exe / .bat / .lnk / .ps1 / .py / 网址",
                 bg=BG_DEEP, fg=TEXT_MUTED, font=FONT_XS).pack(anchor="w", pady=(0, 16))

        # 按钮
        btn_row = tk.Frame(body, bg=BG_DEEP)
        btn_row.pack(fill="x", pady=(4, 0))

        cancel_btn = tk.Button(btn_row, text="取消", command=self.destroy,
                                bg=BG_SURFACE, fg=TEXT_SECONDARY, relief="flat",
                                font=FONT, width=10, cursor="hand2", bd=0,
                                activebackground=BG_HOVER, activeforeground=TEXT_PRIMARY,
                                highlightthickness=0)
        cancel_btn.pack(side="right", padx=(6, 0), ipady=4)

        ok_btn = tk.Button(btn_row, text="确定", command=self._ok,
                            bg=ACCENT, fg="white", relief="flat",
                            font=FONT_B, width=10, cursor="hand2", bd=0,
                            activebackground=ACCENT_LIGHT, activeforeground="white",
                            highlightthickness=0)
        ok_btn.pack(side="right", ipady=4)

    def _browse(self):
        path = filedialog.askopenfilename(
            title="选择程序",
            filetypes=[
                ("可执行文件", "*.exe *.bat *.cmd *.lnk *.ps1 *.py"),
                ("所有文件", "*.*"),
            ]
        )
        if path:
            self.path_var.set(path)
            if not self.name_var.get():
                self.name_var.set(os.path.splitext(os.path.basename(path))[0])

    def _ok(self):
        name = self.name_var.get().strip()
        path = self.path_var.get().strip()
        if not name:
            messagebox.showwarning("提示", "请填写软件名称", parent=self)
            return
        if not path:
            messagebox.showwarning("提示", "请填写程序路径", parent=self)
            return
        self.result = {"name": name, "path": path}
        self.destroy()


# ─── 主窗口 ────────────────────────────────────────────────────────────────
class LauncherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("一键软件启动器")
        self.configure(bg=BG_DEEP)
        self.geometry("720x560")
        self.minsize(620, 420)

        # 数据
        self.apps = load_apps()
        self.filtered_apps = self.apps[:]
        self._idx_map = {}          # filtered_index -> original_index
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._filter())

        # 构建 UI
        self._build_ui()
        self._refresh_list()

    # ── 界面构建 ──────────────────────────────────────────────────────────
    def _build_ui(self):
        # ═══ 顶部导航栏 ═══
        nav = tk.Frame(self, bg=BG_SURFACE, height=52)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        # 标题 + logo
        logo_frame = tk.Frame(nav, bg=BG_SURFACE)
        logo_frame.pack(side="left", padx=18)
        tk.Label(logo_frame, text="🚀", bg=BG_SURFACE, fg=ACCENT,
                 font=("Segoe UI Emoji", 16)).pack(side="left")
        tk.Label(logo_frame, text="  一键启动器", bg=BG_SURFACE,
                 fg=TEXT_PRIMARY, font=FONT_TITLE).pack(side="left")

        # 右侧添加按钮
        top_btn_frame = tk.Frame(nav, bg=BG_SURFACE)
        top_btn_frame.pack(side="right", padx=14)

        add_btn = RoundButton(top_btn_frame, "＋ 添加软件", self._add_app,
                               ACCENT, "white", FONT_B, width=110, height=30, radius=7)
        add_btn.pack(side="right")

        # ═══ 搜索栏 ═══
        search_frame = tk.Frame(self, bg=BG_DEEP, height=48)
        search_frame.pack(fill="x")
        search_bar = tk.Frame(search_frame, bg=BG_SURFACE, highlightthickness=1,
                               highlightbackground=BORDER, highlightcolor=ACCENT)
        search_bar.pack(fill="x", padx=18, pady=(10, 0), ipady=3)

        tk.Label(search_bar, text="🔍", bg=BG_SURFACE, fg=TEXT_SECONDARY,
                 font=("Segoe UI Emoji", 11)).pack(side="left", padx=(10, 4))
        search_entry = tk.Entry(search_bar, textvariable=self.search_var,
                                 bg=BG_SURFACE, fg=TEXT_PRIMARY,
                                 insertbackground=TEXT_PRIMARY, relief="flat",
                                 font=FONT, bd=0,
                                 highlightthickness=0)
        search_entry.pack(side="left", fill="x", expand=True, ipady=3)
        search_entry.bind("<Escape>", lambda e: self.search_var.set(""))

        # 清除按钮
        clear_btn = tk.Label(search_bar, text=" ✕ ", bg=BG_SURFACE, fg=TEXT_MUTED,
                              font=FONT_XS, cursor="hand2")
        clear_btn.pack(side="right", padx=8)
        clear_btn.bind("<Button-1>", lambda e: self.search_var.set(""))

        # ═══ 列表区域 ═══
        list_outer = tk.Frame(self, bg=BG_DEEP)
        list_outer.pack(fill="both", expand=True, padx=18, pady=(10, 0))

        # 列标题
        col_header = tk.Frame(list_outer, bg=BG_SURFACE)
        col_header.pack(fill="x")

        tk.Label(col_header, text="软件", bg=BG_SURFACE, fg=TEXT_MUTED,
                 font=FONT_XS, width=6).pack(side="left", padx=(16, 0), pady=8)
        tk.Label(col_header, text="名称", bg=BG_SURFACE, fg=TEXT_MUTED,
                 font=FONT_XS, width=14).pack(side="left", pady=8)
        tk.Label(col_header, text="路径", bg=BG_SURFACE, fg=TEXT_MUTED,
                 font=FONT_XS).pack(side="left", padx=8, pady=8, fill="x", expand=True)
        tk.Label(col_header, text="操作", bg=BG_SURFACE, fg=TEXT_MUTED,
                 font=FONT_XS, width=16).pack(side="right", padx=16, pady=8)

        # Canvas + 滚动
        canvas_frame = tk.Frame(list_outer, bg=BG_DEEP)
        canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg=BG_DEEP, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=BG_DEEP)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 鼠标滚轮
        def _on_mousewheel(e):
            self.canvas.yview_scroll(-1 * (e.delta // 120), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # ═══ 底部状态栏 ═══
        footer = tk.Frame(self, bg=BG_SURFACE, height=48)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        self.status_label = tk.Label(footer, text="就绪", bg=BG_SURFACE,
                                      fg=TEXT_SECONDARY, font=FONT_SM)
        self.status_label.pack(side="left", padx=18)

        # 一键启动按钮
        self.launch_all_btn = RoundButton(footer, "⚡ 一键全部启动", self._launch_all,
                                           SUCCESS, "white", FONT_B, width=140,
                                           height=32, radius=8)
        self.launch_all_btn.pack(side="right", padx=16)

    # ── 搜索过滤 ──────────────────────────────────────────────────────────
    def _filter(self):
        keyword = self.search_var.get().strip().lower()
        if not keyword:
            self.filtered_apps = self.apps[:]
        else:
            self.filtered_apps = [
                a for a in self.apps
                if keyword in a["name"].lower() or keyword in a["path"].lower()
            ]
        self._refresh_list()

    # ── 刷新列表 ──────────────────────────────────────────────────────────
    def _refresh_list(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        shown = self.filtered_apps
        # 重建索引映射
        self._idx_map = {}
        for fi, app in enumerate(shown):
            for oi, a in enumerate(self.apps):
                if a["name"] == app["name"] and a["path"] == app["path"]:
                    self._idx_map[fi] = oi
                    break

        if not shown:
            msg = "没有匹配的软件" if self.search_var.get().strip() else "暂无软件，点击右上角「＋ 添加软件」开始配置"
            empty = tk.Frame(self.scroll_frame, bg=BG_DEEP)
            empty.pack(fill="both", expand=True, pady=60)
            tk.Label(empty, text="📭", bg=BG_DEEP, fg=TEXT_MUTED,
                     font=("Segoe UI Emoji", 32)).pack()
            tk.Label(empty, text=msg, bg=BG_DEEP, fg=TEXT_SECONDARY,
                     font=FONT).pack(pady=(8, 0))
        else:
            for idx, app in enumerate(shown):
                self._build_card(idx, app)

        total = len(self.apps)
        shown_n = len(shown)
        if shown_n < total:
            self.status_label.config(text=f"已筛选 {shown_n}/{total} 个软件")
        else:
            self.status_label.config(text=f"共 {total} 个软件")

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # ── 构建卡片行 ────────────────────────────────────────────────────────
    def _build_card(self, idx, app):
        color = ICON_COLORS[idx % len(ICON_COLORS)]
        card = tk.Frame(self.scroll_frame, bg=BG_CARD)
        card.pack(fill="x", pady=2)

        # 悬停效果
        def on_enter(e):
            card.config(bg=BG_HOVER)
            for child in card.winfo_children():
                try:
                    child.config(bg=BG_HOVER)
                except Exception:
                    pass
        def on_leave(e):
            card.config(bg=BG_CARD)
            for child in card.winfo_children():
                try:
                    child.config(bg=BG_CARD)
                except Exception:
                    pass
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        # 图标
        icon = IconCircle(card, app["name"], color, size=34)
        icon.pack(side="left", padx=(12, 6), pady=8)

        # 名称
        tk.Label(card, text=app["name"], bg=BG_CARD, fg=TEXT_PRIMARY,
                 font=FONT_B, width=14, anchor="w").pack(side="left", padx=(4, 8), pady=8)

        # 路径
        path_text = app["path"]
        if len(path_text) > 50:
            path_text = "…" + path_text[-48:]
        tk.Label(card, text=path_text, bg=BG_CARD, fg=TEXT_SECONDARY,
                 font=FONT_MONO, anchor="w").pack(side="left", padx=4,
                                                    pady=8, fill="x", expand=True)

        # 操作按钮
        btn_area = tk.Frame(card, bg=BG_CARD)
        btn_area.pack(side="right", padx=8)

        # 启动按钮
        launch_btn = RoundButton(btn_area, "▶ 启动",
                                  lambda i=idx: self._launch_one(i),
                                  ACCENT2, "white", FONT_SM, width=64, height=26, radius=5)
        launch_btn.pack(side="left", padx=2)

        # 编辑按钮
        edit_btn = RoundButton(btn_area, "✎",
                                lambda i=idx: self._edit_app(i),
                                BG_HOVER, TEXT_SECONDARY, FONT_SM, width=28, height=26, radius=5)
        edit_btn.pack(side="left", padx=1)

        # 删除按钮
        del_btn = RoundButton(btn_area, "✕",
                               lambda i=idx: self._delete_app(i),
                               DANGER, "white", FONT_XS, width=28, height=26, radius=5)
        del_btn.pack(side="left", padx=1)

        # ── 操作方法 ──────────────────────────────────────────────────────────
    def _add_app(self):
        dlg = AppDialog(self, title="添加软件")
        if dlg.result:
            self.apps.append(dlg.result)
            save_apps(self.apps)
            self._filter()

    def _edit_app(self, idx):
        real_idx = self._real_index(idx)
        if real_idx is None:
            return
        dlg = AppDialog(self, title="编辑软件", data=self.apps[real_idx])
        if dlg.result:
            self.apps[real_idx] = dlg.result
            save_apps(self.apps)
            self._filter()

    def _delete_app(self, idx):
        real_idx = self._real_index(idx)
        if real_idx is None:
            return
        name = self.apps[real_idx]["name"]
        confirm = messagebox.askyesno("确认删除", f"确定要删除「{name}」吗？", parent=self)
        if confirm:
            self.apps.pop(real_idx)
            save_apps(self.apps)
            self._filter()

    def _real_index(self, filtered_idx):
        """将过滤列表索引映射为原始 apps 列表索引"""
        return self._idx_map.get(filtered_idx, None)

    def _launch_one(self, idx):
        real_idx = self._real_index(idx)
        if real_idx is None:
            return
        app = self.apps[real_idx]
        result = launch_app(app["path"])
        if result is True:
            self._toast(f"✅ 已启动：{app['name']}", SUCCESS)
        else:
            messagebox.showerror("启动失败",
                                 f"无法启动「{app['name']}」\n\n{result}", parent=self)

    def _launch_all(self):
        if not self.apps:
            messagebox.showinfo("提示", "还没有添加任何软件，请先点击「添加软件」", parent=self)
            return

        # 禁用按钮防重复
        self.launch_all_btn.set_disabled(True)
        self.status_label.config(text=f"🚀 正在启动 {len(self.apps)} 个软件…")

        def do_launch():
            results = []
            for app in self.apps:
                r = launch_app(app["path"])
                results.append((app["name"], r))

            self.after(0, lambda: self._on_launch_done(results))

        thread = threading.Thread(target=do_launch, daemon=True)
        thread.start()

    def _on_launch_done(self, results):
        self.launch_all_btn.set_disabled(False)
        failed = [n for n, r in results if r is not True]

        if not failed:
            self._toast(f"✅ 已成功启动全部 {len(results)} 个软件！", SUCCESS)
            self.status_label.config(text=f"共 {len(self.apps)} 个软件")
        else:
            msg = "以下软件未能成功启动：\n\n" + "\n".join(failed)
            messagebox.showerror("部分启动失败", msg, parent=self)
            self.status_label.config(text=f"失败 {len(failed)}/{len(results)} 个")

    def _toast(self, msg, color=SUCCESS):
        """顶部滑入提示条"""
        toast = tk.Frame(self, bg=color)
        toast.place(x=0, y=50, relwidth=1, height=36)
        tk.Label(toast, text="  " + msg, bg=color, fg="white",
                 font=FONT_B).pack(side="left", padx=14, pady=4)
        self.after(3000, toast.destroy)


# ─── 入口 ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = LauncherApp()
    app.mainloop()
