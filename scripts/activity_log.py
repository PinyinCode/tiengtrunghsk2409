# -*- coding: utf-8 -*-
"""
Activity Log — Ghi log hoạt động của user.
- Cung cấp window.__logActivity(email, type, title, detail, metadata)
- Tự động chống log trùng (3 giây)
- Hỗ trợ các type: login, logout, chat, renewal, favorite, practice, admin, other
- Fallback localStorage nếu chưa login
"""


def build_activity_log_js():
    return r"""
/* ═══════════════════════════════════════════════════════════════
   📝 ACTIVITY LOG — Ghi log hoạt động của user
   Cung cấp: window.__logActivity(email, type, title, detail, metadata)
   ═══════════════════════════════════════════════════════════════ */
(function() {
    'use strict';

    var FIRESTORE_COLLECTION = 'activity_logs';
    var MIN_INTERVAL = 3000;      // Chống log trùng trong 3 giây
    var MAX_LOG_PER_MINUTE = 30;  // Rate limit: tối đa 30 log/phút

    var _lastLog = {};       // { key: timestamp }
    var _minuteLog = [];     // Timestamps của log trong 1 phút

    /**
     * Kiểm tra rate limit
     */
    function checkRateLimit() {
        var now = Date.now();
        _minuteLog = _minuteLog.filter(function(t) {
            return now - t < 60000;
        });
        if (_minuteLog.length >= MAX_LOG_PER_MINUTE) {
            console.warn('[ActivityLog] ⏸ Rate limit — bỏ qua');
            return false;
        }
        _minuteLog.push(now);
        return true;
    }

    /**
     * Ghi log hoạt động
     * @param {string} email    - Email user
     * @param {string} type     - 'login' | 'logout' | 'chat' | 'renewal' | 'favorite' | 'practice' | 'admin' | 'other'
     * @param {string} title    - Tiêu đề (VD: "Đăng nhập thành công")
     * @param {string} detail   - Chi tiết (optional)
     * @param {object} metadata - Dữ liệu bổ sung (optional)
     */
    window.__logActivity = function(email, type, title, detail, metadata) {
        try {
            if (!email) {
                console.warn('[ActivityLog] Thiếu email');
                return;
            }

            // ─── Chống log trùng trong 3s ───
            var key = email + '|' + (type || 'other') + '|' +
                      (title || '').substring(0, 30) + '|' +
                      (detail || '').substring(0, 30);
            var now = Date.now();
            if (_lastLog[key] && (now - _lastLog[key]) < MIN_INTERVAL) {
                return;
            }
            _lastLog[key] = now;

            // ─── Rate limit ───
            if (!checkRateLimit()) return;

            // ─── Lấy DB ───
            var db = window.db;
            if (!db) {
                console.warn('[ActivityLog] Chưa có Firestore (window.db)');
                return;
            }

            if (typeof firebase === 'undefined' || !firebase.firestore) {
                console.warn('[ActivityLog] Firebase chưa load');
                return;
            }

            // ─── Chuẩn bị data ───
            var logData = {
                email: String(email).toLowerCase(),
                type: type || 'other',
                title: title || 'Hoạt động',
                detail: detail || '',
                at: firebase.firestore.FieldValue.serverTimestamp()
            };

            if (metadata && typeof metadata === 'object') {
                logData.metadata = metadata;
            }

            // ─── Ghi Firestore ───
            db.collection(FIRESTORE_COLLECTION).add(logData)
                .then(function(ref) {
                    console.log('[ActivityLog] ✅', type, '—', title);
                })
                .catch(function(e) {
                    console.warn('[ActivityLog] ❌', e.message);
                });

        } catch(e) {
            console.warn('[ActivityLog] Error:', e);
        }
    };

    // ═══════════════════════════════════════════════════════════
    // ⭐ AUTO LOG — Tự động ghi log một số sự kiện
    // ═══════════════════════════════════════════════════════════

    /**
     * Tự động log khi user login
     * Gọi từ watchAuth hoặc sau khi login thành công
     */
    window.__logLogin = function(email, name) {
        if (!email) {
            var u = window.currentUser;
            if (!u || !u.email) return;
            email = u.email;
            name = u.name;
        }

        // Chống log trùng session
        try {
            var key = 'log_login_' + email + '_' + new Date().toDateString();
            if (sessionStorage.getItem(key)) return;
            sessionStorage.setItem(key, '1');
        } catch(e) {}

        var device = 'Unknown';
        try {
            var ua = navigator.userAgent || '';
            if (/Mobile|Android|iPhone/i.test(ua)) device = 'Mobile';
            else if (/Tablet|iPad/i.test(ua)) device = 'Tablet';
            else device = 'Desktop';

            // Browser
            if (/Chrome/i.test(ua) && !/Edg/i.test(ua)) device += ' · Chrome';
            else if (/Firefox/i.test(ua)) device += ' · Firefox';
            else if (/Safari/i.test(ua) && !/Chrome/i.test(ua)) device += ' · Safari';
            else if (/Edg/i.test(ua)) device += ' · Edge';
        } catch(e) {}

        window.__logActivity(
            email,
            'login',
            'Đăng nhập thành công',
            device,
            { device: device, ua: navigator.userAgent }
        );
    };

    /**
     * Tự động log khi user logout
     */
    window.__logLogout = function(email) {
        if (!email) {
            var u = window.currentUser;
            if (!u || !u.email) return;
            email = u.email;
        }

        window.__logActivity(
            email,
            'logout',
            'Đăng xuất',
            '',
            {}
        );
    };

    /**
     * Log khi user gửi chat
     */
    window.__logChat = function(email, text, from) {
        if (!email || !text) return;

        var title = (from === 'admin')
            ? 'Nhận tin nhắn từ Admin'
            : 'Gửi tin nhắn cho Admin';

        window.__logActivity(
            email,
            'chat',
            title,
            String(text).substring(0, 100),
            { length: text.length, from: from || 'user' }
        );
    };

    /**
     * Log khi user gửi yêu cầu gia hạn
     */
    window.__logRenewal = function(email, amount, packageLabel, days, isPermanent) {
        if (!email) return;

        var detail = (amount || 0).toLocaleString('vi-VN') + 'đ · ' +
                     (packageLabel || 'Gói') + ' · ' +
                     (isPermanent ? 'Vĩnh viễn' : (days || 0) + ' ngày');

        window.__logActivity(
            email,
            'renewal',
            'Yêu cầu gia hạn: ' + (packageLabel || ''),
            detail,
            { amount: amount, days: days, isPermanent: !!isPermanent }
        );
    };

    /**
     * Log khi admin xác nhận gia hạn
     */
    window.__logRenewalConfirmed = function(email, amount, newExpiry) {
        if (!email) return;

        var detail = (amount || 0).toLocaleString('vi-VN') + 'đ';
        if (newExpiry) detail += ' · Hạn mới: ' + newExpiry;

        window.__logActivity(
            email,
            'renewal',
            'Admin đã xác nhận gia hạn',
            detail,
            { confirmed: true }
        );
    };

    /**
     * Log khi user thêm/bỏ yêu thích
     */
    window.__logFavorite = function(email, action, stt, text) {
        if (!email) return;

        var title = (action === 'add')
            ? 'Thêm câu vào yêu thích'
            : 'Bỏ câu khỏi yêu thích';

        var detail = text ? String(text).substring(0, 80) : ('Câu #' + (stt || ''));

        window.__logActivity(
            email,
            'favorite',
            title,
            detail,
            { action: action, stt: stt }
        );
    };

    /**
     * Log khi user luyện tập
     * Không log mọi câu — chỉ log theo batch để tránh spam
     */
    window.__logPractice = function(email, count, correct, hsk) {
        if (!email) return;

        var detail = 'HSK ' + (hsk || '?') + ' · ' +
                     'Đúng: ' + (correct || 0) + '/' + (count || 0);

        window.__logActivity(
            email,
            'practice',
            'Luyện tập ' + (count || 0) + ' câu',
            detail,
            { count: count, correct: correct, hsk: hsk }
        );
    };

    /**
     * Log hành động admin
     */
    window.__logAdmin = function(email, action, detail) {
        if (!email) return;

        window.__logActivity(
            email,
            'admin',
            action || 'Hành động admin',
            detail || '',
            { adminAction: true }
        );
    };

    console.log('✅ Activity Log module loaded');
})();
"""
