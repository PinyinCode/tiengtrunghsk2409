# -*- coding: utf-8 -*-
"""
ui_override.py
═══════════════════════════════════════════════════════════════════
OVERRIDE UI — không đụng vào ui_template.py gốc.

Cách dùng trong convert.py:

    from ui_template import build_ui_css, build_ui_html, build_ui_js
    from ui_override import (
        override_ui_css, override_ui_html, override_ui_js,
        override_fullwidth_css,
    )

    full_css = override_ui_css(build_ui_css()) + ...
    ui_html  = override_ui_html(build_ui_html())
    full_js  = override_ui_js(build_ui_js()) + ...

Cơ chế:
  • CSS:   Thay block "DATASET SELECTOR" cũ (layout ngang)
           bằng block mới (layout dọc).
           Fix 2 bug CSS trong ui_template.py gốc.
  • HTML:  Đổi <div class="ds-main-row">...</div>
           → <div class="ds-list" id="dsList"></div>
  • JS:    Chèn OVERRIDE cuối file JS để ghi đè
           initDatasetSelector() + markCurrentDatasetActive().
  • FULLWIDTH_CSS: Xóa block .ds-main-row nếu còn.
═══════════════════════════════════════════════════════════════════
"""
import re


# ═══════════════════════════════════════════════════════════════════
#  CSS MỚI — Layout dọc cho Dataset Selector
# ═══════════════════════════════════════════════════════════════════
NEW_DATASET_CSS = r"""/* ============================================================ */
/* DATASET SELECTOR - LAYOUT DỌC (1 CỘT)                         */
/* ============================================================ */
.dataset-selector{
    margin-bottom:.75rem;
    padding:.75rem .9rem;
    background:linear-gradient(135deg,var(--surface),var(--surface-2));
    border:1.5px solid var(--border);
    border-radius:14px;
    box-shadow:var(--shadow-sm);
}
.ds-label{
    display:flex;align-items:center;gap:.4rem;
    font-size:.7rem;font-weight:800;
    color:var(--text-3);text-transform:uppercase;
    letter-spacing:.5px;margin-bottom:.5rem;
}
.ds-label i{color:var(--primary);font-size:.85rem}

/* ═══════════════════════════════════════════════════════════ */
/* DANH SÁCH TAB DỌC — mỗi tab 1 card full-width                 */
/* ═══════════════════════════════════════════════════════════ */
.ds-list{
    display:flex;
    flex-direction:column;
    gap:.5rem;
}
.ds-row-tab{
    display:flex;
    align-items:center;
    gap:.75rem;
    width:100%;
    padding:.85rem 1rem;
    border-radius:12px;
    border:1.5px solid var(--border);
    background:var(--surface);
    color:var(--text);
    font-family:inherit;
    font-size:.9rem;
    font-weight:800;
    cursor:pointer;
    transition:all .2s cubic-bezier(.34,1.56,.64,1);
    text-align:left;
    position:relative;
}
.ds-row-tab:hover{
    transform:translateY(-1px);
    border-color:var(--primary);
    box-shadow:0 6px 16px rgba(15,23,42,.08);
}
.ds-row-tab > i:first-child{
    font-size:1.15rem;
    color:var(--tab-color, var(--primary));
    flex-shrink:0;
    width:24px;
    text-align:center;
    transition:color .2s;
}
.ds-row-tab > .ds-row-label{
    flex:1;
    min-width:0;
    overflow:hidden;
    text-overflow:ellipsis;
    white-space:nowrap;
    line-height:1.3;
}
.ds-row-tab > .ds-row-meta{
    display:inline-flex;
    align-items:center;
    gap:.5rem;
    flex-shrink:0;
    color:var(--text-3);
    font-size:.8rem;
    font-weight:700;
}
.ds-row-tab.active{
    background:linear-gradient(135deg,#4f46e5,#7c3aed 60%,#a855f7);
    color:#fff;
    border-color:transparent;
    box-shadow:0 6px 18px rgba(124,58,237,.4);
    transform:translateY(-1px);
}
.ds-row-tab.active > i:first-child{color:#fff;}
.ds-row-tab.active > .ds-row-meta{color:rgba(255,255,255,.85);}

.ds-row-tab[data-locked="1"]{
    opacity:.6;
    filter:grayscale(.4);
    cursor:pointer;
}
.ds-row-tab[data-locked="1"]:hover{
    opacity:.85;
    filter:grayscale(0);
    border-color:#dc2626;
    background:rgba(220,38,38,.06);
}
.ds-row-tab[data-locked="1"] > i:first-child{color:#dc2626;}

.ds-row-tab.ds-row-spec{
    background:linear-gradient(135deg,
        color-mix(in srgb, #7c3aed 8%, var(--surface)),
        color-mix(in srgb, #7c3aed 3%, var(--surface)));
    border-color:color-mix(in srgb, #7c3aed 30%, var(--border));
}
.ds-row-tab.ds-row-spec > i:first-child{color:#7c3aed;}
.ds-row-tab.ds-row-spec:hover{
    border-color:#7c3aed;
    box-shadow:0 6px 20px rgba(124,58,237,.25);
}
.ds-row-tab.ds-row-spec.active{
    background:linear-gradient(135deg,#4f46e5,#7c3aed);
    color:#fff;
    border-color:transparent;
}
.ds-row-tab.ds-row-spec.active > i:first-child{color:#fff;}

.ds-row-arrow{
    font-size:.7rem;
    opacity:.7;
    transition:transform .3s ease;
}
.ds-row-tab.ds-row-spec.active .ds-row-arrow{
    transform:rotate(180deg);
    opacity:1;
}

.ds-row-tab .ds-new-badge{
    position:absolute;
    top:-8px;
    right:-6px;
    padding:.18rem .5rem;
    border-radius:50px;
    background:linear-gradient(135deg,#ef4444,#dc2626 50%,#b91c1c);
    color:#fff;
    font-size:.58rem;
    font-weight:900;
    letter-spacing:.5px;
    text-transform:uppercase;
    box-shadow:
        0 2px 8px rgba(220,38,38,.5),
        0 0 0 2px var(--surface);
    animation:dsNewPulse 1.6s ease-in-out infinite;
    pointer-events:none;
    line-height:1.2;
    white-space:nowrap;
    z-index:10;
}
.ds-row-tab .ds-new-badge::before{
    content:'';
    position:absolute;
    inset:-4px;
    border-radius:50px;
    background:radial-gradient(circle,rgba(220,38,38,.4),transparent 70%);
    animation:dsNewGlow 1.6s ease-in-out infinite;
    z-index:-1;
}
@keyframes dsNewPulse{
    0%,100%{
        transform:scale(1);
        box-shadow:
            0 2px 8px rgba(220,38,38,.5),
            0 0 0 2px var(--surface);
    }
    50%{
        transform:scale(1.12);
        box-shadow:
            0 4px 14px rgba(220,38,38,.8),
            0 0 0 2px var(--surface);
    }
}
@keyframes dsNewGlow{
    0%,100%{opacity:.4;transform:scale(1)}
    50%{opacity:.9;transform:scale(1.4)}
}
.ds-row-tab.active .ds-new-badge{display:none;}
[data-theme="dark"] .ds-row-tab .ds-new-badge{
    box-shadow:
        0 2px 8px rgba(220,38,38,.7),
        0 0 0 2px var(--surface-2);
}

.ds-row-tab.ds-row-fav{
    border-color:rgba(239,68,68,.35);
    background:linear-gradient(135deg,#fef2f2,#fee2e2);
    color:#dc2626;
}
.ds-row-tab.ds-row-fav > i:first-child{color:#ef4444;}
.ds-row-tab.ds-row-fav > .ds-row-meta{color:#dc2626;}
.ds-row-tab.ds-row-fav:hover{
    border-color:#ef4444;
    box-shadow:0 6px 20px rgba(239,68,68,.25);
}
.ds-row-tab.ds-row-fav.active{
    background:linear-gradient(135deg,#ef4444,#dc2626);
    color:#fff;
    border-color:transparent;
}
.ds-row-tab.ds-row-fav.active > i:first-child,
.ds-row-tab.ds-row-fav.active > .ds-row-meta{color:#fff;}
[data-theme="dark"] .ds-row-tab.ds-row-fav{
    background:linear-gradient(135deg,rgba(239,68,68,.15),rgba(220,38,38,.1));
    border-color:rgba(239,68,68,.5);
    color:#fca5a5;
}
[data-theme="dark"] .ds-row-tab.ds-row-fav.active{
    background:linear-gradient(135deg,#ef4444,#dc2626);
    color:#fff;
}

.ds-row-tab.ds-row-fav .ds-fav-badge{
    position:absolute;
    top:-8px;
    right:-6px;
    min-width:22px;
    height:22px;
    padding:0 .4rem;
    border-radius:50px;
    background:linear-gradient(135deg,#ef4444,#dc2626);
    color:#fff;
    font-size:.65rem;
    font-weight:900;
    display:flex;
    align-items:center;
    justify-content:center;
    box-shadow:0 2px 8px rgba(239,68,68,.5),0 0 0 2px var(--surface);
    animation:favBadgePulse 2s ease-in-out infinite;
    z-index:10;
    line-height:1;
}
.ds-row-tab.ds-row-fav .ds-fav-badge[data-count="0"]{display:none;}
@keyframes favBadgePulse{
    0%,100%{transform:scale(1);}
    50%{transform:scale(1.1);}
}
.ds-row-tab.ds-row-fav .ds-fav-lock{
    position:absolute;
    top:-8px;
    right:-6px;
    width:22px;
    height:22px;
    border-radius:50%;
    background:linear-gradient(135deg,#dc2626,#b91c1c);
    color:#fff;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:.62rem;
    box-shadow:0 2px 8px rgba(220,38,38,.55),0 0 0 2px var(--surface);
    z-index:10;
}
.ds-row-tab.ds-row-fav.fav-locked{
    opacity:.65;
    cursor:pointer;
}
.ds-row-tab.ds-row-fav.fav-locked:hover{
    opacity:.85;
    border-color:#dc2626;
    background:rgba(220,38,38,.06);
}
.ds-row-tab.ds-row-fav.fav-locked > i:first-child{color:#dc2626;}
[data-theme="dark"] .ds-row-tab.ds-row-fav.fav-locked > i:first-child{color:#fca5a5;}

/* ═══════════════════════════════════════════════════════════ */
/* DROPDOWN CHUYÊN NGÀNH + SUB-BUTTONS                          */
/* ═══════════════════════════════════════════════════════════ */
.ds-sub-wrap{
    margin-top:.65rem;padding-top:.65rem;
    border-top:1.5px dashed var(--border);
    animation:dsFadeIn .25s ease-out;
}
@keyframes dsFadeIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}
.ds-sub-label{
    display:flex;align-items:center;gap:.35rem;
    font-size:.68rem;font-weight:800;
    color:var(--text-3);text-transform:uppercase;
    letter-spacing:.4px;margin-bottom:.5rem;
}
.ds-sub-label i{color:var(--amber);font-size:.8rem}

.ds-sub-grid{
    display:flex;
    flex-wrap:wrap;
    gap:.5rem;
}
.ds-sub-btn{
    display:inline-flex;
    align-items:center;
    justify-content:flex-start;
    gap:.45rem;
    padding:.62rem 1.05rem .65rem;
    border-radius:50px;
    background:linear-gradient(135deg,
        color-mix(in srgb, var(--ds-color, #2563eb) 12%, var(--surface)),
        color-mix(in srgb, var(--ds-color, #2563eb) 4%, var(--surface)));
    border:2px solid color-mix(in srgb, var(--ds-color, #2563eb) 40%, var(--border));
    color:var(--text);
    font-size:.78rem;
    font-weight:800;
    font-family:inherit;
    cursor:pointer;
    transition:all .2s ease;
    text-align:left;
    position:relative;
    white-space:nowrap;
    box-shadow:0 2px 6px color-mix(in srgb, var(--ds-color, #2563eb) 18%, transparent);
    letter-spacing:0;
    line-height:1.5;
    overflow:visible;
    text-rendering:optimizeLegibility;
    -webkit-font-smoothing:antialiased;
    -moz-osx-font-smoothing:grayscale;
    font-feature-settings:"kern" 1,"liga" 1;
    -webkit-text-size-adjust:100%;
    text-size-adjust:100%;
}
.ds-sub-btn i:first-child{
    font-size:.95rem;
    color:var(--ds-color, var(--primary));
    transition:.2s;
    flex-shrink:0;
    line-height:1;
}
.ds-sub-btn span{
    flex:1 1 auto;
    min-width:0;
    display:inline-block;
    line-height:1.5;
    padding:.06em 0 .1em;
    text-rendering:optimizeLegibility;
    overflow-wrap:break-word;
    word-break:normal;
    white-space:nowrap;
}
.ds-sub-btn:hover{
    border-color:var(--ds-color, var(--primary));
    background:linear-gradient(135deg,
        color-mix(in srgb, var(--ds-color, #2563eb) 20%, var(--surface)),
        color-mix(in srgb, var(--ds-color, #2563eb) 8%, var(--surface)));
    transform:translateY(-2px);
    box-shadow:0 6px 16px color-mix(in srgb, var(--ds-color, #2563eb) 30%, transparent);
}
.ds-sub-btn.active{
    background:linear-gradient(135deg,
        var(--ds-color, var(--primary)),
        color-mix(in srgb, var(--ds-color, #2563eb) 72%, #000));
    color:#fff;
    border-color:var(--ds-color, var(--primary));
    box-shadow:0 6px 18px color-mix(in srgb, var(--ds-color, #2563eb) 55%, transparent);
    transform:translateY(-1px);
}
.ds-sub-btn.active i:first-child{color:#fff;}
@media(max-width:500px){
    .ds-sub-btn{
        padding:.55rem .85rem .58rem;
        font-size:.74rem;
        line-height:1.5;
    }
    .ds-sub-btn i:first-child{ font-size:.85rem; }
    .ds-sub-btn span{
        line-height:1.5;
        padding:.05em 0 .08em;
    }
}

.ds-sub-btn.locked {
    opacity: 0.6;
    cursor: not-allowed;
    filter: grayscale(0.4);
    padding-right: 1.9rem;
}
.ds-sub-btn.locked:hover {
    transform: none;
    background: var(--surface);
    border-color: var(--border);
    box-shadow: 0 1px 2px rgba(15,23,42,.04);
}
.ds-sub-btn.locked i:first-child {
    color: var(--text-3) !important;
}
.ds-sub-lock {
    position: absolute;
    top: 50%;
    right: 6px;
    transform: translateY(-50%);
    font-size: 0.58rem;
    color: #dc2626;
    background: rgba(220, 38, 38, 0.14);
    padding: 2px 4px;
    border-radius: 5px;
    line-height: 1;
    pointer-events: none;
    box-shadow: 0 1px 3px rgba(220, 38, 38, 0.2);
}
[data-theme="dark"] .ds-sub-lock {
    color: #fca5a5;
    background: rgba(220, 38, 38, 0.3);
}
.ds-main-lock {
    font-size: 0.7rem;
    color: #dc2626;
    margin-left: 0.35rem;
    padding: 2px 5px;
    background: rgba(220, 38, 38, 0.12);
    border-radius: 5px;
    line-height: 1;
    display: inline-flex;
    align-items: center;
    flex-shrink: 0;
}
[data-theme="dark"] .ds-main-lock {
    color: #fca5a5;
    background: rgba(220, 38, 38, 0.28);
}
.ds-row-tab.ds-row-spec.has-lock {
    border-color: rgba(220, 38, 38, 0.35);
}
.ds-row-tab.ds-row-spec.has-lock:hover {
    border-color: #dc2626;
    background: rgba(220, 38, 38, 0.06);
}
.ds-row-tab.ds-row-spec.has-lock.active {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    border-color: transparent;
}

/* Fallback: tab Yêu thích nếu module trả class cũ .ds-btn */
.ds-list .ds-btn[data-dataset-group="favorites"]{
    display:flex;
    align-items:center;
    gap:.75rem;
    width:100%;
    padding:.85rem 1rem;
    border-radius:12px;
    border:1.5px solid rgba(239,68,68,.35);
    background:linear-gradient(135deg,#fef2f2,#fee2e2);
    color:#dc2626;
    font-family:inherit;
    font-size:.9rem;
    font-weight:800;
    cursor:pointer;
    transition:all .2s cubic-bezier(.34,1.56,.64,1);
    text-align:left;
    position:relative;
}
.ds-list .ds-btn[data-dataset-group="favorites"]:hover{
    transform:translateY(-1px);
    border-color:#ef4444;
    box-shadow:0 6px 20px rgba(239,68,68,.25);
}
.ds-list .ds-btn[data-dataset-group="favorites"].active{
    background:linear-gradient(135deg,#ef4444,#dc2626);
    color:#fff;
    border-color:transparent;
}
.ds-list .ds-btn[data-dataset-group="favorites"] > i:first-child{
    color:#ef4444;
    font-size:1.15rem;
    flex-shrink:0;
    width:24px;
    text-align:center;
}
.ds-list .ds-btn[data-dataset-group="favorites"].active > i:first-child{
    color:#fff;
}
.ds-list .ds-btn[data-dataset-group="favorites"] > span:not(.ds-fav-badge){
    flex:1;
    min-width:0;
}

@media(max-width:500px){
    .ds-row-tab{
        padding:.7rem .85rem;
        font-size:.85rem;
        gap:.6rem;
    }
    .ds-row-tab > i:first-child{font-size:1rem;width:20px;}
    .ds-row-tab > .ds-row-meta{font-size:.74rem;}
}
"""


# ═══════════════════════════════════════════════════════════════════
#  HTML MỚI cho Dataset Selector
# ═══════════════════════════════════════════════════════════════════
NEW_DATASET_HTML = r"""<!-- DATASET SELECTOR — LAYOUT DỌC -->
<div class="dataset-selector" id="datasetSelector">
    <div class="ds-label">
        <i class="fas fa-layer-group"></i>
        <span>Bộ dữ liệu</span>
    </div>
    <div class="ds-list" id="dsList" role="tablist">
        <!-- JS render động từ DATASET_REGISTRY -->
    </div>
    <div class="ds-sub-wrap" id="dsSubWrap" style="display:none">
        <div class="ds-sub-label">
            <i class="fas fa-tags"></i>
            <span>Chọn ngành</span>
        </div>
        <div class="ds-sub-grid" id="dsSubGrid"></div>
    </div>
</div>"""


# ═══════════════════════════════════════════════════════════════════
#  JS MỚI — override 4 hàm
# ═══════════════════════════════════════════════════════════════════
NEW_JS_OVERRIDE = r"""
/* ═══════════════════════════════════════════════════════════════ */
/* ⚡ UI OVERRIDE — layout dọc cho Dataset Selector              */
/* (chèn SAU định nghĩa gốc → tự động ghi đè)                    */
/* ═══════════════════════════════════════════════════════════════ */

function initDatasetSelector() {
    if (typeof DATASET_REGISTRY === 'undefined' || !DATASET_REGISTRY) return;

    var list = $('dsList');
    if (!list) return;
    list.innerHTML = '';

    /* ─── PHÂN LOẠI ─── */
    var mainDss = [];
    var specDss = [];
    Object.keys(DATASET_REGISTRY).forEach(function(id) {
        var ds = DATASET_REGISTRY[id];
        if (ds.type === 'specialty') specDss.push(ds);
        else mainDss.push(ds);
    });

    mainDss.sort(function(a, b) { return (a.order || 0) - (b.order || 0); });
    specDss.sort(function(a, b) { return (a.order || 0) - (b.order || 0); });

    var canAccessSpec = (typeof canAccessChuyenNganh === 'function')
                        ? canAccessChuyenNganh() : true;

    /* ─── 1. TAB CHÍNH ─── */
    mainDss.forEach(function(ds) {
        list.appendChild(buildRowTab({
            dataset: ds,
            label: (ds.count + ' câu ' + (ds.shortName || ds.name).toLowerCase()),
            color: ds.color || '#4f46e5',
            locked: false
        }));
    });

    /* ─── 2. TAB CHUYÊN NGÀNH ─── */
    if (specDss.length > 0) {
        list.appendChild(buildSpecRowTab(specDss.length, canAccessSpec));
    }

    /* ─── 3. TAB YÊU THÍCH ─── */
    var favBuilder = (typeof favRenderRowTab === 'function') ? favRenderRowTab
                    : (typeof favRenderTab === 'function')    ? favRenderTab
                    : null;
    if (favBuilder) {
        try {
            var favTab = favBuilder();
            if (favTab && favTab.nodeType === 1) {
                favTab.classList.add('ds-row-tab');
                favTab.classList.add('ds-row-fav');
                list.appendChild(favTab);
            }
        } catch(e) { console.warn('favRenderRowTab error:', e); }
    }

    /* ─── 4. RENDER DROPDOWN ─── */
    var subGrid = $('dsSubGrid');
    if (subGrid) {
        subGrid.innerHTML = '';
        specDss.forEach(function(ds) {
            subGrid.appendChild(buildSpecSubBtn(ds, canAccessSpec));
        });
    }

    markCurrentDatasetActive();
}


function buildRowTab(opts) {
    var ds = opts.dataset;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'ds-row-tab';
    btn.dataset.dataset = ds.id;
    btn.dataset.locked = opts.locked ? '1' : '0';
    btn.style.setProperty('--tab-color', opts.color);
    btn.title = ds.name + ' (' + ds.count + ' câu)' +
                (opts.locked ? ' — Cần gia hạn' : '');

    var icon = document.createElement('i');
    icon.className = 'fas ' + (ds.icon || 'fa-folder');
    btn.appendChild(icon);

    var label = document.createElement('span');
    label.className = 'ds-row-label';
    var txt = opts.label || ds.shortName || ds.name;
    label.textContent = txt.normalize ? txt.normalize('NFC') : txt;
    btn.appendChild(label);

    btn.addEventListener('click', function() {
        if (this.dataset.locked === '1') {
            if (typeof showChuyenNganhLockMessage === 'function') {
                showChuyenNganhLockMessage();
            }
            return;
        }
        if (typeof switchDataset === 'function') switchDataset(ds.id);
        var wrap = $('dsSubWrap');
        if (wrap) wrap.style.display = 'none';
        var specRow = document.querySelector('.ds-row-spec');
        if (specRow) specRow.classList.remove('active');
    });

    return btn;
}


function buildSpecRowTab(specCount, canAccess) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'ds-row-tab ds-row-spec';
    btn.dataset.specRow = '1';
    btn.style.setProperty('--tab-color', '#7c3aed');

    var icon = document.createElement('i');
    icon.className = 'fas fa-industry';
    btn.appendChild(icon);

    var label = document.createElement('span');
    label.className = 'ds-row-label';
    label.textContent = 'Chuyên ngành';
    btn.appendChild(label);

    var meta = document.createElement('span');
    meta.className = 'ds-row-meta';

    if (!canAccess) {
        var lock = document.createElement('i');
        lock.className = 'fas fa-lock';
        lock.style.color = '#dc2626';
        meta.appendChild(lock);
    }

    var arrow = document.createElement('i');
    arrow.className = 'fas fa-chevron-down ds-row-arrow';
    meta.appendChild(arrow);
    btn.appendChild(meta);

    var badge = document.createElement('span');
    badge.className = 'ds-new-badge';
    badge.textContent = 'NEW';
    btn.appendChild(badge);

    btn.addEventListener('click', function() {
        var wrap = $('dsSubWrap');
        if (!wrap) return;
        var isOpen = wrap.style.display !== 'none';
        wrap.style.display = isOpen ? 'none' : 'block';
        this.classList.toggle('active', !isOpen);
        if (!isOpen) {
            setTimeout(function() {
                wrap.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 100);
        }
    });

    return btn;
}


function buildSpecSubBtn(ds, canAccess) {
    var btn = document.createElement('button');
    btn.className = 'ds-sub-btn' + (canAccess ? '' : ' locked');
    btn.dataset.dataset = ds.id;
    btn.dataset.locked = canAccess ? '0' : '1';
    btn.style.setProperty('--ds-color', ds.color || '#7c3aed');
    btn.title = ds.name + ' (' + ds.count + ' câu)';

    var icon = document.createElement('i');
    icon.className = 'fas ' + (ds.icon || 'fa-folder');
    btn.appendChild(icon);

    var nameSpan = document.createElement('span');
    nameSpan.textContent = ds.name.normalize ? ds.name.normalize('NFC') : ds.name;
    btn.appendChild(nameSpan);

    if (!canAccess) {
        var lock = document.createElement('i');
        lock.className = 'fas fa-lock ds-sub-lock';
        btn.appendChild(lock);
    }

    btn.addEventListener('click', function(e) {
        if (this.dataset.locked === '1') {
            e.preventDefault();
            e.stopPropagation();
            if (typeof showChuyenNganhLockMessage === 'function') {
                showChuyenNganhLockMessage();
            }
            return;
        }
        if (typeof switchDataset === 'function') switchDataset(ds.id);
        var subGrid = $('dsSubGrid');
        if (subGrid) {
            subGrid.querySelectorAll('.ds-sub-btn').forEach(function(b) {
                b.classList.remove('active');
            });
        }
        this.classList.add('active');
        var specRow = document.querySelector('.ds-row-spec');
        if (specRow) specRow.classList.add('active');
    });

    return btn;
}


function markCurrentDatasetActive() {
    var current = (typeof CURRENT_DATASET !== 'undefined') ? CURRENT_DATASET : '';
    var isFav = (typeof favState !== 'undefined' && favState && favState.currentView);

    document.querySelectorAll('.ds-row-tab').forEach(function(t) {
        t.classList.remove('active');
    });
    document.querySelectorAll('.ds-sub-btn').forEach(function(b) {
        b.classList.remove('active');
    });

    if (isFav) {
        if (typeof favUpdateLockState === 'function') favUpdateLockState();
        return;
    }

    if (!current && typeof DATASET_REGISTRY !== 'undefined') {
        var firstId = Object.keys(DATASET_REGISTRY)[0];
        if (firstId) {
            var tabFirst = document.querySelector('.ds-row-tab[data-dataset="' + firstId + '"]');
            if (tabFirst) tabFirst.classList.add('active');
        }
        return;
    }

    if (typeof DATASET_REGISTRY !== 'undefined' && DATASET_REGISTRY[current]) {
        var ds = DATASET_REGISTRY[current];
        if (ds.type === 'specialty') {
            var specRow = document.querySelector('.ds-row-spec');
            if (specRow) specRow.classList.add('active');
            var wrap = $('dsSubWrap');
            if (wrap) wrap.style.display = 'block';
            var targetBtn = document.querySelector('.ds-sub-btn[data-dataset="' + current + '"]');
            if (targetBtn) targetBtn.classList.add('active');
        } else {
            var wrap2 = $('dsSubWrap');
            if (wrap2) wrap2.style.display = 'none';
            var specRow2 = document.querySelector('.ds-row-spec');
            if (specRow2) specRow2.classList.remove('active');
            var targetTab = document.querySelector('.ds-row-tab[data-dataset="' + current + '"]');
            if (targetTab) targetTab.classList.add('active');
        }
    }
}
"""


# ═══════════════════════════════════════════════════════════════════
#  HÀM PUBLIC
# ═══════════════════════════════════════════════════════════════════
def override_ui_css(css_original):
    """Áp đè CSS mới lên CSS gốc."""
    css = css_original

    # ─── 1. Thay block DATASET SELECTOR ───
    pattern = re.compile(
        r'/\* =+\s*\*/\s*'
        r'/\* DATASET SELECTOR - 2 CAP.*?'
        r'(?=/\* =+\s*\*/\s*/\* FLASHCARD UI)',
        re.DOTALL
    )
    if pattern.search(css):
        css = pattern.sub(NEW_DATASET_CSS + "\n\n", css, count=1)
        print("✅ override_ui_css: Đã thay block DATASET SELECTOR")
    else:
        print("⚠️  override_ui_css: Không tìm thấy block DATASET SELECTOR cũ")

    # ─── 2. Fix bug .fav-btn.locked ───
    broken_fav_locked = """.fav-btn.locked{
    color:#dc2626;
   {
 background:rgba(220,   38,38,.1);
}
.fav-btn position.locked:hover{
    transform:scale(1:.12);
    background:absolutergba(220,38,38;
,.2);
    color:#b91c1c;
}"""
    fixed_fav_locked = """.fav-btn.locked{
    color:#dc2626;
    background:rgba(220,38,38,.1);
}
.fav-btn.locked:hover{
    transform:scale(1.12);
    background:rgba(220,38,38,.2);
    color:#b91c1c;
}"""
    if broken_fav_locked in css:
        css = css.replace(broken_fav_locked, fixed_fav_locked, 1)
        print("✅ override_ui_css: Đã fix bug .fav-btn.locked")
    else:
        pattern2 = re.compile(
            r'\.fav-btn\.locked\{\s*color:#dc2626;\s*\{.*?color:#b91c1c;\s*\}',
            re.DOTALL
        )
        if pattern2.search(css):
            css = pattern2.sub(fixed_fav_locked, css, count=1)
            print("✅ override_ui_css: Đã fix bug .fav-btn.locked (pattern 2)")

    # ─── 3. Fix bug .ds-fav-badge thiếu { ───
    broken_badge = '.ds-btn[data-dataset-group="favorites"] .ds-fav-badge    top:-8px;'
    fixed_badge = '.ds-btn[data-dataset-group="favorites"] .ds-fav-badge{\n    top:-8px;'
    if broken_badge in css:
        css = css.replace(broken_badge, fixed_badge, 1)
        print("✅ override_ui_css: Đã fix bug .ds-fav-badge")

    return css


def override_ui_html(html_original):
    """Thay block .ds-main-row bằng .ds-list."""
    html = html_original

    # Pattern A: từ comment DATASET SELECTOR → hết .ds-main-row
    pattern = re.compile(
        r'<!-- DATASET SELECTOR[^>]*-->.*?'
        r'<div class="ds-main-row">.*?</div>\s*'
        r'(?=<div class="ds-sub-wrap" id="dsSubWrap")',
        re.DOTALL
    )
    if pattern.search(html):
        html = pattern.sub(NEW_DATASET_HTML + "\n\n", html, count=1)
        print("✅ override_ui_html: Đã thay block DATASET SELECTOR HTML")
        return html

    # Pattern B: chỉ thay .ds-main-row → .ds-list
    old_inner = re.compile(
        r'<div class="ds-main-row">.*?(<!-- __FAV_DATASET_TAB__ -->).*?</div>',
        re.DOTALL
    )
    if old_inner.search(html):
        html = old_inner.sub(
            '<div class="ds-list" id="dsList" role="tablist">\n'
            '        \\1\n'
            '    </div>',
            html,
            count=1
        )
        print("✅ override_ui_html: Đã thay .ds-main-row → .ds-list (pattern B)")
        return html

    # Pattern C: tìm .ds-main-row bất kỳ
    old_simple = re.compile(
        r'<div class="ds-main-row">(.*?)</div>',
        re.DOTALL
    )
    if old_simple.search(html):
        html = old_simple.sub(
            '<div class="ds-list" id="dsList" role="tablist">\n        \\1\n    </div>',
            html,
            count=1
        )
        print("✅ override_ui_html: Đã thay .ds-main-row → .ds-list (pattern C)")
        return html

    print("⚠️  override_ui_html: Không tìm thấy .ds-main-row")
    return html


def override_ui_js(js_original):
    """Chèn OVERRIDE cuối file JS (function declaration tự ghi đè)."""
    js = js_original + "\n" + NEW_JS_OVERRIDE
    print("✅ override_ui_js: Đã chèn OVERRIDE cuối file JS")
    return js


def override_fullwidth_css(css_original):
    """Xóa block .ds-main-row khỏi FULLWIDTH_CSS (nếu có)."""
    css = css_original

    pattern = re.compile(
        r'/\* ═+\s*\*/\s*'
        r'/\* ★★★ FAVORITES TAB — 3 TAB CÙNG HÀNG TRÊN PC ★★★ \*/\s*'
        r'/\* ═+\s*\*/\s*'
        r'.*?(?=/\* ═+\s*\*/\s*/\* ★★★ HEADER DESIGN)',
        re.DOTALL
    )
    if pattern.search(css):
        css = pattern.sub("", css, count=1)
        print("✅ override_fullwidth_css: Đã xóa block .ds-main-row")
    else:
        print("ℹ️  override_fullwidth_css: Không có .ds-main-row (OK)")

    return css
