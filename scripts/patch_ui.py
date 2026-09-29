# -*- coding: utf-8 -*-
"""
patch_ui.py — Tự động thêm tab "1000 câu giao tiếp" vào ui_template.py
Chạy: python patch_ui.py
"""
import os
import sys
import shutil
import re
from datetime import datetime

UI_PY = "ui_template.py"


# ═══════════════════════════════════════════════════════════════════
#  NỘI DUNG CHÈN
# ═══════════════════════════════════════════════════════════════════

# ─── HTML: nút tab mới (sau nút Tổng hợp) ───
HTML_TAB2 = '''
        <button class="ds-btn ds-btn-primary" data-dataset="giaotiep" id="dsGiaotiepBtn">
            <i class="fas fa-comments"></i>
            <span id="dsGiaotiepLabel">1000 câu giao tiếp</span>
        </button>'''

# ─── JS: cập nhật label tab 2 theo count thực tế ───
JS_LABEL_TAB2 = '''
    var gtLabel = $('dsGiaotiepLabel');
    if (gtLabel && typeof RAW_DATA_2 !== 'undefined' && Array.isArray(RAW_DATA_2)) {
        gtLabel.textContent = RAW_DATA_2.length + ' câu giao tiếp';
    }'''

# ─── JS: handler click cho nút tab 2 ───
JS_HANDLER_TAB2 = '''
    /* ═══════════════════════════════════════════════════════════
       NÚT TAB 2 (1000 câu giao tiếp) — Click để về tab giao tiếp
       ═══════════════════════════════════════════════════════════ */
    document.querySelectorAll('.ds-btn[data-dataset="giaotiep"]').forEach(function(btn) {
        if (btn.__boundDataset2) return;
        btn.__boundDataset2 = true;
        btn.addEventListener('click', function() {
            switchDataset('giaotiep');
            var sub = $('dsSubWrap');
            if (sub) sub.style.display = 'none';

            /* Bỏ active TẤT CẢ tab */
            document.querySelectorAll('.ds-btn').forEach(function(b) {
                b.classList.remove('active');
            });
            btn.classList.add('active');
        });
    });
'''

# ─── JS: nhánh trong switchDataset() cho tab 2 ───
JS_SWITCH_BRANCH = '''
    /* ⭐ TAB 2: 1000 câu giao tiếp */
    if (datasetId === 'giaotiep') {
        if (typeof window.__switchToTab2 === 'function') {
            window.__switchToTab2();
        } else {
            console.warn('__switchToTab2 chưa được load');
            return;
        }

        window.__onboardingOverride = null;

        state = { search:'', hsk:'', subject:'' };
        if ($('searchInput')) $('searchInput').value = '';
        if ($('hskFilter')) $('hskFilter').value = '';
        if ($('subjectFilter')) $('subjectFilter').value = '';

        buildFilters();
        applyFilter();
        updateResultCount();

        if ($('fabGroup')) $('fabGroup').classList.remove('open');

        /* Cập nhật trạng thái Yêu thích */
        if (typeof favUpdateLockState === 'function') favUpdateLockState();

        return;
    }
'''

# ─── JS: cập nhật markCurrentDatasetActive() ───
JS_MARK_UPDATE = '''
    document.querySelectorAll('.ds-btn[data-dataset="giaotiep"]').forEach(function(b) {
        b.classList.toggle('active', current === 'giaotiep');
    });'''


# ═══════════════════════════════════════════════════════════════════
#  UTIL
# ═══════════════════════════════════════════════════════════════════
def log(icon, msg):
    print(f"{icon}  {msg}")


# ═══════════════════════════════════════════════════════════════════
#  PATCH STEPS
# ═══════════════════════════════════════════════════════════════════
def patch_step_1_html_tab(src):
    """Chèn nút tab mới sau nút Tổng hợp trong ds-main-row."""
    if 'ds-btn-primary" data-dataset="giaotiep"' in src:
        log("⏭️ ", "Step 1: nút tab giaotiep đã có — bỏ qua")
        return src

    # Tìm nút Tổng hợp trong ds-main-row
    pattern = (
        r'(<button class="ds-btn ds-btn-primary active" data-dataset="tonghop">.*?</button>)'
    )
    m = re.search(pattern, src, re.DOTALL)
    if not m:
        log("❌", "Step 1: Không tìm thấy nút Tổng hợp trong ds-main-row — FAIL")
        return None

    insert_pos = m.end()
    src = src[:insert_pos] + HTML_TAB2 + src[insert_pos:]
    log("✅", "Step 1: Đã chèn nút tab '1000 câu giao tiếp' vào ds-main-row")
    return src


def patch_step_2_label_js(src):
    """Chèn code cập nhật label tab 2 theo count."""
    if 'gtLabel' in src and 'dsGiaotiepLabel' in src:
        log("⏭️ ", "Step 2: cập nhật label giaotiep đã có — bỏ qua")
        return src

    # Tìm sau đoạn cập nhật labelEl của Tổng hợp
    pattern = r"(labelEl\.textContent = count \+ ' câu phản xạ tổng hợp VPCX';\s*\n\s*\})"
    m = re.search(pattern, src)
    if not m:
        log("⚠️ ", "Step 2: Không tìm thấy đoạn label Tổng hợp — thử pattern khác")
        # fallback pattern lỏng hơn
        pattern = r"(labelEl\.textContent = count \+ ' câu phản xạ tổng hợp VPCX';\s*\n\s*\})"
        m = re.search(pattern, src)
        if not m:
            log("⚠️ ", "Step 2: Bỏ qua (không critical)")
            return src

    insert_pos = m.end()
    src = src[:insert_pos] + JS_LABEL_TAB2 + src[insert_pos:]
    log("✅", "Step 2: Đã chèn code cập nhật label tab 2")
    return src


def patch_step_3_handler_js(src):
    """Chèn handler click cho nút tab 2, ngay sau handler Tổng hợp."""
    if 'btn.__boundDataset2' in src:
        log("⏭️ ", "Step 3: handler tab 2 đã có — bỏ qua")
        return src

    # Tìm khối handler Tổng hợp (kết thúc bằng dấu "});" sau khi addEventListener)
    # Đặc trưng: có data-dataset="tonghop" và kết thúc bằng "btn.classList.add('active');"
    pattern = (
        r"(document\.querySelectorAll\('\.ds-btn\[data-dataset=\"tonghop\"\]'\)\.forEach\(function\(btn\) \{.*?"
        r"btn\.classList\.add\('active'\);\s*\n\s*\}\s*\);\s*\n\s*\})"
    )
    m = re.search(pattern, src, re.DOTALL)
    if not m:
        log("❌", "Step 3: Không tìm thấy handler Tổng hợp — FAIL")
        return None

    insert_pos = m.end()
    src = src[:insert_pos] + JS_HANDLER_TAB2 + src[insert_pos:]
    log("✅", "Step 3: Đã chèn handler click cho tab 2")
    return src


def patch_step_4_switch_branch(src):
    """Chèn nhánh xử lý 'giaotiep' trong switchDataset()."""
    if "datasetId === 'giaotiep'" in src:
        log("⏭️ ", "Step 4: nhánh switch giaotiep đã có — bỏ qua")
        return src

    # Tìm đầu hàm switchDataset
    pattern = r"(function switchDataset\(datasetId\) \{\s*\n\s*if \(!DATASET_REGISTRY\[datasetId\]\) return;)"
    m = re.search(pattern, src)
    if not m:
        log("❌", "Step 4: Không tìm thấy đầu hàm switchDataset — FAIL")
        return None

    insert_pos = m.end()
    src = src[:insert_pos] + JS_SWITCH_BRANCH + src[insert_pos:]
    log("✅", "Step 4: Đã chèn nhánh switch cho tab 'giaotiep'")
    return src


def patch_step_5_mark_active(src):
    """Cập nhật markCurrentDatasetActive() để active nút tab 2."""
    if "data-dataset=\"giaotiep\"]').forEach" in src and 'JS_MARK_UPDATE' not in src:
        # Đã có sẵn (chạy lại patch)
        pass

    # Tìm khối markCurrentDatasetActive
    pattern = r"(function markCurrentDatasetActive\(\) \{\s*\n\s*var current = .*?\n)(\s*\})"
    m = re.search(pattern, src, re.DOTALL)
    if not m:
        log("❌", "Step 5: Không tìm thấy markCurrentDatasetActive — FAIL")
        return None

    # Kiểm tra đã chèn chưa
    check_pattern = r"\.ds-btn\[data-dataset=\"giaotiep\"\]"
    block = src[m.start():m.end()]
    if re.search(check_pattern, block):
        log("⏭️ ", "Step 5: mark active cho giaotiep đã có — bỏ qua")
        return src

    # Chèn ngay sau dòng querySelectorAll cho tonghop
    pattern2 = (
        r"(\s*document\.querySelectorAll\('\.ds-btn\[data-dataset=\"tonghop\"\]'\)\.forEach\("
        r"function\(b\) \{\s*\n\s*b\.classList\.toggle\('active', current === 'tonghop'\);\s*\n\s*\}\);)"
    )
    m2 = re.search(pattern2, src)
    if not m2:
        log("⚠️ ", "Step 5: Không tìm thấy dòng toggle tonghop — thử cách khác")
        # Fallback: chèn sau dòng có "current === 'tonghop'"
        pattern3 = r"(\s*b\.classList\.toggle\('active', current === 'tonghop'\);)"
        m3 = re.search(pattern3, src)
        if not m3:
            log("⚠️ ", "Step 5: Bỏ qua (không critical)")
            return src
        # Tìm dấu `});` tiếp theo để chèn SAU khi block đóng
        end_idx = src.find('});', m3.end())
        if end_idx == -1:
            log("⚠️ ", "Step 5: Bỏ qua (không tìm được vị trí đóng block)")
            return src
        insert_pos = end_idx + 3  # sau '});'
        src = src[:insert_pos] + JS_MARK_UPDATE + src[insert_pos:]
        log("✅", "Step 5: Đã chèn mark active cho giaotiep (fallback)")
        return src

    insert_pos = m2.end()
    src = src[:insert_pos] + JS_MARK_UPDATE + src[insert_pos:]
    log("✅", "Step 5: Đã chèn mark active cho giaotiep")
    return src


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════
def main():
    print("=" * 65)
    print("  🔧 PATCH UI — '1000 câu giao tiếp' → ui_template.py")
    print("=" * 65)

    if not os.path.isfile(UI_PY):
        log("❌", f"Không tìm thấy {UI_PY} trong thư mục hiện tại!")
        log("💡", f"Thư mục hiện tại: {os.getcwd()}")
        sys.exit(1)

    # Backup
    backup_name = UI_PY + f".{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    shutil.copy2(UI_PY, backup_name)
    log("💾", f"Đã backup: {backup_name}")

    # Đọc file
    with open(UI_PY, "r", encoding="utf-8") as f:
        src = f.read()

    original_len = len(src)

    # Chạy các bước
    steps = [
        patch_step_1_html_tab,
        patch_step_2_label_js,
        patch_step_3_handler_js,
        patch_step_4_switch_branch,
        patch_step_5_mark_active,
    ]

    for step_fn in steps:
        result = step_fn(src)
        if result is None:
            log("💥", f"PATCH THẤT BẠI ở {step_fn.__name__}")
            log("💾", f"File gốc chưa bị thay đổi. Khôi phục: copy {backup_name} {UI_PY}")
            sys.exit(1)
        src = result

    # Ghi file
    with open(UI_PY, "w", encoding="utf-8") as f:
        f.write(src)

    print()
    print("=" * 65)
    log("🎉", f"HOÀN THÀNH! ui_template.py: {original_len} → {len(src)} bytes")
    print("=" * 65)
    print()
    print("📋 KIỂM TRA:")
    print("   1. Mở ui_template.py → tìm 'giaotiep' → phải có 5 chỗ")
    print("   2. Chạy: python main.py")
    print("   3. Mở index.html → thấy 3 tab ngang hàng:")
    print("      [Tổng hợp] [1000 câu giao tiếp] [Chuyên ngành]")
    print()


if __name__ == "__main__":
    main()
