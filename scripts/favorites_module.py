# -*- coding: utf-8 -*-
"""
Module FAVORITES — Tính năng Yêu thích câu.

Quy tắc tier:
  - ACTIVE / ADMIN  → dùng đầy đủ (lưu Firebase cloud + cache localStorage)
  - TRIAL / DEMO / EXPIRED → chỉ hiển thị icon khoá 🔒 + tab mờ 🔒
                              bấm vào mở dialog mời đăng nhập / gia hạn

★ FIX (2026-09): MỖI DATASET LƯU YÊU THÍCH RIÊNG BIỆT
   Key = "{datasetId}::{stt}" — câu #5 ở "Tổng hợp" KHÁC câu #5 ở "Nhân sự"
   → Không còn bug "dính tim" khi đổi dataset
"""


# ═══════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════
def build_favorites_css():
    return r"""
/* ═══════════════════════════════════════════════════════════════
   ❤️ FAVORITES — Nút tim trên card
   ═══════════════════════════════════════════════════════════════ */
.fav-btn{
    width:clamp(28px,2.8vw,32px);
    height:clamp(28px,2.8vw,32px);
    border-radius:50%;
    border:none;
    background:var(--surface-2);
    color:var(--text-3);
    cursor:pointer;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    font-size:clamp(.72rem,.9vw,.85rem);
    transition:all .2s cubic-bezier(.34,1.56,.64,1);
    flex-shrink:0;
    position:relative;
}
.fav-btn:hover{
    transform:scale(1.15);
    background:rgba(239,68,68,.12);
    color:#ef4444;
}
.fav-btn:active{transform:scale(.92);}
.fav-btn.active{color:#ef4444;background:rgba(239,68,68,.12);}
.fav-btn.active i{animation:favHeartPop .4s cubic-bezier(.34,1.56,.64,1);}
@keyframes favHeartPop{
    0%{transform:scale(1);}
    40%{transform:scale(1.4);}
    70%{transform:scale(.9);}
    100%{transform:scale(1);}
}
.fav-btn.active::after{
    content:'';position:absolute;inset:-4px;border-radius:50%;
    border:2px solid rgba(239,68,68,.4);
    animation:favRing .5s ease-out;pointer-events:none;
}
@keyframes favRing{
    0%{opacity:1;transform:scale(.8);}
    100%{opacity:0;transform:scale(1.4);}
}
.fav-btn.locked{color:#dc2626;background:rgba(220,38,38,.1);}
.fav-btn.locked:hover{
    transform:scale(1.12);background:rgba(220,38,38,.2);color:#b91c1c;
}
.fav-btn.locked i{font-size:.65rem;}
[data-theme="dark"] .fav-btn.locked{color:#fca5a5;background:rgba(220,38,38,.25);}
[data-theme="dark"] .fav-btn.locked:hover{background:rgba(220,38,38,.4);color:#fecaca;}

/* ═══════════════════════════════════════════════════════════════
   ❤️ Nút tim FLOAT (Practice Full) — góc phải
   ═══════════════════════════════════════════════════════════════ */
.pf-fav-float{
    position:fixed;
    right:clamp(14px,2vw,22px);
    bottom:calc(80px + env(safe-area-inset-bottom));
    display:none;align-items:center;gap:.5rem;
    padding:.65rem 1.1rem .65rem .9rem;
    border-radius:999px;
    border:2px solid rgba(239,68,68,.4);
    background:linear-gradient(135deg,#fef2f2,#fee2e2);
    color:#dc2626;
    font-size:clamp(.85rem,1vw,.95rem);font-weight:800;font-family:inherit;
    cursor:pointer;z-index:2450;
    transition:all .25s cubic-bezier(.34,1.56,.64,1);
    box-shadow:0 8px 24px rgba(239,68,68,.35),0 2px 8px rgba(0,0,0,.1);
    text-transform:uppercase;letter-spacing:.3px;
}
.pf-fav-float.show{display:inline-flex}
.pf-fav-float i{
    font-size:clamp(1.15rem,1.4vw,1.35rem);
    transition:transform .3s cubic-bezier(.34,1.56,.64,1);
}
.pf-fav-float:hover{
    transform:translateY(-3px) scale(1.05);
    border-color:#ef4444;
    box-shadow:0 12px 32px rgba(239,68,68,.5),0 4px 12px rgba(0,0,0,.15);
}
.pf-fav-float:hover i{transform:scale(1.15);}
.pf-fav-float:active{transform:translateY(-1px) scale(1.02);}
.pf-fav-float:not(.active):not(.locked){
    background:linear-gradient(135deg,#fef2f2,#fee2e2);
    color:#dc2626;border-color:rgba(239,68,68,.4);
}
.pf-fav-float.active{
    background:linear-gradient(135deg,#ef4444,#dc2626);
    color:#fff;border-color:#dc2626;
    box-shadow:0 8px 28px rgba(239,68,68,.6),0 2px 8px rgba(220,38,38,.3);
    animation:pfFavPulse 2s ease-in-out infinite;
}
.pf-fav-float.active i{animation:favHeartPop .5s cubic-bezier(.34,1.56,.64,1);}
.pf-fav-float.active::after{
    content:'';position:absolute;inset:-4px;border-radius:999px;
    border:2px solid rgba(239,68,68,.5);
    animation:favRing 1s ease-out infinite;pointer-events:none;
}
@keyframes pfFavPulse{
    0%,100%{box-shadow:0 8px 28px rgba(239,68,68,.6),0 2px 8px rgba(220,38,38,.3);}
    50%{box-shadow:0 8px 36px rgba(239,68,68,.85),0 4px 12px rgba(220,38,38,.4);}
}
.pf-fav-float.locked{
    background:linear-gradient(135deg,#fef3c7,#fde68a);
    color:#b45309;border-color:rgba(217,119,6,.5);animation:none;
}
.pf-fav-float.locked:hover{
    background:linear-gradient(135deg,#fde68a,#fcd34d);
    color:#92400e;border-color:#d97706;
    transform:translateY(-3px) scale(1.05);
}
.pf-fav-float.locked::after{display:none;}
.pf-fav-float .pf-fav-float-label{display:inline-block;white-space:nowrap;}
[data-theme="dark"] .pf-fav-float{
    background:linear-gradient(135deg,rgba(239,68,68,.2),rgba(220,38,38,.15));
    border-color:rgba(239,68,68,.5);color:#fca5a5;
}
[data-theme="dark"] .pf-fav-float.active{
    background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;
}
[data-theme="dark"] .pf-fav-float.locked{
    background:linear-gradient(135deg,rgba(217,119,6,.25),rgba(180,83,9,.2));
    color:#fcd34d;border-color:rgba(217,119,6,.5);
}

/* ═══════════════════════════════════════════════════════════════
   ❤️ Nút toggle "Chỉ câu yêu thích" (Practice Full)
   ═══════════════════════════════════════════════════════════════ */
.pf-fav-only-float{
    position:fixed;
    left:clamp(14px,2vw,22px);
    bottom:calc(80px + env(safe-area-inset-bottom));
    display:none;align-items:center;gap:.5rem;
    padding:.65rem 1.1rem .65rem .9rem;
    border-radius:999px;
    border:2px solid var(--border);
    background:var(--surface);
    color:var(--text-2);
    font-size:clamp(.82rem,.95vw,.92rem);font-weight:800;font-family:inherit;
    cursor:pointer;z-index:2450;
    transition:all .25s cubic-bezier(.34,1.56,.64,1);
    box-shadow:0 4px 14px rgba(0,0,0,.12);
    text-transform:uppercase;letter-spacing:.3px;user-select:none;
}
.pf-fav-only-float.show{display:inline-flex;}
.pf-fav-only-float i{
    font-size:clamp(1rem,1.2vw,1.15rem);
    transition:transform .3s cubic-bezier(.34,1.56,.64,1);
}
.pf-fav-only-float:hover{
    transform:translateY(-3px) scale(1.04);
    border-color:#ef4444;color:#dc2626;
    box-shadow:0 8px 22px rgba(239,68,68,.3);
}
.pf-fav-only-float:active{transform:translateY(-1px) scale(1.01);}
.pf-fav-only-float .pf-fav-only-count{
    min-width:20px;height:20px;padding:0 .4rem;border-radius:50px;
    background:rgba(239,68,68,.15);color:#dc2626;
    font-size:.68rem;font-weight:900;
    display:inline-flex;align-items:center;justify-content:center;
    line-height:1;transition:.2s;
}
.pf-fav-only-float.active{
    background:linear-gradient(135deg,#ef4444,#dc2626);
    color:#fff;border-color:#dc2626;
    box-shadow:0 8px 24px rgba(239,68,68,.5);
}
.pf-fav-only-float.active i{animation:favHeartPop .4s cubic-bezier(.34,1.56,.64,1);}
.pf-fav-only-float.active .pf-fav-only-count{
    background:rgba(255,255,255,.3);color:#fff;
}
.pf-fav-only-float.locked{
    background:linear-gradient(135deg,#fef3c7,#fde68a);
    color:#b45309;border-color:rgba(217,119,6,.5);
}
.pf-fav-only-float.locked:hover{
    background:linear-gradient(135deg,#fde68a,#fcd34d);
    color:#92400e;border-color:#d97706;
    transform:translateY(-3px) scale(1.04);
}
.pf-fav-only-float.locked .pf-fav-only-count{
    background:rgba(217,119,6,.2);color:#92400e;
}
.pf-fav-only-float.empty{opacity:.55;}
.pf-fav-only-float.empty .pf-fav-only-count{display:none;}
[data-theme="dark"] .pf-fav-only-float{
    background:var(--surface-2);border-color:var(--border);color:var(--text-2);
}
[data-theme="dark"] .pf-fav-only-float.active{
    background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;border-color:#dc2626;
}
[data-theme="dark"] .pf-fav-only-float.locked{
    background:linear-gradient(135deg,rgba(217,119,6,.25),rgba(180,83,9,.2));
    color:#fcd34d;border-color:rgba(217,119,6,.5);
}

/* ═══════════════════════════════════════════════════════════════
   ❤️ Responsive
   ═══════════════════════════════════════════════════════════════ */
@media (max-width:500px){
    .pf-fav-float{
        padding:.55rem .9rem .55rem .75rem;font-size:.78rem;
        bottom:calc(78px + env(safe-area-inset-bottom));
    }
    .pf-fav-float i{font-size:1.05rem;}
    .pf-fav-float .pf-fav-float-label{display:none;}

    .pf-fav-only-float{
        padding:.55rem .9rem .55rem .75rem;font-size:.78rem;
        bottom:calc(78px + env(safe-area-inset-bottom));
    }
    .pf-fav-only-float i{font-size:1rem;}
    .pf-fav-only-float .pf-fav-only-label{display:none;}
}
@media (max-width:400px){
    .pf-fav-float{padding:.5rem;min-width:46px;justify-content:center;}
    .pf-fav-only-float{padding:.5rem;min-width:46px;justify-content:center;}
}
@media (max-height:550px) and (orientation:landscape){
    .pf-fav-float{
        bottom:calc(64px + env(safe-area-inset-bottom));
        transform:scale(.9);transform-origin:right bottom;
    }
    .pf-fav-only-float{
        bottom:calc(64px + env(safe-area-inset-bottom));
        transform:scale(.9);transform-origin:left bottom;
    }
}

/* ═══════════════════════════════════════════════════════════════
   ❤️ Tab trong dataset selector
   ═══════════════════════════════════════════════════════════════ */
.ds-btn[data-dataset-group="favorites"]{position:relative;overflow:visible;}
.ds-btn[data-dataset-group="favorites"] .ds-fav-badge{
    position:absolute;top:-8px;right:-6px;
    min-width:22px;height:22px;padding:0 .4rem;border-radius:50px;
    background:linear-gradient(135deg,#ef4444,#dc2626);
    color:#fff;font-size:.65rem;font-weight:900;
    display:flex;align-items:center;justify-content:center;
    box-shadow:0 2px 8px rgba(239,68,68,.5),0 0 0 2px var(--surface);
    animation:favBadgePulse 2s ease-in-out infinite;
    z-index:10;line-height:1;
}
.ds-btn[data-dataset-group="favorites"] .ds-fav-badge[data-count="0"]{display:none;}
@keyframes favBadgePulse{
    0%,100%{transform:scale(1);}
    50%{transform:scale(1.1);}
}
.ds-btn[data-dataset-group="favorites"] .ds-fav-lock{
    position:absolute;top:-8px;right:-6px;width:22px;height:22px;border-radius:50%;
    background:linear-gradient(135deg,#dc2626,#b91c1c);
    color:#fff;display:flex;align-items:center;justify-content:center;
    font-size:.62rem;
    box-shadow:0 2px 8px rgba(220,38,38,.55),0 0 0 2px var(--surface);
    z-index:10;
}
.ds-btn[data-dataset-group="favorites"] i:first-child{color:#ef4444;}
.ds-btn[data-dataset-group="favorites"].active i:first-child{color:#fff;}
.ds-btn[data-dataset-group="favorites"].fav-locked{opacity:.65;cursor:pointer;}
.ds-btn[data-dataset-group="favorites"].fav-locked:hover{
    opacity:.85;border-color:#dc2626;background:rgba(220,38,38,.06);
}
.ds-btn[data-dataset-group="favorites"].fav-locked i:first-child{color:#dc2626;}
[data-theme="dark"] .ds-btn[data-dataset-group="favorites"].fav-locked i:first-child{color:#fca5a5;}

/* ═══════════════════════════════════════════════════════════════
   ❤️ Dropdown item (bộ dữ liệu)
   ═══════════════════════════════════════════════════════════════ */
.ds-dropdown-item[data-dataset-group="favorites"]{position:relative;}
.ds-dropdown-item[data-dataset-group="favorites"] .ds-dd-fav-icon{color:#ef4444;}
.ds-dropdown-item[data-dataset-group="favorites"].active .ds-dd-fav-icon{color:#fff;}
.ds-dropdown-item[data-dataset-group="favorites"] .ds-dd-fav-badge{
    margin-left:auto;min-width:20px;height:20px;padding:0 .42rem;border-radius:50px;
    background:linear-gradient(135deg,#ef4444,#dc2626);
    color:#fff;font-size:.62rem;font-weight:900;
    display:inline-flex;align-items:center;justify-content:center;
    box-shadow:0 2px 6px rgba(239,68,68,.45);line-height:1;
}
.ds-dropdown-item[data-dataset-group="favorites"] .ds-dd-fav-badge[data-count="0"]{display:none;}
.ds-dropdown-item[data-dataset-group="favorites"] .ds-dd-fav-lock{
    margin-left:auto;color:#dc2626;font-size:.7rem;
}
.ds-dropdown-item[data-dataset-group="favorites"].fav-locked{opacity:.7;}
.ds-dropdown-item[data-dataset-group="favorites"].fav-locked .ds-dd-fav-icon{color:#dc2626;}
[data-theme="dark"] .ds-dropdown-item[data-dataset-group="favorites"].fav-locked .ds-dd-fav-icon{
    color:#fca5a5;
}

/* ═══════════════════════════════════════════════════════════════
   ❤️ Empty states
   ═══════════════════════════════════════════════════════════════ */
.fav-empty{
    grid-column:1 / -1;padding:3rem 1.5rem;text-align:center;
    background:linear-gradient(135deg,rgba(239,68,68,.04),rgba(220,38,38,.02));
    border:2px dashed rgba(239,68,68,.25);border-radius:16px;
}
[data-theme="dark"] .fav-empty{
    background:linear-gradient(135deg,rgba(239,68,68,.1),rgba(220,38,38,.05));
    border-color:rgba(239,68,68,.35);
}
.fav-empty .fav-empty-icon{
    width:70px;height:70px;margin:0 auto 1rem;border-radius:50%;
    background:linear-gradient(135deg,rgba(239,68,68,.15),rgba(220,38,38,.1));
    color:#ef4444;display:flex;align-items:center;justify-content:center;
    font-size:1.8rem;animation:favEmptyFloat 3s ease-in-out infinite;
}
@keyframes favEmptyFloat{
    0%,100%{transform:translateY(0) scale(1);}
    50%{transform:translateY(-6px) scale(1.05);}
}
.fav-empty .fav-empty-title{
    font-size:1.05rem;font-weight:800;color:var(--text);margin-bottom:.4rem;
}
.fav-empty .fav-empty-desc{
    font-size:.85rem;color:var(--text-2);line-height:1.5;
    max-width:420px;margin:0 auto;
}
.fav-empty .fav-empty-desc b{color:#dc2626;font-weight:800;}
.fav-locked-empty{
    grid-column:1 / -1;padding:3rem 1.5rem;text-align:center;
    background:linear-gradient(135deg,rgba(220,38,38,.06),rgba(185,28,28,.03));
    border:2px dashed rgba(220,38,38,.35);border-radius:16px;
}
.fav-locked-empty .fav-empty-cta{
    display:inline-flex;align-items:center;gap:.4rem;margin-top:1rem;
    padding:.6rem 1.2rem;border-radius:50px;border:none;
    background:linear-gradient(135deg,#dc2626,#b91c1c);
    color:#fff;font-size:.85rem;font-weight:800;font-family:inherit;
    cursor:pointer;box-shadow:0 6px 18px rgba(220,38,38,.4);
    transition:all .2s;text-transform:uppercase;letter-spacing:.3px;
}
.fav-locked-empty .fav-empty-cta:hover{
    transform:translateY(-2px) scale(1.03);
    box-shadow:0 10px 26px rgba(220,38,38,.6);
}

/* ═══════════════════════════════════════════════════════════════
   ❤️ Toast
   ═══════════════════════════════════════════════════════════════ */
.fav-toast{
    position:fixed;top:80px;left:50%;
    transform:translateX(-50%) translateY(-20px);
    padding:.7rem 1.2rem;border-radius:50px;
    font-size:.85rem;font-weight:800;font-family:inherit;color:#fff;
    z-index:9999;opacity:0;
    transition:opacity .25s ease, transform .3s cubic-bezier(.34,1.56,.64,1);
    pointer-events:none;display:flex;align-items:center;gap:.5rem;
    max-width:90vw;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
    box-shadow:0 8px 24px rgba(0,0,0,.25);
}
.fav-toast.show{opacity:1;transform:translateX(-50%) translateY(0);}
.fav-toast.add{background:linear-gradient(135deg,#ef4444,#dc2626);}
.fav-toast.remove{background:linear-gradient(135deg,#64748b,#475569);}
.fav-toast.warn{background:linear-gradient(135deg,#f59e0b,#d97706);}
.fav-toast i{font-size:1rem;}

/* ═══════════════════════════════════════════════════════════════
   ★ FIX 2026-09: KHÔNG ZOOM TO
   ═══════════════════════════════════════════════════════════════ */
.pf-fav-float,
.pf-fav-only-float {
    max-width: 180px;
    max-height: 44px;
    padding: .55rem .95rem .55rem .8rem;
    font-size: .82rem;
    box-sizing: border-box;
}
.pf-fav-float i,
.pf-fav-only-float i {
    font-size: 1.05rem;
}

@media (min-width: 1600px) {
    .pf-fav-float,
    .pf-fav-only-float {
        max-width: 170px;
        max-height: 42px;
        font-size: .8rem;
        padding: .5rem .85rem .5rem .75rem;
    }
    .pf-fav-float i,
    .pf-fav-only-float i {
        font-size: 1rem;
    }
}

@media (max-height: 550px) and (orientation: landscape) {
    .pf-fav-float {
        transform: scale(.9) !important;
        transform-origin: right bottom;
    }
    .pf-fav-only-float {
        transform: scale(.9) !important;
        transform-origin: right bottom;
    }
}

/* ═══════════════════════════════════════════════════════════════
   ★ NÚT TOGGLE "CHỈ CÂU YÊU THÍCH" — TRẠNG THÁI CÂU KHÔNG PHẢI YÊU THÍCH
   ═══════════════════════════════════════════════════════════════ */
.pf-fav-only-float.current-not-fav {
    opacity: 0.5 !important;
    filter: grayscale(0.6);
    cursor: not-allowed;
    pointer-events: auto;
}

.pf-fav-only-float.current-not-fav:hover {
    transform: none !important;
    border-color: var(--border) !important;
    color: var(--text-2) !important;
    box-shadow: 0 4px 14px rgba(0,0,0,.12) !important;
    opacity: 0.6 !important;
}

.pf-fav-only-float.current-not-fav i {
    animation: none !important;
}

.pf-fav-only-float.current-not-fav .pf-fav-only-count {
    background: rgba(148, 163, 184, 0.2);
    color: var(--text-3);
}

[data-theme="dark"] .pf-fav-only-float.current-not-fav {
    background: var(--surface-2);
    border-color: var(--border);
    color: var(--text-3);
}

[data-theme="dark"] .pf-fav-only-float.current-not-fav:hover {
    background: var(--surface-2) !important;
    border-color: var(--border) !important;
}
"""


# ═══════════════════════════════════════════════════════════════
# HTML SNIPPETS
# ═══════════════════════════════════════════════════════════════
def build_favorites_html():
    return {
        "dataset_tab":
            '<button class="ds-btn ds-btn-primary" data-dataset-group="favorites" id="dsFavBtn">\n'
            '            <i class="far fa-heart"></i>\n'
            '            <span>Yêu thích</span>\n'
            '            <span class="ds-fav-badge" id="favTabBadge" data-count="0"></span>\n'
            '            <i class="fas fa-lock ds-fav-lock" id="favTabLock" style="display:none;"></i>\n'
            '        </button>',

        "dataset_dropdown_item":
            '<button class="ds-dropdown-item" data-dataset-group="favorites" id="dsFavDropdownItem" type="button">\n'
            '            <i class="far fa-heart ds-dd-fav-icon"></i>\n'
            '            <span>Yêu thích</span>\n'
            '            <span class="ds-dd-fav-badge" id="favDropdownBadge" data-count="0"></span>\n'
            '            <i class="fas fa-lock ds-dd-fav-lock" id="favDropdownLock" style="display:none;"></i>\n'
            '        </button>',

        "pf_float_btn":
            '<button class="pf-fav-float" id="pfFavBtn" type="button" '
            'title="Thêm vào yêu thích" aria-label="Thêm vào yêu thích">'
            '<i class="far fa-heart"></i>'
            '<span class="pf-fav-float-label">Like</span>'
            '</button>',

        "pf_fav_only_btn":
            '<button class="pf-fav-only-float" id="pfFavOnlyBtn" type="button" '
            'title="Chỉ luyện câu yêu thích" aria-label="Chỉ luyện câu yêu thích">'
            '<i class="far fa-heart"></i>'
            '<span class="pf-fav-only-label">Favorites Only</span>'
            '<span class="pf-fav-only-count" id="pfFavOnlyCount">0</span>'
            '</button>',
    }


# ═══════════════════════════════════════════════════════════════
# JS — Toàn bộ logic
# ═══════════════════════════════════════════════════════════════
def build_favorites_js():
    return r"""
/* ═══════════════════════════════════════════════════════════════
   ❤️ FAVORITES — Module quản lý câu yêu thích
   
   ★ KEY FORMAT: "{datasetId}::{stt}"
   Ví dụ: "tonghop::5" hoặc "nhansu::5"
   → Mỗi dataset lưu yêu thích RIÊNG BIỆT
   ═══════════════════════════════════════════════════════════════ */

/* ============ STATE ============ */
var favState = {
    items: {},
    loaded: false,
    loading: false,
    sortMode: 'recent',
    listener: null,
    currentView: false,
    filteringOnly: false,
    pfOnlyFav: false,
    __renderTimer: null
};

/* ═══════════════════════════════════════════════════════════════
   ★ HELPER: TẠO KEY YÊU THÍCH CÓ DATASET PREFIX
   ═══════════════════════════════════════════════════════════════ */
function getFavKey(stt) {
    if (stt === null || stt === undefined) return '';
    var dsId = (typeof CURRENT_DATASET !== 'undefined' && CURRENT_DATASET)
               ? CURRENT_DATASET
               : 'tonghop';
    return dsId + '::' + String(stt);
}

function getFavKeyInDataset(stt, datasetId) {
    if (stt === null || stt === undefined) return '';
    var dsId = datasetId || 'tonghop';
    return dsId + '::' + String(stt);
}

/* ═══ Check yêu thích theo stt (dùng dataset hiện tại) ═══ */
function favHas(stt) {
    if (stt === null || stt === undefined) return false;
    var key = getFavKey(stt);
    return !!favState.items[key];
}

/* ═══ Check yêu thích theo dataset cụ thể ═══ */
function favHasInDataset(stt, datasetId) {
    if (stt === null || stt === undefined) return false;
    if (!datasetId) return favHas(stt);
    var key = getFavKeyInDataset(stt, datasetId);
    return !!favState.items[key];
}

/* ============ TIER CHECK ============ */
function favCanUse() {
    if (typeof window.APP_TIER === 'undefined') return false;
    return window.APP_TIER === 'active';
}

function favIsLoggedIn() {
    return typeof currentUser !== 'undefined' && currentUser !== null;
}

function favGetCurrentEmail() {
    if (favIsLoggedIn() && currentUser.email) return currentUser.email.toLowerCase();
    return null;
}

function favGetStorageKey() {
    var email = favGetCurrentEmail();
    return email ? ('favorites_cache_' + email) : 'favorites_guest';
}

/* ============ LOCK DIALOG ============ */
function favShowLockDialog() {
    if (!favIsLoggedIn()) {
        if (confirm('❤️ Yêu thích câu\n\n' +
                    'Bạn cần ĐĂNG NHẬP và GIA HẠN để dùng tính năng này.\n\n' +
                    'Đăng nhập ngay?')) {
            if (typeof showLoginModal === 'function') showLoginModal();
        }
        return;
    }
    var tier = (typeof window.APP_TIER !== 'undefined') ? window.APP_TIER : 'demo';
    if (tier === 'demo' || tier === 'trial' || tier === 'expired') {
        if (confirm('❤️ Yêu thích câu\n\n' +
                    'Chỉ tài khoản ĐÃ GIA HẠN mới dùng được tính năng này.\n\n' +
                    'Gia hạn ngay để lưu câu yêu thích?')) {
            if (typeof openRenewalModal === 'function') openRenewalModal();
        }
        return;
    }
}

/* ============ LOAD / SAVE LOCAL ============ */
function favLoadFromLocal() {
    try {
        var key = favGetStorageKey();
        var cached = JSON.parse(localStorage.getItem(key) || 'null');
        if (cached && cached.items && typeof cached.items === 'object') {
            favState.items = cached.items;
            return true;
        }
    } catch(e) {}
    return false;
}

function favSaveToLocal() {
    try {
        var key = favGetStorageKey();
        localStorage.setItem(key, JSON.stringify({
            items: favState.items,
            savedAt: Date.now()
        }));
    } catch(e) {}
}

/* ============ LOAD / LISTEN CLOUD ============ */
async function favLoadFromCloud() {
    if (!favCanUse()) return;
    var email = favGetCurrentEmail();
    if (!email || typeof db === 'undefined' || !db) return;
    if (favState.loading) return;
    favState.loading = true;

    try {
        var snap = await db.collection('favorites').doc(email).collection('items').get();
        var items = {};
        snap.forEach(function(doc) {
            var d = doc.data() || {};
            /* ⭐ Key mới: "dataset::stt" — Key cũ chỉ có "stt" → gán "tonghop" */
            var key = d.key || (d.dataset ? (d.dataset + '::' + d.stt) : ('tonghop::' + (d.stt || doc.id)));
            items[key] = {
                key: key,
                stt: String(d.stt || doc.id || ''),
                dataset: d.dataset || 'tonghop',
                addedAt: d.addedAt ? (d.addedAt.toMillis ? d.addedAt.toMillis() : d.addedAt) : Date.now(),
                hsk: d.hsk || '',
                subject: d.subject || ''
            };
        });
        favState.items = items;
        favState.loaded = true;
        favSaveToLocal();
        favNotifyChanged();
        favListenCloud();
    } catch(e) {
        console.warn('[Favorites] Load cloud error:', e);
    } finally {
        favState.loading = false;
    }
}

function favListenCloud() {
    if (!favCanUse()) return;
    var email = favGetCurrentEmail();
    if (!email || typeof db === 'undefined' || !db) return;

    if (favState.listener) {
        try { favState.listener(); } catch(e) {}
        favState.listener = null;
    }

    favState.listener = db.collection('favorites').doc(email).collection('items')
        .onSnapshot(function(snap) {
            var items = {};
            snap.forEach(function(doc) {
                var d = doc.data() || {};
                var key = d.key || (d.dataset ? (d.dataset + '::' + d.stt) : ('tonghop::' + (d.stt || doc.id)));
                items[key] = {
                    key: key,
                    stt: String(d.stt || doc.id || ''),
                    dataset: d.dataset || 'tonghop',
                    addedAt: d.addedAt ? (d.addedAt.toMillis ? d.addedAt.toMillis() : d.addedAt) : Date.now(),
                    hsk: d.hsk || '',
                    subject: d.subject || ''
                };
            });
            favState.items = items;
            favState.loaded = true;
            favSaveToLocal();
            favNotifyChanged();
        }, function(err) {
            console.warn('[Favorites] Listener error:', err);
        });
}

/* ============ ADD / REMOVE ============ */
async function favAdd(stt, record) {
    if (!favCanUse()) { favShowLockDialog(); return false; }
    var email = favGetCurrentEmail();
    if (!email) { favShowLockDialog(); return false; }

    /* ⭐ Key có dataset prefix */
    var key = getFavKey(stt);
    var dsId = (typeof CURRENT_DATASET !== 'undefined') ? CURRENT_DATASET : 'tonghop';

    /* ═══ Check admin ═══ */
    var isAdmin = (typeof currentUser !== 'undefined'
                   && currentUser
                   && currentUser.role === 'admin');

    /* ═══ Giới hạn 500 tim/ngày ═══ */
    var MAX_PER_DAY = 500;
    var today = new Date().toDateString();

    if (!isAdmin) {
        var dayKey = 'fav_daily_' + email;
        var daily = { date: today, count: 0 };

        try {
            var saved = JSON.parse(localStorage.getItem(dayKey) || 'null');
            if (saved && saved.date === today) {
                daily = saved;
            } else {
                daily = { date: today, count: 0 };
            }
        } catch(e) {
            daily = { date: today, count: 0 };
        }

        if (daily.count >= MAX_PER_DAY) {
            var tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            tomorrow.setHours(0, 0, 0, 0);
            var hoursLeft = Math.ceil((tomorrow - Date.now()) / 3600000);
            favShowToast('Đã đạt giới hạn ' + MAX_PER_DAY + ' tim hôm nay. Còn ' + hoursLeft + 'h!', 'warn');
            return false;
        }

        daily.count++;
        daily.date = today;
        try {
            localStorage.setItem(dayKey, JSON.stringify(daily));
        } catch(e) {}
    }

    /* ═══ Lưu local với KEY có dataset ═══ */
    favState.items[key] = {
        key: key,
        stt: String(stt),
        dataset: dsId,
        addedAt: Date.now(),
        hsk: record && record.hsk ? record.hsk : '',
        subject: record && record.subject ? record.subject : ''
    };
    favSaveToLocal();
    favNotifyChanged();

    /* ═══ Đồng bộ Firestore — dùng key làm doc ID ═══ */
    if (typeof db !== 'undefined' && db) {
        try {
            await db.collection('favorites').doc(email)
                .collection('items').doc(encodeURIComponent(key)).set({
                    key: key,
                    stt: String(stt),
                    dataset: dsId,
                    hsk: favState.items[key].hsk,
                    subject: favState.items[key].subject,
                    addedAt: firebase.firestore.FieldValue.serverTimestamp()
                });
        } catch(e) {
            console.warn('[Favorites] Add cloud error:', e);
            delete favState.items[key];
            favSaveToLocal();
            favNotifyChanged();

            if (!isAdmin) {
                try {
                    var dayKey2 = 'fav_daily_' + email;
                    var d2 = JSON.parse(localStorage.getItem(dayKey2) || 'null');
                    if (d2 && d2.date === today && d2.count > 0) {
                        d2.count--;
                        localStorage.setItem(dayKey2, JSON.stringify(d2));
                    }
                } catch(e2) {}
            }
            favShowToast('Lỗi lưu! Thử lại sau', 'warn');
            return false;
        }
    }
    return true;
}

async function favRemove(stt) {
    if (!favCanUse()) { favShowLockDialog(); return false; }
    var email = favGetCurrentEmail();
    if (!email) return false;

    /* ⭐ Key có dataset prefix */
    var key = getFavKey(stt);
    var backup = favState.items[key];
    if (!backup) return true;

    delete favState.items[key];
    favSaveToLocal();
    favNotifyChanged();

    if (typeof db !== 'undefined' && db) {
        try {
            await db.collection('favorites').doc(email)
                .collection('items').doc(encodeURIComponent(key)).delete();
        } catch(e) {
            console.warn('[Favorites] Remove cloud error:', e);
            favState.items[key] = backup;
            favSaveToLocal();
            favNotifyChanged();
            return false;
        }
    }
    return true;
}

async function favToggle(stt, record) {
    if (!favCanUse()) { favShowLockDialog(); return; }
    var key = getFavKey(stt);
    if (favState.items[key]) {
        var ok = await favRemove(stt);
        if (ok) favShowToast('Đã xoá khỏi yêu thích', 'remove');
    } else {
        var ok2 = await favAdd(stt, record);
        if (ok2) favShowToast('Đã thêm vào yêu thích', 'add');
    }
}

async function favClearAll() {
    if (!favCanUse()) { favShowLockDialog(); return; }
    var email = favGetCurrentEmail();
    if (!email) return;

    var count = favCount();
    if (count === 0) {
        favShowToast('Chưa có câu yêu thích nào', 'warn');
        return;
    }

    if (!confirm('Xoá TẤT CẢ ' + count + ' câu yêu thích?\n\nKhông thể hoàn tác!')) return;

    var backup = favState.items;
    favState.items = {};
    favSaveToLocal();
    favNotifyChanged();

    if (typeof db !== 'undefined' && db) {
        try {
            var snap = await db.collection('favorites').doc(email).collection('items').get();
            if (snap.size === 0) return;

            var BATCH_SIZE = 450;
            var docs = [];
            snap.forEach(function(doc) { docs.push(doc.ref); });

            for (var i = 0; i < docs.length; i += BATCH_SIZE) {
                var batch = db.batch();
                var chunk = docs.slice(i, i + BATCH_SIZE);
                chunk.forEach(function(ref) { batch.delete(ref); });
                await batch.commit();
            }
        } catch(e) {
            console.warn('[Favorites] Clear cloud error:', e);
            favState.items = backup;
            favSaveToLocal();
            favNotifyChanged();
            favShowToast('Lỗi! Thử lại sau', 'warn');
            return;
        }
    }
    favShowToast('Đã xoá tất cả yêu thích', 'remove');
}

/* ============ COUNT ============ */
function favCount() {
    return Object.keys(favState.items).length;
}

/* ═══ Đếm số câu yêu thích trong 1 dataset cụ thể ═══ */
function favCountInDataset(datasetId) {
    var count = 0;
    var prefix = (datasetId || 'tonghop') + '::';
    Object.keys(favState.items).forEach(function(key) {
        if (key.indexOf(prefix) === 0) count++;
    });
    return count;
}

/* ============ DAILY LIMIT ============ */
function favGetDailyRemaining() {
    var email = favGetCurrentEmail();
    if (!email) return 0;

    var isAdmin = (typeof currentUser !== 'undefined'
                   && currentUser
                   && currentUser.role === 'admin');
    if (isAdmin) return Infinity;

    var MAX_PER_DAY = 500;
    var today = new Date().toDateString();

    try {
        var saved = JSON.parse(localStorage.getItem('fav_daily_' + email) || 'null');
        if (saved && saved.date === today) {
            return Math.max(0, MAX_PER_DAY - saved.count);
        }
    } catch(e) {}

    return MAX_PER_DAY;
}

function favGetDailyUsed() {
    var email = favGetCurrentEmail();
    if (!email) return 0;

    var today = new Date().toDateString();
    try {
        var saved = JSON.parse(localStorage.getItem('fav_daily_' + email) || 'null');
        if (saved && saved.date === today) {
            return saved.count;
        }
    } catch(e) {}
    return 0;
}

/* ============ LẤY RECORDS ============ */
function favGetRecordsFromArray(sourceArray, datasetId) {
    if (!sourceArray || !sourceArray.length) return [];
    var out = [];
    var seen = {};
    var dsId = datasetId || 'tonghop';

    for (var i = 0; i < sourceArray.length; i++) {
        var r = sourceArray[i];
        var key = dsId + '::' + String(r.stt);
        if (r && favState.items[key] && !seen[key]) {
            seen[key] = true;
            out.push(r);
        }
    }
    return out;
}

function favGetRecords() {
    /* ⭐ Quét TẤT CẢ dataset với key có dataset prefix */
    if (typeof DATASET_REGISTRY !== 'undefined' && DATASET_REGISTRY) {
        var allRecords = [];
        Object.keys(DATASET_REGISTRY).forEach(function(dsId) {
            var ds = DATASET_REGISTRY[dsId];
            if (ds && Array.isArray(ds.data)) {
                var dsRecords = favGetRecordsFromArray(ds.data, dsId);
                allRecords = allRecords.concat(dsRecords);
            }
        });
        return allRecords;
    }

    if (typeof RAW_DATA === 'undefined' || !RAW_DATA) return [];
    var curDs = (typeof CURRENT_DATASET !== 'undefined') ? CURRENT_DATASET : 'tonghop';
    return favGetRecordsFromArray(RAW_DATA, curDs);
}

function favIsFavoriteRecord(r) {
    if (!r) return false;
    return favHas(r.stt);
}

/* ============ SORT ============ */
function favGetSortedList() {
    var items = Object.keys(favState.items).map(function(k) { return favState.items[k]; });
    var mode = favState.sortMode;

    if (mode === 'oldest') {
        items.sort(function(a, b) { return (a.addedAt || 0) - (b.addedAt || 0); });
    } else if (mode === 'stt') {
        items.sort(function(a, b) {
            var na = parseInt(a.stt) || 0;
            var nb = parseInt(b.stt) || 0;
            return na - nb;
        });
    } else {
        items.sort(function(a, b) { return (b.addedAt || 0) - (a.addedAt || 0); });
    }
    return items;
}

/* ═══════════════════════════════════════════════════════════════
   ★ QUÉT LẠI TẤT CẢ NÚT TIM
   ═══════════════════════════════════════════════════════════════ */
function favScanAllHeartButtons() {
    var can = (typeof favCanUse === 'function') ? favCanUse() : false;

    document.querySelectorAll('.fav-btn[data-stt]').forEach(function(btn) {
        var stt = btn.dataset.stt;
        if (!stt) return;

        var active = (typeof favHas === 'function') ? favHas(stt) : false;
        var icon = btn.querySelector('i');

        if (!can) {
            btn.classList.add('locked');
            btn.classList.remove('active');
            if (icon) icon.className = 'fas fa-lock';
            btn.title = 'Cần gia hạn để dùng Yêu thích';
            return;
        }

        btn.classList.remove('locked');
        btn.classList.toggle('active', active);
        if (icon) {
            icon.className = active ? 'fas fa-heart' : 'far fa-heart';
        }
        btn.title = active ? 'Xoá khỏi yêu thích' : 'Thêm vào yêu thích';
    });

    if (typeof favUpdatePfFloatBtn === 'function') {
        favUpdatePfFloatBtn();
    }
    if (typeof favUpdatePfOnlyFavBtn === 'function') {
        favUpdatePfOnlyFavBtn();
    }
}

/* ═══════════════════════════════════════════════════════════════
   ★ LỌC DROPDOWN "CÂU:" — khi bật toggle chỉ hiện câu yêu thích
   ═══════════════════════════════════════════════════════════════ */
function favGetQuestionsForDropdown() {
    if (typeof RAW_DATA === 'undefined' || !RAW_DATA) return [];

    if (!favState.pfOnlyFav || !favCanUse()) {
        return RAW_DATA;
    }

    var out = [];
    for (var i = 0; i < RAW_DATA.length; i++) {
        if (favHas(RAW_DATA[i].stt)) {
            out.push(RAW_DATA[i]);
        }
    }
    return out;
}

function favRefreshQuestionDropdown() {
    if (typeof window.pfBuildQuickNav === 'function') {
        try {
            window.pfBuildQuickNav();
            return true;
        } catch(e) {
            console.warn('[Favorites] pfBuildQuickNav error:', e);
        }
    }
    return false;
}

/* ═══════════════════════════════════════════════════════════════
   NÚT TIM FLOAT (Practice Full)
   ═══════════════════════════════════════════════════════════════ */
function favUpdatePfFloatBtn() {
    var pfBtn = document.getElementById('pfFavBtn');
    if (!pfBtn) return;

    var icon = pfBtn.querySelector('i');
    var label = pfBtn.querySelector('.pf-fav-float-label');
    var can = favCanUse();
    var stt = (typeof pfCurrentStt !== 'undefined' && pfCurrentStt) ? String(pfCurrentStt) : null;

    if (!can) {
        pfBtn.classList.add('locked');
        pfBtn.classList.remove('active');
        if (icon) icon.className = 'fas fa-lock';
        if (label) label.textContent = 'Khoá';
        pfBtn.title = 'Cần gia hạn để dùng Yêu thích';
        return;
    }

    pfBtn.classList.remove('locked');
    var active = stt ? favHas(stt) : false;
    pfBtn.classList.toggle('active', active);
    if (icon) icon.className = active ? 'fas fa-heart' : 'far fa-heart';
    if (label) label.textContent = 'Like';
    pfBtn.title = active ? 'Xoá khỏi yêu thích' : 'Thêm vào yêu thích';
}

/* ═══════════════════════════════════════════════════════════════
   NÚT TOGGLE "CHỈ CÂU YÊU THÍCH" (Practice Full)
   ═══════════════════════════════════════════════════════════════ */
function favUpdatePfOnlyFavBtn() {
    var btn = document.getElementById('pfFavOnlyBtn');
    if (!btn) return;

    var icon = btn.querySelector('i');
    var countEl = document.getElementById('pfFavOnlyCount');
    var can = favCanUse();
    var count = favCount();

    if (!can) {
        btn.classList.add('locked');
        btn.classList.remove('active', 'empty', 'current-not-fav');
        if (icon) icon.className = 'fas fa-lock';
        btn.title = 'Cần gia hạn để dùng Yêu thích';
        if (countEl) countEl.textContent = '0';
        return;
    }

    btn.classList.remove('locked');
    if (countEl) countEl.textContent = count;

    if (count === 0) {
        btn.classList.add('empty');
        btn.classList.remove('active', 'current-not-fav');
        if (icon) icon.className = 'far fa-heart';
        btn.title = 'Chưa có câu yêu thích nào';
        if (favState.pfOnlyFav) {
            favState.pfOnlyFav = false;
        }
        return;
    }

    btn.classList.remove('empty');

    var currentStt = (typeof pfCurrentStt !== 'undefined' && pfCurrentStt)
                     ? String(pfCurrentStt)
                     : null;
    var currentIsFav = currentStt ? favHas(currentStt) : false;

    if (!favState.pfOnlyFav && !currentIsFav) {
        btn.classList.add('current-not-fav');
        btn.classList.remove('active');
        if (icon) icon.className = 'far fa-heart';
        btn.title = 'Câu hiện tại chưa được yêu thích. Bấm ❤️ để thêm vào yêu thích trước.';
        return;
    }

    btn.classList.remove('current-not-fav');

    if (favState.pfOnlyFav) {
        btn.classList.add('active');
        if (icon) icon.className = 'fas fa-heart';
        btn.title = 'Đang chỉ luyện câu yêu thích — bấm để tắt';
    } else {
        btn.classList.remove('active');
        if (icon) icon.className = 'far fa-heart';
        btn.title = 'Chỉ luyện câu yêu thích';
    }
}

function favTogglePfOnlyFav() {
    if (!favCanUse()) { favShowLockDialog(); return; }

    var count = favCount();
    if (count === 0) {
        favShowToast('Chưa có câu yêu thích nào để luyện', 'warn');
        return;
    }

    var currentStt = (typeof pfCurrentStt !== 'undefined' && pfCurrentStt)
                     ? String(pfCurrentStt)
                     : null;
    var currentIsFav = currentStt ? favHas(currentStt) : false;

    if (!favState.pfOnlyFav) {
        if (!currentStt) {
            favShowToast('Không xác định được câu hiện tại', 'warn');
            return;
        }

        if (!currentIsFav) {
            favShowToast(
                'Câu #' + currentStt + ' chưa được yêu thích. Bấm ❤️ để thêm vào yêu thích trước.',
                'warn'
            );
            return;
        }

        favState.pfOnlyFav = true;
        favUpdatePfOnlyFavBtn();
        favRefreshQuestionDropdown();
        favShowToast('Chỉ luyện ' + count + ' câu yêu thích', 'add');
        return;
    }

    favState.pfOnlyFav = false;
    favUpdatePfOnlyFavBtn();
    favRefreshQuestionDropdown();
    favShowToast('Luyện tất cả câu', 'remove');
}

/* ═══════════════════════════════════════════════════════════════
   NOTIFY CHANGES
   ═══════════════════════════════════════════════════════════════ */
function favNotifyChanged() {
    if (typeof favScanAllHeartButtons === 'function') {
        favScanAllHeartButtons();
    }

    var count = favCount();
    ['favTabBadge', 'favDropdownBadge'].forEach(function(id) {
        var badge = document.getElementById(id);
        if (badge) {
            badge.textContent = count;
            badge.dataset.count = count;
        }
    });

    if (favState.currentView && favState.filteringOnly) {
        if (typeof window.render === 'function') {
            clearTimeout(favState.__renderTimer);
            favState.__renderTimer = setTimeout(function() {
                window.render();
            }, 80);
        } else {
            favRenderCurrentTab();
        }
    }
}

/* ═══════════════════════════════════════════════════════════════
   UPDATE LOCK STATE
   ═══════════════════════════════════════════════════════════════ */
function favUpdateLockState() {
    var can = favCanUse();

    var favTab = document.getElementById('dsFavBtn');
    if (favTab) {
        favTab.classList.toggle('fav-locked', !can);
        var lockEl = document.getElementById('favTabLock');
        var badgeEl = document.getElementById('favTabBadge');
        if (can) {
            if (lockEl) lockEl.style.display = 'none';
            if (badgeEl) badgeEl.style.display = '';
        } else {
            if (lockEl) lockEl.style.display = 'flex';
            if (badgeEl) badgeEl.style.display = 'none';
        }
    }

    var favDd = document.getElementById('dsFavDropdownItem');
    if (favDd) {
        favDd.classList.toggle('fav-locked', !can);
        var ddLock = document.getElementById('favDropdownLock');
        var ddBadge = document.getElementById('favDropdownBadge');
        if (can) {
            if (ddLock) ddLock.style.display = 'none';
            if (ddBadge) ddBadge.style.display = '';
        } else {
            if (ddLock) ddLock.style.display = 'inline-flex';
            if (ddBadge) ddBadge.style.display = 'none';
        }
    }

    document.querySelectorAll('.fav-btn[data-stt]').forEach(function(btn) {
        var icon = btn.querySelector('i');
        if (can) {
            btn.classList.remove('locked');
            if (icon) {
                var active = favHas(btn.dataset.stt);
                btn.classList.toggle('active', active);
                icon.className = active ? 'fas fa-heart' : 'far fa-heart';
            }
            btn.title = favHas(btn.dataset.stt) ? 'Xoá khỏi yêu thích' : 'Thêm vào yêu thích';
        } else {
            btn.classList.add('locked');
            btn.classList.remove('active');
            if (icon) icon.className = 'fas fa-lock';
            btn.title = 'Cần gia hạn để dùng Yêu thích';
        }
    });

    favUpdatePfFloatBtn();
    favUpdatePfOnlyFavBtn();

    if (!can && favState.currentView) {
        favExitFilterMode();
        if (typeof switchDataset === 'function') switchDataset('tonghop');
        if (typeof markCurrentDatasetActive === 'function') markCurrentDatasetActive();
    }
}

/* ═══════════════════════════════════════════════════════════════
   TOAST
   ═══════════════════════════════════════════════════════════════ */
function favShowToast(message, type) {
    var old = document.getElementById('favToast');
    if (old) old.remove();

    var toast = document.createElement('div');
    toast.id = 'favToast';
    toast.className = 'fav-toast ' + (type || 'add');

    var iconClass = 'fa-heart';
    if (type === 'remove') iconClass = 'fa-heart-broken';
    if (type === 'warn') iconClass = 'fa-info-circle';

    toast.innerHTML = '<i class="fas ' + iconClass + '"></i><span>' + message + '</span>';
    document.body.appendChild(toast);

    requestAnimationFrame(function() { toast.classList.add('show'); });
    setTimeout(function() {
        toast.classList.remove('show');
        setTimeout(function() { if (toast.parentNode) toast.remove(); }, 300);
    }, 1800);
}

/* ═══════════════════════════════════════════════════════════════
   RENDER TAB YÊU THÍCH
   ═══════════════════════════════════════════════════════════════ */
function favRenderCurrentTab() {
    if (!favState.currentView) return;
    if (typeof mobileWrapper === 'undefined' || !mobileWrapper) return;
    if (typeof RAW_DATA === 'undefined' || !RAW_DATA) return;

    var can = favCanUse();

    if (!can) {
        mobileWrapper.innerHTML = '<div class="fav-locked-empty">' +
            '<div style="width:70px;height:70px;margin:0 auto 1rem;border-radius:50%;' +
            'background:linear-gradient(135deg,#dc2626,#b91c1c);color:#fff;' +
            'display:flex;align-items:center;justify-content:center;font-size:1.8rem;">' +
                '<i class="fas fa-lock"></i>' +
            '</div>' +
            '<div style="font-size:1.05rem;font-weight:800;margin-bottom:.4rem;color:#dc2626;">' +
                'Tính năng Yêu thích đang bị khoá' +
            '</div>' +
            '<div style="font-size:.85rem;color:var(--text-2);line-height:1.5;max-width:420px;margin:0 auto;">' +
                (favIsLoggedIn()
                    ? 'Chỉ tài khoản <b>đã gia hạn</b> mới lưu được câu yêu thích và đồng bộ trên mọi thiết bị.'
                    : 'Vui lòng <b>đăng nhập</b> và <b>gia hạn</b> để dùng tính năng này.') +
            '</div>' +
            '<button style="margin-top:1rem;padding:.6rem 1.2rem;border-radius:50px;border:none;' +
            'background:linear-gradient(135deg,#dc2626,#b91c1c);color:#fff;font-weight:800;cursor:pointer;' +
            'font-family:inherit;text-transform:uppercase;letter-spacing:.3px;" ' +
            'onclick="favShowLockDialog()">' +
                '<i class="fas ' + (favIsLoggedIn() ? 'fa-gem' : 'fa-sign-in-alt') + '"></i>' +
                (favIsLoggedIn() ? ' Gia hạn ngay' : ' Đăng nhập ngay') +
            '</button>' +
        '</div>';
        return;
    }

    var allFavRecords = favGetRecords();
    var items = favGetSortedList();

    if (items.length === 0) {
        mobileWrapper.innerHTML = '<div class="fav-empty">' +
            '<div class="fav-empty-icon"><i class="far fa-heart"></i></div>' +
            '<div class="fav-empty-title">Chưa có câu yêu thích nào</div>' +
            '<div class="fav-empty-desc">' +
                'Bấm vào biểu tượng <b>❤️ trái tim</b> trên mỗi câu để lưu lại. ' +
                'Các câu yêu thích sẽ được đồng bộ trên mọi thiết bị khi bạn đăng nhập.' +
            '</div>' +
        '</div>';
        return;
    }

    var isAdminUser = (typeof currentUser !== 'undefined'
                       && currentUser
                       && currentUser.role === 'admin');
    var counterHtml = '';

    if (isAdminUser) {
        counterHtml = '<span style="font-size:.7rem;font-weight:700;color:#7c3aed;' +
                      'padding:.15rem .55rem;background:rgba(124,58,237,.12);border-radius:50px;' +
                      'display:inline-flex;align-items:center;gap:.25rem;">' +
                      '<i class="fas fa-infinity"></i> Admin không giới hạn</span>';
    } else {
        var used = (typeof favGetDailyUsed === 'function') ? favGetDailyUsed() : 0;
        var MAX_PER_DAY = 500;
        var color = used >= 450 ? '#dc2626' : (used >= 350 ? '#f59e0b' : '#16a34a');
        var bgColor = used >= 450 ? 'rgba(220,38,38,.15)' :
                      used >= 350 ? 'rgba(245,158,11,.15)' : 'rgba(22,163,74,.12)';
        counterHtml = '<span style="font-size:.7rem;font-weight:700;color:' + color + ';' +
                      'padding:.15rem .55rem;background:' + bgColor + ';border-radius:50px;' +
                      'display:inline-flex;align-items:center;gap:.25rem;">' +
                      '<i class="fas fa-calendar-day"></i> ' + used + '/' + MAX_PER_DAY + ' hôm nay</span>';
    }

    var headerHtml = '<div class="fav-header" style="grid-column:1 / -1;' +
        'display:flex;align-items:center;gap:.5rem;padding:.65rem .85rem;' +
        'background:linear-gradient(135deg,rgba(239,68,68,.08),rgba(220,38,38,.04));' +
        'border:1.5px solid rgba(239,68,68,.25);border-radius:12px;margin-bottom:.75rem;flex-wrap:wrap;">' +

        '<div style="display:flex;align-items:center;gap:.45rem;font-size:.88rem;font-weight:800;flex:1 1 auto;flex-wrap:wrap;">' +
            '<i class="fas fa-heart" style="color:#ef4444;"></i>' +
            '<span>Yêu thích</span>' +
            '<span style="font-size:.72rem;font-weight:700;color:#dc2626;' +
            'background:rgba(239,68,68,.15);padding:.15rem .55rem;border-radius:50px;">' +
                items.length + ' câu</span>' +
            counterHtml +
        '</div>' +

        '<select onchange="favOnSortChange(this.value)" ' +
        'style="padding:.35rem 1.8rem .35rem .7rem;border-radius:50px;border:1.5px solid var(--border);' +
        'background:var(--surface);color:var(--text);font-size:.72rem;font-weight:700;cursor:pointer;' +
        'font-family:inherit;outline:none;">' +
            '<option value="recent"' + (favState.sortMode === 'recent' ? ' selected' : '') + '>Mới nhất</option>' +
            '<option value="oldest"' + (favState.sortMode === 'oldest' ? ' selected' : '') + '>Cũ nhất</option>' +
            '<option value="stt"' + (favState.sortMode === 'stt' ? ' selected' : '') + '>Theo STT</option>' +
        '</select>' +

        '<button onclick="favClearAll()" ' +
        'style="padding:.35rem .75rem;border-radius:50px;border:1.5px solid rgba(220,38,38,.35);' +
        'background:var(--surface);color:#dc2626;font-size:.72rem;font-weight:700;cursor:pointer;' +
        'font-family:inherit;display:inline-flex;align-items:center;gap:.3rem;">' +
            '<i class="fas fa-trash-alt"></i> Xoá hết' +
        '</button>' +
    '</div>';

    var filteredFav = allFavRecords.filter(function(r) {
        if (typeof state !== 'undefined') {
            if (state.search) {
                var s = state.search;
                var inVi = (r.vi || '').toLowerCase().indexOf(s) !== -1;
                var inZh = (r.zh || '').toLowerCase().indexOf(s) !== -1;
                var inPinyin = (r.pinyin || '').toLowerCase().indexOf(s) !== -1;
                var inTopic = (r.topic || '').toLowerCase().indexOf(s) !== -1;
                var inSubject = (r.subject || '').toLowerCase().indexOf(s) !== -1;
                if (!inVi && !inZh && !inPinyin && !inTopic && !inSubject) return false;
            }
            if (state.hsk && r.hsk !== state.hsk) return false;
            if (state.subject && r.subject !== state.subject) return false;
        }
        return true;
    });

    /* ⭐ Sắp xếp dùng key có dataset */
    var sortMode = favState.sortMode || 'recent';
    if (sortMode === 'oldest') {
        filteredFav.sort(function(a, b) {
            var ka = getFavKey(a.stt);
            var kb = getFavKey(b.stt);
            var ta = favState.items[ka] ? favState.items[ka].addedAt : 0;
            var tb = favState.items[kb] ? favState.items[kb].addedAt : 0;
            return ta - tb;
        });
    } else if (sortMode === 'stt') {
        filteredFav.sort(function(a, b) {
            var na = parseInt(a.stt) || 0;
            var nb = parseInt(b.stt) || 0;
            return na - nb;
        });
    } else {
        filteredFav.sort(function(a, b) {
            var ka = getFavKey(a.stt);
            var kb = getFavKey(b.stt);
            var ta = favState.items[ka] ? favState.items[ka].addedAt : 0;
            var tb = favState.items[kb] ? favState.items[kb].addedAt : 0;
            return tb - ta;
        });
    }

    var cardsHtml = headerHtml;

    if (filteredFav.length === 0) {
        cardsHtml += '<div class="no-data" style="grid-column:1 / -1;">' +
            '<i class="fas fa-search"></i>Không tìm thấy câu yêu thích nào khớp bộ lọc' +
            '</div>';
    } else {
        filteredFav.forEach(function(r) {
            cardsHtml += favBuildCardHtml(r);
        });
    }

    mobileWrapper.innerHTML = cardsHtml;

    setTimeout(function() {
        if (typeof favUpdateLockState === 'function') favUpdateLockState();
    }, 50);
}

function favBuildCardHtml(r) {
    var zhJs = escapeJs(r.zh);
    var viJs = escapeJs(r.vi);
    var pinyinJs = escapeJs(r.pinyin);
    var zhHtml = escapeHtml(r.zh);
    var viHtml = escapeHtml(r.vi);
    var sttSafe = escapeHtml(r.stt);
    var sttJs = escapeJs(r.stt);

    var audio = r.zh ? '<button class="audio-btn" onclick="speakText(\'' + zhJs + '\', this, event)" title="Nghe"><i class="fas fa-volume-up"></i></button>' : '';
    var writeBtn = '';
    if (r.zh) {
        writeBtn = '<button class="write-btn" onclick="openWriter(\'' + zhJs + '\', \'' + viJs + '\', \'' + pinyinJs + '\', event)" title="Luyện viết"><i class="fas fa-pen-fancy"></i></button>';
    }
    var fullBtn = '';
    if (r.zh) {
        fullBtn = '<button class="practice-full-btn" onclick="openPracticeFull(\'' + sttJs + '\', event)" title="Luyện tập full màn hình"><i class="fas fa-expand"></i></button>';
    }

    var can = favCanUse();
    var active = favHas(r.stt);
    var favBtn = '<button class="fav-btn' +
        (active ? ' active' : '') +
        (!can ? ' locked' : '') +
        '" data-stt="' + sttSafe + '" ' +
        'onclick="favOnCardBtnClick(event, \'' + sttJs + '\')" ' +
        'title="' + (active ? 'Xoá khỏi yêu thích' : 'Thêm vào yêu thích') + '">' +
        '<i class="' + (!can ? 'fas fa-lock' : (active ? 'fas fa-heart' : 'far fa-heart')) + '"></i>' +
    '</button>';

    var practiceInput = '<input type="text" class="practice-input" placeholder="Gõ tiếng Trung..." data-answer="' + zhHtml + '" data-stt="' + sttSafe + '" oninput="checkInput(this)" autocomplete="off">';

    return '<div class="card" data-hsk="' + (r.hsk || '') + '" onclick="toggleFocus(\'' + sttJs + '\', this)" data-stt="' + sttSafe + '">' +
        '<div class="card-header">' +
            '<div class="card-stt">' + sttSafe + '</div>' +
            '<div class="card-meta">' +
                (r.hsk ? '<span class="card-tag hsk">' + escapeHtml(r.hsk) + '</span>' : '') +
            '</div>' +
            '<div onclick="event.stopPropagation()" class="action-group">' +
                audio + writeBtn + fullBtn + favBtn +
            '</div>' +
        '</div>' +
        '<div class="card-body">' +
            (r.vi ? '<div class="card-vi">' + viHtml + '</div>' : '') +
            '<div class="card-zh">' + zhHtml + '</div>' +
            (r.pinyin ? '<div class="card-pinyin">' + escapeHtml(r.pinyin) + '</div>' : '') +
        '</div>' +
        '<div class="card-practice" onclick="event.stopPropagation()">' +
            practiceInput +
        '</div>' +
    '</div>';
}

/* ═══════════════════════════════════════════════════════════════
   EVENT HANDLERS
   ═══════════════════════════════════════════════════════════════ */
window.favOnCardBtnClick = function(evt, stt) {
    evt.stopPropagation();
    if (evt.preventDefault) evt.preventDefault();

    if (!favCanUse()) { favShowLockDialog(); return; }

    var record = null;
    if (typeof RAW_DATA !== 'undefined') {
        for (var i = 0; i < RAW_DATA.length; i++) {
            if (String(RAW_DATA[i].stt) === String(stt)) { record = RAW_DATA[i]; break; }
        }
    }
    favToggle(stt, record);
};

window.favOnPfBtnClick = function(evt) {
    if (evt) { evt.stopPropagation(); if (evt.preventDefault) evt.preventDefault(); }
    if (typeof pfCurrentStt === 'undefined' || !pfCurrentStt) return;
    if (!favCanUse()) { favShowLockDialog(); return; }

    var record = null;
    if (typeof RAW_DATA !== 'undefined') {
        for (var i = 0; i < RAW_DATA.length; i++) {
            if (String(RAW_DATA[i].stt) === String(pfCurrentStt)) { record = RAW_DATA[i]; break; }
        }
    }
    favToggle(pfCurrentStt, record).then(function() {
        favUpdatePfFloatBtn();
    });
};

window.favTogglePfOnlyFav = favTogglePfOnlyFav;

window.favOnSortChange = function(mode) {
    favState.sortMode = mode || 'recent';
    try { localStorage.setItem('favSortMode', favState.sortMode); } catch(e) {}
    if (typeof window.render === 'function') window.render();
    else favRenderCurrentTab();
};

/* ═══════════════════════════════════════════════════════════════
   CLICK TAB YÊU THÍCH
   ═══════════════════════════════════════════════════════════════ */
function favOnTabClick(evt) {
    if (evt) { evt.stopPropagation(); if (evt.preventDefault) evt.preventDefault(); }

    if (!favCanUse()) { favShowLockDialog(); return; }

    document.querySelectorAll('.ds-btn').forEach(function(b) { b.classList.remove('active'); });
    document.querySelectorAll('.ds-sub-btn').forEach(function(b) { b.classList.remove('active'); });
    document.querySelectorAll('.ds-dropdown-item').forEach(function(b) { b.classList.remove('active'); });

    var tabBtn = document.getElementById('dsFavBtn');
    if (tabBtn) tabBtn.classList.add('active');
    var ddBtn = document.getElementById('dsFavDropdownItem');
    if (ddBtn) ddBtn.classList.add('active');

    var subWrap = document.getElementById('dsSubWrap');
    if (subWrap) subWrap.style.display = 'none';

    favState.currentView = true;
    favState.filteringOnly = true;

    if (typeof state !== 'undefined') {
        state.search = '';
        state.hsk = '';
        state.subject = '';
    }
    try {
        var si = document.getElementById('searchInput');
        if (si) si.value = '';
        var hf = document.getElementById('hskFilter');
        if (hf) hf.value = '';
        var sf = document.getElementById('subjectFilter');
        if (sf) sf.value = '';
        var cb = document.getElementById('clearSearchBtn');
        if (cb) cb.classList.remove('show');
    } catch(e) {}
    if (typeof updateFilterUI === 'function') updateFilterUI();

    window.__onboardingOverride = null;
    var obBanner = document.getElementById('onboardingActiveBanner');
    if (obBanner) obBanner.style.display = 'none';

    var favRecords = favGetRecords();

    try {
        filtered = favRecords;
    } catch(e1) {
        try { window.filtered = favRecords; } catch(e2) {}
    }
    try { window.filtered = favRecords; } catch(e) {}

    try { renderedCount = 0; } catch(e) { try { window.renderedCount = 0; } catch(e2) {} }

    if (typeof favRenderCurrentTab === 'function') {
        favRenderCurrentTab();
    } else if (typeof window.render === 'function') {
        window.render(true);
    }

    setTimeout(function() {
        var mainEl = document.getElementById('mainContent');
        if (mainEl) {
            var yOffset = mainEl.getBoundingClientRect().top + window.scrollY - 100;
            window.scrollTo({ top: yOffset, behavior: 'smooth' });
        }
    }, 150);

    if (favCanUse() && !favState.loaded) {
        favLoadFromCloud();
    }
}

function favExitFilterMode() {
    if (!favState.filteringOnly) return;
    favState.filteringOnly = false;
    favState.currentView = false;
    favState.pfOnlyFav = false;
    var tabBtn = document.getElementById('dsFavBtn');
    if (tabBtn) tabBtn.classList.remove('active');
    var ddBtn = document.getElementById('dsFavDropdownItem');
    if (ddBtn) ddBtn.classList.remove('active');
    if (typeof favUpdatePfOnlyFavBtn === 'function') favUpdatePfOnlyFavBtn();
}

/* ═══════════════════════════════════════════════════════════════
   INIT
   ═══════════════════════════════════════════════════════════════ */
function initFavorites() {
    try {
        var savedSort = localStorage.getItem('favSortMode');
        if (savedSort) favState.sortMode = savedSort;
    } catch(e) {}

    favLoadFromLocal();

    var pfBtn = document.getElementById('pfFavBtn');
    if (pfBtn && !pfBtn.__favBound) {
        pfBtn.__favBound = true;
        pfBtn.addEventListener('click', window.favOnPfBtnClick);
    }

    var pfOnlyBtn = document.getElementById('pfFavOnlyBtn');
    if (pfOnlyBtn && !pfOnlyBtn.__favBound) {
        pfOnlyBtn.__favBound = true;
        pfOnlyBtn.addEventListener('click', function(evt) {
            evt.stopPropagation();
            if (evt.preventDefault) evt.preventDefault();
            favTogglePfOnlyFav();
        });
    }

    var favTab = document.getElementById('dsFavBtn');
    if (favTab && !favTab.__favBound) {
        favTab.__favBound = true;
        favTab.addEventListener('click', favOnTabClick);
    }

    var favDd = document.getElementById('dsFavDropdownItem');
    if (favDd && !favDd.__favBound) {
        favDd.__favBound = true;
        favDd.addEventListener('click', function(evt) {
            if (evt) { evt.stopPropagation(); if (evt.preventDefault) evt.preventDefault(); }
            var dd = favDd.closest('.ds-dropdown, .dataset-dropdown, [class*="dropdown"]');
            if (dd) dd.classList.remove('show', 'open');
            favOnTabClick(evt);
        });
    }

    favUpdateLockState();
    if (favCanUse()) favLoadFromCloud();
    favNotifyChanged();
    favSyncFloatVisibility();
}

/* ═══════════════════════════════════════════════════════════════
   HIỆN/ẨN NÚT FLOAT THEO PRACTICE FULL MODAL
   ═══════════════════════════════════════════════════════════════ */
function favSyncFloatVisibility() {
    var pfModal = document.getElementById('practiceFullModal');
    var pfFavFloat = document.getElementById('pfFavBtn');
    var pfOnlyFloat = document.getElementById('pfFavOnlyBtn');

    var isOpen = pfModal && pfModal.classList.contains('show');

    if (isOpen) {
        if (pfFavFloat) {
            pfFavFloat.classList.add('show');
            pfFavFloat.style.display = 'inline-flex';
        }
        if (pfOnlyFloat) {
            pfOnlyFloat.classList.add('show');
            pfOnlyFloat.style.display = 'inline-flex';
        }
        favUpdatePfFloatBtn();
        favUpdatePfOnlyFavBtn();

        setTimeout(function() {
            favRefreshQuestionDropdown();
        }, 80);
    } else {
        if (pfFavFloat) {
            pfFavFloat.classList.remove('show');
            pfFavFloat.style.display = 'none';
        }
        if (pfOnlyFloat) {
            pfOnlyFloat.classList.remove('show');
            pfOnlyFloat.style.display = 'none';
        }
    }
}

/* ═══════════════════════════════════════════════════════════════
   WATCH PRACTICE FULL MODAL
   ═══════════════════════════════════════════════════════════════ */
(function() {
    function attach() {
        var pfModal = document.getElementById('practiceFullModal');
        if (!pfModal) return false;
        if (pfModal.__favObserved) return true;
        pfModal.__favObserved = true;

        var obs = new MutationObserver(function(mutations) {
            mutations.forEach(function(m) {
                if (m.attributeName === 'class') {
                    if (typeof favSyncFloatVisibility === 'function') {
                        favSyncFloatVisibility();
                    }
                }
            });
        });
        obs.observe(pfModal, { attributes: true });
        return true;
    }

    if (!attach()) {
        var _tries = 0;
        var _iv = setInterval(function() {
            _tries++;
            if (attach() || _tries > 60) clearInterval(_iv);
        }, 200);
    }
})();

/* ═══════════════════════════════════════════════════════════════
   ★ THEO DÕI pfCurrentStt → CẬP NHẬT NÚT FLOAT + SCAN HEART
   ═══════════════════════════════════════════════════════════════ */
(function() {
    var _lastPfStt = null;

    function syncPfState() {
        var cur = (typeof pfCurrentStt !== 'undefined' && pfCurrentStt)
                  ? String(pfCurrentStt)
                  : null;
        if (cur === _lastPfStt) return;
        _lastPfStt = cur;
        if (!cur) return;

        if (typeof favUpdatePfFloatBtn === 'function') {
            favUpdatePfFloatBtn();
        }

        if (typeof favUpdatePfOnlyFavBtn === 'function') {
            favUpdatePfOnlyFavBtn();
        }

        if (typeof favScanAllHeartButtons === 'function') {
            favScanAllHeartButtons();
        }

        if (typeof favState !== 'undefined' && favState.pfOnlyFav) {
            var isNewFav = (typeof favHas === 'function') ? favHas(cur) : false;
            if (!isNewFav) {
                favState.pfOnlyFav = false;
                if (typeof favUpdatePfOnlyFavBtn === 'function') {
                    favUpdatePfOnlyFavBtn();
                }
                if (typeof favRefreshQuestionDropdown === 'function') {
                    favRefreshQuestionDropdown();
                }
                if (typeof favShowToast === 'function') {
                    favShowToast('Đã tắt "Chỉ câu yêu thích"', 'warn');
                }
            }
        }
    }

    setInterval(syncPfState, 250);
})();

/* ═══════════════════════════════════════════════════════════════
   ★ PATCH render() — Quét lại nút tim sau render
   ═══════════════════════════════════════════════════════════════ */
(function() {
    function tryPatch() {
        if (typeof window.render !== 'function') return false;
        if (window.render.__favScanPatched) return true;

        var _origRender = window.render;
        window.render = function() {
            var result = _origRender.apply(this, arguments);

            setTimeout(function() {
                if (typeof favScanAllHeartButtons === 'function') {
                    favScanAllHeartButtons();
                }
            }, 10);

            return result;
        };
        window.render.__favScanPatched = true;
        return true;
    }

    if (!tryPatch()) {
        var _tries = 0;
        var _iv = setInterval(function() {
            _tries++;
            if (tryPatch() || _tries > 40) clearInterval(_iv);
        }, 100);
    }
})();

/* ═══════════════════════════════════════════════════════════════
   ★ PATCH switchDataset() — Tự tắt lọc khi đổi dataset khác
   ═══════════════════════════════════════════════════════════════ */
(function() {
    function tryPatch() {
        if (typeof window.switchDataset !== 'function') return false;
        if (window.switchDataset.__favPatched) return true;

        var _origSwitch = window.switchDataset;
        window.switchDataset = function(group, sub) {
            if (group !== 'favorites') {
                favExitFilterMode();
            }
            return _origSwitch.apply(this, arguments);
        };
        window.switchDataset.__favPatched = true;
        return true;
    }

    if (!tryPatch()) {
        var _tries = 0;
        var _iv = setInterval(function() {
            _tries++;
            if (tryPatch() || _tries > 40) clearInterval(_iv);
        }, 100);
    }
})();

/* ═══════════════════════════════════════════════════════════════
   ★ PATCH openPracticeFull
   ═══════════════════════════════════════════════════════════════ */
(function() {
    function tryPatch() {
        if (typeof window.openPracticeFull !== 'function') return false;
        if (window.openPracticeFull.__favFilterPatched) return true;

        var _origOpenPF = window.openPracticeFull;
        window.openPracticeFull = function(stt, evt) {
            if (favState.pfOnlyFav && favCanUse()) {
                var favList = favGetRecords();
                if (favList.length === 0) {
                    favShowToast('Chưa có câu yêu thích nào', 'warn');
                    return;
                }
                var targetStt = String(stt);
                var isFav = favList.some(function(r) {
                    return String(r.stt) === targetStt;
                });
                if (!isFav) {
                    stt = String(favList[0].stt);
                }
            }

            var result = _origOpenPF.apply(this, arguments);

            setTimeout(function() {
                if (typeof favScanAllHeartButtons === 'function') {
                    favScanAllHeartButtons();
                }
                if (typeof favRefreshQuestionDropdown === 'function') {
                    favRefreshQuestionDropdown();
                }
            }, 30);
            setTimeout(function() {
                if (typeof favRefreshQuestionDropdown === 'function') {
                    favRefreshQuestionDropdown();
                }
            }, 200);

            return result;
        };
        window.openPracticeFull.__favFilterPatched = true;
        return true;
    }

    if (!tryPatch()) {
        var _tries = 0;
        var _iv = setInterval(function() {
            _tries++;
            if (tryPatch() || _tries > 40) clearInterval(_iv);
        }, 100);
    }
})();

/* ═══════════════════════════════════════════════════════════════
   ★ PATCH loadPracticeFull
   ═══════════════════════════════════════════════════════════════ */
(function() {
    function tryPatch() {
        if (typeof window.loadPracticeFull !== 'function') return false;
        if (window.loadPracticeFull.__favUnifiedPatched) return true;

        var _origLoadPF = window.loadPracticeFull;
        window.loadPracticeFull = function(stt) {
            var result = _origLoadPF.apply(this, arguments);

            setTimeout(function() {
                var newStt = (typeof pfCurrentStt !== 'undefined' && pfCurrentStt)
                             ? String(pfCurrentStt)
                             : null;
                if (!newStt) return;

                if (typeof favScanAllHeartButtons === 'function') {
                    favScanAllHeartButtons();
                }

                if (typeof favState !== 'undefined' && favState.pfOnlyFav) {
                    var isNewFav = (typeof favHas === 'function') ? favHas(newStt) : false;

                    if (!isNewFav) {
                        favState.pfOnlyFav = false;

                        if (typeof favUpdatePfOnlyFavBtn === 'function') {
                            favUpdatePfOnlyFavBtn();
                        }
                        if (typeof favRefreshQuestionDropdown === 'function') {
                            favRefreshQuestionDropdown();
                        }
                        if (typeof favShowToast === 'function') {
                            favShowToast('Đã tắt "Chỉ câu yêu thích"', 'warn');
                        }
                    }
                }

                if (typeof favUpdatePfOnlyFavBtn === 'function') {
                    favUpdatePfOnlyFavBtn();
                }
            }, 50);

            return result;
        };
        window.loadPracticeFull.__favUnifiedPatched = true;
        return true;
    }

    if (!tryPatch()) {
        var _tries = 0;
        var _iv = setInterval(function() {
            _tries++;
            if (tryPatch() || _tries > 40) clearInterval(_iv);
        }, 100);
    }
})();

/* ═══════════════════════════════════════════════════════════════
   ★ PATCH: ĐỔI BỘ DỮ LIỆU — Reset toggle + scan heart
   ═══════════════════════════════════════════════════════════════ */
(function() {
    'use strict';

    var _datasetChangeTimer = null;

    function handleDatasetChange() {
        console.log('[Favorites] Đổi bộ dữ liệu → đồng bộ');

        if (typeof favState !== 'undefined') {
            favState.pfOnlyFav = false;
        }

        if (typeof favUpdatePfOnlyFavBtn === 'function') {
            favUpdatePfOnlyFavBtn();
        }

        if (typeof favRefreshQuestionDropdown === 'function') {
            favRefreshQuestionDropdown();
        }

        setTimeout(function() {
            if (typeof favScanAllHeartButtons === 'function') {
                favScanAllHeartButtons();
            }

            var newStt = (typeof pfCurrentStt !== 'undefined' && pfCurrentStt)
                         ? String(pfCurrentStt)
                         : null;
            var isNewFav = newStt && typeof favHas === 'function' ? favHas(newStt) : false;
            console.log('[Favorites] Câu mới #' + newStt + ' | liked: ' + isNewFav);

        }, 100);
    }

    function attachListener() {
        var sel = document.getElementById('pfDatasetSelect');
        if (!sel) return false;
        if (sel.__favDatasetBound) return true;

        sel.__favDatasetBound = true;

        sel.addEventListener('change', function() {
            console.log('[Favorites] #pfDatasetSelect change fired');

            if (_datasetChangeTimer) clearTimeout(_datasetChangeTimer);
            _datasetChangeTimer = setTimeout(function() {
                handleDatasetChange();
                setTimeout(function() {
                    if (typeof favScanAllHeartButtons === 'function') {
                        favScanAllHeartButtons();
                    }
                }, 500);
            }, 250);
        });

        console.log('✅ [Favorites] Đã gắn listener cho #pfDatasetSelect');
        return true;
    }

    if (!attachListener()) {
        var _tries = 0;
        var _iv = setInterval(function() {
            _tries++;
            if (attachListener() || _tries > 60) clearInterval(_iv);
        }, 200);
    }
})();

/* ═══════════════════════════════════════════════════════════════
   ★ PATCH điều hướng next/prev
   ═══════════════════════════════════════════════════════════════ */
(function() {
    function patchNavigateFn(fnName) {
        if (typeof window[fnName] !== 'function') return false;
        if (window[fnName].__favFilterPatched) return true;

        var _orig = window[fnName];
        window[fnName] = function() {
            if (!favState.pfOnlyFav || !favCanUse()) {
                var res = _orig.apply(this, arguments);
                setTimeout(function() {
                    if (typeof favScanAllHeartButtons === 'function') {
                        favScanAllHeartButtons();
                    }
                }, 30);
                return res;
            }

            var favList = favGetRecords();
            if (favList.length === 0) {
                return _orig.apply(this, arguments);
            }

            var direction = (fnName.toLowerCase().indexOf('prev') !== -1) ? -1 : 1;

            var curStt = (typeof pfCurrentStt !== 'undefined') ? String(pfCurrentStt) : null;
            var curIdx = -1;
            for (var i = 0; i < favList.length; i++) {
                if (String(favList[i].stt) === curStt) { curIdx = i; break; }
            }

            var nextIdx;
            if (curIdx === -1) {
                nextIdx = 0;
            } else {
                nextIdx = curIdx + direction;
                if (nextIdx < 0) nextIdx = favList.length - 1;
                if (nextIdx >= favList.length) nextIdx = 0;
            }

            var nextStt = String(favList[nextIdx].stt);
            if (typeof window.openPracticeFull === 'function') {
                window.openPracticeFull(nextStt);
                return;
            }
            return _orig.apply(this, arguments);
        };
        window[fnName].__favFilterPatched = true;
        return true;
    }

    var fns = ['pfNavigate', 'pfNext', 'pfPrev', 'practiceNext', 'practicePrev', 'nextPractice', 'prevPractice'];
    var _tries = 0;
    var _iv = setInterval(function() {
        _tries++;
        fns.forEach(function(fn) {
            if (typeof window[fn] === 'function' && !window[fn].__favFilterPatched) {
                patchNavigateFn(fn);
            }
        });
        if (_tries > 40) clearInterval(_iv);
    }, 200);
})();

/* ═══════════════════════════════════════════════════════════════
   PUBLIC API
   ═══════════════════════════════════════════════════════════════ */
window.favUpdateLockState = favUpdateLockState;
window.favNotifyChanged = favNotifyChanged;
window.favSyncFloatVisibility = favSyncFloatVisibility;
window.favUpdatePfFloatBtn = favUpdatePfFloatBtn;
window.favUpdatePfOnlyFavBtn = favUpdatePfOnlyFavBtn;
window.favGetRecords = favGetRecords;
window.favGetQuestionsForDropdown = favGetQuestionsForDropdown;
window.favRefreshQuestionDropdown = favRefreshQuestionDropdown;
window.favHas = favHas;
window.favHasInDataset = favHasInDataset;
window.favCount = favCount;
window.favCountInDataset = favCountInDataset;
window.favExitFilterMode = favExitFilterMode;
window.favState = favState;
window.favScanAllHeartButtons = favScanAllHeartButtons;
window.getFavKey = getFavKey;

window.favRefreshUI = function() {
    favUpdateLockState();
    favNotifyChanged();
    if (favCanUse() && !favState.loaded) {
        favLoadFromCloud();
    }
    if (!favIsLoggedIn()) {
        favState.items = {};
        favState.loaded = false;
        if (favState.listener) {
            try { favState.listener(); } catch(e) {}
            favState.listener = null;
        }
        favUpdateLockState();
    }
};

/* ═══════════════════════════════════════════════════════════════
   AUTO-INIT
   ═══════════════════════════════════════════════════════════════ */
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        if (typeof initFavorites === 'function') initFavorites();
        setTimeout(function() {
            if (typeof favSyncFloatVisibility === 'function') favSyncFloatVisibility();
        }, 100);
    });
} else {
    setTimeout(function() {
        if (typeof initFavorites === 'function') initFavorites();
        if (typeof favSyncFloatVisibility === 'function') favSyncFloatVisibility();
    }, 0);
}

/* Auto-refresh khi tier thay đổi */
(function() {
    var _lastTier = null;
    setInterval(function() {
        var t = (typeof window.APP_TIER !== 'undefined') ? window.APP_TIER : null;
        if (t !== _lastTier) {
            _lastTier = t;
            if (typeof window.favRefreshUI === 'function') window.favRefreshUI();
        }
    }, 800);
})();

/* ═══════════════════════════════════════════════════════════════
   ★ PATCH pfBuildQuickNav — Filter dropdown "CÂU:" theo toggle
   ═══════════════════════════════════════════════════════════════ */
(function() {
    function tryPatch() {
        if (typeof window.pfBuildQuickNav !== 'function') return false;
        if (window.pfBuildQuickNav.__favPatched) return true;

        var _origBuildQuickNav = window.pfBuildQuickNav;
        window.pfBuildQuickNav = function() {
            if (!favState.pfOnlyFav || !favCanUse()) {
                return _origBuildQuickNav.apply(this, arguments);
            }

            var sel = document.getElementById('pfQuickNav');
            if (!sel) return;

            var sourceList = [];
            if (typeof filtered !== 'undefined' && Array.isArray(filtered)) {
                for (var i = 0; i < filtered.length; i++) {
                    if (favHas(filtered[i].stt)) sourceList.push(filtered[i]);
                }
            }

            var html = '<option value="">-- Chọn câu (' + sourceList.length + ') --</option>';
            var curStt = (typeof pfCurrentStt !== 'undefined' && pfCurrentStt) ? String(pfCurrentStt) : '';

            for (var j = 0; j < sourceList.length; j++) {
                var r = sourceList[j];
                var vi = (r.vi || '').substring(0, 45);
                var sttRaw = (r.stt !== undefined && r.stt !== null && String(r.stt).trim() !== '')
                             ? '#' + String(r.stt).trim() + ' · '
                             : '';
                var label = sttRaw + 'Câu ' + (j + 1) + ': ' + vi;
                var selected = (String(r.stt) === curStt) ? ' selected' : '';
                html += '<option value="' + String(r.stt) + '"' + selected + '>'
                      + escapeHtml(label) + '</option>';
            }
            sel.innerHTML = html;
            if (pfCurrentStt) sel.value = pfCurrentStt;
        };
        window.pfBuildQuickNav.__favPatched = true;
        return true;
    }

    if (!tryPatch()) {
        var _tries = 0;
        var _iv = setInterval(function() {
            _tries++;
            if (tryPatch() || _tries > 60) clearInterval(_iv);
        }, 200);
    }
})();

/* ═══════════════════════════════════════════════════════════════
   ★ FIX: Dời nút toggle sang góc phải, TRÊN nút tim
   ═══════════════════════════════════════════════════════════════ */
(function() {
    function injectCSS() {
        if (document.getElementById('favOnlyFloatFix')) return;
        var style = document.createElement('style');
        style.id = 'favOnlyFloatFix';
        style.textContent = [
            '/* Fix: nút toggle chỉ câu yêu thích — góc PHẢI, TRÊN nút tim */',
            '.pf-fav-only-float {',
            '    left: auto !important;',
            '    right: clamp(14px, 2vw, 22px) !important;',
            '    bottom: calc(140px + env(safe-area-inset-bottom)) !important;',
            '}',
            '@media (max-width:500px) {',
            '    .pf-fav-only-float {',
            '        bottom: calc(130px + env(safe-area-inset-bottom)) !important;',
            '    }',
            '}',
            '@media (max-height:550px) and (orientation:landscape) {',
            '    .pf-fav-only-float {',
            '        bottom: calc(114px + env(safe-area-inset-bottom)) !important;',
            '        transform-origin: right bottom !important;',
            '    }',
            '}'
        ].join('\n');
        document.head.appendChild(style);
    }
    if (document.head) injectCSS();
    else document.addEventListener('DOMContentLoaded', injectCSS);
})();
