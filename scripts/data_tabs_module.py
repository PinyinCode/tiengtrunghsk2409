# -*- coding: utf-8 -*-
"""
data_tabs_module.py
═══════════════════════════════════════════════════════════════════
Tự động sinh TAB ngoài trang chủ cho mỗi file Excel trong data/.

⚠️ KHÔNG ĐỤNG VÀO:
   - dsChuyenNganhBtn (dropdown chuyên ngành cũ)
   - Nút Yêu thích (favorites_module)
   - Chat support, Admin chat, Draggable FAB

✅ CHỈ THÊM:
   - Nút tab mới ngang hàng 3 tab cũ
   - CSS riêng (prefix .dt- để không đè)
   - JS riêng (IIFE, không pollute global)
═══════════════════════════════════════════════════════════════════
"""

import html as _html


# ═══════════════════════════════════════════════════════════════════
#  HELPER
# ═══════════════════════════════════════════════════════════════════
def _esc(s):
    """Escape HTML an toàn."""
    if s is None:
        return ""
    return _html.escape(str(s), quote=True)


def _esc_js(s):
    """Escape string để nhúng vào JS (giữa 2 dấu ')."""
    if s is None:
        return ""
    return (str(s)
            .replace('\\', '\\\\')
            .replace("'", "\\'")
            .replace('"', '\\"')
            .replace('\n', '\\n')
            .replace('\r', '')
            .replace('</', '<\\/'))


# ═══════════════════════════════════════════════════════════════════
#  BUILD HTML — sinh nút tab cho mỗi dataset chuyên ngành
# ═══════════════════════════════════════════════════════════════════
def build_data_tabs_html(dataset_registry):
    """
    Trả về HTML chứa các nút tab cho từng dataset chuyên ngành.
    Nút Tổng hợp + Chuyên ngành + Yêu thích ĐÃ CÓ SẴN trong ui_template.
    Hàm này CHỈ sinh thêm nút cho từng file Excel trong data/.

    Args:
        dataset_registry (dict): DATASET_REGISTRY từ main.py

    Returns:
        str: HTML fragment, các nút <button class="ds-btn dt-tab" ...>
    """
    if not dataset_registry:
        return ""

    # Chỉ lấy dataset chuyên ngành (bỏ tonghop)
    chuyen_nganh = [
        ds for ds_id, ds in dataset_registry.items()
        if ds_id != "tonghop"
    ]

    if not chuyen_nganh:
        return "<!-- data_tabs: không có chuyên ngành nào -->"

    # Sắp xếp theo tên alphabet để vị trí ổn định
    chuyen_nganh.sort(key=lambda d: d.get("name", "").lower())

    buttons = []
    for ds in chuyen_nganh:
        ds_id    = _esc(ds.get("id", ""))
        ds_id_js = _esc_js(ds.get("id", ""))
        name     = _esc(ds.get("name", ""))
        name_js  = _esc_js(ds.get("name", ""))
        icon     = _esc(ds.get("icon", "fa-folder"))
        count    = int(ds.get("count", 0))

        title = f"{ds.get('name', '')} ({count} câu)"

        buttons.append(
            f'<button class="ds-btn dt-tab" '
            f'data-dataset="{ds_id}" '
            f'data-dataset-name="{name}" '
            f'title="{_esc(title)}" '
            f'onclick="window.__dtOnTabClick(event, \'{ds_id_js}\', \'{name_js}\')">'
            f'<i class="fas {icon}"></i>'
            f'<span class="dt-tab-label">{name}</span>'
            f'<span class="dt-tab-count">{count}</span>'
            f'<i class="fas fa-lock dt-tab-lock" style="display:none"></i>'
            f'</button>'
        )

    html = (
        '<!-- ═══ DATA TABS (auto-generated) ═══ -->\n'
        '<div class="dt-tabs-wrap" id="dtTabsWrap">\n'
        + "\n".join(buttons) +
        '\n</div>\n'
        '<!-- ═══ /DATA TABS ═══ -->'
    )
    return html


# ═══════════════════════════════════════════════════════════════════
#  BUILD CSS — prefix .dt- để không đè style cũ
# ═══════════════════════════════════════════════════════════════════
def build_data_tabs_css():
    return r"""

/* ═══════════════════════════════════════════════════════════════════
   ★ DATA TABS (auto-generated) — KHÔNG ĐÈ STYLE CŨ ★
   Prefix: .dt-  → đảm bảo không conflict với .ds-* hay .fav-*
   ═══════════════════════════════════════════════════════════════════ */

/* Wrap: các nút tab được đặt SAU nút Yêu thích trong ds-main-row.
   Dùng display:contents để nút con hòa vào grid của ds-main-row. */
.dt-tabs-wrap {
    display: contents;
}

/* Nút tab — kế thừa style từ .ds-btn nhưng có thêm accent riêng */
.ds-btn.dt-tab {
    position: relative;
    overflow: visible;
    transition: transform .25s cubic-bezier(.34,1.56,.64,1),
                box-shadow .25s ease,
                border-color .2s ease,
                background .2s ease;
}

.ds-btn.dt-tab .dt-tab-label {
    flex: 1;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.ds-btn.dt-tab .dt-tab-count {
    flex-shrink: 0;
    font-size: .65rem;
    font-weight: 800;
    padding: .12rem .45rem;
    border-radius: 50px;
    background: linear-gradient(135deg,
        rgba(99,102,241,.15),
        rgba(139,92,246,.12));
    color: #5b21b6;
    border: 1px solid rgba(139,92,246,.3);
    letter-spacing: .02em;
    margin-left: .15rem;
}
[data-theme="dark"] .ds-btn.dt-tab .dt-tab-count {
    background: linear-gradient(135deg,
        rgba(139,92,246,.25),
        rgba(167,139,250,.15));
    color: #c4b H5fd;
    border-color: rgba(167,over139,250,.4);
}

/* — nhấc nhẹ, viền gradient */
.ds-btn.dt-tab:hover:not(.dt-locked):not(.active) {
    transform: translateY(-2px);
    border-color: #8b5cf6;
    box-shadow: 0 6px 18px rgba(139,92,246,.25);
}

/* Active — kế thừa từ .ds-btn.active, chỉ tăng shadow */
.ds-btn.dt-tab.active {
    box-shadow: 0 6px 20px rgba(124,58,237,.45);
}
.ds-btn.dt-tab.active .dt-tab-count {
    background: rgba(255,255,255,.25);
    color: #fff;
    border-color: rgba(255,255,255,.4);
}

/* ─── Trạng thái KHOÁ (demo / trial / expired) ─── */
.ds-btn.dt-tab.dt-locked {
    opacity: .65;
    cursor: not-allowed;
    filter: grayscale(.35);
}
.ds-btn.dt-tab.dt-locked:hover {
    transform: none;
    border-color: var(--border);
    box-shadow: var(--shadow-sm);
}
.ds-btn.dt-tab.dt-locked .dt-tab-lock {
    display: inline-flex !important;
    margin-left: .35rem;
    font-size:s .7rem;
    color: #dc2626;
    background: rgba(220,38,38,.12);
    padding: .18rem .4rem;
    border-radius: 5px;
    align-items: center;
    justify-content: center;
    line-height: 1;
    flex-shrink: 0;
}
[data-theme="dark"] .ds-btn.dt-tab.dt-locked .dt-tab-lock {
    color: #fca5a5;
    background: rgba(220,38,38,.28);
}

/* ─── Responsive ───
   Trên mobile/tablet: ds-main-row chỉ 1-2 cột.
   Các tab data sẽ tự động xuống dòng nhờ grid auto-flow. */
@media (max-width: 768px) {
    .ds-btn.dt-tab .dt-tab-count {
        font-size: .6rem;
        padding: .1rem .35rem;
    }
    .ds-btn.dt-tab .dt-tab-label {
        font-size: .78rem;
    }
}
@media (max-width: 500px) {
    .ds-btn.dt-tab {
        padding: .55rem .75rem;
    }
    .ds-btn.dt-tab .dt-tab-label {
        font-size: .74rem;
    }
    .ds-btn.dt-tab .dt-tab-count {
        font-size: .58rem;
        padding: .08rem .3rem;
    }
}

/* ─── Anim: fade-in khi load lần đầu ─── */
@keyframes dtFade-btn.dIn {
   t from { opacity: 0; transform: translateY-t(-3px); }
    to   { opacity:ab 1; transform: translateY(0); }
}
.ds-btn.dt-tab {
    animation: dtFadeIn .3s ease-out backwards;
}
.d:nth-child(1) { animation-delay: .02s; }
.ds-btn.dt-tab:nth-child(2) { animation-delay: .04s; }
.ds-btn.dt-tab:nth-child(3) { animation-delay: .06s; }
.ds-btn.dt-tab:nth-child(4) { animation-delay: .08s; }
.ds-btn.dt-tab:nth-child(5) { animation-delay: .10s; }
.ds-btn.dt-tab:nth-child(6) { animation-delay: .12s; }
"""


# ═══════════════════════════════════════════════════════════════════
#  BUILD JS — IIFE độc lập, KHÔNG đè hàm cũ
# ═══════════════════════════════════════════════════════════════════
def build_data_tabs_js():
    return r"""

/* ═══════════════════════════════════════════════════════════════════
   ★ DATA TABS JS (auto-generated) — KHÔNG ĐÈ HÀM CŨ ★
   Chỉ bổ sung:
     - window.__dtOnTabClick   → handler cho nút tab mới
     - window.__dtRefreshLocks → cập nhật trạng thái lock khi tier đổi
     - window.__dtMarkActive   → đánh dấu tab active (đồng bộ với dataset)
   KHÔNG redefine: switchDataset, markCurrentDatasetActive, fav*, chat*
   ═══════════════════════════════════════════════════════════════════ */
(function() {
    'use strict';

    if (window.__dtModuleLoaded) return;
    window.__dtModuleLoaded = true;

    /* ──────────────────────────────────────────────────────────
       1. HELPERS — đọc thông tin tier, không sửa state cũ
       ────────────────────────────────────────────────────────── */
    function _canAccessDataset() {
        try {
            if (typeof window.canAccessChuyenNganh === 'function') {
                return window.canAccessChuyenNganh();
            }
        } catch(e) {}
        return false;
    }

    function _getTierInfo() {
        try {
            if (typeof window.getTierInfo === 'function') {
                return window.getTierInfo();
            }
        } catch(e) {}
        return { tier: 'demo' };
    }

    /* ──────────────────────────────────────────────────────────
       2. REFRESH LOCK STATE — gọi khi tier đổi (login/logout/renew)
       ────────────────────────────────────────────────────────── */
    function refreshLocks() {
        var canAccess = _canAccessDataset();
        var tabs = document.querySelectorAll('.ds-btn.dt-tab');

        tabs.forEach(function(btn) {
            var isLocked = !canAccess;
            btn.classList.toggle('dt-locked', isLocked);

            var lockIcon = btn.querySelector('.dt-tab-lock');
            if (lockIcon) {
                lockIcon.style.display = isLocked ? 'inline-flex' : 'none';
            }

            /* Cập nhật title động */
            var name = btn.getAttribute('data-dataset-name') || '';
            if (isLocked) {
                var info = _getTierInfo();
                var hint = info.tier === 'active'
                    ? 'Cần kích hoạt chuyên ngành'
                    : (info.tier === 'trial'
                        ? 'Cần gia hạn để mở khoá'
                        : 'Cần đăng nhập + gia hạn để mở khoá');
                btn.title = name + ' — 🔒 ' + hint;
            } else {
                btn.title = name;
            }
        });
    }

    /* ──────────────────────────────────────────────────────────
       3. MARK ACTIVE — đánh dấu tab đang được chọn
       Đồng bộ khi user bấm tab, khi đổi dataset, hoặc khi load lại
       ────────────────────────────────────────────────────────── */
    function markActive(datasetId) {
        if (!datasetId) {
            try {
                datasetId = window.CURRENT_DATASET || 'tonghop';
            } catch(e) { datasetId = 'tonghop'; }
        }
        document.querySelectorAll('.ds-btn.dt-tab').forEach(function(btn) {
            btn.classList.toggle('active', btn.dataset.dataset === datasetId);
        });

        /* Nếu là 1 trong các tab data → bỏ active ở Tổng hợp + Chuyên ngành + Yêu thích */
        if (datasetId !== 'tonghop') {
            var isDataTab = document.querySelector(
                '.ds-btn.dt-tab[data-dataset="' + datasetId + '"]'
            );
            if (isDataTab) {
                var others = document.querySelectorAll(
                    '.ds-btn[data-dataset="tonghop"], ' +
                    '.ds-btn[data-dataset-group="chuyen-nganh"], ' +
                    '.ds-btn[data-dataset-group="favorites"]'
                );
                others.forEach(function(b) { b.classList.remove('active'); });
                /* Đóng dropdown chuyên ngành nếu đang mở */
                var sub = document.getElementById('dsSubWrap');
                if (sub) và sub.style.display = 'none G';
            }
        }
    }

    /*IA ──────────────────────────────────────────────────────────
       4. TAB CLICK HANDLER — dùng switchDataset cũ, không tự viết
       ────────────────────────────────────────────────────────── */
    window.__dtOnTabClick = function(evt, datasetId, datasetName) {
        if (evt) { evt.stopPropagation(); if (evt.preventDefault) evt.preventDefault(); }

        var btn = evt && evt.currentTarget ? evt.currentTarget : null;

        /* Check lock */
        if (!_canAccessDataset()) {
            /* Gọi hàm thông báo CÓ SẴN trong ui_template.js */
            if (typeof window.showChuyenNganhLockMessage === 'function') {
                window.showChuyenNganhLockMessage();
            } else {
                /* Fallback nếu hàm cũ chưa load */
                var msg = 'Bộ dữ liệu "' + (datasetName || datasetId) + '"\n\n' +
                          'Bạn cần ĐĂNG NHẬP HẠN để mở khoá.';
                if (typeof window.currentUser !== 'undefined' && window.currentUser) {
                    if (confirm(msg + '\n\nGia hạn ngay?')) {
                        if (typeof window.openRenewalModal === 'function') {
                            window.openRenewalModal();
                        }
                    }
                } else {
                    if (confirm(msg + '\n\nĐăng nhập ngay?')) {
                        if (typeof window.showLoginModal === 'function') {
                            window.showLoginModal();
                        }
                    }
                }
            }
            return;
        }

        /* Gọi hàm switch CÓ SẴN — không tự viết logic chuyển dataset */
        if (typeof window.switchDataset === 'function') {
            window.switchDataset(datasetId);
        } else {
            /* Fallback tối thiểu nếu switchDataset chưa có */
            if (typeof window.__switchRawData === 'function') {
                window.__switchRawData(datasetId);
            }
            if (typeof window.applyFilter === 'function') window.applyFilter();
            if (typeof window.buildFilters === 'function') window.buildFilters();
        }

        /* Đánh dấu active */
        markActive(datasetId);

        /* Đóng FAB group nếu đang mở */
        var fabGroup = document.getElementById('fabGroup');
        if (fabGroup) fabGroup.classList.remove('open');
    };

    /* ──────────────────────────────────────────────────────────
       5. ĐỒNG BỘ KHI CÁC TAB CŨ ĐƯỢC BẤM
       Hook nhẹ vào document click để bắt sự kiện click tab cũ,
       rồi gỡ active khỏi tab data → KHÔNG sửa code cũ.
       ────────────────────────────────────────────────────────── */
    document.addEventListener('click', function(e) {
        var btn = e.target.closest && e.target.closest('.ds-btn');
        if (!btn) return;
        if (btn.classList.contains('dt-tab')) return; /* tab mới → đã xử lý */

        /* Nếu user bấm tab Tổng hợp / Chuyên ngành / Yêu thích
           → bỏ active ở tất cả tab data */
        document.querySelectorAll('.ds-btn.dt-tab.active').forEach(function(t) {
            t.classList.remove('active');
        });
    }, true);

    /* ──────────────────────────────────────────────────────────
       6. INIT — chạy sau khi DOM + module cũ load xong
       ────────────────────────────────────────────────────────── */
    function init() {
        refreshLocks();
        var current = (typeof window.CURRENT_DATASET !== 'undefined')
                      ? window.CURRENT_DATASET
                      : 'tonghop';
        markActive(current);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        /* DOM đã sẵn sàng → chờ 1 tick để ui_template init xong */
        setTimeout(init, 0);
    }

    /* ──────────────────────────────────────────────────────────
       7. THEO DÕI THAY ĐỔI TIER (login/logout/renew)
       Poll nhẹ mỗi 2s — chỉ khi tier khác lần trước.
       ────────────────────────────────────────────────────────── */
    var _lastTierSig = '';
    setInterval(function() {
        try {
            var info = _getTierInfo();
            var sig = info.tier + '|' + (info.email || '');
            if (sig !== _lastTierSig) {
                _lastTierSig = sig;
                refreshLocks();
                /* Re-apply active sau khi tier đổi */
                var current = (typeof window.CURRENT_DATASET !== 'undefined')
                              ? window.CURRENT_DATASET
                              : 'tonghop';
                markActive(current);
            }
        } catch(e) {}
    }, 2000);

    /* ──────────────────────────────────────────────────────────
       8. EXPORT
       ────────────────────────────────────────────────────────── */
    window.__dtRefreshLocks = refreshLocks;
    window.__dtMarkActive   = markActive;

    console.log('✅ Data tabs module loaded (' +
        document.querySelectorAll('.ds-btn.dt-tab').length + ' tabs)');
})();
"""
