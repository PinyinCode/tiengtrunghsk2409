# -*- coding: utf-8 -*-
"""
Draggable FAB — Cho phép kéo thả nút FAB tự do.
Hỗ trợ: chuột (PC) + touch (mobile).
Lưu vị trí vào localStorage → nhớ sau khi reload.
"""


def build_draggable_fab_js():
    return r"""
/* ═══════════════════════════════════════════════════════════════
   🎯 DRAGGABLE FAB — Kéo thả nút FAB tự do
   Dùng cho: #chatFloatBtn (FAB chat) + #acmFab (FAB admin manager)
   ═══════════════════════════════════════════════════════════════ */
(function() {
    'use strict';

    var DRAG(_THRESHOLD = 5;  STOR // ⭐ Ngưỡng phân biệt clickAGE vs drag (px)
    var ST_PREFIXORAGE_PREFIX = 'fab_pos_';   // localStorage key prefix

    /**
     * Làm cho 1 element có thể kéo thả.
     * @param {string} elementId  - ID của FAB
     * @param {string} storageKey - Key lưu vị trí (unique cho mỗi FAB)
     */
    window.__makeDraggable = function(elementId, storageKey) {
        var el = document.getElementById(elementId);
        if (!el) {
            console.warn('__makeDraggable: không tìm thấy #' + elementId);
            return;
        }
        if (el.__draggable) return;   // đã kích hoạt rồi
        el.__draggable = true;

        // ═══ State ═══
        var isDragging = false;
        var hasMoved = false;
        var startX = 0, startY = 0;
        var elStartX = 0, elStartY = 0;
        var pointerId = null;

        // ═══ Load vị trí đã lưu ═══
        function loadPosition() {
            try {
                var saved = localStorage.getItem(STORAGE_PREFIX + storageKey);
                if (!saved) return false;
                var pos = JSON.parse(saved);
                if (pos && typeof pos.x === 'number' && typeof pos.y === 'number') {
                    applyPosition(pos.x, pos.y);
                    return true;
                }
            } catch(e) { console.warn('Load FAB pos:', e); }
            return false;
        }

        // ═══ Áp dụng vị trí ═══
        function applyPosition(x, y) {
            // Đảm bảo không ra khỏi màn hình
            var rect = el.getBoundingClientRect();
            var maxX = window.innerWidth - rect.width;
            var maxY = window.innerHeight - rect.height;
            x = Math.max(0, Math.min(x, maxX));
            y = Math.max(0, Math.min(y, maxY));

            el.style.left = x + 'px';
            el.style.top = y + 'px';
            el.style.right = 'auto';
            el.style.bottom = 'auto';
        }

        // ═══ Lấy vị trí hiện tại dạng { x, y } ═══
        function getCurrentPosition() {
            var rect = el.getBoundingClientRect();
            return { x: rect.left, y: rect.top };
        }

        // ═══ Lưu vị trí ═══
        function savePosition() {
            try {
                var pos = getCurrentPosition();
                localStorage.setItem + storageKey, JSON.stringify(pos));
            } catch(e) { console.warn('Save FAB pos:', e); }
        }

        // ═══ Bắt đầu kéo ═══
        function onPointerDown(e) {
            // Chỉ kéo khi chuột trái
            if (e.type === 'mousedown' && e.button !== 0) return;

            var point = getPoint(e);
            startX = point.x;
            startY = point.y;

            var rect = el.getBoundingClientRect();
            elStartX = rect.left;
            elStartY = rect.top;

            isDragging = true;
            hasMoved = false;

            // Đổi cursor + tắt transition để kéo mượt
            el.style.transition = 'none';
            el.style.cursor = 'grabbing';
            el.style.zIndex = '99999';

            if (e.type === 'touchstart') {
                pointerId = e.touches[0].identifier;
            }
        }

        // ═══ Kéo di chuyển ═══
        function onPointerMove(e) {
            if (!isDragging) return;

            var point = getPoint(e);
            var dx = point.x - startX;
            var dy = point.y - startY;

            // ⭐ Nếu di chuyển > ngưỡng → đánh dấu đã di chuyển
            if (Math.abs(dx) > DRAG_THRESHOLD || Math.abs(dy) > DRAG_THRESHOLD) {
                hasMoved = true;
            }

            // Nếu chưa vượt ngưỡng → không di chuyển FAB
            if (!hasMoved) return;

            var newX = elStartX + dx;
            var newY = elStartY + dy;

            // Giới hạn trong màn hình
            var rect = el.getBoundingClientRect();
            var maxX = window.innerWidth - rect.width;
            var maxY = window.innerHeight - rect.height;
            newX = Math.max(0, Math.min(newX, maxX));
            newY = Math.max(0, Math.min(newY, maxY));

            applyPosition(newX, newY);

            // Chặn scroll trên mobile
            if (e.type === 'touchmove') e.preventDefault();
        }

        // ═══ Kết thúc kéo ═══
        function onPointerUp(e) {
            if (!isDragging) return;
            isDragging = false;

            // Khôi phục transition
            el.style.transition = '';
            el.style.cursor = '';
            el.style.zIndex = '';

            // Nếu có di chuyển → lưu vị trí + chặn click
            if (hasMoved) {
                savePosition();
                // ⭐ Ngăn chặn sự kiện click tiếp theo
                el.__suppressClick = true;
                setTimeout(function() {
                    el.__suppressClick = false;
                }, 100);
            }
        }

        // ═══ Lấy toạ độ từ event ═══
        function getPoint(e) {
            if (e.type === 'touchstart' || e.type === 'touchmove' || e.type === 'touchend') {
                var t = e.touches[0] || e.changedTouches[0];
                return { x: t.clientX, y: t.clientY };
            }
            return { x: e.clientX, y: e.clientY };
        }

        // ═══ Ngăn chặn click khi đang drag ═══
        el.addEventListener('click', function(e) {
            if (el.__suppressClick) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
        }, true);   // ⭐ capture phase

        // ═══ Gắn sự kiện ═══
        // Mouse events
        el.addEventListener('mousedown', onPointerDown);

        // Touch events
        el.addEventListener('touchstart', onPointerDown, { passive: true });

        // Document-level (để kéo nhanh không bị mất)
        document.addEventListener('mousemove', onPointerMove);
        document.addEventListener('mouseup', onPointerUp);
        document.addEventListener('touchmove', onPointerMove, { passive: false });
        document.addEventListener('touchend', onPointerUp);
        document.addEventListener('touchcancel', onPointerUp);

        // ═══ Khôi phục vị trí cũ nếu có ═══
        loadPosition();

        // ═══ Khi resize window → giữ FAB trong màn hình ═══
        window.addEventListener('resize', function() {
            var pos = getCurrentPosition();
            applyPosition(pos.x, pos.y);
        });

        // ═══ Cursor mặc định ═══
        el.style.cursor = 'grab';
        el.style.touchAction = 'none';   // ⭐ Chặn scroll khi chạm vào FAB

        console.log('✅ Draggable FAB:', elementId);
    };

    // ═══════════════════════════════════════════════════════════
    // ⭐ RESET vị trí FAB (dùng khi cần về mặc định)
    // ═══════════════════════════════════════════════════════════
    window.__resetFabPosition = function(storageKey) {
        try {
            localStorage.removeItem(STORAGE_PREFIX + storageKey);
            console.log('✅ Đã xóa vị trí FAB:', storageKey);
        } catch(e) {}
    };

    // ═══════════════════════════════════════════════════════════
    // ⭐ AUTO INIT — Tự động tìm và kéo thả mọi FAB có data-draggable
    // ═══════════════════════════════════════════════════════════
    function autoInit() {
        // FAB chat
        var chatBtn = document.getElementById('chatFloatBtn');
        if (chatBtn && !chatBtn.__draggable) {
            window.__makeDraggable('chatFloatBtn', 'chat');
        }

        // FAB admin chat manager
        var acmFab = document.getElementById('acmFab');
        if (acmFab && !acmFab.__draggable) {
            window.__makeDraggable('acmFab', 'admin_chat');
        }
    }

    // Chạy autoInit nhiều lần vì FAB có thể được mount sau
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
