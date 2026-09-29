# -*- coding: utf-8 -*-
"""
Chuyển file Excel → HTML tự chứa dữ liệu.
Ghép 6 template: ui + social + accounts (gộp renewal) + intro + favorites + data.

KIẾN TRÚC 2 THƯ MỤC:
  - data/         → TAB CHÍNH (type="main")
  - script/data/  → TAB CHUYÊN NGÀNH (type="specialty")

UI OVERRIDE: Layout dọc + fix bug CSS được đóng gói trong ui_override.py
"""
import json
import os
import sys
import glob
import re
import unicodedata

# ═══════════════════════════════════════════════════════════════════
#  PATH SETUP
# ═══════════════════════════════════════════════════════════════════
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from config_loader import load_config, print_banner, CONFIG_FILE
from data_reader import read_excel
from ui_template import build_ui_css, build_ui_html, build_ui_js
from ui_override import (
    override_ui_css, override_ui_html, override_ui_js,
    override_fullwidth_css,
)
from social_template import (
    build_social_css, build_social_html, build_social_js,
    build_tiktok_bar_html
)
from accounts_template import (
    build_accounts_css,
    build_accounts_html,
    build_accounts_js,
    build_all_auth,
)
from intro_template import (
    build_intro_css,
    build_intro_html,
    build_intro_js,
)
from favorites_module import (
    build_favorites_css,
    build_favorites_html,
    build_favorites_js,
)
from chat_support import (
    build_chat_css,
    build_chat_html,
    build_chat_js,
    build_quota_html,
    build_quota_js,
    build_quota_init_js,
    build_online_section_html,
    build_config_js,
    build_telegram_notify_js,
)
from admin_chat_manager import (
    build_admin_chat_css,
    build_admin_chat_html,
    build_admin_chat_js,
)
from draggable_fab import (
    build_draggable_fab_css,
    build_draggable_fab_js,
)


# ═══════════════════════════════════════════════════════════════════
#  HELPER
# ═══════════════════════════════════════════════════════════════════
def _js_str(s):
    """Escape string để nhúng an toàn vào JS."""
    if s is None:
        return ""
    return (str(s)
            .replace('\\', '\\\\')
            .replace('"', '\\"')
            .replace("'", "\\'")
            .replace('\n', '\\n')
            .replace('\r', '\\r')
            .replace('</', '<\\/'))


def _json_blob(obj, compact=True):
    """Serialize object → JSON an toàn để nhúng vào script."""
    if compact:
        s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    else:
        s = json.dumps(obj, ensure_ascii=False)
    return s.replace("</", "<\\/")


# ═══════════════════════════════════════════════════════════════════
#  LOAD CONFIG
# ═══════════════════════════════════════════════════════════════════
CONFIG = load_config()
print_banner(CONFIG)

OUTPUT_HTML = CONFIG["output_html"]
SHEET_INDEX = CONFIG.get("sheet_index", 0)

_ROOT_DIR = os.path.dirname(_HERE)


def _resolve_path(p):
    """Chuẩn hóa đường dẫn tương đối."""
    if os.path.isabs(p):
        return p
    from_scripts = os.path.join(_HERE, p)
    if os.path.exists(from_scripts):
        return from_scripts
    return os.path.join(_ROOT_DIR, p)


DATA_DIR_MAIN = _resolve_path(CONFIG.get("data_dir", "data"))
DATA_DIR_SPEC = _resolve_path(CONFIG.get("data_dir_specialty", "script/data"))


# ═══════════════════════════════════════════════════════════════════
#  SLUGIFY + ICON
# ═══════════════════════════════════════════════════════════════════
def slugify_dataset_id(filename):
    base = filename.rsplit(".", 1)[0]
    base = re.sub(r'^\d+[_\-\.\s]+', '', base)
    base = unicodedata.normalize("NFD", base)
    base = "".join(c for c in base if unicodedata.category(c) != "Mn")
    base = base.replace("đ", "d").replace("Đ", "D")
    base = re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower()
    return base or "dataset"


def clean_display_name(filename):
    base = filename.rsplit(".", 1)[0]
    base = re.sub(r'^\d+[_\-\.\s]+', '', base)
    name = base.replace("_", " ").strip()
    if name.islower() or name.isupper():
        name = name.title()
    return name


ICON_MAP = {
    "giao tiếp":            "fa-comments",
    "tổng hợp":             "fa-book-open",
    "phản xạ":              "fa-book-open",
    "văn phòng":            "fa-building",
    "văn phòng công xưởng": "fa-building",
    "công xưởng":           "fa-industry",
    "nhân sự":              "fa-users",
    "hành chính":           "fa-briefcase",
    "thu mua":              "fa-shopping-cart",
    "xuất nhập khẩu":       "fa-ship",
    "logistics":            "fa-truck",
    "vận tải":              "fa-truck",
    "kho":                  "fa-warehouse",
    "bán hàng":             "fa-store",
    "kinh doanh":           "fa-chart-line",
    "marketing":            "fa-bullhorn",
    "dịch vụ khách hàng":   "fa-headset",
    "chăm sóc khách hàng":  "fa-headset",
    "kế toán":              "fa-calculator",
    "tài chính":            "fa-coins",
    "sản xuất":             "fa-industry",
    "kế hoạch sản xuất":    "fa-calendar-alt",
    "kỹ thuật":             "fa-tools",
    "bảo trì":              "fa-tools",
    "chất lượng":           "fa-award",
    "qa":                   "fa-award",
    "qc":                   "fa-award",
    "r&d":                  "fa-flask",
    "nghiên cứu":           "fa-flask",
    "giày da":              "fa-shoe-prints",
    "may mặc":              "fa-tshirt",
    "dệt may":              "fa-tshirt",
    "thực phẩm":            "fa-utensils",
    "nông nghiệp":          "fa-seedling",
    "máy tính":             "fa-laptop-code",
    "it":                   "fa-laptop-code",
}

DEFAULT_ICON_NAME = "fa-folder"
UNIFIED_COLOR = "#7c3aed"

TAB_PALETTE = [
    "#4f46e5",
    "#2563eb",
    "#16a34a",
    "#f59e0b",
    "#dc2626",
    "#0891b2",
    "#db2777",
    "#65a30d",
    "#7c3aed",
    "#ea580c",
]


def auto_detect_icon_color(display_name, fallback_index=0):
    key = display_name.strip().lower()
    if key in ICON_MAP:
        return (ICON_MAP[key], UNIFIED_COLOR)
    words = re.split(r'[\s&\-_/,\.]+', key)
    for k in sorted(ICON_MAP.keys(), key=len, reverse=True):
        if k in words:
            return (ICON_MAP[k], UNIFIED_COLOR)
    for k in sorted(ICON_MAP.keys(), key=len, reverse=True):
        if len(k) >= 3 and k in key:
            return (ICON_MAP[k], UNIFIED_COLOR)
    return (DEFAULT_ICON_NAME, UNIFIED_COLOR)


def pick_tab_icon(display_name, index):
    icon, _ = auto_detect_icon_color(display_name, index)
    return icon


def pick_tab_color(index):
    return TAB_PALETTE[index % len(TAB_PALETTE)]


# ═══════════════════════════════════════════════════════════════════
#  QUÉT THƯ MỤC
# ═══════════════════════════════════════════════════════════════════
def scan_excel_folder(folder_path):
    results = []
    if not os.path.isdir(folder_path):
        return results

    files = []
    for ext in ("*.xlsx", "*.xls", "*.csv"):
        files.extend(glob.glob(os.path.join(folder_path, ext)))
    files.sort()

    for filepath in files:
        filename = os.path.basename(filepath)
        if filename.startswith("~$"):
            continue
        try:
            sub_data = read_excel(filepath, 0)
            if not sub_data:
                print("⚠️  " + filename + ": file rỗng, bỏ qua")
                continue

            results.append({
                "filepath": filepath,
                "filename": filename,
                "display_name": clean_display_name(filename),
                "data": sub_data,
                "count": len(sub_data),
            })
        except Exception as e:
            print("❌ Lỗi đọc " + filename + ": " + str(e))
    return results


print("")
print("=" * 60)
print("🔍 TAB CHÍNH — " + DATA_DIR_MAIN)
print("=" * 60)
main_files = scan_excel_folder(DATA_DIR_MAIN)

print("")
print("=" * 60)
print("🔍 CHUYÊN NGÀNH — " + DATA_DIR_SPEC)
print("=" * 60)
spec_files = scan_excel_folder(DATA_DIR_SPEC)


# ═══════════════════════════════════════════════════════════════════
#  DATASET_REGISTRY
# ═══════════════════════════════════════════════════════════════════
DATASET_REGISTRY = {}

# TAB CHÍNH (data/)
for idx, item in enumerate(main_files):
    did = slugify_dataset_id(item["filename"])
    base_id = did
    c = 2
    while did in DATASET_REGISTRY:
        did = base_id + "-" + str(c)
        c += 1

    DATASET_REGISTRY[did] = {
        "id": did,
        "name": item["display_name"],
        "shortName": item["display_name"],
        "icon": pick_tab_icon(item["display_name"], idx),
        "color": pick_tab_color(idx),
        "data": item["data"],
        "count": item["count"],
        "source": item["filename"],
        "type": "main",
        "order": idx + 1,
    }
    print("📑 [TAB] " + item["display_name"].ljust(30) + " — " + str(item["count"]) + " câu")

# CHUYÊN NGÀNH (script/data/)
for idx, item in enumerate(spec_files):
    did = slugify_dataset_id(item["filename"])
    base_id = did
    c = 2
    while did in DATASET_REGISTRY:
        did = base_id + "-" + str(c)
        c += 1

    DATASET_REGISTRY[did] = {
        "id": did,
        "name": item["display_name"],
        "shortName": item["display_name"],
        "icon": auto_detect_icon_color(item["display_name"])[0],
        "color": UNIFIED_COLOR,
        "data": item["data"],
        "count": item["count"],
        "source": item["filename"],
        "type": "specialty",
        "order": idx + 1,
    }
    print("🏭 [SPEC] " + item["display_name"].ljust(29) + " — " + str(item["count"]) + " câu")

if not DATASET_REGISTRY:
    print("")
    print("⚠️  CẢNH BÁO: Không có dataset nào!")
    print("   → Bỏ file Excel vào: " + DATA_DIR_MAIN)
    print("   → Hoặc: " + DATA_DIR_SPEC)

first_dataset_id = next(iter(DATASET_REGISTRY), "")


# ═══════════════════════════════════════════════════════════════════
#  SERIALIZE
# ═══════════════════════════════════════════════════════════════════
dataset_registry_json = _json_blob(DATASET_REGISTRY)

if first_dataset_id:
    _first_data = DATASET_REGISTRY[first_dataset_id]["data"]
else:
    _first_data = []
json_data = _json_blob(_first_data)

firebase_config_json = _json_blob(CONFIG["firebase_config"])
synonyms_json = _json_blob(CONFIG["synonyms"])
fillers_json = _json_blob(CONFIG["filler_words"])
onboarding_config_json = _json_blob(CONFIG.get("onboarding", {}))

telegram_bot_token = CONFIG.get("telegram_bot_token", "")
telegram_chat_id = CONFIG.get("telegram_chat_id", "")


# ═══════════════════════════════════════════════════════════════════
#  AUTH + QUOTA + ONLINE
# ═══════════════════════════════════════════════════════════════════
auth_css, auth_html, auth_js = build_all_auth(CONFIG)

if '<!-- __ADMIN_ONLINE_SECTION__ -->' in auth_html:
    auth_html = auth_html.replace(
        '<!-- __ADMIN_ONLINE_SECTION__ -->',
        build_online_section_html()
    )
    print("✅ Đã chèn User Online section vào Admin Panel")
else:
    print("⚠️  Không tìm thấy placeholder __ADMIN_ONLINE_SECTION__")

if '<!-- __ADMIN_QUOTA_SECTION__ -->' in auth_html:
    auth_html = auth_html.replace(
        '<!-- __ADMIN_QUOTA_SECTION__ -->',
        build_quota_html()
    )
    print("✅ Đã chèn Quota Dashboard vào Admin Panel")
else:
    print("⚠️  Không tìm thấy placeholder __ADMIN_QUOTA_SECTION__")


# ═══════════════════════════════════════════════════════════════════
#  FULLWIDTH CSS
# ═══════════════════════════════════════════════════════════════════
FULLWIDTH_CSS = """
/* FULL-WIDTH SCALE */
.page-wrap { width: 100%; max-width: 100%; margin: 0 auto; overflow-x: hidden; }
.container {
    width: 100% !important;
    max-width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
}
.sticky-top { position: relative !important; width: 100% !important; max-width: 100% !important; }
.main, #mainContent { width: 100% !important; max-width: 100% !important; }
.search-bar { width: 100% !important; max-width: 100% !important; }
.search-bar input { width: 100% !important; max-width: 100% !important; }
.filters {
    display: grid !important;
    width: 100% !important;
    max-width: 100% !important;
    grid-template-columns: 1fr 1fr !important;
    gap: .75rem !important;
}
@media (min-width: 1000px) {
    .filters { grid-template-columns: 220px 260px !important; gap: 1rem !important; }
}
.result-count { margin-top: .5rem !important; }
.mobile-view {
    display: grid !important;
    width: 100% !important;
    max-width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
    gap: 1rem !important;
    grid-template-columns: 1fr !important;
}
@media (min-width: 769px) {
    .mobile-view { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; gap: 1.1rem !important; }
}
@media (min-width: 1800px) {
    .mobile-view { grid-template-columns: repeat(3, minmax(0, 1fr)) !important; gap: 1.2rem !important; }
}
@media (min-width: 2400px) {
    .mobile-view { grid-template-columns: repeat(4, minmax(0, 1fr)) !important; gap: 1.3rem !important; }
}
.demo-banner, .expiry-banner {
    width: 100% !important;
    max-width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
    margin-bottom: 1rem !important;
}
@media (min-width: 1000px) {
    .container { padding-left: 1.5rem !important; padding-right: 1.5rem !important; }
}
@media (min-width: 1400px) {
    .container { padding-left: 2rem !important; padding-right: 2rem !important; }
}
@media (min-width: 1900px) {
    .container { padding-left: 2.5rem !important; padding-right: 2.5rem !important; }
}
@media (max-width: 768px) {
    .container { padding-left: .7rem !important; padding-right: .7rem !important; }
    .mobile-view { gap: .8rem !important; }
}
.practice-full-modal {
    position: fixed !important;
    inset: 0 !important;
    z-index: 2500 !important;
    display: none;
    flex-direction: column !important;
    overflow: hidden !important;
}
.practice-full-modal.show { display: flex !important; }
.practice-full-header,
.pf-filters,
.practice-full-nav {
    flex: 0 0 auto !important;
}
.practice-full-body {
    flex: 1 1 auto !important;
    min-height: 0 !important;
    overflow-y: auto !important;
}
.practice-full-input {
    width: 100% !important;
    text-align: center !important;
    font-size: clamp(1.15rem, 2.2vw, 1.6rem) !important;
}

/* HEADER */
.header { position: relative; padding: .25rem 0; }
.header-inner {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
    gap: 1rem !important;
}
.logo {
    flex: 1 1 auto !important;
    min-width: 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: .9rem !important;
}
.logo-icon {
    width: clamp(46px, 4.5vw, 58px) !important;
    height: clamp(46px, 4.5vw, 58px) !important;
    border-radius: clamp(12px, 1.2vw, 16px) !important;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 40%, #d946ef 100%) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: #fff !important;
    font-size: clamp(1.2rem, 1.8vw, 1.6rem) !important;
    flex-shrink: 0 !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow:
        0 6px 20px rgba(139, 92, 246, 0.45),
        0 2px 6px rgba(139, 92, 246, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
    transition: transform .35s cubic-bezier(.34,1.56,.64,1),
                box-shadow .35s ease !important;
}
.logo-icon::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: linear-gradient(115deg, transparent 30%, rgba(255,255,255,.35) 50%, transparent 70%);
    transform: translateX(-100%) rotate(25deg);
    transition: transform .8s ease;
    pointer-events: none;
}
.logo-icon:hover::before { transform: translateX(100%) rotate(25deg); }
.logo-icon::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 30% 20%, rgba(255,255,255,.4), transparent 55%);
    pointer-events: none;
}
.logo-icon:hover {
    transform: translateY(-2px) rotate(-4deg) scale(1.04);
    box-shadow:
        0 10px 28px rgba(139, 92, 246, 0.6),
        0 4px 10px rgba(139, 92, 246, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
}
.logo-text {
    display: flex !important;
    flex-direction: column !important;
    line-height: 1.1 !important;
    min-width: 0 !important;
    overflow: hidden !important;
    gap: 4px !important;
}
.logo-text .title {
    font-size: clamp(1.25rem, 1.9vw, 1.7rem) !important;
    font-weight: 900 !important;
    letter-spacing: -0.025em !important;
    line-height: 1.15 !important;
    background: linear-gradient(135deg, #1e293b 0%, #4f46e5 50%, #7c3aed 100%) !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    color: transparent !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    position: relative !important;
}
[data-theme="dark"] .logo-text .title {
    background: linear-gradient(135deg, #f1f5f9 0%, #a5b4fc 50%, #c4b5fd 100%) !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}
.logo-text .subtitle {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.4rem !important;
    padding: 0.25rem 0.7rem !important;
    border-radius: 999px !important;
    background: linear-gradient(135deg,
        rgba(99, 102, 241, 0.13) 0%,
        rgba(139, 92, 246, 0.13) 50%,
        rgba(217, 70, 239, 0.13) 100%) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    color: #5b21b6 !important;
    font-size: clamp(.68rem, .85vw, .78rem) !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    margin-top: 3px !important;
    padding-left: 0.6rem !important;
    width: fit-content !important;
    max-width: 100% !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    box-shadow:
        0 1px 3px rgba(139, 92, 246, 0.12),
        inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
    transition: transform .3s ease, box-shadow .3s ease !important;
}
.logo-text .subtitle:hover {
    transform: translateY(-1px);
    box-shadow:
        0 4px 12px rgba(139, 92, 246, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}
.logo-text .subtitle::before {
    content: '✦';
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: #d946ef !important;
    font-size: 0.9em !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    flex-shrink: 0 !important;
    text-shadow:
        0 0 6px rgba(217, 70, 239, 0.7),
        0 0 12px rgba(139, 92, 246, 0.5) !important;
    animation: sparkleSubtitle 2.5s ease-in-out infinite !important;
}
@keyframes sparkleSubtitle {
    0%, 100% { opacity: 0.65; transform: scale(1) rotate(0deg); }
    50% {
        opacity: 1;
        transform: scale(1.2) rotate(18deg);
        text-shadow:
            0 0 10px rgba(217, 70, 239, 0.9),
            0 0 18px rgba(139, 92, 246, 0.7);
    }
}
[data-theme="dark"] .logo-text .subtitle {
    background: linear-gradient(135deg,
        rgba(99, 102, 241, 0.28) 0%,
        rgba(139, 92, 246, 0.28) 50%,
        rgba(217, 70, 239, 0.28) 100%) !important;
    border-color: rgba(165, 180, 252, 0.45) !important;
    color: #ddd6fe !important;
    box-shadow:
        0 1px 3px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
}
[data-theme="dark"] .logo-text .subtitle::before {
    color: #f0abfc !important;
    text-shadow:
        0 0 8px rgba(240, 171, 252, 0.9),
        0 0 16px rgba(165, 180, 252, 0.6) !important;
}
.header-actions {
    flex: 0 0 auto !important;
    margin-left: auto !important;
    display: flex !important;
    gap: .5rem !important;
    align-items: center !important;
}
.header-actions .icon-btn {
    width: clamp(34px, 3vw, 40px) !important;
    height: clamp(34px, 3vw, 40px) !important;
    border-radius: 11px !important;
    border: 1.5px solid var(--border) !important;
    background: var(--surface) !important;
    color: var(--text-2) !important;
    font-size: clamp(.82rem, 1vw, .95rem) !important;
    transition: transform .25s cubic-bezier(.34,1.56,.64,1),
                background .25s ease,
                color .25s ease,
                border-color .25s ease,
                box-shadow .25s ease !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05) !important;
}
.header-actions .icon-btn:hover {
    background: linear-gradient(135deg, #eff6ff, #ede9fe) !important;
    color: #4f46e5 !important;
    border-color: #a5b4fc !important;
    transform: translateY(-2px) scale(1.05) !important;
    box-shadow: 0 6px 16px rgba(139, 92, 246, 0.25) !important;
}
[data-theme="dark"] .header-actions .icon-btn:hover {
    background: linear-gradient(135deg, rgba(59,130,246,.2), rgba(139,92,246,.25)) !important;
    color: #a5b4fc !important;
    border-color: rgba(165, 180, 252, 0.5) !important;
}
.header-actions .trial-badge {
    position: relative !important;
    overflow: hidden !important;
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 50%, #ea580c 100%) !important;
    color: #fff !important;
    font-weight: 800 !important;
    letter-spacing: 0.03em !important;
    border: none !important;
    box-shadow:
        0 3px 10px rgba(245, 158, 11, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.15) !important;
}
.header-actions .trial-badge::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.5), transparent);
    animation: shimmerBadge 2.8s infinite;
    pointer-events: none;
}
@keyframes shimmerBadge {
    0% { left: -100%; }
    60%, 100% { left: 200%; }
}
.header-actions .demo-badge {
    background: linear-gradient(135deg, #fef3c7, #fde68a) !important;
    color: #78350f !important;
    font-weight: 800 !important;
    letter-spacing: 0.04em !important;
    border: 1.5px solid #f59e0b !important;
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.25) !important;
}
@media (max-width: 768px) {
    .logo { gap: .65rem !important; }
    .logo-icon {
        width: 44px !important;
        height: 44px !important;
        border-radius: 11px !important;
        font-size: 1.15rem !important;
    }
    .logo-text { gap: 3px !important; }
    .logo-text .title { font-size: 1.15rem !important; }
    .logo-text .subtitle {
        font-size: .6rem !important;
        padding: 0.2rem 0.55rem !important;
        gap: 0.35rem !important;
    }
    .header-inner { gap: .5rem !important; }
    .header-actions { gap: .35rem !important; }
    .header-actions .icon-btn {
        width: 34px !important;
        height: 34px !important;
        font-size: .82rem !important;
    }
}
@media (max-width: 400px) {
    .logo-text .subtitle { display: none !important; }
    .logo-icon { width: 40px !important; height: 40px !important; font-size: 1rem !important; }
    .logo-text .title { font-size: 1.05rem !important; }
}
"""

FULLWIDTH_CSS = override_fullwidth_css(FULLWIDTH_CSS)


# ═══════════════════════════════════════════════════════════════════
#  GHÉP CSS
# ═══════════════════════════════════════════════════════════════════
full_css = (
    override_ui_css(build_ui_css())
    + "\n/* ==== SOCIAL CSS ==== */\n" + build_social_css()
    + "\n/* ==== ACCOUNTS + RENEWAL CSS ==== */\n" + auth_css
    + "\n/* ==== INTRO CSS ==== */\n" + build_intro_css()
    + "\n/* ==== FAVORITES CSS ==== */\n" + build_favorites_css()
    + "\n/* ==== CHAT SUPPORT CSS ==== */\n" + build_chat_css()
    + "\n/* ==== ADMIN CHAT MANAGER CSS ==== */\n" + build_admin_chat_css()
    + "\n/* ==== DRAGGABLE FAB CSS ==== */\n" + build_draggable_fab_css()
    + "\n/* ==== FULLWIDTH SCALE + HEADER DESIGN ==== */\n" + FULLWIDTH_CSS
)


# ═══════════════════════════════════════════════════════════════════
#  GHÉP HTML BODY
# ═══════════════════════════════════════════════════════════════════
ui_html = override_ui_html(build_ui_html())
ui_html = ui_html.replace("<!-- __TIKTOK_BAR__ -->", build_tiktok_bar_html())
ui_html = ui_html.replace("<!-- __QUICK_INTRO_BANNER__ -->", build_intro_html())

# Chèn tab Yêu thích
_fav_html = build_favorites_html()

_fav_tab_patterns = [
    '<!-- __FAV_DATASET_TAB__ -->',
    '<!-- __FAV_DATASET_ITEM__ -->',
    '<!-- __FAV_ROW_TAB__ -->',
]
_fav_inserted = False
for _pat in _fav_tab_patterns:
    if _fav_inserted:
        break
    if _pat in ui_html:
        ui_html = ui_html.replace(_pat, _fav_html["dataset_tab"])
        _fav_inserted = True
        print("✅ Đã chèn tab Yêu thích (pattern: " + _pat + ")")

if not _fav_inserted:
    print("⚠️  Không tìm thấy placeholder tab Yêu thích")

# Chèn 2 nút float Practice Full
_pf_buttons = _fav_html["pf_float_btn"] + "\n" + _fav_html["pf_fav_only_btn"]
ui_html = ui_html.replace(
    '<a class="pf-tiktok-float" id="pfTiktokFloat"',
    _pf_buttons + '\n<a class="pf-tiktok-float" id="pfTiktokFloat"'
)

# Chèn dropdown item Yêu thích
_dd_patterns = [
    r'(<button[^>]*class="[^"]*ds-dropdown-item[^"]*"[^>]*data-dataset-group="chuyen-nganh"[^>]*>.*?</button>)',
    r'(<button[^>]*id="dsChuyenNganhDropdownItem"[^>]*>.*?</button>)',
    r'(<a[^>]*class="[^"]*ds-dropdown-item[^"]*"[^>]*data-dataset-group="chuyen-nganh"[^>]*>.*?</a>)',
]

_dd_inserted = False
for _pat in _dd_patterns:
    if _dd_inserted:
        break
    _new, _n = re.subn(
        _pat,
        r'\1\n            ' + _fav_html["dataset_dropdown_item"],
        ui_html,
        count=1,
        flags=re.DOTALL
    )
    if _n > 0:
        ui_html = _new
        _dd_inserted = True
        print("✅ Đã chèn 'Yêu thích' vào dropdown bộ dữ liệu")

if not _dd_inserted:
    print("ℹ️  Không tìm thấy dropdown Chuyên ngành")

social_html = build_social_html()
ui_html = ui_html.replace(
    '<div class="writer-modal" id="writerModal">',
    social_html + '\n<div class="writer-modal" id="writerModal">'
)

full_body = (
    '<div class="page-wrap">\n'
    + ui_html
    + "\n" + auth_html
    + "\n" + build_chat_html()
    + "\n" + build_admin_chat_html()
    + '\n</div>'
)


# ═══════════════════════════════════════════════════════════════════
#  GHÉP JS
# ═══════════════════════════════════════════════════════════════════
full_js = (
    build_config_js(CONFIG)
    + "\n/* ==== TELEGRAM NOTIFY ==== */\n" + build_telegram_notify_js()
    + "\n/* ==== UI JS ==== */\n" + override_ui_js(build_ui_js())
    + "\n/* ==== SOCIAL JS ==== */\n" + build_social_js()
    + "\n/* ==== ACCOUNTS + RENEWAL JS ==== */\n" + auth_js
    + "\n/* ==== INTRO JS ==== */\n" + build_intro_js()
    + "\n/* ==== FAVORITES JS ==== */\n" + build_favorites_js()
    + "\n/* ==== CHAT SUPPORT JS ==== */\n" + build_chat_js()
    + "\n/* ==== ADMIN CHAT MANAGER JS ==== */\n" + build_admin_chat_js()
    + "\n/* ==== DRAGGABLE FAB JS ==== */\n" + build_draggable_fab_js()
    + "\n/* ==== QUOTA JS ==== */\n" + build_quota_js()
    + "\n/* ==== QUOTA INIT ==== */\n" + build_quota_init_js()
)

full_js = full_js.replace('<script>', '').replace('</script>', '')
full_js = full_js.replace('<SCRIPT>', '').replace('</SCRIPT>', '')


# ═══════════════════════════════════════════════════════════════════
#  HTML SHELL
# ═══════════════════════════════════════════════════════════════════
HTML_SHELL = r'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, viewport-fit=cover">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<title>Học tiếng Trung · Văn phòng &amp; Công xưởng</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-firestore-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-database-compat.js"></script>
<script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3.5.0/dist/hanzi-writer.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
<style>
__CSS__
</style>
</head>
<body>

__BODY__

<script>
var RAW_DATA = __DATA__;
var DATASET_REGISTRY = __DATASET_REGISTRY__;
var CURRENT_DATASET = "__FIRST_DATASET__";

var FIREBASE_CONFIG = __FIREBASE_CONFIG__;

var DEMO_LIMIT = __DEMO_LIMIT__;
var DEMO_DAILY_LIMIT = __DEMO_DAILY_LIMIT__;
var DEMO_HSK_MAX = __DEMO_HSK_MAX__;

var TRIAL_MAX_QUESTIONS = __TRIAL_MAX_QUESTIONS__;
var TRIAL_MAX_HSK = __TRIAL_MAX_HSK__;
var TRIAL_UNLIMITED_WRITING = __TRIAL_UNLIMITED_WRITING__;

var TARGET_ADMINS = __TARGET_ADMINS__;
var SUPER_ADMIN = "__SUPER_ADMIN__";
var ZALO_PHONE = "__ZALO_PHONE__";
var ZALO_NAME = "__ZALO_NAME__";
var TIKTOK_USERNAME = "__TIKTOK_USERNAME__";
var TIKTOK_NICKNAME = "__TIKTOK_NICKNAME__";
var TIKTOK_AVATAR = "__TIKTOK_AVATAR__";
var TIKTOK_URL = "__TIKTOK_URL__";
var SYNONYMS = __SYNONYMS__;
var FILLER_WORDS = __FILLER_WORDS__;
var ONBOARDING_CONFIG = __ONBOARDING_CONFIG__;

var $ = function(id) { return document.getElementById(id); };

__JS__

window.__switchRawData = function(datasetId) {
    if (!DATASET_REGISTRY || !DATASET_REGISTRY[datasetId]) return false;
    RAW_DATA = DATASET_REGISTRY[datasetId].data || [];
    CURRENT_DATASET = datasetId;
    return true;
};
</script>

<script>
(function() {
    'use strict';
    try {
        var _TG_TOKEN = "__TELEGRAM_BOT_TOKEN__";
        var _TG_CHAT = "__TELEGRAM_CHAT_ID__";

        console.log('Telegram module init:', {
            hasToken: _TG_TOKEN && _TG_TOKEN.indexOf('__') !== 0 && _TG_TOKEN.length > 20,
            chatId: _TG_CHAT || '(empty)'
        });

        window.sendTelegramMessage = function(text) {
            try {
                if (!_TG_TOKEN || !_TG_CHAT || _TG_TOKEN.indexOf('__') === 0 || _TG_TOKEN.length < 20) {
                    console.log('Telegram chua cau hinh - bo qua');
                    return;
                }
                fetch('https://api.telegram.org/bot' + _TG_TOKEN + '/sendMessage', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        chat_id: _TG_CHAT,
                        text: text,
                        parse_mode: 'HTML',
                        disable_web_page_preview: true
                    })
                })
                .then(function(r) { return r.json(); })
                .then(function(d) {
                    if (d.ok) console.log('Telegram sent OK');
                    else console.warn('Telegram error:', d.description);
                })
                .catch(function(e) { console.warn('Telegram fetch:', e); });
            } catch(e) { console.warn('sendTelegramMessage:', e); }
        };

        window.notifyTelegramUserPaid = function(reqData) {
            try {
                var msg = 'YEU CAU GIA HAN MOI\n';
                msg += '-----------------\n';
                msg += 'User: ' + (reqData.name || reqData.email) + '\n';
                msg += 'Email: ' + reqData.email + '\n';
                msg += 'Amount: ' + (reqData.amount || 0).toLocaleString('vi-VN') + 'd\n';
                msg += 'Package: ' + (reqData.packageLabel || reqData.package || '') + '\n';
                msg += 'Code: ' + (reqData.transferCode || '') + '\n';
                window.sendTelegramMessage(msg);
            } catch(e) { console.warn('notifyTelegramUserPaid:', e); }
        };

        window.notifyTelegramAdminConfirmed = function(reqData, newExpiry) {
            try {
                var msg = 'DA XAC NHAN GIA HAN\n';
                msg += '-----------------\n';
                msg += 'User: ' + (reqData.name || reqData.email) + '\n';
                msg += 'Email: ' + reqData.email + '\n';
                msg += 'Amount: ' + (reqData.amount || 0).toLocaleString('vi-VN') + 'd\n';
                if (newExpiry) msg += 'Han moi: ' + newExpiry + '\n';
                window.sendTelegramMessage(msg);
            } catch(e) { console.warn('notifyTelegramAdminConfirmed:', e); }
        };

        console.log('Telegram module loaded');
    } catch(e) {
        console.error('Telegram module failed:', e);
    }
})();
</script>
</body>
</html>'''


# ═══════════════════════════════════════════════════════════════════
#  RENDER + GHI FILE
# ═══════════════════════════════════════════════════════════════════
html_output = (HTML_SHELL
    .replace("__CSS__",  full_css)
    .replace("__BODY__", full_body)
    .replace("__JS__",   full_js)
    .replace("__DATA__",              json_data)
    .replace("__DATASET_REGISTRY__",  dataset_registry_json)
    .replace("__FIREBASE_CONFIG__",   firebase_config_json)
    .replace("__SYNONYMS__",          synonyms_json)
    .replace("__FILLER_WORDS__",      fillers_json)
    .replace("__ONBOARDING_CONFIG__", onboarding_config_json)
    .replace("__FIRST_DATASET__",     _js_str(first_dataset_id))
    .replace("__DEMO_LIMIT__",            str(int(CONFIG["demo_limit"])))
    .replace("__DEMO_DAILY_LIMIT__",      str(int(CONFIG["demo_daily_limit"])))
    .replace("__DEMO_HSK_MAX__",          str(int(CONFIG["demo_hsk_max"])))
    .replace("__TRIAL_MAX_QUESTIONS__",   str(int(CONFIG.get("trial_max_questions", 50))))
    .replace("__TRIAL_MAX_HSK__",         str(int(CONFIG.get("trial_max_hsk", 5))))
    .replace("__TRIAL_UNLIMITED_WRITING__",
             "true" if CONFIG.get("trial_unlimited_writing", True) else "false")
    .replace("__TARGET_ADMINS__",         str(int(CONFIG["target_admins"])))
    .replace("__SUPER_ADMIN__",        _js_str(CONFIG["super_admin"]))
    .replace("__ZALO_PHONE__",         _js_str(CONFIG["zalo_phone"]))
    .replace("__ZALO_NAME__",          _js_str(CONFIG["zalo_name"]))
    .replace("__TIKTOK_USERNAME__",    _js_str(CONFIG["tiktok_username"]))
    .replace("__TIKTOK_NICKNAME__",    _js_str(CONFIG["tiktok_nickname"]))
    .replace("__TIKTOK_AVATAR__",      _js_str(CONFIG["tiktok_avatar"]))
    .replace("__TIKTOK_URL__",         _js_str(CONFIG["tiktok_url"]))
    .replace("__TELEGRAM_BOT_TOKEN__", _js_str(telegram_bot_token))
    .replace("__TELEGRAM_CHAT_ID__",   _js_str(telegram_chat_id))
)

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_output)

size_kb = os.path.getsize(OUTPUT_HTML) / 1024
total_datasets = len(DATASET_REGISTRY)
total_questions = sum(ds["count"] for ds in DATASET_REGISTRY.values())
main_count = sum(1 for ds in DATASET_REGISTRY.values() if ds["type"] == "main")
spec_count = sum(1 for ds in DATASET_REGISTRY.values() if ds["type"] == "specialty")

print("")
print("=" * 60)
print("🎉 Đã tạo: " + OUTPUT_HTML)
print("📦 Kích thước: " + str(round(size_kb, 1)) + " KB")
print("=" * 60)
print("📑 Tab chính   (data/):         " + str(main_count))
print("🏭 Chuyên ngành (script/data/): " + str(spec_count))
print("📚 Tổng dataset:                " + str(total_datasets))
print("📝 Tổng số câu:                 " + str(total_questions))
print("=" * 60)

_onb = CONFIG.get("onboarding", {})
if _onb.get("demo", {}).get("enabled"):
    _d = _onb["demo"]
    print("✅ Onboarding Demo: " + str(_d.get("max_questions", 0)) + " câu, "
          "HSK " + str(_d.get("hsk_allowed", [])) + ", "
          "tối đa " + str(_d.get("topics_per_user", 3)) + " chủ đề")
if _onb.get("trial", {}).get("enabled"):
    _t = _onb["trial"]
    print("✅ Onboarding Trial: " + str(_t.get("max_questions", 0)) + " câu, "
          "HSK " + str(_t.get("hsk_allowed", [])) + ", "
          "tối đa " + str(_t.get("topics_per_user", 5)) + " chủ đề")
