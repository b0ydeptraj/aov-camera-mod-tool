#!/usr/bin/env python3
import contextlib
import io
import queue
import sys
import threading
from pathlib import Path
from tkinter import BooleanVar, Canvas, StringVar, Text, Tk, filedialog, messagebox
from tkinter import ttk

from patch_aov_camera import patch_package, resolve_common_actions


APP_DIR = Path(__file__).resolve().parent


def resource_path(name: str) -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / name
    return APP_DIR / name


DEFAULT_DICT = resource_path("zstd_dict.bin")
CAMERA_LEVELS = {
    "10%": 0.75,
    "20%": 1.5,
    "40%": 3.0,
}


def ui_font(size: int, weight: str | None = None) -> str:
    suffix = f" {weight}" if weight else ""
    return f"{{Segoe UI}} {size}{suffix}"

COLORS = {
    "bg": "#edf1f7",
    "surface": "#ffffff",
    "surface_soft": "#f8fafc",
    "sidebar": "#0f172a",
    "sidebar_2": "#172033",
    "text": "#111827",
    "muted": "#64748b",
    "line": "#d7deea",
    "accent": "#0f766e",
    "accent_hover": "#12877e",
    "accent_soft": "#d9f5f1",
    "danger": "#b42318",
    "terminal": "#0b1220",
    "terminal_text": "#dbeafe",
}


class CameraPatchGui:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Mod Camera Liên Quân")
        self.root.geometry("1080x720")
        self.root.minsize(820, 540)
        self.root.option_add("*Font", ui_font(10))

        self.input_path = StringVar()
        self.dict_path = StringVar(value=str(DEFAULT_DICT))
        self.output_path = StringVar()
        self.camera_level = StringVar(value="20%")
        self.make_backup = BooleanVar(value=False)
        self.status_text = StringVar(value="Sẵn sàng")
        self.side_status_title = StringVar(value="Sẵn sàng")
        self.side_status_detail = StringVar(value="Chọn file để bắt đầu")
        self.queue: queue.Queue[tuple[str, str]] = queue.Queue()
        self.busy = False
        self.pulse_pos = 0
        self.last_result_path = ""

        self._configure_style()
        self._build_ui()
        self.root.after(100, self._poll_queue)

    def run(self) -> None:
        self.root.mainloop()

    def _configure_style(self) -> None:
        self.root.configure(bg=COLORS["bg"])
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure(".", borderwidth=0, focuscolor=COLORS["accent"])
        style.configure("App.TFrame", background=COLORS["bg"])
        style.configure("Main.TFrame", background=COLORS["bg"])
        style.configure("Sidebar.TFrame", background=COLORS["sidebar"])
        style.configure("SidebarPanel.TFrame", background=COLORS["sidebar_2"])
        style.configure("Card.TFrame", background=COLORS["surface"])
        style.configure("CardSoft.TFrame", background=COLORS["surface_soft"])
        style.configure("Action.TFrame", background=COLORS["surface"])
        style.configure("Chip.TFrame", background=COLORS["accent_soft"])

        style.configure("BrandSmall.TLabel", background=COLORS["sidebar"], foreground="#7dd3fc", font=ui_font(9, "bold"))
        style.configure("BrandTitle.TLabel", background=COLORS["sidebar"], foreground="#f8fafc", font=ui_font(25, "bold"))
        style.configure("SidebarMuted.TLabel", background=COLORS["sidebar"], foreground="#94a3b8", font=ui_font(9))
        style.configure("SidebarTitle.TLabel", background=COLORS["sidebar"], foreground="#e2e8f0", font=ui_font(10, "bold"))
        style.configure("SidebarStepNo.TLabel", background=COLORS["accent"], foreground="#ffffff", font=ui_font(9, "bold"), padding=(8, 4))
        style.configure("SidebarStepTitle.TLabel", background=COLORS["sidebar"], foreground="#f8fafc", font=ui_font(10, "bold"))
        style.configure("SidebarStepText.TLabel", background=COLORS["sidebar"], foreground="#94a3b8", font=ui_font(9))
        style.configure("SidebarStatusTitle.TLabel", background=COLORS["sidebar_2"], foreground="#f8fafc", font=ui_font(10, "bold"))
        style.configure("SidebarStatusText.TLabel", background=COLORS["sidebar_2"], foreground="#cbd5e1", font=ui_font(9))

        style.configure("PageTitle.TLabel", background=COLORS["bg"], foreground=COLORS["text"], font=ui_font(24, "bold"))
        style.configure("PageSub.TLabel", background=COLORS["bg"], foreground=COLORS["muted"], font=ui_font(10))
        style.configure("Chip.TLabel", background=COLORS["accent_soft"], foreground=COLORS["accent"], font=ui_font(10, "bold"))
        style.configure("CardTitle.TLabel", background=COLORS["surface"], foreground=COLORS["text"], font=ui_font(13, "bold"))
        style.configure("CardDesc.TLabel", background=COLORS["surface"], foreground=COLORS["muted"], font=ui_font(9))
        style.configure("FieldLabel.TLabel", background=COLORS["surface"], foreground=COLORS["text"], font=ui_font(10, "bold"))
        style.configure("Hint.TLabel", background=COLORS["surface"], foreground=COLORS["muted"], font=ui_font(9))
        style.configure("Number.TLabel", background=COLORS["accent"], foreground="#ffffff", font=ui_font(10, "bold"), padding=(9, 5))
        style.configure("Status.TLabel", background=COLORS["surface"], foreground=COLORS["muted"], font=ui_font(9))
        style.configure("ActionHint.TLabel", background=COLORS["surface"], foreground=COLORS["muted"], font=ui_font(9))

        style.configure("Path.TEntry", fieldbackground=COLORS["surface_soft"], foreground=COLORS["text"], insertcolor=COLORS["text"], bordercolor=COLORS["line"], padding=9)
        style.configure("TSpinbox", fieldbackground=COLORS["surface_soft"], foreground=COLORS["text"], bordercolor=COLORS["line"], padding=7)
        style.configure("TCheckbutton", background=COLORS["surface"], foreground=COLORS["text"])
        style.map("TCheckbutton", background=[("active", COLORS["surface"])], foreground=[("active", COLORS["text"])])

        style.configure("Primary.TButton", background=COLORS["accent"], foreground="#ffffff", font=ui_font(11, "bold"), padding=(24, 13))
        style.map("Primary.TButton", background=[("active", COLORS["accent_hover"]), ("disabled", "#99b8b4")], foreground=[("disabled", "#eef2f7")])
        style.configure("Ghost.TButton", background="#e8eef6", foreground=COLORS["text"], font=ui_font(10, "bold"), padding=(12, 9))
        style.map("Ghost.TButton", background=[("active", "#dbe5f1"), ("disabled", "#edf1f7")], foreground=[("disabled", COLORS["muted"])])
        style.configure("Small.TButton", background="#f1f5f9", foreground=COLORS["text"], font=ui_font(9, "bold"), padding=(10, 7))
        style.map("Small.TButton", background=[("active", "#e2e8f0")])

    def _build_ui(self) -> None:
        shell = ttk.Frame(self.root, style="App.TFrame")
        shell.pack(fill="both", expand=True)
        shell.rowconfigure(0, weight=1)
        shell.columnconfigure(1, weight=1)

        self._build_sidebar(shell)
        self._build_main(shell)

    def _build_sidebar(self, parent: ttk.Frame) -> None:
        sidebar = ttk.Frame(parent, style="Sidebar.TFrame", width=260, padding=(22, 24))
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        ttk.Label(sidebar, text="AOV TOOL", style="BrandSmall.TLabel").pack(anchor="w")
        ttk.Label(sidebar, text="Mod Camera", style="BrandTitle.TLabel").pack(anchor="w", pady=(2, 0))
        ttk.Label(
            sidebar,
            text="Tự động vá CommonActions.pkg.bytes và xuất file mod sạch để bạn đưa lại vào game.",
            style="SidebarMuted.TLabel",
            wraplength=205,
        ).pack(anchor="w", pady=(10, 20))

        self.pulse_canvas = Canvas(sidebar, width=212, height=5, bg=COLORS["sidebar"], highlightthickness=0)
        self.pulse_canvas.pack(fill="x", pady=(0, 24))
        self.pulse_bar = self.pulse_canvas.create_rectangle(0, 0, 212, 5, fill=COLORS["accent"], outline="")

        ttk.Label(sidebar, text="Quy trình", style="SidebarTitle.TLabel").pack(anchor="w", pady=(0, 10))
        self._sidebar_step(sidebar, "1", "Chọn CommonActions", "File gốc cần mod camera")
        self._sidebar_step(sidebar, "2", "Chọn dictionary", "Dùng mặc định hoặc bytesDict mới")
        self._sidebar_step(sidebar, "3", "Chọn nơi lưu", "Tool tạo file đã mod riêng")
        self._sidebar_step(sidebar, "4", "Mod ngay", "Bấm một lần rồi chờ kết quả")

        ttk.Frame(sidebar, style="Sidebar.TFrame").pack(fill="both", expand=True)

        status_box = ttk.Frame(sidebar, style="SidebarPanel.TFrame", padding=(14, 13))
        status_box.pack(fill="x", side="bottom")
        ttk.Label(status_box, textvariable=self.side_status_title, style="SidebarStatusTitle.TLabel").pack(anchor="w")
        ttk.Label(status_box, textvariable=self.side_status_detail, style="SidebarStatusText.TLabel", wraplength=190).pack(anchor="w", pady=(4, 0))

    def _sidebar_step(self, parent: ttk.Frame, number: str, title: str, text: str) -> None:
        row = ttk.Frame(parent, style="Sidebar.TFrame")
        row.pack(fill="x", pady=(0, 13))
        ttk.Label(row, text=number, style="SidebarStepNo.TLabel").grid(row=0, column=0, rowspan=2, sticky="n", padx=(0, 10))
        ttk.Label(row, text=title, style="SidebarStepTitle.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Label(row, text=text, style="SidebarStepText.TLabel", wraplength=165).grid(row=1, column=1, sticky="w", pady=(2, 0))
        row.columnconfigure(1, weight=1)

    def _build_main(self, parent: ttk.Frame) -> None:
        main = ttk.Frame(parent, style="Main.TFrame")
        main.grid(row=0, column=1, sticky="nsew")
        main.rowconfigure(1, weight=1)
        main.columnconfigure(0, weight=1)

        top = ttk.Frame(main, style="Main.TFrame", padding=(28, 24, 28, 12))
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(0, weight=1)

        ttk.Label(top, text="Bộ công cụ mod camera", style="PageTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            top,
            text="Chọn file mới nhất, chọn dictionary nếu bản update đổi, rồi xuất CommonActions đã mod.",
            style="PageSub.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        chip = ttk.Frame(top, style="Chip.TFrame", padding=(13, 8))
        chip.grid(row=0, column=1, rowspan=2, sticky="e", padx=(18, 0))
        ttk.Label(chip, textvariable=self.status_text, style="Chip.TLabel").pack()

        scroll_canvas = Canvas(main, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main, orient="vertical", command=scroll_canvas.yview)
        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        scroll_canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        body = ttk.Frame(scroll_canvas, style="Main.TFrame", padding=(28, 8, 28, 22))
        body_window = scroll_canvas.create_window((0, 0), window=body, anchor="nw")

        def sync_scroll_region(_event=None) -> None:
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

        def sync_body_width(event) -> None:
            scroll_canvas.itemconfigure(body_window, width=event.width)

        def on_mousewheel(event) -> None:
            scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        body.bind("<Configure>", sync_scroll_region)
        scroll_canvas.bind("<Configure>", sync_body_width)
        scroll_canvas.bind_all("<MouseWheel>", on_mousewheel)

        self._build_file_card(body)
        self._build_dict_card(body)
        self._build_output_card(body)
        self._build_options_card(body)
        self._build_log_card(body)

        action = ttk.Frame(main, style="Action.TFrame", padding=(28, 14))
        action.grid(row=2, column=0, columnspan=2, sticky="ew")
        action.columnconfigure(1, weight=1)
        self.patch_button = ttk.Button(action, text="Mod ngay", style="Primary.TButton", command=self._patch)
        self.patch_button.grid(row=0, column=0, sticky="w")
        ttk.Label(action, textvariable=self.status_text, style="Status.TLabel").grid(row=0, column=1, sticky="w", padx=(16, 0))
        ttk.Label(
            action,
            text="Nút này luôn cố định ở dưới. Thu nhỏ cửa sổ vẫn bấm được.",
            style="ActionHint.TLabel",
        ).grid(row=0, column=2, sticky="e", padx=(12, 0))

    def _card(self, parent: ttk.Frame, number: str, title: str, desc: str) -> ttk.Frame:
        card = ttk.Frame(parent, style="Card.TFrame", padding=(20, 18))
        card.pack(fill="x", pady=(0, 14))
        card.columnconfigure(0, weight=1)

        header = ttk.Frame(card, style="Card.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        header.columnconfigure(1, weight=1)
        ttk.Label(header, text=number, style="Number.TLabel").grid(row=0, column=0, rowspan=2, sticky="n", padx=(0, 12))
        ttk.Label(header, text=title, style="CardTitle.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Label(header, text=desc, style="CardDesc.TLabel", wraplength=760).grid(row=1, column=1, sticky="w", pady=(3, 0))
        return card

    def _build_file_card(self, parent: ttk.Frame) -> None:
        card = self._card(parent, "1", "File CommonActions cần mod", "Lấy file trong game hoặc chọn cả thư mục Ages/Resources để tool tự tìm.")
        ttk.Label(card, text="Đường dẫn CommonActions.pkg.bytes", style="FieldLabel.TLabel").grid(row=1, column=0, sticky="w")
        ttk.Entry(card, textvariable=self.input_path, style="Path.TEntry").grid(row=2, column=0, sticky="ew", pady=(7, 10))

        row = ttk.Frame(card, style="Card.TFrame")
        row.grid(row=3, column=0, sticky="ew")
        row.columnconfigure(3, weight=1)
        ttk.Button(row, text="Chọn CommonActions", style="Ghost.TButton", command=self._choose_file).grid(row=0, column=0, sticky="w")
        ttk.Button(row, text="Chọn thư mục", style="Ghost.TButton", command=self._choose_folder).grid(row=0, column=1, sticky="w", padx=(10, 0))
        ttk.Button(row, text="Dùng file mới nhất", style="Small.TButton", command=self._use_latest).grid(row=0, column=2, sticky="w", padx=(10, 0))

        ttk.Label(
            card,
            text=r"Lấy Common ở đây: Documents\Resources\1.62.1\Ages\Prefab_Characters\Prefab_Hero\CommonActions.pkg.bytes",
            style="Hint.TLabel",
            wraplength=840,
        ).grid(row=4, column=0, sticky="w", pady=(11, 0))
        ttk.Label(
            card,
            text="Nếu bạn chọn thư mục, tool chỉ tìm file CommonActions.pkg.bytes đúng nhánh Prefab_Hero.",
            style="Hint.TLabel",
            wraplength=840,
        ).grid(row=5, column=0, sticky="w", pady=(3, 0))

    def _build_dict_card(self, parent: ttk.Frame) -> None:
        card = self._card(parent, "2", "Dictionary zstd", "Bình thường dùng dictionary tích hợp sẵn. Khi game update đổi dictionary thì chọn file mới tại đây.")
        ttk.Label(card, text="Đường dẫn dictionary", style="FieldLabel.TLabel").grid(row=1, column=0, sticky="w")
        ttk.Entry(card, textvariable=self.dict_path, style="Path.TEntry").grid(row=2, column=0, sticky="ew", pady=(7, 10))

        row = ttk.Frame(card, style="Card.TFrame")
        row.grid(row=3, column=0, sticky="ew")
        ttk.Button(row, text="Chọn dictionary", style="Ghost.TButton", command=self._choose_dict).grid(row=0, column=0, sticky="w")
        ttk.Button(row, text="Dùng mặc định", style="Small.TButton", command=self._use_default_dict).grid(row=0, column=1, sticky="w", padx=(10, 0))

        ttk.Label(
            card,
            text=r"Lấy bytesDict trong game ở đây: Documents\Resources\1.62.1\Config\bytesDict.bytes",
            style="Hint.TLabel",
            wraplength=840,
        ).grid(row=4, column=0, sticky="w", pady=(11, 0))
        ttk.Label(
            card,
            text="Lưu ý: bytesDict.bytes của game có thể là file bọc riêng; nếu không chạy được thì dùng zstd_dict.bin đi kèm tool.",
            style="Hint.TLabel",
            wraplength=840,
        ).grid(row=5, column=0, sticky="w", pady=(3, 0))

    def _build_output_card(self, parent: ttk.Frame) -> None:
        card = self._card(parent, "3", "Nơi lưu file đã mod", "Tool có thể tạo file mới để bạn test, không cần ghi đè file gốc.")
        ttk.Label(card, text="Đường dẫn file kết quả", style="FieldLabel.TLabel").grid(row=1, column=0, sticky="w")
        ttk.Entry(card, textvariable=self.output_path, style="Path.TEntry").grid(row=2, column=0, sticky="ew", pady=(7, 10))

        row = ttk.Frame(card, style="Card.TFrame")
        row.grid(row=3, column=0, sticky="ew")
        ttk.Button(row, text="Chọn chỗ lưu", style="Ghost.TButton", command=self._choose_output).grid(row=0, column=0, sticky="w")
        ttk.Button(row, text="Tự đặt cạnh file gốc", style="Small.TButton", command=self._auto_output).grid(row=0, column=1, sticky="w", padx=(10, 0))

        ttk.Label(
            card,
            text="Nếu để trống, tool tự tạo CommonActions_patched.pkg.bytes cạnh file gốc. Sau khi mod xong, đường dẫn này vẫn hiện ở ô trên.",
            style="Hint.TLabel",
            wraplength=840,
        ).grid(row=4, column=0, sticky="w", pady=(11, 0))

    def _build_options_card(self, parent: ttk.Frame) -> None:
        card = self._card(parent, "4", "Thiết lập camera", "Chọn mức phần trăm dễ hiểu. Tool sẽ tự đổi sang giá trị kỹ thuật khi ghi vào XML.")
        settings = ttk.Frame(card, style="Card.TFrame")
        settings.grid(row=1, column=0, sticky="ew")
        settings.columnconfigure(3, weight=1)

        ttk.Label(settings, text="Độ xa camera", style="FieldLabel.TLabel").grid(row=0, column=0, sticky="w")
        level_box = ttk.Combobox(
            settings,
            textvariable=self.camera_level,
            values=list(CAMERA_LEVELS.keys()),
            width=10,
            state="readonly",
        )
        level_box.grid(row=0, column=1, sticky="w", padx=(12, 0))
        ttk.Label(settings, text="Khuyến nghị: 20%. 40% là mức xa mạnh.", style="Hint.TLabel").grid(row=0, column=2, sticky="w", padx=(14, 0))
        ttk.Checkbutton(settings, text="Ghi đè file gốc và tạo backup", variable=self.make_backup).grid(row=1, column=0, columnspan=3, sticky="w", pady=(14, 0))
        ttk.Label(
            settings,
            text="Không tick: tool tạo file mới để test. Tick: tool vá trực tiếp file gốc và tạo .bak.",
            style="Hint.TLabel",
            wraplength=780,
        ).grid(row=2, column=0, columnspan=4, sticky="w", pady=(6, 0))

    def _build_log_card(self, parent: ttk.Frame) -> None:
        card = self._card(parent, "5", "Nhật ký xử lý", "Theo dõi tool đã tìm file, vá entry nào và file kết quả nằm ở đâu.")
        self.log = Text(
            card,
            height=8,
            bg=COLORS["terminal"],
            fg=COLORS["terminal_text"],
            insertbackground=COLORS["terminal_text"],
            relief="flat",
            padx=14,
            pady=12,
            font=("Consolas", 9),
            wrap="word",
        )
        self.log.grid(row=1, column=0, sticky="nsew")
        self._write_log("Sẵn sàng. Chọn CommonActions.pkg.bytes hoặc thư mục, chọn mức %, rồi bấm Mod ngay.\n")

    def _set_status(self, title: str, detail: str | None = None) -> None:
        self.status_text.set(title)
        self.side_status_title.set(title)
        if detail is not None:
            self.side_status_detail.set(detail)

    def _start_pulse(self) -> None:
        self.busy = True
        self.pulse_pos = 0
        self._animate_pulse()

    def _stop_pulse(self) -> None:
        self.busy = False
        width = max(self.pulse_canvas.winfo_width(), 1)
        self.pulse_canvas.coords(self.pulse_bar, 0, 0, width, 5)

    def _animate_pulse(self) -> None:
        if not self.busy:
            return
        width = max(self.pulse_canvas.winfo_width(), 1)
        x0 = (self.pulse_pos % (width + 90)) - 90
        self.pulse_canvas.coords(self.pulse_bar, x0, 0, x0 + 90, 5)
        self.pulse_pos += 7
        self.root.after(35, self._animate_pulse)

    def _write_log(self, text: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", text)
        self.log.see("end")
        self.log.configure(state="disabled")

    def _choose_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Chọn CommonActions.pkg.bytes",
            filetypes=[("CommonActions", "CommonActions*.bytes"), ("Tất cả file", "*.*")],
        )
        if path:
            self.input_path.set(path)
            self._auto_output()
            self._set_status("Đã chọn file", "Kiểm tra nơi lưu rồi bấm Mod ngay")

    def _choose_folder(self) -> None:
        path = filedialog.askdirectory(title="Chọn thư mục Ages hoặc Resources")
        if path:
            self.input_path.set(path)
            self._auto_output()
            self._set_status("Đã chọn thư mục", "Tool sẽ tự tìm CommonActions trong Prefab_Hero")

    def _choose_dict(self) -> None:
        path = filedialog.askopenfilename(
            title="Chọn dictionary zstd",
            filetypes=[
                ("Dictionary", "*.bin *.bytes"),
                ("zstd_dict.bin", "zstd_dict.bin"),
                ("bytesDict.bytes", "bytesDict.bytes"),
                ("Tất cả file", "*.*"),
            ],
        )
        if path:
            self.dict_path.set(path)
            self._set_status("Đã chọn dictionary", "Nếu dictionary đúng, tool sẽ giải nén XML được")

    def _use_default_dict(self) -> None:
        self.dict_path.set(str(DEFAULT_DICT))
        self._set_status("Dùng dictionary mặc định", "Tool đang dùng zstd_dict.bin đi kèm")

    def _guess_output_path(self) -> Path | None:
        raw_path = self.input_path.get().strip().strip('"')
        if not raw_path:
            return None
        try:
            pkg_path = resolve_common_actions(Path(raw_path).expanduser().resolve())
        except BaseException:
            return None
        return pkg_path.with_name("CommonActions_patched.pkg.bytes")

    def _auto_output(self) -> None:
        guessed = self._guess_output_path()
        if guessed:
            self.output_path.set(str(guessed))
            self._set_status("Đã đặt nơi lưu", "File mod sẽ nằm cạnh CommonActions gốc")

    def _choose_output(self) -> None:
        initial = self._guess_output_path()
        kwargs = {
            "title": "Chọn nơi lưu file đã mod",
            "defaultextension": ".bytes",
            "filetypes": [("CommonActions", "*.pkg.bytes"), ("Tất cả file", "*.*")],
        }
        if initial:
            kwargs["initialdir"] = str(initial.parent)
            kwargs["initialfile"] = initial.name
        path = filedialog.asksaveasfilename(**kwargs)
        if path:
            self.output_path.set(path)
            self._set_status("Đã chọn nơi lưu", "Bấm Mod ngay để tạo file")

    def _use_latest(self) -> None:
        candidates = [
            Path.home() / "Downloads" / "1.62.1--3" / "Ages" / "Prefab_Characters" / "Prefab_Hero" / "CommonActions.pkg.bytes",
            Path.home() / "Downloads" / "1.62.1 (3)" / "Ages" / "Ages" / "Prefab_Characters" / "Prefab_Hero" / "CommonActions.pkg.bytes",
        ]
        for candidate in candidates:
            if candidate.exists():
                self.input_path.set(str(candidate))
                self._auto_output()
                self._set_status("Đã dùng file mới nhất", "Kiểm tra nơi lưu rồi bấm Mod ngay")
                return
        messagebox.showinfo("Không tìm thấy", "Không tìm thấy đường dẫn CommonActions.pkg.bytes quen thuộc.")

    def _patch(self) -> None:
        raw_path = self.input_path.get().strip().strip('"')
        if not raw_path:
            messagebox.showwarning("Thiếu file", "Hãy chọn CommonActions.pkg.bytes hoặc thư mục trước.")
            return

        camera_percent = self.camera_level.get().strip()
        height = CAMERA_LEVELS.get(camera_percent)
        if height is None:
            messagebox.showwarning("Sai độ xa", "Hãy chọn mức camera: 10%, 20% hoặc 40%.")
            return

        raw_dict = self.dict_path.get().strip().strip('"')
        if not raw_dict:
            messagebox.showwarning("Thiếu dictionary", "Hãy chọn zstd_dict.bin hoặc dùng dictionary mặc định.")
            return

        raw_output = self.output_path.get().strip().strip('"')
        output = Path(raw_output) if raw_output else self._guess_output_path()
        overwrite_source = self.make_backup.get()
        if not output and not overwrite_source:
            messagebox.showwarning("Thiếu nơi lưu", "Hãy chọn nơi lưu file đã mod.")
            return

        if output and not overwrite_source:
            self.output_path.set(str(output))
            self.last_result_path = str(output)
        else:
            try:
                self.last_result_path = str(resolve_common_actions(Path(raw_path).expanduser().resolve()))
            except BaseException:
                self.last_result_path = raw_path

        self.patch_button.configure(state="disabled")
        self._set_status("Đang mod...", f"Đang ghi mức camera {camera_percent} vào package")
        self._start_pulse()
        self._write_log(f"\n--- Bắt đầu mod camera {camera_percent} ---\n")

        thread = threading.Thread(
            target=self._patch_worker,
            args=(Path(raw_path), Path(raw_dict), output, height, camera_percent, overwrite_source),
            daemon=True,
        )
        thread.start()

    def _patch_worker(
        self,
        input_path: Path,
        dict_path: Path,
        output_path: Path | None,
        height: float,
        camera_percent: str,
        overwrite_source: bool,
    ) -> None:
        stream = io.StringIO()
        try:
            pkg_path = resolve_common_actions(input_path.expanduser().resolve())
            if overwrite_source:
                final_output = None
                backup = True
            else:
                final_output = output_path.expanduser().resolve() if output_path else pkg_path.with_name("CommonActions_patched.pkg.bytes")
                backup = False
            selected_dict = dict_path.expanduser().resolve()
            try:
                with contextlib.redirect_stdout(stream):
                    patch_package(
                        pkg_path=pkg_path,
                        dict_path=selected_dict,
                        height_rate=height,
                        level=17,
                        backup=backup,
                        output_path=final_output,
                    )
            except BaseException as first_exc:
                first_output = stream.getvalue()
                default_dict = DEFAULT_DICT.expanduser().resolve()
                looks_like_dict_error = (
                    "dictionary" in str(first_exc).lower()
                    or "dictionary" in first_output.lower()
                    or "decompression error" in str(first_exc).lower()
                )
                if selected_dict == default_dict or not default_dict.exists() or not looks_like_dict_error:
                    raise

                retry_stream = io.StringIO()
                with contextlib.redirect_stdout(retry_stream):
                    patch_package(
                        pkg_path=pkg_path,
                        dict_path=default_dict,
                        height_rate=height,
                        level=17,
                        backup=backup,
                        output_path=final_output,
                    )
                stream = io.StringIO()
                stream.write(first_output)
                stream.write("\nDictionary bạn chọn không dùng trực tiếp được. Tool đã tự dùng dictionary mặc định đi kèm và mod lại thành công.\n")
                stream.write(retry_stream.getvalue())
            result = "\n".join(line for line in stream.getvalue().splitlines() if not line.startswith("heightRate="))
            result += f"\nMức camera: {camera_percent}\n"
            self.queue.put(("ok", result))
        except BaseException as exc:
            output = stream.getvalue()
            if output:
                output += "\n"
            output += f"Lỗi: {exc}\n"
            self.queue.put(("error", output))

    def _poll_queue(self) -> None:
        try:
            while True:
                kind, text = self.queue.get_nowait()
                self._write_log(text)
                self.patch_button.configure(state="normal")
                self._stop_pulse()
                if kind == "ok":
                    self._set_status("Hoàn tất", "File mod đã được tạo, xem đường dẫn ở ô nơi lưu")
                    if self.last_result_path:
                        messagebox.showinfo("Mod xong", f"Đã tạo file:\n{self.last_result_path}")
                    else:
                        messagebox.showinfo("Mod xong", "CommonActions.pkg.bytes đã được mod.")
                else:
                    self._set_status("Có lỗi", "Xem nhật ký xử lý để biết lỗi cụ thể")
                    messagebox.showerror("Mod lỗi", text[-900:])
        except queue.Empty:
            pass
        self.root.after(100, self._poll_queue)


if __name__ == "__main__":
    CameraPatchGui().run()
