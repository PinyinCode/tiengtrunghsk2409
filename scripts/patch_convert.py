# -*- coding: utf-8 -*-
"""
patch_convert.py — Tự động thêm tab "1000 câu giao tiếp" vào convert.py
Chạy: python patch_convert.py
"""
import os
import sys
import shutil
import re
from datetime import datetime

MAIN_PY = "convert.py"      # ⭐ ĐÃ SỬA: từ main.py → convert.py
BACKUP_SUFFIX = ".bak"


# ═══════════════════════════════════════════════════════════════════
#  NỘI DUNG CÁC ĐOẠN CHÈN
# ═══════════════════════════════════════════════════════════════════

BLOCK_VARS = '''
# ═══════════════════════════════════════════════════════════════════
#  ⭐ TAB 2: "1000 câu giao tiếp" — file 1605.xlsx
#     Đặt CÙNG THƯ MỤC với file Excel tổng hợp
# ═══════════════════════════════════════════════════════════════════
EXCEL_FILE_2 = os.path.join(
    os.path.dirname(os.path.abspath(EXCEL_FILE)),
    "1605.xlsx"
)
TAB2_ID    = "giaotiep"
TAB2_LABEL = "1000 câu giao tiếp"
TAB2_ICON  = "fa-comments"
print(f"📂 File tab 2 dự kiến: {EXCEL_FILE_2}")
'''

BLOCK_READ = '''
# ─── 1b. Đọc dataset tab 2 (1000 câu giao tiếp) ───
data_giaotiep = []
if os.path.isfile(EXCEL_FILE_2):
    try:
        data_giaotiep = read_excel(EXCEL_FILE_2, SHEET_INDEX) or []
        print(f"💬 {TAB2_LABEL}: {len(data_giaotiep)} câu (từ {os.path.basename(EXCEL_FILE_2)})")
    except Exception as e:
        print(f"❌ Lỗi đọc {EXCEL_FILE_2}: {e}")
        data_giaotiep = []
else:
    print(f"⚠️  Không tìm thấy file: {EXCEL_FILE_2}")
    print(f"   → Tab '{TAB2_LABEL}' sẽ trống.")
'''

LINE_SERIALIZE = 'json_data_2 = _json_blob(data_giaotiep)\n'

LINE_REPLACE = '    .replace("__DATA_2__",            json_data_2)\n'

LINE_RAWDATA2 = 'var RAW_DATA_2 = __DATA_2__;\n'

BLOCK_SWITCH = '''
/* ⭐ Switch sang tab 2 (1000 câu giao tiếp) */
window.__switchToTab2 = function() {
    RAW_DATA = RAW_DATA_2 || [];
    CURRENT_DATASET = 'giaotiep';
    return true;
};

/* ⭐ Switch về tab tổng hợp */
window.__switchToTab1 = function() {
    RAW_DATA = (DATASET_REGISTRY && DATASET_REGISTRY['tonghop'])
        ? DATASET_REGISTRY['tonghop'].data
        : [];
    CURRENT_DATASET = 'tonghop';
    return true;
};
'''

LINE_FINAL_PRINT = 'print(f"💬 Tab 2 ({TAB2_LABEL}): {len(data_giaotiep)} câu")\n'


# ═══════════════════════════════════════════════════════════════════
#  UTIL
# ═══════════════════════════════════════════════════════════════════
def log(icon, msg):
    print(f"{icon}  {msg}")

def already_has(content, marker):
    return marker in content


# ═══════════════════════════════════════════════════════════════════
#  PATCH STEPS
# ═══════════════════════════════════════════════════════════════════
def patch_step_1_vars(src):
    if already_has(src, 'EXCEL_FILE_2 = os.path.join'):
        log("⏭️ ", "Step 1: biến EXCEL_FILE_2 đã có — bỏ qua")
        return src
    pattern = r'(DATA_DIR = CONFIG\.get\("data_dir", "data"\)[^\n]*\n)'
    m = re.search(pattern, src)
    if not m:
        log("❌", "Step 1: Không tìm thấy dòng DATA_DIR — FAIL")
        return None
    insert_pos = m.end()
    src = src[:insert_pos] + BLOCK_VARS + src[insert_pos:]
    log("✅", "Step 1: Đã chèn khối khai báo biến tab 2")
    return src


def patch_step_2_read(src):
    if already_has(src, 'data_giaotiep = []'):
        log("⏭️ ", "Step 2: khối đọc data_giaotiep đã có — bỏ qua")
        return src
    pattern = r'(print\(f"📚 Tổng hợp: \{[^\}]*\} câu"\)\n)'
    m = re.search(pattern, src)
    if not m:
        pattern = r'(print\(f"📚 Tổng hợp[^\n]*\n)'
        m = re.search(pattern, src)
    if not m:
        log("❌", "Step 2: Không tìm thấy dòng print Tổng hợp — FAIL")
        return None
    insert_pos = m.end()
    src = src[:insert_pos] + BLOCK_READ + src[insert_pos:]
    log("✅", "Step 2: Đã chèn khối đọc 1605.xlsx")
    return src


def patch_step_3_serialize(src):
    if already_has(src, 'json_data_2 = _json_blob'):
        log("⏭️ ", "Step 3: json_data_2 đã có — bỏ qua")
        return src
    pattern = r'(json_data = _json_blob\(data_tonghop\)\n)'
    m = re.search(pattern, src)
    if not m:
        log("❌", "Step 3: Không tìm thấy json_data = _json_blob — FAIL")
        return None
    insert_pos = m.end()
    src = src[:insert_pos] + LINE_SERIALIZE + src[insert_pos:]
    log("✅", "Step 3: Đã chèn json_data_2")
    return src


def patch_step_4_replace(src):
    if already_has(src, '.replace("__DATA_2__"'):
        log("⏭️ ", "Step 4: replace __DATA_2__ đã có — bỏ qua")
        return src
    pattern = r'(\s*\.replace\("__DATA__",\s*json_data\)\n)'
    m = re.search(pattern, src)
    if not m:
        log("❌", "Step 4: Không tìm thấy .replace('__DATA__') — FAIL")
        return None
    insert_pos = m.end()
    src = src[:insert_pos] + LINE_REPLACE + src[insert_pos:]
    log("✅", "Step 4: Đã chèn replace __DATA_2__")
    return src


def patch_step_5_rawdata2(src):
    if already_has(src, 'var RAW_DATA_2'):
        log("⏭️ ", "Step 5: RAW_DATA_2 đã có — bỏ qua")
        return src
    pattern = r'(var RAW_DATA = __DATA__;\n)'
    m = re.search(pattern, src)
    if not m:
        log("❌", "Step 5: Không tìm thấy var RAW_DATA = __DATA__ — FAIL")
        return None
    insert_pos = m.end()
    src = src[:insert_pos] + LINE_RAWDATA2 + src[insert_pos:]
    log("✅", "Step 5: Đã chèn var RAW_DATA_2")
    return src


def patch_step_6_switch(src):
    if already_has(src, 'window.__switchToTab2'):
        log("⏭️ ", "Step 6: __switchToTab2 đã có — bỏ qua")
        return src
    pattern = r"(window\.__switchRawData = function\(datasetId\) \{.*?\n\};\n)"
    m = re.search(pattern, src, re.DOTALL)
    if not m:
        log("❌", "Step 6: Không tìm thấy __switchRawData — FAIL")
        return None
    insert_pos = m.end()
    src = src[:insert_pos] + BLOCK_SWITCH + src[insert_pos:]
    log("✅", "Step 6: Đã chèn __switchToTab1/__switchToTab2")
    return src


def patch_step_7_print(src):
    if already_has(src, 'Tab 2 ({TAB2_LABEL})'):
        log("⏭️ ", "Step 7: print tab 2 đã có — bỏ qua")
        return src
    pattern = r'(print\(f"👥 User Online[^\n]*\n)'
    m = re.search(pattern, src)
    if not m:
        pattern = r'(\n# ─── Onboarding info ───\n)'
        m = re.search(pattern, src)
    if not m:
        log("⚠️ ", "Step 7: Không tìm được vị trí chèn print — bỏ qua")
        return src
    insert_pos = m.end()
    src = src[:insert_pos] + LINE_FINAL_PRINT + src[insert_pos:]
    log("✅", "Step 7: Đã chèn print summary tab 2")
    return src


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════
def main():
    print("=" * 65)
    print("  🔧 PATCH CONVERT.PY — '1000 câu giao tiếp'")
    print("=" * 65)

    if not os.path.isfile(MAIN_PY):
        log("❌", f"Không tìm thấy {MAIN_PY} trong thư mục hiện tại!")
        log("💡", f"Thư mục hiện tại: {os.getcwd()}")
        sys.exit(1)

    backup_name = MAIN_PY + f".{datetime.now().strftime('%Y%m%d_%H%M%S')}{BACKUP_SUFFIX}"
    shutil.copy2(MAIN_PY, backup_name)
    log("💾", f"Đã backup: {backup_name}")

    with open(MAIN_PY, "r", encoding="utf-8") as f:
        src = f.read()

    original_len = len(src)

    steps = [
        patch_step_1_vars,
        patch_step_2_read,
        patch_step_3_serialize,
        patch_step_4_replace,
        patch_step_5_rawdata2,
        patch_step_6_switch,
        patch_step_7_print,
    ]

    for step_fn in steps:
        result = step_fn(src)
        if result is None:
            log("💥", f"PATCH THẤT BẠI ở {step_fn.__name__}")
            log("💾", f"File gốc chưa bị thay đổi. Khôi phục: copy {backup_name} {MAIN_PY}")
            sys.exit(1)
        src = result

    with open(MAIN_PY, "w", encoding="utf-8") as f:
        f.write(src)

    print()
    print("=" * 65)
    log("🎉", f"HOÀN THÀNH! convert.py: {original_len} → {len(src)} bytes")
    print("=" * 65)
    print()
    print("📋 BƯỚC TIẾP THEO:")
    print("   1. Chạy: python patch_ui.py")
    print("   2. Chạy: python convert.py")
    print("   3. Mở ../index.html kiểm tra")


if __name__ == "__main__":
    main()