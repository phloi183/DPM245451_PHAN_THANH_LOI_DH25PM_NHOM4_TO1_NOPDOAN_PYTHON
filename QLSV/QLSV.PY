import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector


def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="QLSV"
        )
        return conn
    except Exception as e:
        print("Lỗi kết nối MySQL:", e)
        return None


def center_window(win, w=900, h=600):
    win.update_idletasks()
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")


root = tk.Tk()
root.title("QUẢN LÝ SINH VIÊN")
root.configure(bg="white")
center_window(root, 900, 600)
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="white",
    foreground="black",
    fieldbackground="white",
    rowheight=22
)
style.configure(
    "Treeview.Heading",
    background="#e0e0e0",
    foreground="black"
)
style.map("Treeview", background=[("selected", "#cde5ff")])

style.configure(
    "TButton",
    padding=4,
    background="#e0e0e0",
    foreground="black"
)
style.map(
    "TButton",
    background=[("active", "#d0d0d0")]
)


lbl_title = tk.Label(
    root,
    text="QUẢN LÝ SINH VIÊN",
    font=("Arial", 20, "bold"),
    bg="white",
    fg="#008b8b"
)
lbl_title.pack(pady=10)


frame_info = tk.Frame(root, bg="white")
frame_info.pack(pady=5, padx=10, fill="x")

def create_label(text, row, col):
    lbl = tk.Label(
        frame_info,
        text=text,
        bg="white",
        fg="black",
        font=("Arial", 10)
    )
    lbl.grid(row=row, column=col, padx=5, pady=4, sticky="w")
    return lbl

create_label("MSSV", 0, 0)
entry_mssv = tk.Entry(frame_info, width=18, bg="white", fg="black", insertbackground="black")
entry_mssv.grid(row=0, column=1, padx=5, pady=4, sticky="w")

create_label("Lớp", 0, 2)
cbb_lop = ttk.Combobox(
    frame_info,
    values=["DH25PM", "DH25TH", "DH25T", "DH24PM", "DH24TH"],
    width=20
)
cbb_lop.grid(row=0, column=3, padx=5, pady=4, sticky="w")

create_label("Họ lót", 1, 0)
entry_holot = tk.Entry(frame_info, width=25, bg="white", fg="black", insertbackground="black")
entry_holot.grid(row=1, column=1, padx=5, pady=4, sticky="w")

create_label("Khoa", 1, 2)
cbb_khoa = ttk.Combobox(
    frame_info,
    values=["CNTT", "Kinh tế", "Sư phạm", "Nông nghiệp", "Ngoại ngữ"],
    width=20
)
cbb_khoa.grid(row=1, column=3, padx=5, pady=4, sticky="w")

create_label("Tên", 2, 0)
entry_ten = tk.Entry(frame_info, width=18, bg="white", fg="black", insertbackground="black")
entry_ten.grid(row=2, column=1, padx=5, pady=4, sticky="w")

create_label("Phái", 2, 2)
gender_var = tk.StringVar(value="Nam")

frame_gender = tk.Frame(frame_info, bg="white")
frame_gender.grid(row=2, column=3, padx=5, pady=4, sticky="w")

tk.Radiobutton(
    frame_gender, text="Nam", variable=gender_var, value="Nam",
    bg="white", fg="black", selectcolor="white"
).pack(side="left", padx=2)

tk.Radiobutton(
    frame_gender, text="Nữ", variable=gender_var, value="Nữ",
    bg="white", fg="black", selectcolor="white"
).pack(side="left", padx=2)

create_label("Ngày sinh", 3, 0)
date_ngaysinh = DateEntry(
    frame_info,
    width=16,
    background="white",
    foreground="black",
    borderwidth=1,
    date_pattern="yyyy-mm-dd"
)
date_ngaysinh.grid(row=3, column=1, padx=5, pady=4, sticky="w")


frame_filter = tk.Frame(root, bg="white")
frame_filter.pack(pady=5, padx=10, fill="x")

tk.Label(frame_filter, text="Tìm kiếm:", bg="white", fg="black").grid(row=0, column=0, padx=5)
entry_search = tk.Entry(frame_filter, width=25, bg="white", fg="black", insertbackground="black")
entry_search.grid(row=0, column=1, padx=5)

tk.Label(frame_filter, text="Lọc lớp:", bg="white", fg="black").grid(row=0, column=2)
cbb_loc_lop = ttk.Combobox(frame_filter, values=["(Tất cả)", "DH25PM", "DH25TH", "DH25T", "DH24PM"], width=15)
cbb_loc_lop.set("(Tất cả)")
cbb_loc_lop.grid(row=0, column=3, padx=5)

tk.Label(frame_filter, text="Lọc khoa:", bg="white", fg="black").grid(row=0, column=4)
cbb_loc_khoa = ttk.Combobox(frame_filter, values=["(Tất cả)", "CNTT", "Kinh tế", "Sư phạm", "Nông nghiệp"], width=15)
cbb_loc_khoa.set("(Tất cả)")
cbb_loc_khoa.grid(row=0, column=5, padx=5)


columns = ("mssv", "holot", "ten", "phai", "ngaysinh", "lop", "khoa")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col.upper())
tree.pack(padx=10, pady=10, fill="both")


def clear_input():
    entry_mssv.delete(0, tk.END)
    entry_holot.delete(0, tk.END)
    entry_ten.delete(0, tk.END)
    gender_var.set("Nam")
    cbb_lop.set("")
    cbb_khoa.set("")
    entry_search.delete(0, tk.END)
    date_ngaysinh.set_date("2000-01-01")

def load_data(keyword=None, lop=None, khoa=None):
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()

    query = "SELECT * FROM sinhvien WHERE 1=1"
    params = []

    if keyword:
        query += " AND (mssv LIKE %s OR holot LIKE %s OR ten LIKE %s)"
        k = "%" + keyword + "%"
        params.extend([k, k, k])

    if lop and lop != "(Tất cả)":
        query += " AND lop=%s"
        params.append(lop)

    if khoa and khoa != "(Tất cả)":
        query += " AND khoa=%s"
        params.append(khoa)

    cur.execute(query, params)

    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)

    conn.close()

def them_sv():
    conn = connect_db()
    if not conn:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return
    
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO sinhvien VALUES (%s,%s,%s,%s,%s,%s,%s)", (
            entry_mssv.get(),
            entry_holot.get(),
            entry_ten.get(),
            gender_var.get(),
            date_ngaysinh.get(),
            cbb_lop.get(),
            cbb_khoa.get()
        ))
        conn.commit()
        print("Thêm sinh viên thành công.")
        load_data()
        clear_input()
    except Exception as e:
        print("Lỗi thêm:", e)
    finally:
        conn.close()

def sua_sv():
    selected = tree.selection()
    if not selected:
        print("Chưa chọn sinh viên để sửa.")
        return

    values = tree.item(selected[0])["values"]

    entry_mssv.delete(0, tk.END)
    entry_mssv.insert(0, values[0])

    entry_holot.delete(0, tk.END)
    entry_holot.insert(0, values[1])

    entry_ten.delete(0, tk.END)
    entry_ten.insert(0, values[2])

    gender_var.set(values[3])
    date_ngaysinh.set_date(values[4])
    cbb_lop.set(values[5])
    cbb_khoa.set(values[6])

def luu_sv():
    conn = connect_db()
    if not conn:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE sinhvien
            SET holot=%s, ten=%s, phai=%s, ngaysinh=%s, lop=%s, khoa=%s
            WHERE mssv=%s
        """, (
            entry_holot.get(),
            entry_ten.get(),
            gender_var.get(),
            date_ngaysinh.get(),
            cbb_lop.get(),
            cbb_khoa.get(),
            entry_mssv.get()
        ))
        conn.commit()
        print("Đã lưu thông tin sinh viên.")
        load_data()
        clear_input()
    except Exception as e:
        print("Lỗi lưu:", e)
    finally:
        conn.close()
        
def xoa_sv():
    selected = tree.selection()
    if not selected:
        print("Chưa chọn sinh viên để xóa.")
        return

    mssv = tree.item(selected[0])["values"][0]
    
    conn = connect_db()
    if not conn:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM sinhvien WHERE mssv=%s", (mssv,))
        conn.commit()
        print("Đã xóa sinh viên.")
        load_data()
        clear_input()
    except Exception as e:
        print("Lỗi xóa:", e)
    finally:
        conn.close()

def tim_kiem():
    load_data(
        keyword=entry_search.get(),
        lop=cbb_loc_lop.get(),
        khoa=cbb_loc_khoa.get()
    )


frame_btn = tk.Frame(root, bg="white")
frame_btn.pack(pady=5)

ttk.Button(frame_btn, text="Thêm", width=10, command=them_sv).grid(row=0, column=0, padx=5)
ttk.Button(frame_btn, text="Lưu", width=10, command=luu_sv).grid(row=0, column=1, padx=5)
ttk.Button(frame_btn, text="Sửa", width=10, command=sua_sv).grid(row=0, column=2, padx=5)
ttk.Button(frame_btn, text="Xóa", width=10, command=xoa_sv).grid(row=0, column=3, padx=5)
ttk.Button(frame_btn, text="Hủy", width=10, command=clear_input).grid(row=0, column=4, padx=5)
ttk.Button(frame_btn, text="Tìm kiếm", width=10, command=tim_kiem).grid(row=0, column=5, padx=5)
ttk.Button(frame_btn, text="Thoát", width=10, command=root.quit).grid(row=0, column=6, padx=5)

cbb_loc_lop.bind("<<ComboboxSelected>>", lambda e: tim_kiem())
cbb_loc_khoa.bind("<<ComboboxSelected>>", lambda e: tim_kiem())

load_data()
root.mainloop()
