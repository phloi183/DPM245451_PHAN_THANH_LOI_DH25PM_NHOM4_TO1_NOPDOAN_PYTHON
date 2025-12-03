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
root.state("zoomed")          # mở fullscreen
root.title("QUẢN LÝ SINH VIÊN")
root.configure(bg="white")
center_window(root, 900, 600)
root.resizable(True, True)

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
frame_info.columnconfigure(1, weight=1)
frame_info.columnconfigure(3, weight=1)


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


# ====== THÔNG TIN SV (không có điểm) ======
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

# ====== TÌM KIẾM / LỌC ======
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

# ====== BẢNG DỮ LIỆU CHÍNH (CÓ CỘT ĐIỂM) ======
center_frame = tk.Frame(main_frame, bg="white")
center_frame.pack(fill="both", expand=True, padx=10, pady=5)

center_frame.rowconfigure(0, weight=1)
center_frame.columnconfigure(0, weight=1)

columns = (
    "mssv", "holot", "ten", "phai", "ngaysinh",
    "lop", "khoa", "diem1", "diem2", "diem3", "diemtb"
)
tree = ttk.Treeview(center_frame, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col.upper())

tree.grid(row=0, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="ns")

frame_btn = tk.Frame(center_frame, bg="white")
frame_btn.grid(row=1, column=0, columnspan=2, pady=5)


# ================== HÀM XỬ LÝ ==================
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
    """Load dữ liệu sinh viên (có cả cột điểm) lên bảng chính."""
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

    if not mssv or not holot or not ten or not lop or not khoa:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin sinh viên.")
        return

    conn = connect_db()
    if not conn:
        messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu.")
        return

    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO sinhvien
            (mssv, holot, ten, phai, ngaysinh, lop, khoa,
             diem1, diem2, diem3, diemtb)
            VALUES (%s,%s,%s,%s,%s,%s,%s, 0,0,0,0)
            """,
            (
                mssv,
                holot,
                ten,
                gender_var.get(),
                date_ngaysinh.get(),
                lop,
                khoa
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
    # Điểm hiển thị trong bảng, không cần trên form


def luu_sv():
    mssv = entry_mssv.get().strip()
    if not mssv:
        messagebox.showwarning("Thiếu dữ liệu", "Chưa có MSSV để lưu (vui lòng chọn hoặc nhập lại).")
        return

    holot = entry_holot.get().strip()
    ten = entry_ten.get().strip()
    lop = cbb_lop.get().strip()
    khoa = cbb_khoa.get().strip()

    conn = connect_db()
    if not conn:
        messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu.")
        return
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE sinhvien
            SET holot=%s, ten=%s, phai=%s, ngaysinh=%s, lop=%s, khoa=%s
            WHERE mssv=%s
            """,
            (
                holot,
                ten,
                gender_var.get(),
                date_ngaysinh.get(),
                lop,
                khoa,
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
        "MSSV", "HỌ LÓT", "TÊN", "PHÁI", "NGÀY SINH",
        "LỚP", "KHOA", "ĐIỂM 1", "ĐIỂM 2", "ĐIỂM 3", "ĐIỂM TB"
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


# ====== CỬA SỔ TÍNH ĐIỂM ======
def mo_bang_tinh_diem():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn sinh viên cần tính điểm.")
        return

    values = tree.item(selected[0])["values"]
    mssv, holot, ten, phai, ngaysinh, lop, khoa, *_ = values

    win = tk.Toplevel(root)
    win.title(f"Tính điểm cho {mssv}")
    win.configure(bg="white")
    center_window(win, 800, 500)

    fi = tk.Frame(win, bg="white")
    fi.pack(padx=10, pady=10, fill="x")

    def mk_label(parent, text, r, c):
        lbl = tk.Label(parent, text=text, bg="white", fg="black", font=("Arial", 10))
        lbl.grid(row=r, column=c, padx=5, pady=4, sticky="w")
        return lbl

    mk_label(fi, "MSSV", 0, 0)
    e_mssv = tk.Entry(fi, width=18, bg="white")
    e_mssv.grid(row=0, column=1, padx=5, pady=4, sticky="w")
    e_mssv.insert(0, mssv)
    e_mssv.config(state="readonly")

    mk_label(fi, "Họ lót", 1, 0)
    e_holot = tk.Entry(fi, width=25, bg="white")
    e_holot.grid(row=1, column=1, padx=5, pady=4, sticky="w")
    e_holot.insert(0, holot)
    e_holot.config(state="readonly")

    mk_label(fi, "Tên", 2, 0)
    e_ten = tk.Entry(fi, width=18, bg="white")
    e_ten.grid(row=2, column=1, padx=5, pady=4, sticky="w")
    e_ten.insert(0, ten)
    e_ten.config(state="readonly")

    mk_label(fi, "Phái", 0, 2)
    e_phai = tk.Entry(fi, width=10, bg="white")
    e_phai.grid(row=0, column=3, padx=5, pady=4, sticky="w")
    e_phai.insert(0, phai)
    e_phai.config(state="readonly")

    mk_label(fi, "Ngày sinh", 1, 2)
    e_ns = tk.Entry(fi, width=12, bg="white")
    e_ns.grid(row=1, column=3, padx=5, pady=4, sticky="w")
    e_ns.insert(0, str(ngaysinh))
    e_ns.config(state="readonly")

    mk_label(fi, "Lớp", 2, 2)
    e_lop = tk.Entry(fi, width=15, bg="white")
    e_lop.grid(row=2, column=3, padx=5, pady=4, sticky="w")
    e_lop.insert(0, lop)
    e_lop.config(state="readonly")

    mk_label(fi, "Khoa", 3, 0)
    e_khoa = tk.Entry(fi, width=20, bg="white")
    e_khoa.grid(row=3, column=1, padx=5, pady=4, sticky="w")
    e_khoa.insert(0, khoa)
    e_khoa.config(state="readonly")

    mk_label(fi, "Điểm 1", 4, 0)
    e_diem1 = tk.Entry(fi, width=10, bg="white")
    e_diem1.grid(row=4, column=1, padx=5, pady=4, sticky="w")

    mk_label(fi, "Điểm 2", 4, 2)
    e_diem2 = tk.Entry(fi, width=10, bg="white")
    e_diem2.grid(row=4, column=3, padx=5, pady=4, sticky="w")

    mk_label(fi, "Điểm 3", 5, 0)
    e_diem3 = tk.Entry(fi, width=10, bg="white")
    e_diem3.grid(row=5, column=1, padx=5, pady=4, sticky="w")

    mk_label(fi, "Điểm TB", 5, 2)
    e_diemtb = tk.Entry(fi, width=10, bg="white", state="readonly")
    e_diemtb.grid(row=5, column=3, padx=5, pady=4, sticky="w")

    # load điểm cũ (nếu có)
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT diem1, diem2, diem3, diemtb
            FROM sinhvien WHERE mssv=%s
            """,
            (mssv,)
        )
        row = cur.fetchone()
        conn.close()
        if row:
            d1, d2, d3, dtb = row
            if d1 and d1 != 0:
                e_diem1.insert(0, d1)
            if d2 and d2 != 0:
                e_diem2.insert(0, d2)
            if d3 and d3 != 0:
                e_diem3.insert(0, d3)
            if dtb and dtb != 0:
                e_diemtb.config(state="normal")
                e_diemtb.insert(0, f"{dtb:.2f}")
                e_diemtb.config(state="readonly")

    def tinh_tb_local():
        """Tính điểm TB từ 3 điểm và hiển thị, làm tròn 2 chữ số."""
        try:
            d1 = float(e_diem1.get()) if e_diem1.get().strip() != "" else 0
            d2 = float(e_diem2.get()) if e_diem2.get().strip() != "" else 0
            d3 = float(e_diem3.get()) if e_diem3.get().strip() != "" else 0
            tb = round((d1 + d2 + d3) / 3, 2)
        except ValueError:
            tb = 0.0
        e_diemtb.config(state="normal")
        e_diemtb.delete(0, tk.END)
        e_diemtb.insert(0, f"{tb:.2f}")
        e_diemtb.config(state="readonly")
        return tb

    e_diem1.bind("<KeyRelease>", lambda e: tinh_tb_local())
    e_diem2.bind("<KeyRelease>", lambda e: tinh_tb_local())
    e_diem3.bind("<KeyRelease>", lambda e: tinh_tb_local())

    center2 = tk.Frame(win, bg="white")
    center2.pack(fill="both", expand=True, padx=10, pady=5)

    cols2 = ("mssv", "holot", "ten", "phai", "ngaysinh", "lop", "khoa",
             "diem1", "diem2", "diem3", "diemtb")
    tree2 = ttk.Treeview(center2, columns=cols2, show="headings", height=6)
    for c in cols2:
        tree2.heading(c, text=c.upper())
    tree2.grid(row=0, column=0, sticky="nsew")
    sb2 = ttk.Scrollbar(center2, orient="vertical", command=tree2.yview)
    tree2.configure(yscrollcommand=sb2.set)
    sb2.grid(row=0, column=1, sticky="ns")
    center2.rowconfigure(0, weight=1)
    center2.columnconfigure(0, weight=1)

    def load_diem_table():
        for r in tree2.get_children():
            tree2.delete(r)
        conn2 = connect_db()
        if not conn2:
            return
        c2 = conn2.cursor()
        c2.execute(
            """
            SELECT mssv, holot, ten, phai, ngaysinh, lop, khoa,
                   diem1, diem2, diem3, diemtb
            FROM sinhvien
            WHERE mssv=%s
            """,
            (mssv,)
        )
        for r in c2.fetchall():
            tree2.insert("", tk.END, values=r)
        conn2.close()

    load_diem_table()

    fb = tk.Frame(win, bg="white")
    fb.pack(pady=5)

    def luu_diem():
        tb = tinh_tb_local()
        d1 = e_diem1.get().strip() or "0"
        d2 = e_diem2.get().strip() or "0"
        d3 = e_diem3.get().strip() or "0"

        conn3 = connect_db()
        if not conn3:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL.")
            return
        try:
            c3 = conn3.cursor()
            c3.execute(
                """
                UPDATE sinhvien
                SET diem1=%s, diem2=%s, diem3=%s, diemtb=%s
                WHERE mssv=%s
                """,
                (d1, d2, d3, tb, mssv)
            )
            conn3.commit()
            messagebox.showinfo("Thành công", "Đã lưu điểm sinh viên.")
            load_diem_table()
            # reload bảng chính cho thấy điểm mới
            load_data(keyword=entry_search.get(),
                      lop=cbb_loc_lop.get(),
                      khoa=cbb_loc_khoa.get())
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Không thể lưu điểm:\n{ex}")
        finally:
            conn3.close()

    ttk.Button(fb, text="Lưu điểm", width=12, command=luu_diem).grid(row=0, column=0, padx=5)
    ttk.Button(fb, text="Đóng", width=12, command=win.destroy).grid(row=0, column=1, padx=5)


# ====== NÚT CHỨC NĂNG CHÍNH ======
ttk.Button(frame_btn, text="Thêm", width=10, command=them_sv).grid(row=0, column=0, padx=5)
ttk.Button(frame_btn, text="Lưu", width=10, command=luu_sv).grid(row=0, column=1, padx=5)
ttk.Button(frame_btn, text="Sửa", width=10, command=sua_sv).grid(row=0, column=2, padx=5)
ttk.Button(frame_btn, text="Xóa", width=10, command=xoa_sv).grid(row=0, column=3, padx=5)
ttk.Button(frame_btn, text="Hủy", width=10, command=clear_input).grid(row=0, column=4, padx=5)
ttk.Button(frame_btn, text="Tìm kiếm", width=10, command=tim_kiem).grid(row=0, column=5, padx=5)
ttk.Button(frame_btn, text="Tính điểm", width=10, command=mo_bang_tinh_diem).grid(row=0, column=6, padx=5)
ttk.Button(frame_btn, text="Xuất Excel", width=10, command=xuat_excel).grid(row=0, column=7, padx=5)
ttk.Button(frame_btn, text="Thoát", width=10, command=thoat_ung_dung).grid(row=0, column=8, padx=5)

cbb_loc_lop.bind("<<ComboboxSelected>>", lambda e: tim_kiem())
cbb_loc_khoa.bind("<<ComboboxSelected>>", lambda e: tim_kiem())

load_data()
root.mainloop()
