# -*- coding: utf-8 -*-
"""
Chat Support độc lập — User ↔ Admin
Tách hoàn toàn khỏi auth/admin/renewal.
Yêu cầu đã có sẵn (từ Mã 1):
  - window.db            (Firestore)
  - window.currentUser   (object có email, name, role, isDemo...)
  - window.$             (querySelector helper)
  - window.escapeHtml    (escape function)
  - window.showLoginModal
  - window.TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID
"""


# ═══════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════
def build_chat_css():
    return r"""
/* ═══════════ CHAT FAB ═══════════ */
.chat-fab{
    position:fixed;right:20px;
    bottom:calc(95px + env(safe-area-inset-bottom));
    width:56px;height:56px;border-radius:50%;border:none;
    background:linear-gradient(135deg,#4f46e5,#7c3aed);
    color:#fff;cursor:pointer;
    display:flex;align-items:center;justify-content:center;
    font-size:1.35rem;
    box-shadow:0 8px 24px rgba(124,58,237,.45),0 2px 8px rgba(0,0,0,.15);
    z-index:999;
    transition:transform .25s cubic-bezier(.34,1.56,.64,1),box-shadow .25s;
}
.chat-fab:hover{transform:scale(1.1);}
.chat-fab.hidden{display:none}
.chat-fab .fab-badge{
    position:absolute;top:-2px;right:-2px;min-width:22px;height:22px;padding:0 .4rem;
    border-radius:50px;
    background:linear-gradient(135deg,#dc2626,#b91c1c);
    color:#fff;font-size:.7rem;font-weight:900;
    display:none;align-items:center;justify-content:center;
    border:2px solid #fff;line-height:1;
}
.chat-fab .fab-badge.show{display:flex}

/* ═══════════ CHAT MODAL ═══════════ */
.chat-modal{
    position:fixed;inset:0;background:rgba(15,23,42,.85);
    backdrop-filter:blur(6px);z-index:4000;display:none;
    align-items:center;justify-content:center;padding:1rem;
}
.chat-modal.show{display:flex}
.chat-box{
    background:#fff;border-radius:20px;
    width:100%;max-width:540px;height:min(85vh,720px);
    box-shadow:0 20px 60px rgba(0,0,0,.4);
    display:flex;flex-direction:column;overflow:hidden;
    position:relative;
}
[data-theme="dark"] .chat-box{background:#1e293b;}

.chat-header{
    padding:1rem 1.25rem;
    background:linear-gradient(135deg,#4f46e5,#7c3aed);
    color:#fff;display:flex;align-items:center;gap:.75rem;
    flex-shrink:0;
}
.chat-header-back{
    width:34px;height:34px;border-radius:50%;border:none;
    background:rgba(255,255,255,.15);color:#fff;cursor:pointer;
    display:none;align-items:center;justify-content:center;
    font-size:.95rem;flex-shrink:0;
}
.chat-header-back.show{display:flex}
.chat-header-info{flex:1;min-width:0}
.chat-header-info .name{font-weight:800;font-size:.95rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.chat-header-info .status{font-size:.72rem;opacity:.9;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.chat-header-close{
    width:34px;height:34px;border-radius:50%;border:none;
    background:rgba(255,255,255,.2);color:#fff;cursor:pointer;
    display:flex;align-items:center;justify-content:center;
    font-size:1rem;flex-shrink:0;
}
.chat-header-close:hover{background:rgba(255,255,255,.35)}

.chat-body{
    flex:1;min-height:0;overflow-y:auto;
    padding:1rem 1.25rem;
    background:#f8fafc;
    display:flex;flex-direction:column;gap:.45rem;
}
[data-theme="dark"] .chat-body{background:#0f172a;}

.chat-msg{
    display:flex;gap:.4rem;max-width:85%;align-items:flex-end;
}
.chat-msg.from-user{align-self:flex-end;flex-direction:row-reverse}
.chat-msg.from-admin{align-self:flex-start}
.chat-msg .bubble{
    padding:.6rem .85rem;border-radius:16px;
    font-size:.85rem;line-height:1.45;
    word-break:break-word;white-space:pre-wrap;
}
.chat-msg.from-user .bubble{
    background:linear-gradient(135deg,#4f46e5,#7c3aed);
    color:#fff;border-bottom-right-radius:4px;
}
.chat-msg.from-admin .bubble{
    background:#fff;color:#0f172a;
    border:1px solid #e2e8f0;
    border-bottom-left-radius:4px;
}
[data-theme="dark"] .chat-msg.from-admin .bubble{background:#334155;color:#f1f5f9;border-color:#475569;}
.chat-msg .msg-time{
    font-size:.62rem;color:#94a3b8;
    padding:0 .3rem;white-space:nowrap;
    align-self:flex-end;margin-bottom:.15rem;
}
.chat-system{
    align-self:center;font-size:.7rem;color:#64748b;
    background:#e2e8f0;padding:.25rem .75rem;
    border-radius:50px;text-align:center;margin:.3rem 0;
}

.chat-empty{
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    height:100%;text-align:center;color:#94a3b8;
    padding:1.5rem;gap:.75rem;
}
.chat-empty i{font-size:2.5rem;opacity:.35}
.chat-empty .title{font-size:.92rem;font-weight:700;color:#475569;}
.chat-empty .desc{font-size:.78rem;line-height:1.5;max-width:280px;}

.chat-footer{
    padding:.75rem 1rem;
    border-top:1px solid #e2e8f0;
    background:#fff;flex-shrink:0;
    display:flex;flex-direction:column;gap:.5rem;
}
[data-theme="dark"] .chat-footer{background:#1e293b;border-color:#334155;}
.chat-footer-row{display:flex;gap:.5rem;align-items:flex-end;}
.chat-footer textarea{
    flex:1;min-width:0;min-height:42px;max-height:130px;
    padding:.65rem .9rem;border-radius:22px;
    border:1.5px solid #e2e8f0;
    background:#f8fafc;color:#0f172a;
    font-size:.85rem;font-family:inherit;
    outline:none;resize:none;overflow-y:hidden;
    line-height:1.4;
}
[data-theme="dark"] .chat-footer textarea{background:#0f172a;color:#f1f5f9;border-color:#334155;}
.chat-footer textarea:focus{border-color:#4f46e5;}
.chat-send-btn{
    width:44px;height:44px;border-radius:50%;border:none;
    background:linear-gradient(135deg,#4f46e5,#7c3aed);
    color:#fff;cursor:pointer;
    display:flex;align-items:center;justify-content:center;
    font-size:1.05rem;flex-shrink:0;
}
.chat-send-btn:disabled{opacity:.4;cursor:not-allowed;}

.chat-quick-replies{
    display:flex;gap:.35rem;flex-wrap:wrap;padding:.5rem 0;
    border-bottom:1px dashed #e2e8f0;margin-bottom:.1rem;
}
.chat-quick-replies.hidden{display:none}
.chat-quick-btn{
    padding:.3rem .7rem;border-radius:50px;
    border:1.5px solid rgba(37,99,235,.3);
    background:rgba(37,99,235,.08);
    color:#1e40af;font-size:.72rem;font-weight:700;
    cursor:pointer;font-family:inherit;
}
.chat-quick-btn:hover{background:#2563eb;color:#fff;}

/* ═══════════ ADMIN CHAT THREAD LIST ═══════════ */
.admin-chat-thread{
    display:flex;align-items:center;gap:.75rem;
    padding:.75rem .85rem;
    background:#f8fafc;border:1px solid #e2e8f0;
    border-radius:12px;margin-bottom:.5rem;
    cursor:pointer;position:relative;
}
[data-theme="dark"] .admin-chat-thread{background:#334155;border-color:#475569;}
.admin-chat-thread:hover{border-color:#4f46e5;}
.admin-chat-thread.unread{border-color:#dc2626;background:rgba(220,38,38,.05);}
.admin-chat-thread .t-avatar{
    width:42px;height:42px;border-radius:50%;
    background:linear-gradient(135deg,#4f46e5,#7c3aed);
    color:#fff;display:flex;align-items:center;justify-content:center;
    font-weight:800;font-size:1rem;flex-shrink:0;
}
.admin-chat-thread .t-info{flex:1;min-width:0}
.admin-chat-thread .t-name{font-weight:800;font-size:.88rem;margin-bottom:.15rem;}
.admin-chat-thread .t-preview{font-size:.75rem;color:#64748b;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.admin-chat-thread .t-time{font-size:.68rem;color:#94a3b8;flex-shrink:0;}
.admin-chat-thread .t-badge{
    position:absolute;top:-4px;right:-4px;
    min-width:22px;height:22px;padding:0 .4rem;
    border-radius:50px;
    background:#dc2626;color:#fff;
    font-size:.65rem;font-weight:900;
    display:flex;align-items:center;justify-content:center;
}

@media (max-width:600px){
    .chat-box{max-width:100%;height:100vh;max-height:100vh;border-radius:0;}
    .chat-msg{max-width:90%}
}
"""


# ═══════════════════════════════════════════════════════════════
# HTML
# ═══════════════════════════════════════════════════════════════
def build_chat_html():
    return r"""
<!-- ═══ CHAT FAB ═══ -->
<button class="chat-fab hidden" id="chatFab" type="button" title="Chat với Admin">
    <i class="fas fa-comments"></i>
    <span class="fab-badge" id="chatFabBadge">0</span>
</button>

<!-- ═══ CHAT MODAL ═══ -->
<div class="chat-modal" id="chatModal">
    <div class="chat-box">
        <div class="chat-header">
            <button class="chat-header-back" id="chatBack" type="button">
                <i class="fas fa-arrow-left"></i>
            </button>
            <div class="chat-header-info" id="chatHeaderInfo">
                <div class="name">Hỗ trợ Admin</div>
                <div class="status">Thường trả lời trong 5-10 phút</div>
            </div>
            <button class="chat-header-close" id="chatClose" type="button">
                <i class="fas fa-times"></i>
            </button>
        </div>

        <div class="chat-body" id="chatBody">
            <div class="chat-empty">
                <i class="fas fa-comments"></i>
                <div class="title">Đang tải...</div>
            </div>
        </div>

        <div class="chat-footer">
            <div class="chat-quick-replies hidden" id="chatQuickReplies">
                <button class="chat-quick-btn" type="button" data-reply="Đã nhận được, em đợi admin 1-2 phút nhé!">Đã nhận, chờ 1-2 phút</button>
                <button class="chat-quick-btn" type="button" data-reply="Admin đã xác nhận thanh toán. Tài khoản được gia hạn rồi em nhé!">Đã xác nhận thanh toán</button>
                <button class="chat-quick-btn" type="button" data-reply="Em gửi giúp admin ảnh chụp biên lai chuyển khoản nhé.">Xin ảnh biên lai</button>
                <button class="chat-quick-btn" type="button" data-reply="Cảm ơn em đã ủng hộ. Chúc em học tốt! 🎓">Cảm ơn</button>
            </div>
            <div class="chat-footer-row">
                <textarea id="chatInput" placeholder="Nhập tin nhắn..." rows="1" maxlength="1000"></textarea>
                <button class="chat-send-btn" id="chatSendBtn" type="button" disabled>
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
    </div>
</div>
"""


# ═══════════════════════════════════════════════════════════════
# JS
# ═══════════════════════════════════════════════════════════════
def build_chat_js():
    return r"""
/* ═══════════════════════════════════════════════════════════════
   💬 CHAT SUPPORT — Độc lập, không phụ thuộc module auth
   ═══════════════════════════════════════════════════════════════ */
(function() {
    'use strict';

    /* ─── STATE ─── */
    var CHAT = {
        inited: false,
        userUnsub: null,          // user: onSnapshot messages của chính mình
        adminListUnsub: null,     // admin: onSnapshot list threads
        adminOpenUnsub: null,     // admin: onSnapshot messages của 1 thread
        adminCurrentEmail: null,
        pollTimer: null,
        toastTimer: null,
        isOpen: false
    };

    /* ─── HELPERS ─── */
    function $id(id) { return document.getElementById(id); }
    function esc(s) {
        if (s == null) return '';
        return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
                        .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
    }
    function jsStr(s) {
        if (s == null) return '';
        return String(s).replace(/\\/g,'\\\\').replace(/'/g,"\\'").replace(/"/g,'\\"');
    }
    function timeAgo(ms) {
        if (ms < 60000) return 'Vừa xong';
        if (ms < 3600000) return Math.floor(ms/60000) + ' phút trước';
        if (ms < 86400000) return Math.floor(ms/3600000) + ' giờ trước';
        if (ms < 2592000000) return Math.floor(ms/86400000) + ' ngày trước';
        return Math.floor(ms/2592000000) + ' tháng trước';
    }
    function fmtMoney(n) { return String(n||0).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }

    /* ─── GUARDS ─── */
    function getDb() { return window.db || null; }
    function getCu() { return window.currentUser || null; }
    function isAdmin() { var u = getCu(); return u && u.role === 'admin'; }

    /* ═════════════════════════════════════════════════════════
       FAB VISIBILITY
       ═════════════════════════════════════════════════════════ */
    function updateFabVisibility() {
        var fab = $id('chatFab');
        if (!fab) return;
        var u = getCu();
        if (u && u.email) {
            fab.classList.remove('hidden');
        } else {
            fab.classList.add('hidden');
        }
    }

    /* ═════════════════════════════════════════════════════════
       POLL BADGE — 60s
       ═════════════════════════════════════════════════════════ */
    function startBadgePoll() {
        stopBadgePoll();
        pollBadge(); // chạy ngay
        CHAT.pollTimer = setInterval(function() {
            if (document.hidden) return;
            pollBadge();
        }, 60000);
    }
    function stopBadgePoll() {
        if (CHAT.pollTimer) { clearInterval(CHAT.pollTimer); CHAT.pollTimer = null; }
    }
    function pollBadge() {
        var u = getCu(), db = getDb();
        if (!u || !u.email || !db) return;
        if (isAdmin()) { pollAdminBadge(); return; }

        db.collection('chat_threads').doc(u.email).get()
            .then(function(doc) {
                if (!doc.exists) { setFabBadge(0); return; }
                var d = doc.data() || {};
                var unread = d.unreadByUser || 0;
                setFabBadge(unread);
            })
            .catch(function() { /* im lặng */ });
    }
    function pollAdminBadge() {
        // Admin không cần badge trên FAB — chỉ cần biết có tin chưa đọc
        // Dùng count nhẹ, không watch
        var db = getDb();
        if (!db) return;
        // Đếm tổng unreadByAdmin — dùng 1 read đơn giản, limit 30
        db.collection('chat_threads').orderBy('lastMessageAt', 'desc').limit(30).get()
            .then(function(snap) {
                var total = 0;
                snap.forEach(function(d) { total += (d.data().unreadByAdmin || 0); });
                setFabBadge(total);
            })
            .catch(function() {});
    }
    function setFabBadge(n) {
        var el = $id('chatFabBadge');
        if (!el) return;
        if (n > 0) {
            el.textContent = n > 99 ? '99+' : n;
            el.classList.add('show');
        } else {
            el.classList.remove('show');
        }
    }

    /* ═════════════════════════════════════════════════════════
       OPEN / CLOSE
       ═════════════════════════════════════════════════════════ */
    function openChat() {
        var u = getCu();
        if (!u) {
            if (typeof window.showLoginModal === 'function') window.showLoginModal();
            return;
        }
        CHAT.isOpen = true;
        $id('chatModal').classList.add('show');

        // Ẩn dropdown nếu đang mở
        var dd = $id('userDropdown');
        if (dd) dd.classList.remove('show');

        if (isAdmin()) {
            openAdminListView();
        } else {
            openUserView();
        }
    }
    function closeChat() {
        CHAT.isOpen = false;
        $id('chatModal').classList.remove('show');
        detachAll();
    }
    function detachAll() {
        if (CHAT.userUnsub) { try { CHAT.userUnsub(); } catch(e){} CHAT.userUnsub = null; }
        if (CHAT.adminListUnsub) { try { CHAT.adminListUnsub(); } catch(e){} CHAT.adminListUnsub = null; }
        if (CHAT.adminOpenUnsub) { try { CHAT.adminOpenUnsub(); } catch(e){} CHAT.adminOpenUnsub = null; }
        CHAT.adminCurrentEmail = null;
    }

    /* ═════════════════════════════════════════════════════════
       USER VIEW
       ═════════════════════════════════════════════════════════ */
    function restoreUserHeader() {
        $id('chatHeaderInfo').innerHTML =
            '<div class="name">Hỗ trợ Admin</div>' +
            '<div class="status">Thường trả lời trong 5-10 phút</div>';
        $id('chatBack').classList.remove('show');
        $id('chatClose').style.display = 'flex';
        $id('chatQuickReplies').classList.add('hidden');
    }
    function openUserView() {
        restoreUserHeader();
        var u = getCu(), db = getDb();
        if (!db) return;

        var email = u.email;
        var threadRef = db.collection('chat_threads').doc(email);

        // Đảm bảo thread tồn tại (chỉ set nếu chưa từng init trong session)
        var initKey = 'chat_init_' + email;
        var alreadyInit = false;
        try { alreadyInit = sessionStorage.getItem(initKey) === '1'; } catch(e){}
        if (!alreadyInit) {
            threadRef.get().then(function(doc) {
                if (!doc.exists) {
                    threadRef.set({
                        userEmail: email,
                        userName: u.name || email.split('@')[0],
                        lastMessage: '',
                        lastMessageAt: firebase.firestore.FieldValue.serverTimestamp(),
                        lastMessageFrom: 'user',
                        unreadByAdmin: 0,
                        unreadByUser: 0,
                        createdAt: firebase.firestore.FieldValue.serverTimestamp()
                    }, { merge: true }).then(function() {
                        try { sessionStorage.setItem(initKey, '1'); } catch(e){}
                    }).catch(function(){});
                } else {
                    try { sessionStorage.setItem(initKey, '1'); } catch(e){}
                }
            }).catch(function(){});
        }

        // Listen messages
        if (CHAT.userUnsub) { try { CHAT.userUnsub(); } catch(e){} }
        CHAT.userUnsub = threadRef.collection('messages')
            .orderBy('createdAt', 'desc').limit(50)
            .onSnapshot(function(snap) {
                renderUserMessages(snap);
                // Mark read
                threadRef.get().then(function(doc) {
                    if (doc.exists && (doc.data().unreadByUser || 0) > 0) {
                        threadRef.update({ unreadByUser: 0 });
                    }
                }).catch(function(){});
                setFabBadge(0);
            }, function(err) {
                $id('chatBody').innerHTML =
                    '<div class="chat-empty"><i class="fas fa-exclamation-triangle" style="color:#dc2626"></i>' +
                    '<div class="title">Không tải được chat</div>' +
                    '<div class="desc">' + esc(err.message) + '</div></div>';
            });
    }
    function renderUserMessages(snap) {
        var body = $id('chatBody');
        if (!body) return;
        if (snap.empty) {
            body.innerHTML =
                '<div class="chat-empty">' +
                    '<i class="fas fa-comments"></i>' +
                    '<div class="title">Bắt đầu cuộc trò chuyện</div>' +
                    '<div class="desc">Gửi tin nhắn cho admin nếu bạn cần hỗ trợ.</div>' +
                '</div>';
            return;
        }
        var docs = [];
        snap.forEach(function(d){ docs.push(d); });
        docs.reverse();

        var html = '', lastDate = null;
        docs.forEach(function(doc) {
            var d = doc.data();
            var created = d.createdAt ? d.createdAt.toDate() : new Date();
            var dateStr = created.toLocaleDateString('vi-VN');
            if (dateStr !== lastDate) {
                html += '<div class="chat-system">' + dateStr + '</div>';
                lastDate = dateStr;
            }
            var time = created.toLocaleTimeString('vi-VN', {hour:'2-digit',minute:'2-digit'});
            var isMe = (d.from === 'user');
            html += '<div class="chat-msg ' + (isMe?'from-user':'from-admin') + '">' +
                '<div class="bubble">' + esc(d.text||'').replace(/\n/g,'<br>') + '</div>' +
                '<span class="msg-time">' + time + '</span>' +
            '</div>';
        });
        body.innerHTML = html;
        // Auto-scroll nếu đang gần cuối
        var nearBottom = body.scrollHeight - body.scrollTop - body.clientHeight < 150;
        if (nearBottom) setTimeout(function(){ body.scrollTop = body.scrollHeight; }, 30);
    }

    /* ═════════════════════════════════════════════════════════
       ADMIN VIEW — Danh sách threads
       ═════════════════════════════════════════════════════════ */
    function openAdminListView() {
        $id('chatHeaderInfo').innerHTML =
            '<div class="name">Chat hỗ trợ</div>' +
            '<div class="status">Chọn user để trả lời</div>';
        $id('chatBack').classList.remove('show');
        $id('chatClose').style.display = 'flex';
        $id('chatQuickReplies').classList.add('hidden');

        var db = getDb();
        if (!db) return;
        var body = $id('chatBody');
        body.innerHTML = '<div class="chat-empty"><i class="fas fa-spinner fa-pulse"></i><div class="title">Đang tải...</div></div>';

        if (CHAT.adminListUnsub) { try { CHAT.adminListUnsub(); } catch(e){} }
        CHAT.adminListUnsub = db.collection('chat_threads')
            .orderBy('lastMessageAt', 'desc').limit(30)
            .onSnapshot(function(snap) {
                if (snap.empty) {
                    body.innerHTML = '<div class="chat-empty"><i class="fas fa-comments"></i><div class="title">Chưa có hội thoại</div></div>';
                    setFabBadge(0);
                    return;
                }
                var html = '';
                var totalUnread = 0;
                snap.forEach(function(doc) {
                    var d = doc.data();
                    var email = d.userEmail || doc.id;
                    var name = d.userName || email.split('@')[0];
                    var unread = d.unreadByAdmin || 0;
                    totalUnread += unread;
                    var lastAt = d.lastMessageAt ? d.lastMessageAt.toDate() : new Date();
                    var preview = d.lastMessage || '(chưa có tin nhắn)';
                    if (d.lastMessageFrom === 'admin') preview = 'Bạn: ' + preview;
                    var initial = (name.charAt(0) || '?').toUpperCase();

                    html += '<div class="admin-chat-thread' + (unread>0?' unread':'') + '" ' +
                        'onclick="window.__chatOpenThread(\'' + jsStr(email) + '\')">' +
                        '<div class="t-avatar">' + esc(initial) + '</div>' +
                        '<div class="t-info">' +
                            '<div class="t-name">' + esc(name) + '</div>' +
                            '<div class="t-preview">' + esc(preview) + '</div>' +
                        '</div>' +
                        '<div class="t-time">' + timeAgo(Date.now() - lastAt.getTime()) + '</div>' +
                        (unread>0 ? '<div class="t-badge">' + (unread>99?'99+':unread) + '</div>' : '') +
                    '</div>';
                });
                body.innerHTML = html;
                setFabBadge(totalUnread);
            }, function(err) {
                body.innerHTML = '<div class="chat-empty"><i class="fas fa-exclamation-triangle" style="color:#dc2626"></i>' +
                    '<div class="title">Lỗi</div><div class="desc">' + esc(err.message) + '</div></div>';
            });
    }

    /* ═════════════════════════════════════════════════════════
       ADMIN VIEW — Mở 1 thread
       ═════════════════════════════════════════════════════════ */
    function openAdminThread(email) {
        if (!isAdmin()) return;
        CHAT.adminCurrentEmail = email;
        var db = getDb();
        if (!db) return;

        var threadRef = db.collection('chat_threads').doc(email);

        // Header
        threadRef.get().then(function(doc) {
            var d = doc.exists ? doc.data() : {};
            var name = d.userName || email.split('@')[0];
            $id('chatHeaderInfo').innerHTML =
                '<div class="name">' + esc(name) + '</div>' +
                '<div class="status">' + esc(email) + '</div>';
        }).catch(function(){});

        $id('chatBack').classList.add('show');
        $id('chatClose').style.display = 'none';
        $id('chatQuickReplies').classList.remove('hidden');

        // Unsub list
        if (CHAT.adminListUnsub) { try { CHAT.adminListUnsub(); } catch(e){} CHAT.adminListUnsub = null; }

        // Listen messages
        if (CHAT.adminOpenUnsub) { try { CHAT.adminOpenUnsub(); } catch(e){} }
        CHAT.adminOpenUnsub = threadRef.collection('messages')
            .orderBy('createdAt', 'desc').limit(50)
            .onSnapshot(function(snap) {
                renderAdminMessages(snap);
                // Mark read
                threadRef.update({ unreadByAdmin: 0 }).catch(function(){});
            }, function(err) {
                $id('chatBody').innerHTML =
                    '<div class="chat-empty"><i class="fas fa-exclamation-triangle"></i>' +
                    '<div class="title">Lỗi</div><div class="desc">' + esc(err.message) + '</div></div>';
            });
    }
    function renderAdminMessages(snap) {
        var body = $id('chatBody');
        if (snap.empty) {
            body.innerHTML = '<div class="chat-empty"><i class="fas fa-comments"></i>' +
                '<div class="title">Chưa có tin nhắn</div>' +
                '<div class="desc">Gửi tin nhắn chào user để bắt đầu.</div></div>';
            return;
        }
        var docs = [];
        snap.forEach(function(d){ docs.push(d); });
        docs.reverse();

        var html = '', lastDate = null;
        docs.forEach(function(doc) {
            var d = doc.data();
            var created = d.createdAt ? d.createdAt.toDate() : new Date();
            var dateStr = created.toLocaleDateString('vi-VN');
            if (dateStr !== lastDate) {
                html += '<div class="chat-system">' + dateStr + '</div>';
                lastDate = dateStr;
            }
            var time = created.toLocaleTimeString('vi-VN', {hour:'2-digit',minute:'2-digit'});
            var isAdminMsg = (d.from === 'admin');
            // Đảo ngược: tin admin hiển thị bên PHẢI giống user gửi
            html += '<div class="chat-msg ' + (isAdminMsg?'from-user':'from-admin') + '">' +
                '<div class="bubble">' + esc(d.text||'').replace(/\n/g,'<br>') + '</div>' +
                '<span class="msg-time">' + time + '</span>' +
            '</div>';
        });
        body.innerHTML = html;
        var nearBottom = body.scrollHeight - body.scrollTop - body.clientHeight < 150;
        if (nearBottom) setTimeout(function(){ body.scrollTop = body.scrollHeight; }, 30);
    }

    /* ═════════════════════════════════════════════════════════
       SEND
       ═════════════════════════════════════════════════════════ */
    function sendMessage() {
        var input = $id('chatInput');
        var text = input.value.trim();
        if (!text) return;

        var u = getCu(), db = getDb();
        if (!u || !db) return;

        var targetEmail, from;
        if (CHAT.adminCurrentEmail) {
            targetEmail = CHAT.adminCurrentEmail;
            from = 'admin';
        } else if (!isAdmin()) {
            targetEmail = u.email;
            from = 'user';
        } else {
            // Admin ở list view không có target → không gửi
            return;
        }

        var btn = $id('chatSendBtn');
        btn.disabled = true;
        input.value = '';
        autoResize();

        var threadRef = db.collection('chat_threads').doc(targetEmail);
        var msgData = {
            from: from,
            fromEmail: u.email,
            fromName: u.name || 'User',
            text: text,
            read: false,
            createdAt: firebase.firestore.FieldValue.serverTimestamp()
        };
        var threadUpdate = {
            lastMessage: text.substring(0, 100),
            lastMessageAt: firebase.firestore.FieldValue.serverTimestamp(),
            lastMessageFrom: from
        };
        if (from === 'user') {
            threadUpdate.unreadByAdmin = firebase.firestore.FieldValue.increment(1);
            threadUpdate.unreadByUser = 0;
        } else {
            threadUpdate.unreadByUser = firebase.firestore.FieldValue.increment(1);
            threadUpdate.unreadByAdmin = 0;
        }

        threadRef.collection('messages').add(msgData)
            .then(function() { return threadRef.set(threadUpdate, { merge: true }); })
            .catch(function(err) {
                alert('❌ Lỗi gửi tin: ' + err.message);
            })
            .finally(function() {
                btn.disabled = !input.value.trim();
            });
    }
    function autoResize() {
        var inp = $id('chatInput');
        if (!inp) return;
        inp.style.height = 'auto';
        inp.style.height = Math.min(inp.scrollHeight, 130) + 'px';
    }

    /* ═════════════════════════════════════════════════════════
       INIT
       ═════════════════════════════════════════════════════════ */
    function init() {
        if (CHAT.inited) return;
        CHAT.inited = true;

        // FAB click
        var fab = $id('chatFab');
        if (fab) fab.addEventListener('click', openChat);

        // Close
        var closeBtn = $id('chatClose');
        if (closeBtn) closeBtn.addEventListener('click', closeChat);

        // Back (admin thread → list)
        var backBtn = $id('chatBack');
        if (backBtn) backBtn.addEventListener('click', function() {
            if (CHAT.adminOpenUnsub) { try { CHAT.adminOpenUnsub(); } catch(e){} CHAT.adminOpenUnsub = null; }
            CHAT.adminCurrentEmail = null;
            openAdminListView();
        });

        // Click overlay để đóng
        var modal = $id('chatModal');
        if (modal) modal.addEventListener('click', function(e) {
            if (e.target === this) closeChat();
        });

        // ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && CHAT.isOpen) closeChat();
        });

        // Input
        var input = $id('chatInput');
        if (input) {
            input.addEventListener('input', function() {
                autoResize();
                $id('chatSendBtn').disabled = !this.value.trim();
            });
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    if (!this.value.trim()) return;
                    sendMessage();
                }
            });
        }

        // Send button
        var sendBtn = $id('chatSendBtn');
        if (sendBtn) sendBtn.addEventListener('click', sendMessage);

        // Quick replies
        document.querySelectorAll('.chat-quick-btn').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var inp = $id('chatInput');
                inp.value = this.dataset.reply || this.textContent.trim();
                autoResize();
                $id('chatSendBtn').disabled = false;
                inp.focus();
            });
        });

        // Visibility → pause poll khi ẩn
        document.addEventListener('visibilitychange', function() {
            if (document.hidden) {
                stopBadgePoll();
            } else {
                if (getCu() && getCu().email) startBadgePoll();
            }
        });

        // Public API cho admin onclick
        window.__chatOpenThread = openAdminThread;
        window.__chatOpen = openChat;
        window.__chatRefreshBadge = startBadgePoll;
    }

    /* ═════════════════════════════════════════════════════════
       AUTO-START khi có user
       ═════════════════════════════════════════════════════════ */
    function watchAuth() {
        // Theo dõi currentUser thay đổi — dùng polling nhẹ vì Mã 1 không phát event
        var lastEmail = null;
        setInterval(function() {
            var u = getCu();
            var email = u ? u.email : null;
            if (email !== lastEmail) {
                lastEmail = email;
                updateFabVisibility();
                if (email) {
                    startBadgePoll();
                } else {
                    stopBadgePoll();
                    setFabBadge(0);
                    if (CHAT.isOpen) closeChat();
                }
            }
        }, 2000);
    }

    /* Khởi động sau khi DOM sẵn sàng */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            init();
            updateFabVisibility();
            watchAuth();
        });
    } else {
        init();
        updateFabVisibility();
        watchAuth();
    }
})();
"""
