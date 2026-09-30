# -*- coding: utf-8 -*-
import html as _html

def _esc(s):
    if s is None:
        return ""
    return _html.escape(str(s), quote=True)

def _esc_js(s):
    if s is None:
        return ""
    return (str(s)
            .replace('\\', '\\\\')
            .replace("'", "\\'")
            .replace('"', '\\"')
            .replace('\n', '\\n')
            .replace('\r', '')
            .replace('</', '<\\/'))

def build_data_tabs_html(dataset_registry):
    if not dataset_registry:
        return ""
    items = [ds for k, ds in dataset_registry.items() if k != "tonghop"]
    if not items:
        return "<!-- data_tabs empty -->"
    items.sort(key=lambda d: d.get("name", "").lower())

    buttons = []
    for ds in items:
        did = _esc(ds.get("id", ""))
        did_js = _esc_js(ds.get("id", ""))
        name = _esc(ds.get("name", ""))
        name_js = _esc_js(ds.get("name", ""))
        icon = _esc(ds.get("icon", "fa-folder"))
        cnt = int(ds.get("count", 0))
        title = "{} ({} cau)".format(ds.get("name", ""), cnt)

        btn = (
            '<button class="ds-btn dt-tab" '
            'data-dataset="' + did + '" '
            'data-dataset-name="' + name + '" '
            'title="' + _esc(title) + '" '
            'onclick="window.__dtOnTabClick(event, \'' + did_js + '\', \'' + name_js + '\')">'
            '<i class="fas ' + icon + '"></i>'
            '<span class="dt-tab-label">' + name + '</span>'
            '<span class="dt-tab-count">' + str(cnt) + '</span>'
            '<i class="fas fa-lock dt-tab-lock" style="display:none"></i>'
            '</button>'
        )
        buttons.append(btn)

    return (
        '<!-- DATA TABS auto -->\n'
        '<div class="dt-tabs-wrap" id="dtTabsWrap">\n'
        + "\n".join(buttons) +
        '\n</div>\n'
        '<!-- /DATA TABS -->'
    )
   # -*- coding: utf-8 -*-

def build_data_tabs_css():
    return """

.dt-tabs-wrap { display: contents; }

.ds-btn.dt-tab {
    position: relative;
    overflow: visible;
    transition: transform .25s ease, box-shadow .25s ease, border-color .2s ease;
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
    background: rgba(139,92,246,.12);
    color: #5b21b6;
    border: 1px solid rgba(139,92,246,.3);
    margin-left: .15rem;
}

.ds-btn.dt-tab:hover:not(.dt-locked):not(.active) {
    transform: translateY(-2px);
    border-color: #8b5cf6;
    box-shadow: 0 6px 18px rgba(139,92,246,.25);
}

.ds-btn.dt-tab.active {
    box-shadow: 0 6px 20px rgba(124,58,237,.45);
}

.ds-btn.dt-tab.active .dt-tab-count {
    background: rgba(255,255,255,.25);
    color: #fff;
    border-color: rgba(255,255,255,.4);
}

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
    font-size: .7rem;
    color: #dc2626;
    background: rgba(220,38,38,.12);
    padding: .18rem .4rem;
    border-radius: 5px;
    align-items: center;
    justify-content: center;
    line-height: 1;
    flex-shrink: 0;
}

@media (max-width: 768px) {
    .ds-btn.dt-tab .dt-tab-count { font-size: .6rem; }
    .ds-btn.dt-tab .dt-tab-label { font-size: .78rem; }
}

@media (max-width: 500px) {
    .ds-btn.dt-tab { padding: .55rem .75rem; }
    .ds-btn.dt-tab .dt-tab-label { font-size: .74rem; }
    .ds-btn.dt-tab .dt-tab-count { font-size: .58rem; }
}
"""

def build_data_tabs_js():
    return """

(function() {
    'use strict';
    if (window.__dtModuleLoaded) { return; }
    window.__dtModuleLoaded = true;

    function _canAccessDataset() {
        if (typeof window.canAccessChuyenNganh === 'function') {
            return window.canAccessChuyenNganh();
        }
        return false;
    }

    function _getTierInfo() {
        if (typeof window.getTierInfo === 'function') {
            return window.getTierInfo();
        }
        return { tier: 'demo' };
    }

    function refreshLocks() {
        var canAccess = _canAccessDataset();
        var tabs = document.querySelectorAll('.ds-btn.dt-tab');
        tabs.forEach(function(btn) {
            var isLocked = !canAccess;
            btn.classList.toggle('dt-locked', isLocked);
            var lockIcon = btn.querySelector('.dt-tab-lock');
            if (lockIcon) {
                if (isLocked) {
                    lockIcon.style.display = 'inline-flex';
                } else {
                    lockIcon.style.display = 'none';
                }
            }
        });
    }

    function markActive(datasetId) {
        if (!datasetId) {
            if (typeof window.CURRENT_DATASET !== 'undefined') {
                datasetId = window.CURRENT_DATASET;
            } else {
                datasetId = 'tonghop';
            }
        }
        var allTabs = document.querySelectorAll('.ds-btn.dt-tab');
        allTabs.forEach(function(btn) {
            if (btn.dataset.dataset === datasetId) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

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
                others.forEach(function(b) {
                    b.classList.remove('active');
                });
                var subWrap = document.getElementById('dsSubWrap');
                if (subWrap) {
                    subWrap.style.display = 'none';
                }
            }
        }
    }

    window.__dtOnTabClick = function(evt, datasetId, datasetName) {
        if (evt) {
            evt.stopPropagation();
            if (evt.preventDefault) {
                evt.preventDefault();
            }
        }

        if (!_canAccessDataset()) {
            if (typeof window.showChuyenNganhLockMessage === 'function') {
                window.showChuyenNganhLockMessage();
            } else {
                var msg = 'Bo du lieu "' + (datasetName || datasetId) + '"\\n\\n' +
                          'Ban can dang nhap va gia han de mo khoa.';
                if (typeof window.currentUser !== 'undefined' && window.currentUser) {
                    if (confirm(msg + '\\n\\nGia han ngay?')) {
                        if (typeof window.openRenewalModal === 'function') {
                            window.openRenewalModal();
                        }
                    }
                } else {
                    if (confirm(msg + '\\n\\nDang nhap ngay?')) {
                        if (typeof window.showLoginModal === 'function') {
                            window.showLoginModal();
                        }
                    }
                }
            }
            return;
        }

        if (typeof window.switchDataset === 'function') {
            window.switchDataset(datasetId);
        } else {
            if (typeof window.__switchRawData === 'function') {
                window.__switchRawData(datasetId);
            }
            if (typeof window.applyFilter === 'function') {
                window.applyFilter();
            }
            if (typeof window.buildFilters === 'function') {
                window.buildFilters();
            }
        }

        markActive(datasetId);

        var fabGroup = document.getElementById('fabGroup');
        if (fabGroup) {
            fabGroup.classList.remove('open');
        }
    };

    document.addEventListener('click', function(e) {
        var btn = e.target.closest ? e.target.closest('.ds-btn') : null;
        if (!btn) { return; }
        if (btn.classList.contains('dt-tab')) { return; }
        var dtTabs = document.querySelectorAll('.ds-btn.dt-tab.active');
        dtTabs.forEach(function(t) {
            t.classList.remove('active');
        });
    }, true);

    function init() {
        refreshLocks();
        var current = 'tonghop';
        if (typeof window.CURRENT_DATASET !== 'undefined') {
            current = window.CURRENT_DATASET;
        }
        markActive(current);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        setTimeout(init, 0);
    }

    var _lastTierSig = '';
    setInterval(function() {
        var info = _getTierInfo();
        var sig = info.tier + '|' + (info.email || '');
        if (sig !== _lastTierSig) {
            _lastTierSig = sig;
            refreshLocks();
            var current = 'tonghop';
            if (typeof window.CURRENT_DATASET !== 'undefined') {
                current = window.CURRENT_DATASET;
            }
            markActive(current);
        }
    }, 2000);

    window.__dtRefreshLocks = refreshLocks;
    window.__dtMarkActive   = markActive;
})();
"""
