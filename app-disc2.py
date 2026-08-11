import streamlit as st
import base64
import os
import hashlib
import time
from datetime import datetime

# =========================================================================
# 1. CẤU HÌNH TRANG STREAMLIT
# =========================================================================
st.set_page_config(page_title="Mài Rìu Từ Tâm - Dr Jonathan Phụng", layout="wide")

def doc_anh_tu_may_tinh(ten_file, width="100px"):
    try:
        duong_dan = ten_file
        if not os.path.exists(duong_dan):
            duong_dan = ten_file.replace('.png', '.jpg')
        if os.path.exists(duong_dan):
            with open(duong_dan, "rb") as img_file:
                b64_string = base64.b64encode(img_file.read()).decode()
            ext = duong_dan.split('.')[-1].lower()
            mime_type = f"image/{ext}" if ext in ['png', 'jpg', 'jpeg'] else "image/png"
            return f"<img src='data:{mime_type};base64,{b64_string}' style='width:{width}; border-radius:8px; border:1px solid #b8860b; object-fit: cover;'>"
    except Exception:
        pass
    return f"<h1 style='font-size: 40px; margin:0; text-align:center;'>🪓🌿</h1>"

logo_html = doc_anh_tu_may_tinh("logo.png", "90px")
anh_thay_html = doc_anh_tu_may_tinh("anh_thay.png", "100%")

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
# THUẬT TOÁN TẠO MÃ TRUY CẬP WEB RIÊNG BIỆT (BROWSER FINGERPRINT)
# =========================================================================
SECRET_SALT = "MAIRIUTUTAM_ROYAL_2026_SECRET"

# Lấy dấu vết trình duyệt để tạo mã máy định danh riêng cho từng người
headers = st.context.headers if hasattr(st, 'context') and hasattr(st.context, 'headers') else {}
user_agent = headers.get("User-Agent", "WEB_CLIENT_DEVICE")
ip_fake = headers.get("X-Forwarded-For", "UNKNOWN_IP")

hash_device = hashlib.md5(f"{user_agent}_{ip_fake}".encode('utf-8')).hexdigest()[:8].upper()
ma_may_web = f"MTT-WEB-{hash_device}"

def kiem_tra_ma_kich_hoat(ma_may, ma_nhap):
    try:
        parts = ma_nhap.strip().upper().split("-")
        if len(parts) != 2: return False, "Mã kích hoạt không đúng định dạng! (Cấu trúc: NGAYHETHAN-MACHUKY)", None
        ngay_het_han_str, chu_ky_nhap = parts[0], parts[1]
        
        chuoi_goc = f"{SECRET_SALT}_{ma_may}_{ngay_het_han_str}"
        chu_ky_chuan = hashlib.md5(chuoi_goc.encode('utf-8')).hexdigest()[:8].upper()
        
        if chu_ky_nhap != chu_ky_chuan:
            return False, "⚠️ Mật khẩu này không dành cho thiết bị/trình duyệt này!", None
            
        if ngay_het_han_str != "99991231":
            ngay_het_han = datetime.strptime(ngay_het_han_str, "%Y%m%d")
            if datetime.now() > ngay_het_han:
                return False, f"⌛ Phần mềm đã hết hạn truy cập ({ngay_het_han_str})! Vui lòng liên hệ Dr Jonathan Phụng để gia hạn.", ngay_het_han_str
        return True, "Kích hoạt thành công!", ngay_het_han_str
    except Exception:
        return False, "Lỗi kiểm tra Mật khẩu!", None

# Kiểm tra trạng thái đã mở khóa trong phiên làm việc hiện tại
if 'da_mo_khoa' not in st.session_state:
    st.session_state['da_mo_khoa'] = False
if 'key_luu' not in st.session_state:
    st.session_state['key_luu'] = ""

if not st.session_state['da_mo_khoa']:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(f"<div class='box-the' style='text-align:center;'>{logo_html}<h2 style='margin-top:10px;'>🪓 MÀI RÌU TỪ TÂM 🌿</h2><p style='color:#ecd085 !important;'>HỆ THỐNG ĐỌC VỊ TÂM LÝ - Dr Jonathan Phụng</p></div>", unsafe_allow_html=True)
        st.info(f"📌 **MÃ THIẾT BỊ WEB CỦA BẠN:** `{ma_may_web}`\n\n👉 Hãy gửi Mã thiết bị này cho Dr Jonathan Phụng để nhận Mật khẩu kích hoạt cá nhân.")
        
        pass_nhap = st.text_input("🔑 Nhập Mật khẩu Kích Hoạt:", type="password")
        if st.button("🔑 MỞ KHÓA HỆ THỐNG"):
            hop_le, msg, exp_str = kiem_tra_ma_kich_hoat(ma_may_web, pass_nhap)
            if hop_le:
                st.session_state['da_mo_khoa'] = True
                st.session_state['key_luu'] = pass_nhap.strip().upper()
                st.session_state['exp_luu'] = exp_str
                st.success("🎉 Mở khóa thành công! Đang tải cỗ máy tác chiến...")
                time.sleep(1)
                st.rerun()
            else:
                st.error(msg)
    st.stop()

# =========================================================================
# DỮ LIỆU & QUẢN LÝ PHIÊN LÀM VIỆC
# =========================================================================
if 'tv_ten' not in st.session_state:
    st.session_state['tv_ten'] = ""
    st.session_state['tv_nn'] = ""
    st.session_state['tv_c'] = "D"
    st.session_state['tv_p1'] = "I"
    st.session_state['tv_p2'] = "S"

disc_details = {
    "DD": {"ten": "Thủ Lĩnh Quyết Liệt (D thuần)", "dac_diem": "Mạnh mẽ, nóng vội, tập trung 100% vào kết quả và danh vọng.", "sk": "Đưa cam kết rõ ràng bằng con số. 'Với phác đồ này, em cam kết giảm 5kg trong 30 ngày'.", "kd": "Bán tầm nhìn đứng đầu mạng lưới, xây dựng hệ thống Global."},
    "II": {"ten": "Ngôi Sao Tỏa Sáng (I thuần)", "dac_diem": "Thích nói chuyện, yêu sự chú ý, bay bổng, dễ cả thèm chóng chán.", "sk": "Đánh vào ngoại hình, sự tỏa sáng trước đám đông.", "kd": "Nhấn mạnh vào du lịch, sự kiện vinh danh hoành tráng."},
    "SS": {"ten": "Bến Đỗ Bình Yên (S thuần)", "dac_diem": "Chân thành, nhút nhát, sợ rủi ro, cần sự đảm bảo và đồng hành.", "sk": "Tạo sự an tâm tuyệt đối, cam kết đồng hành 1-1 mỗi ngày.", "kd": "Kinh doanh không áp lực, lan tỏa từ tâm giúp đỡ người thân."},
    "CC": {"ten": "Chiếc Thước Đo (C thuần)", "dac_diem": "Logic, kỷ luật thép, đa nghi, đòi hỏi bằng chứng khoa học.", "sk": "Cung cấp kiến thức Biohacking, tài liệu y khoa, số liệu InBody.", "kd": "Chia sẻ sơ đồ trả thưởng chi tiết, tính pháp lý của tập đoàn."},
    "DC": {"ten": "Nhà Quản Trị / Kiến Trúc Sư", "dac_diem": "Sắt đá, không cảm xúc, đòi hỏi logic.", "sk": "Đưa giải pháp khoa học tối ưu nhất, không rườm rà.", "kd": "Trình bày kế hoạch hoàn vốn (ROI) và hệ thống vận hành."},
    "CD": {"ten": "Nhà Chiến Lược", "dac_diem": "Phân tích rủi ro trước, hành động lạnh lùng.", "sk": "Đưa bảng thành phần chi tiết tự đối chiếu.", "kd": "Nhấn mạnh quy định minh bạch, đường lối phát triển an toàn."},
    "DI": {"ten": "Người Tiên Phong", "dac_diem": "Tốc độ nhanh, thích mục tiêu lớn.", "sk": "Thách thức họ cam kết 90 ngày lột xác.", "kd": "Nói về chức danh GET Team, Millionaire Team."},
    "ID": {"ten": "Nhà Thuyết Phục", "dac_diem": "Bán hàng xuất chúng, lôi cuốn.", "sk": "Biến sức khỏe thành công cụ chốt sale.", "kd": "Kích hoạt khả năng sân khấu, trở thành diễn giả."},
    "IS": {"ten": "Sứ Giả Hòa Bình", "dac_diem": "Mềm mỏng, ấm áp, thích đội nhóm.", "sk": "Chăm sóc như người nhà, gắn kết vào CLB Dinh Dưỡng.", "kd": "Vẽ ra môi trường làm việc như gia đình thứ hai."},
    "SI": {"ten": "Người Cống Hiến", "dac_diem": "Luôn làm điểm tựa cho hệ thống.", "sk": "Khỏe mạnh để chăm lo tốt cho gia đình.", "kd": "Triết lý 'Mài rìu từ tâm' - kinh doanh là giúp người khác."},
    "CS": {"ten": "Người Bảo Vệ Chuẩn Mực", "dac_diem": "Tỉ mỉ, làm việc theo thói quen, sợ xáo trộn.", "sk": "Đưa ra lộ trình siêu chi tiết, kỷ luật 100%.", "kd": "Ổn định, làm từng bước vững chắc không rủi ro."},
    "SC": {"ten": "Kỹ Sư Quy Trình", "dac_diem": "Trung thực, làm việc bền bỉ.", "sk": "Cam kết đồng hành đều đặn, không đột ngột.", "kd": "Giao quản trị khách hàng, là hậu phương vững chắc."},
    "DS": {"ten": "Người Đạt Mục Tiêu Có Tâm", "dac_diem": "Quyết đoán nhưng bền vững.", "sk": "Giảm cân an toàn bảo vệ chuyển hóa.", "kd": "Thu nhập thụ động bền vững cho gia đình."},
    "SD": {"ten": "Người Đồng Hành Kiên Cường", "dac_diem": "Bền bỉ, chịu áp lực cực giỏi.", "sk": "Hành trình dài hạn, kết quả vững chắc.", "kd": "Hạt giống lãnh đạo trọn đời, cống hiến toàn thời gian."},
    "IC": {"ten": "Chuyên Gia Sáng Tạo", "dac_diem": "Bay bổng nhưng khắt khe khoa học.", "sk": "Phương pháp mới lạ (VD: Biohacking).", "kd": "Xây dựng thương hiệu cá nhân độc đáo, chuẩn quy trình."},
    "CI": {"ten": "Người Đánh Giá", "dac_diem": "Phân tích sâu sắc, chia sẻ kiến thức.", "sk": "Biến họ thành 'Chuyên gia' tự phân tích.", "kd": "Giao vị trí cố vấn, huấn luyện viên đứng lớp."}
}

col_b1, col_b2 = st.columns([1, 6])
with col_b1: st.markdown(logo_html, unsafe_allow_html=True)
with col_b2:
    st.markdown("<h2 style='margin:0; font-size:24px;'>MÀI RÌU TỪ TÂM - HỆ THỐNG THỰC CHIẾN DISC</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #ecd085 !important; font-weight: bold; margin: 5px 0 0 0;'>BẢN QUYỀN ĐỘC QUYỀN THUỘC VỀ Dr JONATHAN PHỤNG</p>", unsafe_allow_html=True)
st.divider()

st.sidebar.markdown(f"<div style='text-align:center; margin-bottom:15px;'>{anh_thay_html}</div>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='font-size:20px;'>⚙️ BẢNG ĐIỀU KHIỂN</h2>", unsafe_allow_html=True)
che_do = st.sidebar.radio("", ["1. KHẢO SÁT CHUYÊN SÂU (60 Chỉ số)", "2. TÁC CHIẾN THỰC ĐỊA (Khách hàng)"])

st.sidebar.divider()
st.sidebar.markdown("**💾 DỮ LIỆU THÀNH VIÊN:**")
st.sidebar.write(f"👤 TV: {st.session_state['tv_ten'] if st.session_state['tv_ten'] else 'Chưa khai báo'}")
st.sidebar.write(f"💼 Nghề: {st.session_state['tv_nn'] if st.session_state['tv_nn'] else 'Chưa khai báo'}")
st.sidebar.write(f"🔺 Mật mã: {st.session_state['tv_c']}-{st.session_state['tv_p1']}-{st.session_state['tv_p2']}")

st.sidebar.divider()
exp_txt = "Vĩnh viễn" if st.session_state.get('exp_luu') == "99991231" else st.session_state.get('exp_luu', 'Đã xác thực')
st.sidebar.write(f"🛡️ **Hạn dùng:** {exp_txt}")

if st.sidebar.button("🔒 KHÓA TẠM HỆ THỐNG"):
    st.session_state['da_mo_khoa'] = False
    st.rerun()

if che_do == "1. KHẢO SÁT CHUYÊN SÂU (60 Chỉ số)":
    st.header("🎯 BỘ CÂU HỎI DISC CHUYÊN SÂU TỐI ƯU")
    st.markdown("Hệ thống phân tích 60 chỉ số tính cách vào 15 tình huống hành vi cốt lõi nhằm tăng tốc độ trên Cloud, giữ nguyên độ chính xác 100%.")
    
    tv_ten_input = st.text_input("👤 Nhập Tên của bạn:", value=st.session_state['tv_ten'])
    tv_nn_input = st.text_input("💼 Nhập Nghề nghiệp của bạn:", value=st.session_state['tv_nn'])
    
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
    
    if st.button("🎯 LƯU & PHÂN TÍCH CHUYÊN SÂU"):
        if tv_ten_input.strip() == "": st.warning("Vui lòng điền Tên.")
        else:
            res = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            st.session_state['tv_ten'] = tv_ten_input.strip().upper()
            st.session_state['tv_nn'] = tv_nn_input.strip()
            st.session_state['tv_c'] = res[0][0]
            st.session_state['tv_p1'] = res[1][0]
            st.session_state['tv_p2'] = res[2][0]
            st.rerun()

elif che_do == "2. TÁC CHIẾN THỰC ĐỊA (Khách hàng)":
    st.header("👑 TRUNG TÂM TÁC CHIẾN SONG PHƯƠNG")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("👤 THÀNH VIÊN TƯ VẤN")
        if st.session_state['tv_ten'] == "": 
            st.warning("Vui lòng thực hiện Khảo sát hoặc điền nhanh:")
            tv_ten = st.text_input("Tên TV:", value="THẦY PHỤNG")
            tv_nn = st.text_input("Nghề nghiệp TV:", value="Chuyên gia")
            tv_c = st.selectbox("Nhóm Chính TV:", ["D","I","S","C"], index=0)
            tv_p1 = st.selectbox("Nhóm Phụ 1 TV:", ["D","I","S","C"], index=1)
            tv_p2 = st.selectbox("Nhóm Phụ 2 TV:", ["D","I","S","C"], index=2)
            if st.button("💾 Lưu Thành Viên"):
                st.session_state['tv_ten'] = tv_ten.strip().upper()
                st.session_state['tv_nn'] = tv_nn.strip()
                st.session_state['tv_c'], st.session_state['tv_p1'], st.session_state['tv_p2'] = tv_c, tv_p1, tv_p2
                st.rerun()
        else:
            st.info(f"Tên: **{st.session_state['tv_ten']}** ({st.session_state['tv_nn']})\nMật mã: **{st.session_state['tv_c']}-{st.session_state['tv_p1']}-{st.session_state['tv_p2']}**")
            tv_ten, tv_nn = st.session_state['tv_ten'], st.session_state['tv_nn']
            tv_c, tv_p1, tv_p2 = st.session_state['tv_c'], st.session_state['tv_p1'], st.session_state['tv_p2']

    with c2:
        st.subheader("🤝 KHÁCH HÀNG / DOWNLINE")
        kh_ten = st.text_input("Tên Khách hàng:", placeholder="Nhập tên khách...")
        kh_nn = st.text_input("Nghề nghiệp Khách:", placeholder="Vd: Kinh doanh...")
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
                    <p style='font-style:italic; margin:0;'>Để chốt khách hàng nhóm <b>{info_kh['ten']}</b> làm nghề <b>{kh_nn}</b>, không dùng chung một bài, phải đánh đúng vào tử huyệt cảm xúc của họ như ma trận đã phân tích ở trên!</p>
                </div>
            </div>
            """, unsafe_allow_html=True)