"""
Script: scripts/generate_bt2_docx.py
Mục đích: Tự động biên soạn Báo cáo Bài tập 2 chuẩn 7 mục (6-9 trang) sang định dạng Microsoft Word (.docx).
Loại bỏ hoàn toàn mã nguồn thô và triệt tiêu 100% lỗi 'Error! Bookmark not defined'.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Đặt màu nền cho ô trong bảng."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Đặt khoảng đệm (padding) cho ô trong bảng."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def style_table(table, col_widths=None, header_bg="1F2937", alt_bg="F9FAFB"):
    """Định dạng bảng chuyên nghiệp chuẩn khoa học."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        # Tránh gãy dòng ngang trang
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if i == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            for cell in row.cells:
                set_cell_background(cell, header_bg)
                set_cell_margins(cell, 120, 120, 160, 160)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        r.font.bold = True
                        r.font.color.rgb = RGBColor(255, 255, 255)
                        r.font.size = Pt(9.5)
                        r.font.name = "Arial"
        else:
            bg = alt_bg if i % 2 == 1 else "FFFFFF"
            for cell in row.cells:
                if bg != "FFFFFF":
                    set_cell_background(cell, bg)
                set_cell_margins(cell, 90, 90, 140, 140)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(9.0)
                        r.font.name = "Arial"
    
    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                if idx < len(row.cells):
                    row.cells[idx].width = width

def build_bt2_docx():
    doc = docx.Document()
    
    # 1. Cấu hình lề trang 2cm chuẩn ISO
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69)

    # Đặt font chữ mặc định
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Arial'
    font.size = Pt(10)
    font.color.rgb = RGBColor(31, 41, 55)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    screenshots_dir = os.path.join(base_dir, "docs", "screenshots")

    # ==============================================================================
    # TRANG BÌA (COVER PAGE)
    # ==============================================================================
    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_univ.add_run("TRƯỜNG ĐẠI HỌC VĂN LANG\nKHOA CÔNG NGHỆ THÔNG TIN\n")
    r1.font.bold = True
    r1.font.size = Pt(12)
    r1.font.color.rgb = RGBColor(17, 24, 39)
    
    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_after = Pt(24)
    r_div = p_div.add_run("-------------------- *** --------------------")
    r_div.font.color.rgb = RGBColor(156, 163, 175)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("BÁO CÁO BÀI TẬP 2\nHIỆN THỰC HÓA MODULE CỐT LÕI (15%)\n")
    r_title.font.bold = True
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(30, 64, 175)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(28)
    r_sub = p_sub.add_run("Học phần: Chuyên đề tốt nghiệp 1 (CDTN01)\nHệ thống Smart CRM – Mekong Mobile\nLuồng 05: Quản lý Kho linh kiện thay thế\nTrack chuyên ngành: Kỹ thuật phần mềm (Software Engineering - SE)")
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(75, 85, 99)

    # Bảng thông tin sinh viên & Git Tag
    info_table = doc.add_table(rows=6, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w = [Inches(2.5), Inches(4.2)]
    
    info_data = [
        ("Họ và tên sinh viên:", "Huỳnh Nguyễn Bảo Ngọc"),
        ("Mã số sinh viên (MSSV):", "2374802010339 (Lớp: K27)"),
        ("Giảng viên hướng dẫn:", "TS. Nguyễn Trí Hải"),
        ("Ngày nộp & Hoàn thiện:", "29/10/2026 (Bản chuẩn hóa cập nhật: 12/11/2026)"),
        ("GitHub Repository (Public):", "https://github.com/Johnny120905/CDTN01.git"),
        ("Git Release Tag BT2:", "v0.2  (Commit: e6698d58737cefbe0776fadaa75115e46cac58c4)")
    ]
    for idx, (label, val) in enumerate(info_data):
        row = info_table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.text = label
        cell_lbl.paragraphs[0].runs[0].font.bold = True
        cell_lbl.paragraphs[0].runs[0].font.size = Pt(10)
        cell_lbl.paragraphs[0].runs[0].font.color.rgb = RGBColor(31, 41, 55)
        cell_val.text = val
        cell_val.paragraphs[0].runs[0].font.size = Pt(10)
        cell_val.paragraphs[0].runs[0].font.color.rgb = RGBColor(17, 24, 39)
        if "v0.2" in val or "github" in val:
            cell_val.paragraphs[0].runs[0].font.bold = True
            cell_val.paragraphs[0].runs[0].font.color.rgb = RGBColor(30, 64, 175)
        set_cell_margins(cell_lbl, 80, 80, 100, 100)
        set_cell_margins(cell_val, 80, 80, 100, 100)
        set_cell_background(cell_lbl, "F3F4F6")
        set_cell_background(cell_val, "F9FAFB")
        row.cells[0].width = col_w[0]
        row.cells[1].width = col_w[1]

    doc.add_page_break()

    # ==============================================================================
    # MỤC LỤC TỔNG HỢP (CLEAN TABLE OF CONTENTS - NO ERROR BOOKMARKS)
    # ==============================================================================
    h_toc = doc.add_paragraph()
    r = h_toc.add_run("MỤC LỤC BÁO CÁO")
    r.font.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = RGBColor(30, 64, 175)
    h_toc.paragraph_format.space_after = Pt(14)

    toc_items = [
        ("MỤC 1: TÓM TẮT HỆ THỐNG ĐÃ LÀM", "Trang 3"),
        ("    1.1. Phạm vi và các chức năng hệ thống thực hiện được", "Trang 3"),
        ("    1.2. Đánh giá mức độ hoàn thành các hạng mục", "Trang 3"),
        ("MỤC 2: KIẾN TRÚC ĐÃ HIỆN THỰC", "Trang 4"),
        ("    2.1. Sơ đồ Kiến trúc Phân lớp Thực tế (Layered Clean Architecture)", "Trang 4"),
        ("    2.2. Bảng ánh xạ cấu trúc thư mục mã nguồn thực tế với từng tầng", "Trang 4"),
        ("MỤC 3: MODULE CỐT LÕI", "Trang 5"),
        ("    3.1. Các quy tắc nghiệp vụ cốt lõi đã hiện thực (BR-01 đến BR-05)", "Trang 5"),
        ("    3.2. Hiện thực tiêu chí SE S1: Đầy đủ 4 thao tác CRUD cho >= 2 thực thể", "Trang 5"),
        ("    3.3. Minh chứng các màn hình nghiệp vụ chạy thực tế", "Trang 6"),
        ("MỤC 4: BỘ KIỂM THỬ", "Trang 6"),
        ("    4.1. Ba nhóm trường hợp kiểm thử đại diện", "Trang 6"),
        ("    4.2. Bảng tổng hợp kết quả kiểm thử tự động (67/67 Tests PASS 100%)", "Trang 7"),
        ("    4.3. Bảng tự đánh giá các tiêu chí kỹ thuật (Đối chiếu Bảng 4.2 Đề bài)", "Trang 7"),
        ("MỤC 5: MODULE MỞ RỘNG / TRÌNH BÀY KẾT QUẢ", "Trang 7"),
        ("    5.1. Kiến trúc giao diện Web Single Page Application (SPA)", "Trang 7"),
        ("    5.2. Minh chứng ảnh chụp đầy đủ BA trạng thái: Đang tải, Rỗng, Lỗi", "Trang 8"),
        ("MỤC 6: CÁCH DỰNG LẠI HỆ THỐNG", "Trang 8"),
        ("    6.1. Khởi chạy nhanh bằng Docker Compose (Đúng <= 2 lệnh)", "Trang 8"),
        ("    6.2. Danh mục tài khoản kiểm thử mẫu dựng sẵn theo vai trò (RBAC)", "Trang 8"),
        ("MỤC 7: THAY ĐỔI SO VỚI THIẾT KẾ BÀI TẬP 1 & TIẾP THU NHẬN XÉT", "Trang 9"),
        ("    7.1. Bảng đối chiếu các thay đổi sau phản hồi Bài tập 1 (TD-01..05)", "Trang 9"),
        ("    7.2. Bảng tiếp thu nhận xét Bài tập 2 và các hành động khắc phục hoàn thiện", "Trang 9"),
        ("PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI (BẮT BUỘC)", "Trang 10")
    ]
    
    toc_table = doc.add_table(rows=len(toc_items), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, page_str) in enumerate(toc_items):
        row = toc_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.text = title
        c1.text = page_str
        c0.paragraphs[0].runs[0].font.size = Pt(9.5)
        c1.paragraphs[0].runs[0].font.size = Pt(9.5)
        if title.startswith("MỤC") or title.startswith("PHỤ"):
            c0.paragraphs[0].runs[0].font.bold = True
            c1.paragraphs[0].runs[0].font.bold = True
            c0.paragraphs[0].runs[0].font.color.rgb = RGBColor(30, 64, 175)
            c1.paragraphs[0].runs[0].font.color.rgb = RGBColor(30, 64, 175)
        c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        set_cell_margins(c0, 40, 40, 60, 60)
        set_cell_margins(c1, 40, 40, 60, 60)
        c0.width = Inches(5.5)
        c1.width = Inches(1.2)

    doc.add_page_break()

    # ==============================================================================
    # MỤC 1: TÓM TẮT HỆ THỐNG ĐÃ LÀM (0.5 - 1 TRANG)
    # ==============================================================================
    h1 = doc.add_paragraph()
    r = h1.add_run("MỤC 1: TÓM TẮT HỆ THỐNG ĐÃ LÀM")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(30, 64, 175)
    h1.paragraph_format.space_before = Pt(8)
    h1.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Phân hệ Kho linh kiện thay thế (Luồng 05) thuộc Hệ thống Smart CRM – Mekong Mobile phục vụ số hóa "
        "toàn diện quy trình quản lý tồn kho, tra cứu linh kiện thời gian thực theo chi nhánh (L5-WH-890), "
        "cấp phát linh kiện bảo hành cho kỹ thuật viên, nhập kho bù hàng và giám sát KPI điều hành. Hệ thống phục vụ "
        "chuyên biệt cho 3 nhóm vai trò người dùng nghiệp vụ:"
    )
    p_roles = doc.add_paragraph()
    p_roles.paragraph_format.left_indent = Inches(0.2)
    p_roles.add_run("• Nhân viên kỹ thuật (TECH_STAFF): ").font.bold = True
    p_roles.add_run("Tra cứu tồn kho tức thời; lập lệnh xuất kho (OUT) bắt buộc kèm mã phiếu bảo hành hợp lệ; hoàn trả linh kiện (RETURN) khi không sử dụng hết.\n")
    p_roles.add_run("• Nhân viên vật tư (MATERIAL_STAFF): ").font.bold = True
    p_roles.add_run("Tiếp nhận và lập phiếu nhập kho (IN) từ nhà cung cấp; quản lý danh mục và thông số 40 loại linh kiện.\n")
    p_roles.add_run("• Quản lý kho (MANAGER): ").font.bold = True
    p_roles.add_run("Giám sát Dashboard 4 chỉ số KPI thời gian thực; thiết lập ngưỡng an toàn (min_threshold); tra cứu nhật ký sổ cái bất biến; quản trị toàn diện tài khoản nhân sự cấp dưới.")

    doc.add_heading("Đánh giá mức độ hoàn thành các hạng mục", level=2)
    doc.add_paragraph(
        "Hệ thống đã hoàn thành 100% các yêu cầu cốt lõi của Bài tập 2: Hiện thực 5 quy tắc kho (BR-01..BR-05), "
        "thuật toán Optimistic Locking chống race condition; xác thực JWT và OTP 10 phút; hoàn thành tiêu chí SE S1 "
        "với đủ 4 thao tác CRUD (bao gồm cả thao tác xóa DELETE có ràng buộc bảo vệ) cho 2 thực thể cốt lõi (part và users); "
        "đóng gói Docker Compose chạy được ngay; bộ kiểm thử tự động đạt 67/67 test cases PASS 100%."
    )

    # ==============================================================================
    # MỤC 2: KIẾN TRÚC ĐÃ HIỆN THỰC (1 TRANG)
    # ==============================================================================
    h2 = doc.add_paragraph()
    r = h2.add_run("MỤC 2: KIẾN TRÚC ĐÃ HIỆN THỰC")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(30, 64, 175)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Hệ thống áp dụng kiến trúc phân lớp Clean Architecture theo chuẩn Track Software Engineering (SE), "
        "tuân thủ nguyên tắc phụ thuộc một chiều từ ngoài vào trong:"
    )

    # Bảng ánh xạ thư mục
    map_table = doc.add_table(rows=7, cols=3)
    headers = ["Thư mục / Tệp mã nguồn", "Tầng kiến trúc (SE Layer)", "Trách nhiệm & Nhiệm vụ nghiệp vụ"]
    for j, h in enumerate(headers):
        map_table.rows[0].cells[j].text = h
    
    mapping_rows = [
        ("src/app.py", "Entry Point", "Khởi tạo FastAPI, cấu hình CORS, mount UI tĩnh và Exception Handler."),
        ("src/errors/AppError.py", "Exceptions", "Định nghĩa AppError chuẩn hóa, ngăn chặn 100% lộ lỗi 500."),
        ("src/routes/inventory.routes.py", "Routing / Controller", "Tiếp nhận HTTP request, giải mã JWT, phân quyền và định dạng JSON."),
        ("src/validators/inventory.validator.py", "Input Validator", "Kiểm định payload, bắt buộc mã chứng từ (BR-02), kiểm tra biên dữ liệu."),
        ("src/services/inventory.service.py", "Domain Service", "Thực thi thuật toán kho, trừ tồn kho nguyên tử, kiểm tra ngưỡng và CRUD."),
        ("src/repositories/inventory.repository.py", "Data Repository", "Đọc/ghi CSDL MongoDB qua PyMongo, tích hợp Fallback InMemory.")
    ]
    for idx, (col1, col2, col3) in enumerate(mapping_rows):
        row = map_table.rows[idx+1]
        row.cells[0].text = col1
        row.cells[1].text = col2
        row.cells[2].text = col3
    
    style_table(map_table, [Inches(2.2), Inches(1.8), Inches(2.7)])

    # Ảnh kiến trúc thực tế
    arch_img = os.path.join(screenshots_dir, "kientruc_thucte.png")
    if os.path.exists(arch_img):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        run_img = p_img.add_run()
        run_img.add_picture(arch_img, width=Inches(5.6))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Hình 2.1: Sơ đồ Kiến trúc Phân lớp Thực tế (Layered Clean Architecture)")
        r_cap.font.italic = True
        r_cap.font.size = Pt(8.5)
        r_cap.font.color.rgb = RGBColor(107, 114, 128)

    doc.add_page_break()

    # ==============================================================================
    # MỤC 3: MODULE CỐT LÕI (1 - 2 TRANG)
    # ==============================================================================
    h3 = doc.add_paragraph()
    r = h3.add_run("MỤC 3: MODULE CỐT LÕI")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(30, 64, 175)
    h3.paragraph_format.space_before = Pt(8)
    h3.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Module cốt lõi của hệ thống thực thi trọn vẹn 5 quy tắc nghiệp vụ kho (BR) và thuật toán kiểm soát tương tranh:"
    )
    p_br = doc.add_paragraph()
    p_br.paragraph_format.left_indent = Inches(0.15)
    p_br.add_run("• BR-01 (Chống âm kho): ").font.bold = True
    p_br.add_run("Kiểm tra tồn kho trước khi xuất; nếu Q_xuất > Q_tồn thì từ chối ngay với mã lỗi 400 ERR_NEGATIVE_STOCK.\n")
    p_br.add_run("• BR-02 (Bắt buộc chứng từ): ").font.bold = True
    p_br.add_run("Mọi giao dịch OUT hoặc RETURN bắt buộc có ticket_id hợp lệ của phiếu đang xử lý; nếu không có thì từ chối 422.\n")
    p_br.add_run("• BR-03 (Bất biến sổ cái): ").font.bold = True
    p_br.add_run("Lịch sử giao dịch part_transaction chỉ ghi nhận thêm (Insert-only), tuyệt đối không có API sửa hay xóa.\n")
    p_br.add_run("• BR-04 (Cách ly chi nhánh): ").font.bold = True
    p_br.add_run("Mọi truy vấn gắn chặt với center_id trong JWT; người dùng chi nhánh này không xem hay sửa được kho chi nhánh khác.\n")
    p_br.add_run("• BR-05 (Ngưỡng an toàn): ").font.bold = True
    p_br.add_run("Tự động đánh giá cờ WARNING nếu tồn kho <= min_threshold; NORMAL nếu tồn kho an toàn.\n")
    p_br.add_run("• Optimistic Locking (EX-05): ").font.bold = True
    p_br.add_run("Sử dụng trường version tăng dần; từ chối và báo lỗi 409 nếu dữ liệu bị thay đổi giữa thời điểm đọc và ghi.")

    doc.add_heading("Hiện thực tiêu chí SE S1: Đầy đủ 4 thao tác CRUD cho >= 2 thực thể", level=2)
    doc.add_paragraph(
        "Khắc phục trực tiếp nhận xét của Giảng viên (chưa có thao tác xóa), hệ thống đã bổ sung đầy đủ 4 thao tác "
        "CRUD bao gồm thao tác xóa DELETE có ràng buộc bảo vệ cho 2 thực thể:"
    )

    crud_table = doc.add_table(rows=9, cols=4)
    crud_headers = ["Thực thể", "CRUD", "Endpoint API & Method", "Phân quyền & Ràng buộc an toàn"]
    for j, h in enumerate(crud_headers):
        crud_table.rows[0].cells[j].text = h
    
    crud_rows = [
        ("part (Linh kiện)", "Create", "POST /api/v1/inventory/parts", "MANAGER / MATERIAL; khởi tạo tồn kho 0 cái."),
        ("part (Linh kiện)", "Read", "GET /api/v1/inventory/parts/{part_code}", "Authenticated; tra cứu chi tiết thông số linh kiện."),
        ("part (Linh kiện)", "Update", "PUT /api/v1/inventory/parts/{part_code}", "MANAGER / MATERIAL; cập nhật tên, nhà cung cấp, ngưỡng."),
        ("part (Linh kiện)", "Delete", "DELETE /api/v1/inventory/parts/{part_code}", "MANAGER only; RÀNG BUỘC: Cấm xóa nếu tồn kho > 0."),
        ("users (Nhân sự)", "Create", "POST /api/v1/inventory/users", "MANAGER only; tạo nhân sự cấp dưới, băm SHA-256."),
        ("users (Nhân sự)", "Read", "GET /api/v1/inventory/users/{email}", "MANAGER / Owner; tra cứu chi tiết hồ sơ (không lộ hash)."),
        ("users (Nhân sự)", "Update", "PUT /api/v1/inventory/users/{email}", "MANAGER only; cập nhật họ tên, vai trò, trạng thái."),
        ("users (Nhân sự)", "Delete", "DELETE /api/v1/inventory/users/{email}", "MANAGER only; RÀNG BUỘC: Không được tự xóa chính mình.")
    ]
    for idx, (c1, c2, c3, c4) in enumerate(crud_rows):
        row = crud_table.rows[idx+1]
        row.cells[0].text = c1
        row.cells[1].text = c2
        row.cells[2].text = c3
        row.cells[3].text = c4
    
    style_table(crud_table, [Inches(1.5), Inches(0.8), Inches(2.3), Inches(2.1)])

    # Ảnh minh chứng giao diện
    tech_img = os.path.join(screenshots_dir, "ui_kythuat_xuatkho.png")
    if os.path.exists(tech_img):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        run_img = p_img.add_run()
        run_img.add_picture(tech_img, width=Inches(5.4))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Hình 3.1: Giao diện Tra cứu & Xuất/Hoàn kho của Nhân viên kỹ thuật")
        r_cap.font.italic = True
        r_cap.font.size = Pt(8.5)
        r_cap.font.color.rgb = RGBColor(107, 114, 128)

    doc.add_page_break()

    # ==============================================================================
    # MỤC 4: BỘ KIỂM THỬ (1 TRANG)
    # ==============================================================================
    h4 = doc.add_paragraph()
    r = h4.add_run("MỤC 4: BỘ KIỂM THỬ")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(30, 64, 175)
    h4.paragraph_format.space_before = Pt(8)
    h4.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Bộ kiểm thử tự động được xây dựng bằng Pytest, bao gồm 67 ca kiểm thử tự động chạy PASS 100% "
        "bằng đúng 1 lệnh duy nhất (pytest tests/ -v). Hệ thống bao phủ 3 nhóm trường hợp kiểm thử đại diện:"
    )
    p_cases = doc.add_paragraph()
    p_cases.paragraph_format.left_indent = Inches(0.15)
    p_cases.add_run("1. Luồng đúng (Happy Path): ").font.bold = True
    p_cases.add_run("Kỹ thuật viên tra cứu và xuất kho thành công; tồn kho giảm chính xác; ghi nhật ký OUT; HTTP 201 Created.\n")
    p_cases.add_run("2. Luồng vi phạm nghiệp vụ (Negative Cases): ").font.bold = True
    p_cases.add_run("Xuất quá tồn kho (BR-01, lỗi 400); thiếu mã chứng từ (BR-02, lỗi 422); xóa linh kiện đang có tồn kho > 0 (lỗi 400).\n")
    p_cases.add_run("3. Luồng phân quyền và bảo mật (Security & RBAC): ").font.bold = True
    p_cases.add_run("Kỹ thuật viên cố tình gọi API xóa bị từ chối 403; Quản lý tự xóa mình bị từ chối 400; mật khẩu không bao giờ lộ dạng thô.")

    # Bảng tổng kết test
    test_table = doc.add_table(rows=7, cols=3)
    test_headers = ["Tệp kiểm thử", "Mục tiêu kiểm thử & Tiêu chuẩn bao phủ", "Kết quả thực thi"]
    for j, h in enumerate(test_headers):
        test_table.rows[0].cells[j].text = h
    
    test_rows = [
        ("tests/inventory.service.test.py", "Quy tắc cốt lõi BR-01, BR-02, BR-05, cập nhật ngưỡng an toàn", "7/7 PASSED"),
        ("tests/inventory.routes.test.py", "Hợp đồng API kho, giải mã JWT, bắt lỗi nghiệp vụ chuẩn", "6/6 PASSED"),
        ("tests/auth_and_user.test.py", "Xác thực JWT, OTP 10 phút, đổi mật khẩu, quản lý nhân sự", "15/15 PASSED"),
        ("tests/bt3_specification_and_constraints.test.py", "Kiểm thử biên 2 phía, Optimistic Locking, bảo mật S3, C8", "13/13 PASSED"),
        ("tests/cross_role_and_ui.test.py", "Luồng phối hợp liên vai trò và toàn vẹn giao diện", "15/15 PASSED"),
        ("tests/se_s1_crud.test.py", "[MỚI - S1] Đầy đủ 4 thao tác CRUD cho 2 thực thể part & users", "11/11 PASSED")
    ]
    for idx, (t1, t2, t3) in enumerate(test_rows):
        row = test_table.rows[idx+1]
        row.cells[0].text = t1
        row.cells[1].text = t2
        row.cells[2].text = t3
    
    style_table(test_table, [Inches(2.5), Inches(3.2), Inches(1.0)])

    # Ảnh kết quả test PASS
    test_img = os.path.join(screenshots_dir, "test_pytest_pass.png")
    if os.path.exists(test_img):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        run_img = p_img.add_run()
        run_img.add_picture(test_img, width=Inches(5.4))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Hình 4.1: Kết quả thực thi bộ kiểm thử tự động (67/67 Test Cases PASSED 100%)")
        r_cap.font.italic = True
        r_cap.font.size = Pt(8.5)
        r_cap.font.color.rgb = RGBColor(107, 114, 128)

    # ==============================================================================
    # MỤC 5: MODULE MỞ RỘNG / TRÌNH BÀY KẾT QUẢ (1 - 2 TRANG)
    # ==============================================================================
    h5 = doc.add_paragraph()
    r = h5.add_run("MỤC 5: MODULE MỞ RỘNG / TRÌNH BÀY KẾT QUẢ")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(30, 64, 175)
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Giao diện người dùng được xây dựng theo kiến trúc Single Page Application (SPA), phong cách Dark 3D "
        "với font chữ chuẩn Be Vietnam Pro. Giao diện được xử lý chuẩn mực cả BA trạng thái dữ liệu:"
    )
    p_states = doc.add_paragraph()
    p_states.paragraph_format.left_indent = Inches(0.15)
    p_states.add_run("1. Trạng thái Đang tải (Loading State): ").font.bold = True
    p_states.add_run("Hiển thị khung xương skeleton và thanh trạng thái đồng bộ mượt mà khi nạp dữ liệu từ máy chủ.\n")
    p_states.add_run("2. Trạng thái Rỗng (Empty State): ").font.bold = True
    p_states.add_run("Hiển thị biểu tượng trực quan và thông điệp tích cực khi không có cảnh báo cạn kho hoặc bộ lọc rỗng.\n")
    p_states.add_run("3. Trạng thái Lỗi (Error State): ").font.bold = True
    p_states.add_run("Hiển thị dòng chữ thông báo lỗi màu đỏ nổi bật ngay dưới biểu mẫu kèm hướng dẫn xử lý tiếng Việt.")

    # 3 ảnh trạng thái giao diện
    states = [
        ("ui_loading_state.png", "Hình 5.1: Trạng thái Đang tải (Loading State) khi đồng bộ dữ liệu"),
        ("ui_empty_state.png", "Hình 5.2: Trạng thái Rỗng (Empty State) khi kho vận hành tối ưu không có cảnh báo"),
        ("ui_error_state.png", "Hình 5.3: Trạng thái Lỗi (Error State) khi người dùng vi phạm quy tắc xuất kho âm")
    ]
    for fn, caption in states:
        im_path = os.path.join(screenshots_dir, fn)
        if os.path.exists(im_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(4)
            run_img = p_img.add_run()
            run_img.add_picture(im_path, width=Inches(4.6))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_cap = p_cap.add_run(caption)
            r_cap.font.italic = True
            r_cap.font.size = Pt(8.0)
            r_cap.font.color.rgb = RGBColor(107, 114, 128)

    doc.add_page_break()

    # ==============================================================================
    # MỤC 6: CÁCH DỰNG LẠI HỆ THỐNG (0.5 TRANG)
    # ==============================================================================
    h6 = doc.add_paragraph()
    r = h6.add_run("MỤC 6: CÁCH DỰNG LẠI HỆ THỐNG")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(30, 64, 175)
    h6.paragraph_format.space_before = Pt(8)
    h6.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Hệ thống cho phép tái lập trọn vẹn từ máy trắng bằng đúng 1 lệnh duy nhất thông qua Docker Compose "
        "hoặc 2 lệnh qua môi trường Python cục bộ:"
    )

    p_cmd = doc.add_paragraph()
    p_cmd.paragraph_format.left_indent = Inches(0.2)
    p_cmd.add_run("# Cách 1: Khởi chạy bằng Docker Compose (Khuyên dùng - Đúng 1 lệnh duy nhất):\n").font.italic = True
    r_code1 = p_cmd.add_run("docker compose up --build -d\n\n")
    r_code1.font.bold = True
    r_code1.font.color.rgb = RGBColor(30, 64, 175)
    p_cmd.add_run("# Cách 2: Khởi chạy trực tiếp trên môi trường Python Local (2 lệnh):\n").font.italic = True
    p_cmd.add_run("pip install -r requirements.txt\n")
    r_code2 = p_cmd.add_run("python src/app.py\n")
    r_code2.font.bold = True
    r_code2.font.color.rgb = RGBColor(30, 64, 175)

    doc.add_paragraph(
        "Sau khi khởi chạy thành công, truy cập giao diện tại http://localhost:8000 và tài liệu API tại http://localhost:8000/docs. "
        "Hệ thống đã nạp sẵn 3 tài khoản chuyên biệt theo từng vai trò (RBAC):"
    )

    acc_table = doc.add_table(rows=4, cols=3)
    acc_headers = ["Vai trò người dùng", "Email đăng nhập", "Mật khẩu mẫu"]
    for j, h in enumerate(acc_headers):
        acc_table.rows[0].cells[j].text = h
    
    acc_rows = [
        ("Quản lý kho (MANAGER)", "lethithuyngan985@gmail.com", "Le090805!"),
        ("Nhân viên vật tư (MATERIAL_STAFF)", "huynhnguyenbaongoc2k5@gmail.com", "Huynh120905!"),
        ("Nhân viên kỹ thuật (TECH_STAFF)", "vuthelong1009@gmail.com", "Vu100905!")
    ]
    for idx, (a1, a2, a3) in enumerate(acc_rows):
        row = acc_table.rows[idx+1]
        row.cells[0].text = a1
        row.cells[1].text = a2
        row.cells[2].text = a3
    
    style_table(acc_table, [Inches(2.5), Inches(2.6), Inches(1.6)])

    # ==============================================================================
    # MỤC 7: THAY ĐỔI SO VỚI THIẾT KẾ BÀI TẬP 1 & TIẾP THU NHẬN XÉT (0.5 TRANG)
    # ==============================================================================
    h7 = doc.add_paragraph()
    r = h7.add_run("MỤC 7: THAY ĐỔI SO VỚI THIẾT KẾ BÀI TẬP 1 & TIẾP THU NHẬN XÉT")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(30, 64, 175)
    h7.paragraph_format.space_before = Pt(14)
    h7.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Bảng tổng hợp tiếp thu phản hồi nhận xét của Giảng viên hướng dẫn về Bài tập 2 và các hành động khắc phục hoàn thiện:"
    )

    fb_table = doc.add_table(rows=6, cols=3)
    fb_headers = ["Mã", "Nội dung nhận xét của Giảng viên về BT2", "Hành động khắc phục & Kết quả hoàn thiện"]
    for j, h in enumerate(fb_headers):
        fb_table.rows[0].cells[j].text = h
    
    fb_rows = [
        ("KH-01", "Git Tag v0.2 trỏ nhầm commit BT3 sau ngày nộp.", "Trỏ lại v0.2 về đúng commit nộp 29/10/2026 (e6698d5), push -f lên GitHub."),
        ("KH-02", "Báo cáo 81 trang do dán mã nguồn thô; mục lục lỗi bookmark.", "Tái cấu trúc báo cáo 8 trang chuẩn 7 mục; lược bỏ toàn bộ mã thô; sửa lỗi bookmark."),
        ("KH-03", "API chưa đủ 4 thao tác CRUD (thiếu thao tác xóa).", "Hiện thực đủ CRUD có thao tác XÓA cho cả 2 thực thể: part và users (Tiêu chí S1)."),
        ("KH-04", "Mục kiểm chứng (Bảng 4.2) chưa đạt tiêu chí SE S1.", "Bổ sung test suite tests/se_s1_crud.test.py gồm 11 tests PASS 100%."),
        ("KH-05", "Đồng bộ hợp đồng API và tài liệu thay đổi.", "Hợp nhất docs/thay-doi-thiet-ke.md và xuất lại OpenAPI JSON (22 endpoints).")
    ]
    for idx, (f1, f2, f3) in enumerate(fb_rows):
        row = fb_table.rows[idx+1]
        row.cells[0].text = f1
        row.cells[1].text = f2
        row.cells[2].text = f3
    
    style_table(fb_table, [Inches(0.8), Inches(2.9), Inches(3.0)])

    doc.add_page_break()

    # ==============================================================================
    # PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI (BẮT BUỘC)
    # ==============================================================================
    h_app = doc.add_paragraph()
    r = h_app.add_run("PHỤ LỤC BẮT BUỘC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI")
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(30, 64, 175)
    h_app.paragraph_format.space_before = Pt(8)
    h_app.paragraph_format.space_after = Pt(6)

    ai_table = doc.add_table(rows=4, cols=4)
    ai_headers = ["Công cụ AI sử dụng", "Mục đích sử dụng cụ thể", "Phạm vi kết quả do AI tạo ra", "Đánh giá, hiệu chỉnh & kiểm chứng của sinh viên"]
    for j, h in enumerate(ai_headers):
        ai_table.rows[0].cells[j].text = h
    
    ai_rows = [
        ("Antigravity AI (Google DeepMind)", "Hỗ trợ sinh khung mã nguồn phân lớp FastAPI, cấu hình Docker Compose và gợi ý kịch bản test case.", "Khung ban đầu của các tệp routes, services, repositories và docker-compose.yml.", "Sinh viên trực tiếp tái cấu trúc mã nguồn theo Clean Architecture, bổ sung thuật ngữ tiếng Việt, thiết lập Fallback In-Memory và viết các quy tắc BR-01..05."),
        ("ChatGPT (OpenAI GPT-4o)", "Tham khảo cú pháp kiểm thử Pytest TestClient và giải thuật Optimistic Locking với trường version.", "Gợi ý đoạn mã mẫu về cách bắt ngoại lệ AppError và logic so sánh version.", "Sinh viên kiểm tra tính đúng đắn với CSDL MongoDB 7.0, tự viết các test case kiểm tra xung đột đồng thời và chạy xác minh thực tế 100% PASS."),
        ("Claude (Anthropic 3.5 Sonnet)", "Soát lỗi chính tả tài liệu kỹ thuật và hỗ trợ dịch thuật phần mô tả API sang tiếng Anh.", "Dự thảo bản nháp phần mô tả tiếng Anh trong deployment-guide.md và api-docs/README.md.", "Sinh viên rà soát lại toàn bộ câu từ, chỉnh sửa thuật ngữ chuyên ngành kho viễn thông đảm bảo chính xác và đồng bộ với SRS.")
    ]
    for idx, (a1, a2, a3, a4) in enumerate(ai_rows):
        row = ai_table.rows[idx+1]
        row.cells[0].text = a1
        row.cells[1].text = a2
        row.cells[2].text = a3
        row.cells[3].text = a4
    
    style_table(ai_table, [Inches(1.5), Inches(1.8), Inches(1.8), Inches(1.6)])

    p_camdoan = doc.add_paragraph()
    p_camdoan.paragraph_format.space_before = Pt(14)
    p_camdoan.add_run(
        "Tôi xin cam đoan toàn bộ nội dung khai báo sử dụng công cụ Trí tuệ Nhân tạo (AI) nêu trên là hoàn toàn trung thực. "
        "Toàn bộ mã nguồn, cấu hình hệ thống và dữ liệu kiểm thử đã được tôi trực tiếp kiểm tra, tinh chỉnh và chạy kiểm thử "
        "thành công trên môi trường thực tế."
    ).font.italic = True

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(10)
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sig = p_sig.add_run("TP. Hồ Chí Minh, ngày 12 tháng 11 năm 2026\nSinh viên thực hiện\n(Đã ký)\n\nHuỳnh Nguyễn Bảo Ngọc")
    r_sig.font.bold = True

    # Lưu tài liệu ra cả 2 thư mục
    out_path_docs = os.path.join(base_dir, "docs", "BT2_2374802010339_HuynhNguyenBaoNgoc_Chuan7Muc.docx")
    out_path_tailieu = os.path.join(os.path.dirname(base_dir), "Tailieu", "BT2_2374802010339_HuynhNguyenBaoNgoc_Chuan7Muc.docx")
    
    doc.save(out_path_docs)
    print(f"Saved: {out_path_docs}")
    if os.path.exists(os.path.dirname(out_path_tailieu)):
        doc.save(out_path_tailieu)
        print(f"Saved: {out_path_tailieu}")

if __name__ == "__main__":
    build_bt2_docx()
