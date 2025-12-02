import tkinter as tk  
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
from openpyxl import Workbook 


def connect_db():  
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="0404",
            database="QLSV"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Lỗi kết nối", f"Không kết nối được MySQL:\n{e}")
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


main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill="both", expand=True)

lbl_title = tk.Label(
    main_frame,
    text="QUẢN LÝ SINH VIÊN",
    font=("Arial", 20, "bold"),
    bg="white",
    fg="#008b8b"
)
lbl_title.pack(pady=10)

frame_info = tk.Frame(main_frame, bg="white")
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



create_label("Điểm 1", 3, 2)
entry_diem1 = tk.Entry(frame_info, width=10, bg="white", fg="black", insertbackground="black")
entry_diem1.grid(row=3, column=3, padx=5, pady=4, sticky="w")

create_label("Điểm 2", 4, 0)
entry_diem2 = tk.Entry(frame_info, width=10, bg="white", fg="black", insertbackground="black")
entry_diem2.grid(row=4, column=1, padx=5, pady=4, sticky="w")

create_label("Điểm 3", 4, 2)
entry_diem3 = tk.Entry(frame_info, width=10, bg="white", fg="black", insertbackground="black")
entry_diem3.grid(row=4, column=3, padx=5, pady=4, sticky="w")

create_label("Điểm TB", 5, 0)
entry_diemtb = tk.Entry(frame_info, width=10, bg="white", fg="black", state="readonly")
entry_diemtb.grid(row=5, column=1, padx=5, pady=4, sticky="w")


def tinh_diem_tb():
    """Tính điểm trung bình từ 3 điểm, làm tròn 2 chữ số và hiển thị lên ô Điểm TB."""
    try:
        d1 = float(entry_diem1.get()) if entry_diem1.get().strip() != "" else 0
        d2 = float(entry_diem2.get()) if entry_diem2.get().strip() != "" else 0
        d3 = float(entry_diem3.get()) if entry_diem3.get().strip() != "" else 0
        tb = round((d1 + d2 + d3) / 3, 2)
    except ValueError:
        tb = 0

    entry_diemtb.config(state="normal")
    entry_diemtb.delete(0, tk.END)
    entry_diemtb.insert(0, tb)
    entry_diemtb.config(state="readonly")
    return tb



entry_diem1.bind("<KeyRelease>", lambda e: tinh_diem_tb())
entry_diem2.bind("<KeyRelease>", lambda e: tinh_diem_tb())
entry_diem3.bind("<KeyRelease>", lambda e: tinh_diem_tb())



frame_filter = tk.Frame(main_frame, bg="white")
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


center_frame = tk.Frame(main_frame, bg="white")
center_frame.pack(fill="both", expand=True, padx=10, pady=5)

center_frame.rowconfigure(0, weight=1)
center_frame.columnconfigure(0, weight=1)

columns = ("mssv", "holot", "ten", "phai", "ngaysinh", "lop", "khoa",
           "diem1", "diem2", "diem3", "diemtb")
tree = ttk.Treeview(center_frame, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col.upper())

tree.grid(row=0, column=0, sticky="nsew")  

 
scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="ns")

 
frame_btn = tk.Frame(center_frame, bg="white")
frame_btn.grid(row=1, column=0, columnspan=2, pady=5)



def clear_input():
    entry_mssv.delete(0, tk.END)
    entry_holot.delete(0, tk.END)
    entry_ten.delete(0, tk.END)
    gender_var.set("Nam")
    cbb_lop.set("")
    cbb_khoa.set("")
    entry_search.delete(0, tk.END)
    date_ngaysinh.set_date("2000-01-01")
    entry_diem1.delete(0, tk.END)
    entry_diem2.delete(0, tk.END)
    entry_diem3.delete(0, tk.END)
    entry_diemtb.config(state="normal")
    entry_diemtb.delete(0, tk.END)
    entry_diemtb.config(state="readonly")


def load_data(keyword=None, lop=None, khoa=None):
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()

    query = """
        SELECT mssv, holot, ten, phai, ngaysinh, lop, khoa,
               diem1, diem2, diem3, diemtb
        FROM sinhvien
        WHERE 1=1
    """
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
    mssv = entry_mssv.get().strip()
    holot = entry_holot.get().strip()
    ten = entry_ten.get().strip()
    lop = cbb_lop.get().strip()
    khoa = cbb_khoa.get().strip()
    diem1 = entry_diem1.get().strip()
    diem2 = entry_diem2.get().strip()
    diem3 = entry_diem3.get().strip()

    if not mssv or not holot or not ten or not lop or not khoa:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin sinh viên.")
        return

    if diem1 == "":
        diem1 = "0"
    if diem2 == "":
        diem2 = "0"
    if diem3 == "":
        diem3 = "0"

    tb = tinh_diem_tb()

    conn = connect_db()
    if not conn:
        messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu.")
        return

    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO sinhvien(mssv, holot, ten, phai, ngaysinh, lop, khoa,
                                 diem1, diem2, diem3, diemtb)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                mssv,
                holot,
                ten,
                gender_var.get(),
                date_ngaysinh.get(),
                lop,
                khoa,
                diem1,
                diem2,
                diem3,
                tb
            )
        )
        conn.commit()
        messagebox.showinfo("Thành công", "Thêm sinh viên thành công.")
        load_data()
        clear_input()
    except Exception as e:
        messagebox.showerror("Lỗi thêm", f"Không thể thêm sinh viên:\n{e}")
        print("Lỗi thêm:", e)
    finally:
        conn.close()


def sua_sv():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn sinh viên cần sửa.")
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

    entry_diem1.delete(0, tk.END)
    entry_diem2.delete(0, tk.END)
    entry_diem3.delete(0, tk.END)
    entry_diemtb.config(state="normal")
    entry_diemtb.delete(0, tk.END)

    entry_diem1.insert(0, values[7])
    entry_diem2.insert(0, values[8])
    entry_diem3.insert(0, values[9])
    entry_diemtb.insert(0, values[10])
    entry_diemtb.config(state="readonly")


def luu_sv():
    mssv = entry_mssv.get().strip()
    if not mssv:
        messagebox.showwarning("Thiếu dữ liệu", "Chưa có MSSV để lưu (vui lòng chọn hoặc nhập lại).")
        return

    holot = entry_holot.get().strip()
    ten = entry_ten.get().strip()
    lop = cbb_lop.get().strip()
    khoa = cbb_khoa.get().strip()
    diem1 = entry_diem1.get().strip()
    diem2 = entry_diem2.get().strip()
    diem3 = entry_diem3.get().strip()

    if diem1 == "":
        diem1 = "0"
    if diem2 == "":
        diem2 = "0"
    if diem3 == "":
        diem3 = "0"

    tb = tinh_diem_tb()

    conn = connect_db()
    if not conn:
        messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu.")
        return
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE sinhvien
            SET holot=%s, ten=%s, phai=%s, ngaysinh=%s, lop=%s, khoa=%s,
                diem1=%s, diem2=%s, diem3=%s, diemtb=%s
            WHERE mssv=%s
            """,
            (
                holot,
                ten,
                gender_var.get(),
                date_ngaysinh.get(),
                lop,
                khoa,
                diem1,
                diem2,
                diem3,
                tb,
                mssv
            )
        )
        conn.commit()
        if cur.rowcount == 0:
            messagebox.showwarning("Không tìm thấy", "Không tìm thấy sinh viên với MSSV đã nhập.")
        else:
            messagebox.showinfo("Thành công", "Đã lưu thông tin sinh viên.")
        load_data()
        clear_input()
    except Exception as e:
        messagebox.showerror("Lỗi lưu", f"Không thể lưu thông tin sinh viên:\n{e}")
        print("Lỗi lưu:", e)
    finally:
        conn.close()


def xoa_sv():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn sinh viên cần xóa.")
        return

    mssv = tree.item(selected[0])["values"][0]

    confirm = messagebox.askyesno(
        "Xác nhận xóa",
        f"Bạn có chắc chắn muốn xóa sinh viên có MSSV: {mssv} không?"
    )
    if not confirm:
        return

    conn = connect_db()
    if not conn:
        messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu.")
        return

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM sinhvien WHERE mssv=%s", (mssv,))
        conn.commit()
        if cur.rowcount == 0:
            messagebox.showwarning("Không tìm thấy", "Không tìm thấy sinh viên để xóa.")
        else:
            messagebox.showinfo("Thành công", "Đã xóa sinh viên.")
        load_data()
        clear_input()
    except Exception as e:
        messagebox.showerror("Lỗi xóa", f"Không thể xóa sinh viên:\n{e}")
        print("Lỗi xóa:", e)
    finally:
        conn.close()


def tim_kiem():
    load_data(
        keyword=entry_search.get(),
        lop=cbb_loc_lop.get(),
        khoa=cbb_loc_khoa.get()
    )


def thoat_ung_dung():
    if messagebox.askokcancel("Thoát", "Bạn có chắc chắn muốn thoát chương trình?"):
        root.destroy()


def xuat_excel():
    if not tree.get_children():
        messagebox.showwarning("Không có dữ liệu", "Không có dữ liệu để xuất Excel.")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "SinhVien"

    headers = [
        "MSSV", "HỌ LÓT", "TÊN", "PHÁI", "NGÀY SINH", "LỚP", "KHOA",
        "ĐIỂM 1", "ĐIỂM 2", "ĐIỂM 3", "ĐIỂM TB"
    ]
    ws.append(headers)

    for item in tree.get_children():
        row = tree.item(item)["values"]
        ws.append(row)

    file_name = "sinhvien.xlsx"
    try:
        wb.save(file_name)
        messagebox.showinfo("Xuất Excel", f"Đã xuất dữ liệu ra file {file_name} trong thư mục hiện tại.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể lưu file Excel:\n{e}")


ttk.Button(frame_btn, text="Thêm", width=10, command=them_sv).grid(row=0, column=0, padx=5)
ttk.Button(frame_btn, text="Lưu", width=10, command=luu_sv).grid(row=0, column=1, padx=5)
ttk.Button(frame_btn, text="Sửa", width=10, command=sua_sv).grid(row=0, column=2, padx=5)
ttk.Button(frame_btn, text="Xóa", width=10, command=xoa_sv).grid(row=0, column=3, padx=5)
ttk.Button(frame_btn, text="Hủy", width=10, command=clear_input).grid(row=0, column=4, padx=5)
ttk.Button(frame_btn, text="Tìm kiếm", width=10, command=tim_kiem).grid(row=0, column=5, padx=5)
ttk.Button(frame_btn, text="Xuất Excel", width=10, command=xuat_excel).grid(row=0, column=6, padx=5)
ttk.Button(frame_btn, text="Thoát", width=10, command=thoat_ung_dung).grid(row=0, column=7, padx=5)

cbb_loc_lop.bind("<<ComboboxSelected>>", lambda e: tim_kiem())
cbb_loc_khoa.bind("<<ComboboxSelected>>", lambda e: tim_kiem())

load_data()
root.mainloop()
