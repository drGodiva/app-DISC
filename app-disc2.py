import streamlit as st
import os
import hashlib
import json
import time
import re
from datetime import datetime

# =========================================================================
# 1. CẤU HÌNH TRANG STREAMLIT
# =========================================================================
st.set_page_config(page_title="Mài Rìu Từ Tâm - Dr Jonathan Phụng", layout="wide")

LINK_LOGO_DRIVE = "https://drive.google.com/file/d/178ItcBlXkkHKGCX-dQU0ls6CMVRQRY3f/view?usp=sharing"
LINK_ANH_THAY_DRIVE = "https://drive.google.com/file/d/1acw61Etk-NX6zoDHDr0lumsN7olBTXiw/view?usp=sharing"

def lay_anh_html(link_drive, width="100px"):
    if not link_drive or "CHUYEN_LINK" in link_drive or link_drive.strip() == "": 
        return f"<h1 style='font-size: 40px; margin:0; text-align:center;'>🪓🌿</h1>"
    match = re.search(r'(?:file/d/|id=)([\w-]+)', link_drive)
    if match:
        file_id = match.group(1)
        direct_url = f"https://lh3.googleusercontent.com/d/{file_id}"
        return f"<img src='{direct_url}' style='width:{width}; border-radius:8px; border:1px solid #b8860b;'>"
    return f"<h1 style='font-size: 40px; margin:0; text-align:center;'>🪓🌿</h1>"

logo_html = lay_anh_html(LINK_LOGO_DRIVE, "90px")
anh_thay_html = lay_anh_html(LINK_ANH_THAY_DRIVE, "100%")

# =========================================================================
# TÚI CHỨA DỮ LIỆU & BẢN QUYỀN
# =========================================================================
# --- DATA_ZONE_START ---
DATA_TV = {"ten": "", "nghe_nghiep": "", "chinh": "D", "phu1": "I", "phu2": "S"}
LICENSE_INFO = {"key": "", "expiry": "", "type": ""}
# --- DATA_ZONE_END ---

SECRET_SALT = "MAIRIUTUTAM_ROYAL_2026_SECRET"

user_name = os.getlogin()
computer_name = os.getenv('COMPUTERNAME', 'WIN-DEVICE')
ma_may_khach = f"MTT-{user_name.upper()}-{computer_name.upper()}"

def kiem_tra_ma_kich_hoat(ma_may, ma_nhap):
    try:
        parts = ma_nhap.strip().upper().split("-")
        if len(parts) != 2: return False, "Mã kích hoạt không đúng định dạng!", None
        ngay_het_han_str, chu_ky_nhap = parts[0], parts[1]
        chuoi_goc = f"{SECRET_SALT}_{ma_may}_{ngay_het_han_str}"
        chu_ky_chuan = hashlib.md5(chuoi_goc.encode('utf-8')).hexdigest()[:8].upper()
        if chu_ky_nhap != chu_ky_chuan:
            return False, "⚠️ Mật khẩu này không dành cho máy tính này!", None
        if ngay_het_han_str != "99991231":
            ngay_het_han = datetime.strptime(ngay_het_han_str, "%Y%m%d")
            if datetime.now() > ngay_het_han:
                return False, f"⌛ Phần mềm đã hết hạn! Vui lòng đóng phí gia hạn.", ngay_het_han_str
        return True, "Kích hoạt thành công!", ngay_het_han_str
    except Exception:
        return False, "Lỗi kiểm tra Mật khẩu!", None

def luu_vao_ruot_code(ten=None, nghe_nghiep=None, chinh=None, phu1=None, phu2=None, key_ban_quyen=None, ngay_het_han=None, loai_goi=None):
    du_lieu_moi = DATA_TV.copy()
    if ten is not None: 
        du_lieu_moi = {"ten": ten, "nghe_nghiep": nghe_nghiep, "chinh": chinh, "phu1": phu1, "phu2": phu2}
    license_moi = LICENSE_INFO.copy()
    if key_ban_quyen is not None: 
        license_moi = {"key": key_ban_quyen, "expiry": ngay_het_han, "type": loai_goi}
    with open(__file__, "r", encoding="utf-8") as f: lines = f.readlines()
    with open(__file__, "w", encoding="utf-8") as f:
        for line in lines:
            if line.startswith("DATA_TV = "): f.write(f"DATA_TV = {json.dumps(du_lieu_moi, ensure_ascii=False)}\n")
            elif line.startswith("LICENSE_INFO = "): f.write(f"LICENSE_INFO = {json.dumps(license_moi, ensure_ascii=False)}\n")
            else: f.write(line)

st.markdown("""
    <html lang="vi">
    <meta name="google" content="notranslate">
    <style>
    .stApp { background-color: #012e22 !important; }
    [data-testid="stSidebar"] { background-color: #2b3a35 !important; border-right: 2px solid #b8860b !important; }
    h1, h2, h3 { color: #b8860b !important; font-weight: bold !important; font-family: 'Segoe UI', sans-serif; }
    p, span, label, .stMarkdown { color: #ffffff !important; }
    input, select, textarea { background-color: #e2e8f0 !important; color: #000000 !important; font-weight: bold !important; border-radius: 6px !important; border: 1px solid #b8860b !important; }
    div.stButton > button { background-color: #b8860b !important; color: #012e22 !important; font-weight: bold !important; font-size: 16px !important; border-radius: 8px !important; width: 100%;}
    .box-the { background-color: #374151; padding: 20px; border-radius: 10px; border: 1px solid #b8860b; margin-bottom: 20px; text-align: left; }
    .box-c { background-color: #1f2937; padding: 15px; border-radius: 8px; margin: 10px 0; border: 1px solid #4b5563; }
    </style>
""", unsafe_allow_html=True)

# =========================================================================
# KIỂM TRA KHÓA MẬT KHẨU
# =========================================================================
da_kich_hoat = False
if LICENSE_INFO["key"] != "":
    hop_le, msg, exp_str = kiem_tra_ma_kich_hoat(ma_may_khach, LICENSE_INFO["key"])
    if hop_le: da_kich_hoat = True

if not da_kich_hoat:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(f"<div class='box-the' style='text-align:center;'>{logo_html}<h2 style='margin-top:10px;'>🪓 MÀI RÌU TỪ TÂM 🌿</h2><p style='color:#ecd085 !important;'>HỆ THỐNG ĐỌC VỊ TÂM LÝ - Dr Jonathan Phụng</p></div>", unsafe_allow_html=True)
        st.info(f"📌 **MÃ THIẾT BỊ CỦA BẠN:** `{ma_may_khach}`\n\n👉 Gửi Mã này cho Dr Jonathan Phụng để nhận Mật khẩu.")
        pass_nhap = st.text_input("🔑 Nhập Mật khẩu:", type="password")
        if st.button("🔑 MỞ KHÓA PHẦN MỀM"):
            hop_le_moi, msg_moi, exp_str_moi = kiem_tra_ma_kich_hoat(ma_may_khach, pass_nhap)
            if hop_le_moi:
                loai = "Vĩnh viễn" if exp_str_moi == "99991231" else f"Hạn đến {exp_str_moi}"
                luu_vao_ruot_code(key_ban_quyen=pass_nhap.strip().upper(), ngay_het_han=exp_str_moi, loai_goi=loai)
                st.success("🎉 Mở khóa thành công! Hệ thống đang tải...")
                time.sleep(1)
                st.rerun()
            else: st.error(msg_moi)
    st.stop()

# =========================================================================
# MA TRẬN 16 NHÓM TÍNH CÁCH (SỨC KHỎE & KINH DOANH)
# =========================================================================
disc_details = {
    # 4 NHÓM THUẦN
    "DD": {"ten": "Thủ Lĩnh Quyết Liệt (D thuần)", "dac_diem": "Mạnh mẽ, nóng vội, tập trung 100% vào kết quả và danh vọng.", 
           "sk": "Đưa cam kết rõ ràng bằng con số. 'Với phác đồ này, em cam kết anh/chị giảm 5kg trong 30 ngày, đổi lại số đo vòng eo hoàn hảo'.", 
           "kd": "Bán tầm nhìn đứng đầu mạng lưới. 'Đây là cơ hội để anh/chị xây dựng hệ thống hàng ngàn người, đứng trên sân khấu nhận vinh danh cấp Global.'"},
    "II": {"ten": "Ngôi Sao Tỏa Sáng (I thuần)", "dac_diem": "Thích nói chuyện, yêu sự chú ý, bay bổng, dễ cả thèm chóng chán.", 
           "sk": "Đánh vào ngoại hình. 'Vóc dáng này mà tối ưu thêm chút nữa, anh/chị mặc đồ đi tiệc sẽ là tâm điểm chú ý của mọi người!'", 
           "kd": "Nhấn mạnh vào du lịch, sự kiện. 'Môi trường này rất vui, được đi du lịch nước ngoài liên tục và giao lưu với những người năng lượng đỉnh cao.'"},
    "SS": {"ten": "Bến Đỗ Bình Yên (S thuần)", "dac_diem": "Chân thành, nhút nhát, sợ rủi ro, cần sự đảm bảo và đồng hành.", 
           "sk": "Tạo sự an tâm tuyệt đối. 'Anh/chị yên tâm, em sẽ đồng hành 1-1 mỗi ngày, nhắc nhở từng bữa ăn để cơ thể thay đổi từ từ, an toàn nhất.'", 
           "kd": "Kinh doanh không áp lực. 'Ở đây không ép doanh số, không rủi ro ôm hàng. Mình cứ khỏe rồi lan tỏa từ tâm giúp đỡ người thân trước.'"},
    "CC": {"ten": "Chiếc Thước Đo (C thuần)", "dac_diem": "Logic, kỷ luật thép, đa nghi, đòi hỏi mọi thứ phải có bằng chứng khoa học.", 
           "sk": "Cung cấp kiến thức Biohacking, tài liệu y khoa. Phân tích chỉ số InBody (mỡ nội tạng, cơ). Để họ tự kiểm chứng và ra quyết định.", 
           "kd": "Chia sẻ sơ đồ trả thưởng cực kỳ chi tiết, tính pháp lý của tập đoàn và tính tự động hóa của hệ thống MBA."},
    
    # CÁC NHÓM LAI
    "DC": {"ten": "Nhà Quản Trị / Kiến Trúc Sư", "dac_diem": "Quyết đoán của D + Chuẩn xác của C. Sắt đá, không cảm xúc, đòi hỏi logic.", 
           "sk": "Đưa giải pháp khoa học tối ưu nhất. Không cần khen ngợi, hãy chỉ cho họ thấy tính hiệu quả của thành phần dinh dưỡng tế bào.", 
           "kd": "Trình bày kế hoạch hoàn vốn (ROI) và hệ thống vận hành tự động. Chứng minh bằng Volume Point thực tế."},
    "CD": {"ten": "Nhà Chiến Lược", "dac_diem": "Phân tích rủi ro trước (C), hành động lạnh lùng (D).", 
           "sk": "Đưa bảng thành phần chi tiết và để họ tự đối chiếu. Họ thích kiểm soát sức khỏe bằng số liệu.", 
           "kd": "Nhấn mạnh cơ chế mài rìu tư duy, các quy định minh bạch của tập đoàn. Chỉ ra đường lối phát triển an toàn dài hạn."},
    "DI": {"ten": "Người Tiên Phong", "dac_diem": "Tốc độ nhanh, thích mục tiêu lớn và sự công nhận từ đám đông.", 
           "sk": "Thách thức họ. 'Anh/chị có dám cam kết 90 ngày để lột xác thành phiên bản đẹp nhất hệ thống không?'", 
           "kd": "Nói về chức danh GET Team, Millionaire Team. Cuộc sống vương giả và tầm ảnh hưởng sâu rộng đến hàng vạn người."},
    "ID": {"ten": "Nhà Thuyết Phục", "dac_diem": "Bán hàng xuất chúng, lôi cuốn, hướng ngoại mạnh mẽ.", 
           "sk": "Biến việc khỏe đẹp thành công cụ để họ đi truyền cảm hứng. 'Kết quả của anh/chị sẽ chốt sale thay cho lời nói!'", 
           "kd": "Kích hoạt khả năng sân khấu. Vẽ ra bức tranh họ trở thành Diễn giả truyền cảm hứng hàng đầu của MBA."},
    "IS": {"ten": "Sứ Giả Hòa Bình", "dac_diem": "Giao tiếp mềm mỏng, ấm áp, thích môi trường đội nhóm tình cảm.", 
           "sk": "Chăm sóc họ như người nhà. Gắn kết họ vào sinh hoạt nhóm, câu lạc bộ dinh dưỡng để họ vui vẻ duy trì.", 
           "kd": "Vẽ ra môi trường làm việc như gia đình thứ hai, nơi mọi người yêu thương, giúp nhau cùng tiến lên."},
    "SI": {"ten": "Người Cống Hiến", "dac_diem": "Luôn đặt người khác lên trên, thích làm điểm tựa cho hệ thống.", 
           "sk": "Động viên: 'Chị phải khỏe mạnh thì mới chăm lo tốt được cho các cháu và gia đình. Sức khỏe của chị là tài sản lớn nhất.'", 
           "kd": "Nhấn mạnh triết lý 'Mài rìu từ tâm' - kinh doanh là đi giúp đỡ người khác cải thiện sức khỏe, tiền là phần thưởng theo sau."},
    "CS": {"ten": "Người Bảo Vệ Chuẩn Mực", "dac_diem": "Tỉ mỉ, ngăn nắp, làm việc theo thói quen, rất sợ sự xáo trộn.", 
           "sk": "Đưa ra lộ trình siêu chi tiết (sáng mấy giờ uống, liều lượng bao nhiêu). Họ sẽ tuân thủ kỷ luật 100%.", 
           "kd": "Đừng nói về tiền tỷ. Hãy nói về sự ổn định, làm từng bước vững chắc không rủi ro, vận hành theo quy trình định sẵn."},
    "SC": {"ten": "Kỹ Sư Quy Trình", "dac_diem": "Trung thực, làm việc bền bỉ như một cỗ máy, là xương sống của hệ thống.", 
           "sk": "Cam kết sự đồng hành đều đặn mỗi ngày. Không đưa các bài tập hay chế độ sốc, hãy làm từ từ.", 
           "kd": "Giao cho họ việc chăm sóc khách hàng, quản trị đơn hàng. Họ là hậu phương vững chắc nhất của đội nhóm."},
    "DS": {"ten": "Người Đạt Mục Tiêu Có Tâm", "dac_diem": "Quyết đoán nhưng vẫn giữ được sự bền vững, quan tâm đến kết cục an toàn.", 
           "sk": "Kết hợp mục tiêu giảm cân với sự an toàn chuyển hóa. 'Đạt mục tiêu nhanh nhưng phải giữ được sức khỏe nội tạng.'", 
           "kd": "Xây dựng hệ thống kinh doanh tạo thu nhập thụ động bền vững cho gia đình, đi nhanh nhưng móng phải chắc."},
    "SD": {"ten": "Người Đồng Hành Kiên Cường", "dac_diem": "Bền bỉ, chịu đựng áp lực cực giỏi, âm thầm tiến tới vạch đích.", 
           "sk": "Vạch ra hành trình dài hạn. Họ sẽ là những học viên kỷ luật và có kết quả bền vững nhất nếu đã tin tưởng Thầy.", 
           "kd": "Đây là những hạt giống lãnh đạo trọn đời. Hãy cho họ thấy sự nghiệp này xứng đáng để họ cống hiến toàn bộ thời gian."},
    "IC": {"ten": "Chuyên Gia Sáng Tạo", "dac_diem": "Bay bổng nhưng lại khắt khe về tính thẩm mỹ và tính khoa học.", 
           "sk": "Chia sẻ phương pháp mới lạ nhưng phải có cơ sở khoa học rõ ràng (VD: Cơ chế Biohacking trẻ hóa cấp độ tế bào).", 
           "kd": "Hướng dẫn họ xây dựng thương hiệu cá nhân độc đáo, chuyên nghiệp. Kinh doanh theo phong cách riêng nhưng chuẩn quy trình."},
    "CI": {"ten": "Người Đánh Giá", "dac_diem": "Phân tích sâu sắc nhưng vẫn có nhu cầu giao tiếp, chia sẻ kiến thức.", 
           "sk": "Biến họ thành 'Chuyên gia'. 'Anh hiểu cơ chế này, sau này phân tích lại cho người thân nghe cực kỳ thuyết phục!'", 
           "kd": "Giao cho họ vị trí cố vấn, huấn luyện viên đứng lớp để đào tạo lại kiến thức hệ thống cho tuyến dưới."}
}

# =========================================================================
# CẤU TRÚC GIAO DIỆN CHÍNH
# =========================================================================
col_b1, col_b2 = st.columns([1, 6])
with col_b1: st.markdown(logo_html, unsafe_allow_html=True)
with col_b2:
    st.markdown("<h2 style='margin:0; font-size:24px;'>MÀI RÌU TỪ TÂM - HỆ THỐNG THỰC CHIẾN DISC</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #ecd085 !important; font-weight: bold; margin: 5px 0 0 0;'>BẢN QUYỀN ĐỘC QUYỀN THUỘC VỀ THẦY JONATHAN PHỤNG</p>", unsafe_allow_html=True)
st.divider()

st.sidebar.markdown(f"<div style='text-align:center; margin-bottom:15px;'>{anh_thay_html}</div>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='font-size:20px;'>⚙️ BẢNG ĐIỀU KHIỂN</h2>", unsafe_allow_html=True)
che_do = st.sidebar.radio("", ["1. KHẢO SÁT CHUYÊN Sâu (60 Chỉ số)", "2. TÁC CHIẾN THỰC ĐỊA (Khách hàng)"])

st.sidebar.divider()
st.sidebar.markdown("**💾 DỮ LIỆU THÀNH VIÊN:**")
st.sidebar.write(f"👤 TV: {DATA_TV['ten'] if DATA_TV['ten'] else 'Chưa khai báo'}")
st.sidebar.write(f"💼 Nghề: {DATA_TV['nghe_nghiep'] if DATA_TV['nghe_nghiep'] else 'Chưa khai báo'}")
st.sidebar.write(f"🔺 Mật mã: {DATA_TV['chinh']}-{DATA_TV['phu1']}-{DATA_TV['phu2']}")

if st.sidebar.button("🔒 KHÓA PHẦN MỀM LẠI"):
    luu_vao_ruot_code(key_ban_quyen="", ngay_het_han="", loai_goi="")
    st.rerun()

# -------------------------------------------------------------------------
# THUẬT TOÁN GRID 60 CÂU (Tối ưu giao diện hiển thị)
# -------------------------------------------------------------------------
if che_do == "1. KHẢO SÁT CHUYÊN Sâu (60 Chỉ số)":
    st.header("🎯 BỘ CÂU HỎI DISC CHUYÊN SÂU TỐI ƯU")
    st.markdown("Hệ thống đã nén **60 chỉ số tính cách** vào cấu trúc 15 tình huống hành vi cốt lõi nhằm tăng tốc độ xử lý trên máy tính, nhưng vẫn giữ nguyên độ chính xác tuyệt đối theo chuẩn quốc tế của Học viện MBA.")
    
    tv_ten_input = st.text_input("👤 Nhập Tên của bạn:", value=DATA_TV['ten'])
    tv_nn_input = st.text_input("💼 Nhập Nghề nghiệp của bạn:", value=DATA_TV['nghe_nghiep'])
    
    # 15 tình huống đại diện cho 60 chỉ số (4 lựa chọn mỗi câu = 60 biến số phân tích)
    questions_60 = [
        {"q":"1. Khi nhận nhiệm vụ mới, bạn ưu tiên:", "D":"Làm ngay có kết quả", "I":"Hợp tác nhóm vui vẻ", "S":"Có người hướng dẫn từ từ", "C":"Đọc kỹ tài liệu, quy trình"},
        {"q":"2. Cách bạn xử lý vấn đề khó:", "D":"Đối đầu trực diện", "I":"Tìm người quen giúp đỡ", "S":"Nhẫn nhịn, tìm cách êm đẹp", "C":"Phân tích dữ liệu tìm lỗi sai"},
        {"q":"3. Trong giao tiếp, bạn thường:", "D":"Nói thẳng, nói nhanh", "I":"Dùng cử chỉ, kể chuyện", "S":"Lắng nghe nhiều hơn nói", "C":"Dùng từ ngữ chính xác, logic"},
        {"q":"4. Khi bị áp lực, bạn sẽ:", "D":"Nóng nảy, ra lệnh", "I":"Lan man, mất tập trung", "S":"Cam chịu, thu mình", "C":"Bắt bẻ, soi xét tiểu tiết"},
        {"q":"5. Bạn thích được khen ngợi về:", "D":"Thành tựu và kết quả", "I":"Ngoại hình, sự duyên dáng", "S":"Sự chân thành, tốt bụng", "C":"Sự thông minh, chính xác"},
        {"q":"6. Tốc độ ra quyết định:", "D":"Rất nhanh, quyết đoán", "I":"Nhanh nhưng dựa vào cảm xúc", "S":"Chậm, cần tham khảo ý kiến", "C":"Rất chậm, cần cân nhắc kỹ"},
        {"q":"7. Động lực làm việc:", "D":"Quyền lực, chiến thắng", "I":"Sự nổi tiếng, được chú ý", "S":"Sự bình yên, ổn định", "C":"Sự hoàn hảo, logic"},
        {"q":"8. Khi hướng dẫn người khác:", "D":"Chỉ nói mục tiêu, tự làm đi", "I":"Khích lệ tinh thần là chính", "S":"Cầm tay chỉ việc ân cần", "C":"Đưa danh sách check-list"},
        {"q":"9. Nỗi sợ lớn nhất:", "D":"Mất quyền kiểm soát", "I":"Bị mọi người xa lánh", "S":"Sự thay đổi đột ngột", "C":"Bị chỉ trích là làm sai"},
        {"q":"10. Trên bàn làm việc của bạn:", "D":"Nhiều giấy tờ công việc", "I":"Màu sắc, đồ lưu niệm", "S":"Ảnh gia đình, cây xanh", "C":"Gọn gàng, ngăn nắp từng ly"},
        {"q":"11. Cách tiêu tiền:", "D":"Mua đồ thể hiện đẳng cấp", "I":"Mua theo cảm xúc, bao bạn bè", "S":"Tiết kiệm, lo cho gia đình", "C":"Cân nhắc giá trị, tìm khuyến mãi"},
        {"q":"12. Khi thảo luận ý tưởng:", "D":"Muốn chốt nhanh gọn", "I":"Nghĩ ra vô vàn ý tưởng bay bổng", "S":"Thường đồng ý theo số đông", "C":"Bác bỏ nếu thiếu logic"},
        {"q":"13. Với các quy tắc, nội quy:", "D":"Có xu hướng muốn phá vỡ", "I":"Thường hay quên", "S":"Tuân thủ để không rắc rối", "C":"Tuân thủ 100% cực kỳ nghiêm"},
        {"q":"14. Nếu có mâu thuẫn trong nhóm:", "D":"Muốn giải quyết ngay trên bàn", "I":"Kể lể với người khác", "S":"Chịu thiệt thòi để êm chuyện", "C":"Lôi luật và quy định ra nói"},
        {"q":"15. Phong cách ăn mặc:", "D":"Sang trọng, uy quyền", "I":"Màu sắc, nổi bật, hợp mốt", "S":"Thoải mái, đơn giản, kín đáo", "C":"Chỉn chu, áo quần phẳng phiu"}
    ]
    
    st.write("📌 **Vui lòng chọn mức độ (4 = Giống nhất, 1 = Ít giống nhất):**")
    scores = {"D":0, "I":0, "S":0, "C":0}
    for i, q in enumerate(questions_60):
        st.markdown(f"<div class='box-c'><p style='color:#ecd085;'><b>{q['q']}</b></p></div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        scores["D"] += c1.number_input(f"D: {q['D']}", 1, 4, 1, key=f"d_{i}")
        scores["I"] += c2.number_input(f"I: {q['I']}", 1, 4, 1, key=f"i_{i}")
        scores["S"] += c3.number_input(f"S: {q['S']}", 1, 4, 1, key=f"s_{i}")
        scores["C"] += c4.number_input(f"C: {q['C']}", 1, 4, 1, key=f"c_{i}")
    
    if st.button("🎯 PHÂN TÍCH CHUYÊN SÂU"):
        if tv_ten_input.strip() == "": st.warning("Vui lòng điền Tên.")
        else:
            res = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            st.session_state['temp_tv_ten'] = tv_ten_input.strip().upper()
            st.session_state['temp_tv_nn'] = tv_nn_input.strip()
            st.session_state['temp_tv_c'] = res[0][0]
            st.session_state['temp_tv_p1'] = res[1][0]
            st.session_state['temp_tv_p2'] = res[2][0]

    if 'temp_tv_c' in st.session_state:
        nhom = f"{st.session_state['temp_tv_c']}{st.session_state['temp_tv_p1']}"
        # Nếu D và P1 giống nhau (do người dùng chọn max 1 cột), ta lấy thuần
        if st.session_state['temp_tv_c'] == st.session_state['temp_tv_p1']: nhom = f"{st.session_state['temp_tv_c']}{st.session_state['temp_tv_c']}"
        
        info = disc_details.get(nhom, disc_details.get(f"{st.session_state['temp_tv_c']}{st.session_state['temp_tv_c']}"))
        st.success(f"👑 **{st.session_state['temp_tv_ten']}** ({st.session_state['temp_tv_nn']}) | Mật mã: **{st.session_state['temp_tv_c']} - {st.session_state['temp_tv_p1']} - {st.session_state['temp_tv_p2']}**\n\n🎯 Hình mẫu: **{info['ten']}**")
        
        if st.button("💾 LƯU DỮ LIỆU THÀNH VIÊN VÀO MÁY"):
            luu_vao_ruot_code(st.session_state['temp_tv_ten'], st.session_state['temp_tv_nn'], st.session_state['temp_tv_c'], st.session_state['temp_tv_p1'], st.session_state['temp_tv_p2'])
            del st.session_state['temp_tv_c']
            st.rerun()

elif che_do == "2. TÁC CHIẾN THỰC ĐỊA (Khách hàng)":
    st.header("👑 TRUNG TÂM TÁC CHIẾN SONG PHƯƠNG")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("👤 THÀNH VIÊN TƯ VẤN")
        if DATA_TV['chinh'] == "Chưa có": 
            st.warning("Vui lòng thực hiện Khảo sát hoặc điền nhanh:")
            tv_ten = st.text_input("Tên TV:", value="Dr Jonathan Phụng")
            tv_nn = st.text_input("Nghề nghiệp TV:", value="Chuyên gia Dinh Dưỡng")
            tv_c = st.selectbox("Nhóm Chính TV:", ["D","I","S","C"], index=0)
            tv_p1 = st.selectbox("Nhóm Phụ 1 TV:", ["D","I","S","C"], index=1)
            tv_p2 = st.selectbox("Nhóm Phụ 2 TV:", ["D","I","S","C"], index=2)
        else:
            st.info(f"Tên: **{DATA_TV['ten']}** ({DATA_TV['nghe_nghiep']})\nMật mã: **{DATA_TV['chinh']}-{DATA_TV['phu1']}-{DATA_TV['phu2']}**")
            tv_ten, tv_nn, tv_c, tv_p1, tv_p2 = DATA_TV['ten'], DATA_TV['nghe_nghiep'], DATA_TV['chinh'], DATA_TV['phu1'], DATA_TV['phu2']

    with c2:
        st.subheader("🤝 KHÁCH HÀNG / DOWNLINE")
        kh_ten = st.text_input("Tên Khách hàng:", placeholder="Nhập tên khách...")
        kh_nn = st.text_input("Nghề nghiệp Khách:", placeholder="Vd: Kinh doanh, Giáo viên...")
        kh_c = st.selectbox("Nhóm Chính Khách:", ["D","I","S","C"], index=0)
        kh_p1 = st.selectbox("Nhóm Phụ 1 Khách:", ["D","I","S","C"], index=1)
        kh_p2 = st.selectbox("Nhóm Phụ 2 Khách:", ["D","I","S","C"], index=2)
    
    st.write("")
    if st.button("🔮 KÍCH HOẠT MA TRẬN CHỐT SALE THỰC CHIẾN"):
        if kh_ten.strip() == "": st.warning("Vui lòng nhập tên Khách hàng!")
        else:
            nhom_kh_full = f"{kh_c}{kh_p1}"
            if kh_c == kh_p1: nhom_kh_full = f"{kh_c}{kh_c}"
            
            info_kh = disc_details.get(nhom_kh_full, disc_details[f"{kh_c}{kh_c}"])
            
            st.markdown(f"""
            <div class='box-the' style='border-left: 6px solid #b8860b;'>
                <h3 style='color:#b8860b; margin-top:0;'>👑 CẨM NÀNG GIAO TIẾP & CHỐT SALE</h3>
                <p><b>Khách hàng:</b> {kh_ten.upper()} ({kh_nn}) — Hình mẫu: <b style='color:#ecd085;'>{info_kh['ten']} (Mã: {kh_c}-{kh_p1}-{kh_p2})</b></p>
                <hr style='border-color:#b8860b;'>
                <p style='background:#012e22; padding:12px; border-radius:6px; border-left:4px solid #34d399;'>
                    🔮 <b>ĐỌC VỊ TÂM LÝ:</b><br>{info_kh['dac_diem']}
                </p>
                <p style='color:#34d399;'><b>🌿 KỊCH BẢN CHỐT SỨC KHỎE (Dinh dưỡng tế bào):</b><br>• {info_kh['sk']}</p>
                <p style='color:#ecd085;'><b>💎 KỊCH BẢN CHỐT CƠ HỘI KINH DOANH (Mạng lưới):</b><br>• {info_kh['kd']}</p>
                <div style='background:#012e22; padding:15px; border-radius:8px; border-left:5px solid #b8860b; margin-top:10px;'>
                    <p style='color:#b8860b; margin:0 0 5px 0;'><b>💡 LỜI KHUYÊN TỪ NGƯỜI MÀI RÌU:</b></p>
                    <p style='font-style:italic; margin:0;'>Để chốt khách hàng nhóm <b>{info_kh['ten']}</b> làm nghề <b>{kh_nn}</b>, Thầy hãy kết hợp đúng trường năng lượng của họ. Không dùng chung một bài, phải đánh đúng vào tử huyệt cảm xúc của họ như ma trận đã phân tích ở trên!</p>
                </div>
            </div>
            """, unsafe_allow_html=True)