# -*- coding: utf-8 -*-
"""
Draggable FAB — Cho phép kéo thả nút FAB tự do.
- Mặc định: cả 2 nút giữ nguyên vị trí như hiện tại (CSS)
- USER thường: chỉ kéo được 1 nút (FAB chat tím)
- ADMIN: kéo được cả 2 nút (chat tím + admin manager xanh)
- Mỗi user/admin có vị trí RIÊNG (theo email)
- Sync Firestore → đa máy
- Fallback localStorage nếu chưa login / offline
"""


def build_draggable_fab_css():
    """CSS bổ trợ cho draggable FAB."""
    return r"""
/* ═══════════════════════════════════════════════════════════════
   🎯 DRAGGABLE FAB — CSS bổ trợ
   ═══════════════════════════════════════════════════════════════ */

/* Khi FAB đang được kéo → tắt transition để mượt */
.acm-fab.dragging,
.chat-float-btn.dragging{
    transition:none !important;
    cursor:grabbing !important;
}

/* FAB có thể kéo → đổi cursor thành grab */
.acm-fab[data-draggable="1"],
.chat-float-btn[data-draggable="1"]{
    cursor:grab;
    touch-action:none;
    -webkit-user-select:none;
    user-select:none;
    -webkit-touch-callout:none;
}

/* Đang kéo → cursor grabbing */
.acm-fab[data-draggable="1"]:active,
.chat-float-btn[data-draggable="1"]:active{
    cursor:grabbing;
}

/* Toast thông báo */
.fab-toast{
    position:fixed;
    bottom:120px;
    left:50%;
    transform:translateX(-50%) translateY(20px);
    background:rgba(15,23,42,.95);
    color:#fff;
    padding:.7rem 1.2rem;
    border-radius:50px;
    font-size:.85rem;
    font-weight:600;
    z-index:99999;
    opacity:0;
    transition:opacity .3s, transform .3s;
    pointer-events:none;
    box-shadow:0 8px 24px rgba(0,0,0,.3);
    max-width:80vw;
    text-align:center;
}
.fab-toast.show{
    opacity:1;
    transform:translateX(-50%) translateY(0);
}
"""


def build_draggable_fab_js():
    return r"""
/* ═══════════════════════════════════════════════════════════════
   🎯 DRAGGABLE FAB — Kéo thả nút FAB tự do
   - USER: chỉ FAB chat (tím)
   - ADMIN: cả FAB chat + FAB admin manager (xanh)
   - Mặc định giữ nguyên vị trí CSS
   ═══════════════════════════════════════════════════════════════ */
(function() {
    'use strict';

    var DRAG_THRESHOLD = 5;
    var STORAGE_PREFIX = 'fab_pos_';
    var FIRESTORE_COLLECTION = 'user_prefs';
    var FIRESTORE_FIELD_PREFIX = 'fab_pos_';

    function getUser() {
        try { return window.currentUser || null; }
        catch(e) { return null; }
    }
    function getUserEmail() {
        var u = getUser();
        return (u && u.email) ? u.email : null;
    }
    function isAdmin() {
        var u = getUser();
        return u && u.role === 'admin';
    }
    function getUserKey(baseKey) {
        var email = getUserEmail();
        return baseKey + '_' + (email || 'guest');
    }

    function showToast(msg) {
        var t = document.getElementById('fabToast');
        if (!t) {
            t = document.createElement('div');
            t.id = 'fabToast';
            t.className = 'fab-toast';
            document.body.appendChild(t);
        }
        t.textContent = msg;
        t.classList.add('show');
        clearTimeout(t._timer);
        t._timer = setTimeout(function() { t.classList.remove('show'); }, 2000);
    }

    // ═══════════════════════════════════════════════════════════
    // MAIN — Làm cho 1 FAB kéo thả được
    // ═══════════════════════════════════════════════════════════
    window.__makeDraggable = function(elementId, baseStorageKey) {
        var el = document.getElementById(elementId);
        if (!el) {
            console.warn('__makeDraggable: không tìm thấy #' + elementId);
            return;
        }
        if (el.__draggable) return;
        el.__draggable = true;
        el.__baseKey = baseStorageKey;
        el.setAttribute('data-draggable', '1');

        var isDragging = false;
        var hasMoved = false;
        var startX = 0, startY = 0;
        var elStartX = 0, elStartY = 0;
        var storageKey = getUserKey(baseStorageKey);

        // ─────────────────────────────────────────────────────
        // Vị trí
        // ─────────────────────────────────────────────────────
        function applyPosition(x, y) {
            var rect = el.getBoundingClientRect();
            var maxX = window.innerWidth - rect.width - 4;
            var maxY = window.innerHeight - rect.height - 4;
            x = Math.max(4, Math.min(x, maxX));
            y = Math.max(4, Math.min(y, maxY));

            el.style.left = x + 'px';
            el.style.top = y + 'px';
            el.style.right = 'auto';
            el.style.bottom = 'auto';
        }

        function getCurrentPosition() {
            var rect = el.getBoundingClientRect();
            return { x: Math.round(rect.left), y: Math.round(rect.top) };
        }

        function fromLocalStorage() {
            try {
                var saved = localStorage.getItem(STORAGE_PREFIX + storageKey);
                if (saved) {
                    var pos = JSON.parse(saved);
                    if (pos && typeof pos.x === 'number') {
                        applyPosition(pos.x, pos.y);
                        return true;
                    }
                }
            } catch(e) {}
            return false;
        }

        function loadPosition() {
            var email = getUserEmail();
            var db = window.db;

            // ⭐ Nếu chưa login hoặc chưa có db → chỉ dùng localStorage
            if (!email || !db) {
                fromLocalStorage();
                return;
            }

            // ⭐ Load Firestore trước
            var fieldName = FIRESTORE_FIELD_PREFIX + baseStorageKey;
            db.collection(FIRESTORE_COLLECTION).doc(email).get()
                .then(function(doc) {
                    if (doc.exists) {
                        var data = doc.data();
                        var pos = data[fieldName];
                        if (pos && typeof pos.x === 'number') {
                            applyPosition(pos.x, pos.y);
                            try {
                                localStorage.setItem(
                                    STORAGE_PREFIX + storageKey,
                                    JSON.stringify({ x: pos.x, y: pos.y })
                                );
                            } catch(e) {}
                            return;
                        }
                    }
                    // Không có trong Firestore → localStorage
                    fromLocalStorage();
                })
                .catch(function(e) {
                    console.warn('FAB load Firestore error:', e);
                    fromLocalStorage();
                });
        }

        function savePosition() {
            var pos = getCurrentPosition();

            // 1. localStorage
            try {
                localStorage.setItem(
                    STORAGE_PREFIX + storageKey,
                    JSON.stringify(pos)
                );
            } catch(e) {}

            // 2. Firestore
            var email = getUserEmail();
            var db = window.db;
            if (email && db) {
                var fieldName = FIRESTORE_FIELD_PREFIX + baseStorageKey;
                var update = {};
                update[fieldName] = pos;
                db.collection(FIRESTORE_COLLECTION).doc(email)
                    .set(update, { merge: true })
                    .catch(function(e) {
                        console.warn('FAB save Firestore error:', e);
                    });
            }
        }

        // ─────────────────────────────────────────────────────
        // Pointer events
        // ─────────────────────────────────────────────────────
        function getPoint(e) {
            if (e.touches && e.touches.length) {
                return { x: e.touches[0].clientX, y: e.touches[0].clientY };
            }
            if (e.changedTouches && e.changedTouches.length) {
                return { x: e.changedTouches[0].clientX, y: e.changedTouches[0].clientY };
            }
            return { x: e.clientX, y: e.clientY };
        }

        function onPointerDown(e) {
            if (e.type === 'mousedown' && e.button !== 0) return;

            var point = getPoint(e);
            startX = point.x;
            startY = point.y;

            var rect = el.getBoundingClientRect();
            elStartX = rect.left;
            elStartY = rect.top;

            isDragging = true;
            hasMoved = false;

            el.style.transition = 'none';
            el.classList.add('dragging');
            el.style.zIndex = '99999';
        }

        function onPointerMove(e) {
            if (!isDragging) return;

            var point = getPoint(e);
            var dx = point.x - startX;
            var dy = point.y - startY;

            if (Math.abs(dx) > DRAG_THRESHOLD || Math.abs(dy) > DRAG_THRESHOLD) {
                hasMoved = true;
            }

            if (!hasMoved) return;

            var newX = elStartX + dx;
            var newY = elStartY + dy;
            applyPosition(newX, newY);

            if (e.cancelable) e.preventDefault();
        }

        function onPointerUp(e) {
            if (!isDragging) return;
            isDragging = false;

            el.style.transition = '';
            el.classList.remove('dragging');
            el.style.zIndex = '';

            if (hasMoved) {
                savePosition();
                el.__suppressClick = true;
                setTimeout(function() { el.__suppressClick = false; }, 150);
            }
        }

        // Chặn click sau khi drag
        el.addEventListener('click', function(e) {
            if (el.__suppressClick) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
        }, true);

        el.addEventListener('mousedown', onPointerDown);
        el.addEventListener('touchstart', onPointerDown, { passive: true });

        document.addEventListener('mousemove', onPointerMove);
        document.addEventListener('mouseup', onPointerUp);
        document.addEventListener('touchmove', onPointerMove, { passive: false });
        document.addEventListener('touchend', onPointerUp);
        document.addEventListener('touchcancel', onPointerUp);

        // Load vị trí
        loadPosition();

        // Resize
        window.addEventListener('resize', function() {
            var pos = getCurrentPosition();
            applyPosition(pos.x, pos.y);
        });

        console.log('✅ Draggable FAB:', elementId, '| key:', storageKey);
    };

    // ═══════════════════════════════════════════════════════════
    // RESET vị trí
    // ═══════════════════════════════════════════════════════════
    window.__resetFabPosition = function(baseKey) {
        var email = getUserEmail();
        var storageKey = getUserKey(baseKey);

        try { localStorage.removeItem(STORAGE_PREFIX + storageKey); } catch(e) {}

        if (email && window.db) {
            var fieldName = FIRESTORE_FIELD_PREFIX + baseKey;
            var update = {};
            update[fieldName] = firebase.firestore.FieldValue.delete();
            window.db.collection(FIRESTORE_COLLECTION).doc(email)
                .update(update).catch(function() {});
        }

        showToast('✅ Đã reset vị trí nút');
        setTimeout(function() { location.reload(); }, 600);
    };

    // ═══════════════════════════════════════════════════════════
    // AUTO INIT — Quyết định FAB nào được kéo
    // ═══════════════════════════════════════════════════════════
    function initChatFab() {
        var chatBtn = document.getElementById('chatFloatBtn');
        if (!chatBtn) return;

        var chatKey = getUserKey('chat');

        // Nếu user đổi → reset
        if (chatBtn.__draggable && chatBtn.__storageKey !== chatKey) {
            chatBtn.__draggable = false;
            chatBtn.__storageKey = null;
            chatBtn.style.left = '';
            chatBtn.style.top = '';
            chatBtn.style.right = '';
            chatBtn.style.bottom = '';
        }

        if (!chatBtn.__draggable) {
            window.__makeDraggable('chatFloatBtn', 'chat');
            chatBtn.__storageKey = chatKey;
        }
    }

    function initAcmFab() {
        // ⭐ CHỈ ADMIN mới được kéo FAB xanh lá
        if (!isAdmin()) return;

        var acmFab = document.getElementById('acmFab');
        if (!acmFab) return;

        var acmKey = getUserKey('admin_chat');

        if (acmFab.__draggable && acmFab.__storageKey !== acmKey) {
            acmFab.__draggable = false;
            acmFab.__storageKey = null;
            acmFab.style.left = '';
            acmFab.style.top = '';
            acmFab.style.right = '';
            acmFab.style.bottom = '';
        }

        if (!acmFab.__draggable) {
            window.__makeDraggable('acmFab', 'admin_chat');
            acmFab.__storageKey = acmKey;
        }
    }

    function autoInit() {
        initChatFab();   // ⭐ Mọi user đều kéo được FAB chat
        initAcmFab();    // ⭐ Chỉ admin kéo được FAB admin manager
    }

    // ═══════════════════════════════════════════════════════════
    // WATCH user change → re-init
    // ═══════════════════════════════════════════════════════════
    var _lastEmail = null;
    var _lastRole = null;
    setInterval(function() {
        try {
            var u = getUser();
            var email = u ? u.email : null;
            var role = u ? (u.role || 'user') : null;

            if (email === _lastEmail && role === _lastRole) return;
            _lastEmail = email;
            _lastRole = role;

            // Reset
            ['chatFloatBtn', 'acmFab'].forEach(function(id) {
                var el = document.getElementById(id);
                if (el) {
                    el.__draggable = false;
                    el.__storageKey = null;
                    el.style.left = '';
                    el.style.top = '';
                    el.style.right = '';
                    el.style.bottom = '';
                }
            });

            setTimeout(autoInit, 300);
            console.log('🎯 FAB re-init cho:', email || 'guest', '| role:', role || '-');
        } catch(e) {}
    }, 2000);

    // ═══════════════════════════════════════════════════════════
    // KHỞI ĐỘNG
    // ═══════════════════════════════════════════════════════════
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', autoInit);
    } else {
        autoInit();
    }
    setTimeout(autoInit, 1000);
    setTimeout(autoInit, 3000);

    console.log('✅ Draggable FAB module loaded');
})();
"""
