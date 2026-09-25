# -*- coding: utf-8 -*-
"""
Đọc file Excel → list dict.
⚡ KHI ĐỔI CẤU TRÚC EXCEL: chỉ cần sửa hàm read_excel() bên dưới.
Format chuẩn trả về: [{"stt","hsk","topic","subject","vi","zh","pinyin"}, ...]

✅ TỰ ĐỘNG CHUYỂN SỐ Ả RẬP → SỐ HÁN trong cột Tiếng Trung:
   "订单是500个" → "订单是五百个"
   "B-02库位"   → "B-02库位" (giữ nguyên vì có chữ cái)
   "500MB"      → "500MB"    (giữ nguyên vì dính MB)
"""
import openpyxl
import os
import re
import sys

# ═══════════════════════════════════════════════════════════════════
#  CHUYỂN SỐ Ả RẬP → SỐ HÁN
# ═══════════════════════════════════════════════════════════════════
try:
    import cn2an
    HAS_CN2AN = True
except ImportError:
    HAS_CN2AN = False
    print("⚠️  Không có cn2an — số Ả Rập sẽ giữ nguyên")
    print("   Cài: pip install cn2an")


# ─── Fallback nếu không có cn2an ───
_CN_DIGITS = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
_CN_UNITS = ['', '十', '百', '千']


def _num_to_chinese_basic(num):
    """Fallback đổi số 0-9999 thành Hán (không hỗ trợ số lớn)."""
    if num == 0:
        return '零'
    if num < 0:
        return '负' + _num_to_chinese_basic(-num)

    result = ''
    unit_idx = 0
    n = num
    while n > 0:
        digit = n % 10
        if digit != 0:
            if not (unit_idx == 1 and digit == 1 and n < 20 and result == ''):
                result = _CN_DIGITS[digit] + _CN_UNITS[unit_idx] + result
            else:
                result = _CN_UNITS[unit_idx] + result
        else:
            if result and not result.startswith('零'):
                result = '零' + result
        n //= 10
        unit_idx += 1

    if result.startswith('一十'):
        result = result[1:]
    return result


def _num_to_chinese(num):
    """Đổi số nguyên → Hán. Dùng cn2an nếu có, fallback nếu không."""
    if HAS_CN2AN:
        try:
            return cn2an.an2cn(num)
        except Exception:
            pass
    return _num_to_chinese_basic(num)


def convert_arabic_to_chinese(text):
    """
    Chuyển số Ả Rập trong câu → số Hán.
    KHÔNG chuyển nếu số thuộc mã/thuật ngữ:
      - Đứng sau chữ cái hoặc dấu gạch: B-02, IP, USB
      - Đứng trước chữ cái: 500MB, 2TB
      - Là phần của version: v2.0, 3.5.1
    """
    if not text or not isinstance(text, str):
        return text

    def replace(match):
        num = int(match.group(0))
        return _num_to_chinese(num)

    # Regex: chỉ convert số đứng độc lập
    #   (?<![A-Za-z\-\.]) — không đứng sau chữ cái/gạch/chấm
    #   \d+               — chuỗi số
    #   (?![A-Za-z]|\.\d) — không đứng trước chữ cái hoặc .số
    pattern = r'(?<![A-Za-z\-\.])\d+(?![A-Za-z]|\.\d)'
    return re.sub(pattern, replace, text)


# ═══════════════════════════════════════════════════════════════════
#  CLEAN
# ═══════════════════════════════════════════════════════════════════
def clean(s):
    if s is None:
        return ""
    return (str(s).replace('\n', ' ').replace('\r', ' ')
            .replace('\t', ' ').replace('\\', '\\\\'))


# ═══════════════════════════════════════════════════════════════════
#  READ EXCEL
# ═══════════════════════════════════════════════════════════════════
def read_excel(excel_file, sheet_index=0):
    print(f"\n📖 Đang đọc file: {excel_file}")
    if not os.path.exists(excel_file):
        print(f"❌ Không tìm thấy file {excel_file}")
        sys.exit(1)

    wb = openpyxl.load_workbook(excel_file, data_only=True)
    ws = wb.worksheets[sheet_index]
    print(f"📊 Sheet: {ws.title} - {ws.max_row} dòng")

    # ↓↓↓ CẤU HÌNH CỘT Ở ĐÂY (đổi khi Excel đổi cấu trúc) ↓↓↓
    COL_STT = 0
    COL_HSK = 1
    COL_TOPIC = 2
    COL_SUBJECT = 3
    COL_VI = 4
    COL_ZH = 5
    COL_PINYIN = 6
    DATA_START = 2
    # ↑↑↑ HẾT PHẦN CẦN SỬA ↑↑↑

    data = []
    converted_count = 0

    for row in ws.iter_rows(min_row=DATA_START, values_only=True):
        if not row or len(row) <= max(COL_VI, COL_ZH):
            continue

        stt = row[COL_STT] if COL_STT < len(row) and row[COL_STT] is not None else ""
        hsk = clean(row[COL_HSK]) if COL_HSK < len(row) else ""
        topic = clean(row[COL_TOPIC]) if COL_TOPIC < len(row) else ""
        subject = clean(row[COL_SUBJECT]) if COL_SUBJECT < len(row) else ""
        vi = clean(row[COL_VI]) if COL_VI < len(row) else ""
        zh = clean(row[COL_ZH]) if COL_ZH < len(row) else ""
        pinyin = clean(row[COL_PINYIN]) if COL_PINYIN < len(row) else ""

        if not vi and not zh:
            continue

        # ⬇️ CHUYỂN SỐ Ả RẬP → SỐ HÁN
        zh_original = zh
        zh = convert_arabic_to_chinese(zh)
        if zh != zh_original:
            converted_count += 1

        data.append({
            "stt": str(stt), "hsk": hsk, "topic": topic, "subject": subject,
            "vi": vi, "zh": zh, "pinyin": pinyin
        })

    print(f"✅ Đã đọc {len(data)} câu")
    if converted_count > 0:
        print(f"🔄 Đã chuyển số Ả Rập → Hán: {converted_count} câu")
    return data


# ═══════════════════════════════════════════════════════════════════
#  TEST
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("TEST convert_arabic_to_chinese")
    print("=" * 60)
    tests = [
        "订单是500个，但是实际只收到480个。",
        "系统里的数量比实际数量多了20个。",
        "系统库存和实际库存差了50个。",
        "系统里的消耗数量比实际少了30个。",
        "系统记录的数量比实际多了20个。",
        "这批物料实际放在B-02库位。",
        "不能自己修改这台电脑的IP地址。",
        "这个文件很大，有500MB。",
        "使用的是WPS版本v2.0。",
        "今天是2024年12月25日。",
    ]
    for t in tests:
        result = convert_arabic_to_chinese(t)
        marker = "✅" if result != t else "➖"
        print(f"  {marker} {t}")
        if result != t:
            print(f"     → {result}")
