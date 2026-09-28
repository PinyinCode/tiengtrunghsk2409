# -*- coding: utf-8 -*-
"""
Admin Chat Manager — Trình quản lý chat riêng cho admin.
- Hiển thị TOÀN BỘ user (kể cả chưa nhắn tin)
- Merge: users collection + chat_threads collection
- Filter: có tin nhắn / chưa có / có tin chưa đọc
- Search: tìm theo tên / email
- Click user → mở chat
"""


def build_admin_chat_css():
    return r"""
/* ═══════════════════════════════════════════════════════════════
   📋 ADMIN CHAT MANAGER — Trình quản lý chat cho admin
   ═══════════════════════════════════════════════════════════════ */
.acm-modal{
    position:fixed;inset:0;
    background:rgba(15,23,42,.75);
    backdrop-filter:blur(6px);
    z-index:5000;
    display:none;
    align-items:center;justify-content:center;
    padding:1rem;
    pointer-events:none;
}
.acm-modal.show{display:flex;pointer-events:auto;}

.acm-box{
    background:#fff;
    border-radius:20px;
    width:100%;
    max-width:960px;
    height:min(85vh, 800px);
    display:flex;flex-direction:column;overflow:hidden;
    box-shadow:0 30px 80px rgba(0,0,0,.4);
    animation:acmSlideIn .3s cubic-bezier(.34,1.56,.64,1);
}
@keyframes acmSlideIn{
    from{opacity:0;transform:scale(.9) translateY(30px);}
    to{opacity:1;transform:scale(1) translateY(0);}
}
[data-theme="dark"] .acm-box{
    background:#1e293b;
    box-shadow:0 30px 80px rgba(0,0,0,.8);
}

/* ─── HEADER ─── */
.acm-header{
    padding:1rem 1.25rem;
    background:linear-gradient(135deg,#4f46e5,#7c3aed);
    color:#fff;
    display:flex;align-items:center;gap:1rem;
    flex-shrink:0;
}
.acm-header h3{
    font-size:1.05rem;font-weight:800;
    margin:0;flex:1;
    display:flex;align-items:center;gap:.5rem;
}
.acm-header h3 i{font-size:1.2rem;}
.acm-close{
    width:36px;height:36px;border-radius:50%;
    border:none;background:rgba(255,255,255,.2);
    color:#fff;cursor:pointer;
    display:flex;align-items:center;justify-content:center;
    font-size:1rem;flex-shrink:0;transition:.15s;
}
.acm-close:hover{background:rgba(255,255,255,.35);transform:scale(1.05);}

/* ─── STATS BAR ─── */
.acm-stats{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(120px,1fr));
    gap:.5rem;
    padding:.75rem 1.25rem;
    background:#f8fafc;
    border-bottom:1px solid #e2e8f0;
    flex-shrink:0;
}
[data-theme="dark"] .acm-stats{background:#0f172a;border-color:#334155;}
.acm-stat{
    padding:.5rem .75rem;
    background:#fff;
    border-radius:10px;
    border:1px solid #e2e8f0;
    text-align:center;
    transition:.15s;
    cursor:pointer;
}
[data-theme="dark"] .acm-stat{background:#1e293b;border-color:#334155;}
.acm-stat:hover{border-color:#4f46e5;transform:translateY(-2px);box-shadow:0 4px 12px rgba(79,70,229,.15);}
.acm-stat.active{background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;border-color:transparent;}
.acm-stat .acm-stat-value{
    font-size:1.35rem;font-weight:900;line-height:1;
    color:#4f46e5;display:block;margin-bottom:.15rem;
}
.acm-stat.active .acm-stat-value{color:#fff;}
.acm-stat .acm-stat-label{
    font-size:.65rem;text-transform:uppercase;
    letter-spacing:.4px;color:#64748b;font-weight:700;
}
.acm-stat.active .acm-stat-label{color:rgba(255,255,255,.9);}
[data-theme="dark"] .acm-stat .acm-stat-label{color:#94a3b8;}

/* ─── SEARCH BAR ─── */
.acm-search{
    padding:.75rem 1.25rem;
    background:#fff;
    border-bottom:1px solid #e2e8f0;
    flex-shrink:0;
    display:flex;gap:.5rem;align-items:center;
}
[data-theme="dark"] .acm-search{background:#1e293b;border-color:#334155;}
.acm-search-input{
    flex:1;min-width:0;
    padding:.55rem 1rem;
    border-radius:50px;
    border:1.5px solid #e2e8f0;
    background:#f8fafc;
    color:#0f172a;
    font-size:.85rem;font-family:inherit;outline:none;
    transition:.15s;
}
[data-theme="dark"] .acm-search-input{
    background:#0f172a;color:#f1f5f9;border-color:#334155;
}
.acm-search-input:focus{border-color:#4f46e5;box-shadow:0 0 0 3px rgba(79,70,229,.1);}
.acm-refresh-btn{
    width:40px;height:40px;border-radius:10px;
    border:none;background:#eff6ff;color:#4f46e5;
    cursor:pointer;display:flex;align-items:center;justify-content:center;
    font-size:.9rem;flex-shrink:0;transition:.15s;
}
.acm-refresh-btn:hover{background:#4f46e5;color:#fff;transform:rotate(180deg);}
.acm-refresh-btn.spinning{animation:acmSpin .6s linear infinite;}
@keyframes acmSpin{to{transform:rotate(360deg);}}

/* ─── LIST ─── */
.acm-list{
    flex:1;min-height:0;overflow-y:auto;
    padding:.75rem 1.25rem;
    background:#f8fafc;
}
[data-theme="dark"] .acm-list{background:#0f172a;}

.acm-user{
    display:flex;align-items:center;gap:.75rem;
    padding:.75rem .85rem;
    background:#fff;
    border:1px solid #e2e8f0;
    border-radius:12px;
    margin-bottom:.5rem;
    cursor:pointer;
    transition:.15s;
    position:relative;
}
[data-theme="dark"] .acm-user{background:#1e293b;border-color:#334155;}
.acm-user:hover{border-color:#4f46e5;box-shadow:0 2px 8px rgba(79,70,229,.15);transform:translateX(2px);}
.acm-user.has-unread{border-color:#dc2626;background:linear-gradient(90deg,rgba(220,38,38,.05),transparent);}
.acm-user.no-thread{opacity:.85;}

.acm-user-avatar{
    width:44px;height:44px;border-radius:50%;
    background:linear-gradient(135deg,#4f46e5,#7c3aed);
    color:#fff;
    display:flex;align-items:center;justify-content:center;
    font-weight:800;font-size:1rem;flex-shrink:0;
    position:relative;
}
.acm-user-avatar.online::after{
    content:'';position:absolute;bottom:0;right:0;
    width:12px;height:12px;border-radius:50%;
    background:#16a34a;border:2px solid #fff;
    animation:acmPulse 2s infinite;
}
[data-theme="dark"] .acm-user-avatar.online::after{border-color:#1e293b;}
@keyframes acmPulse{
    0%,100%{box-shadow:0 0 0 2px rgba(22,163,74,.3);}
    50%{box-shadow:0 0 0 5px rgba(22,163,74,.1);}
}
.acm-user-avatar.no-thread{
    background:linear-gradient(135deg,#94a3b8,#64748b);
}

.acm-user-info{flex:1;min-width:0;}
.acm-user-name{
    font-weight:800;font-size:.88rem;
    color:#0f172a;margin-bottom:.15rem;
    overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
    display:flex;align-items:center;gap:.35rem;
}
[data-theme="dark"] .acm-user-name{color:#f1f5f9;}
.acm-user-name .acm-tier{
    font-size:.55rem;font-weight:700;
    padding:.1rem .4rem;border-radius:50px;
    text-transform:uppercase;letter-spacing:.3px;
}
.acm-user-name .acm-tier.active{background:#dcfce7;color:#166534;}
.acm-user-name .acm-tier.trial{background:#fef3c7;color:#92400e;}
.acm-user-name .acm-tier.demo{background:#e0e7ff;color:#3730a3;}
.acm-user-name .acm-tier.admin{background:linear-gradient(135deg,#fbbf24,#f59e0b);color:#fff;}
.acm-user-name .acm-tier.expired{background:#fee2e2;color:#991b1b;}

.acm-user-email{
    font-size:.72rem;color:#64748b;
    overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
    margin-bottom:.1rem;
}
.acm-user-preview{
    font-size:.75rem;color:#94a3b8;
    overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
    font-style:italic;
}
.acm-user-preview b{color:#4f46e5;font-style:normal;font-weight:700;}
[data-theme="dark"] .acm-user-preview{color:#64748b;}

.acm-user-meta{
    display:flex;flex-direction:column;align-items:flex-end;
    gap:.3rem;flex-shrink:0;
}
.acm-user-time{
    font-size:.68rem;color:#94a3b8;white-space:nowrap;
}
.acm-user-badge{
    min-width:22px;height:22px;padding:0 .4rem;
    border-radius:50px;
    background:#dc2626;color:#fff;
    font-size:.65rem;font-weight:900;
    display:flex;align-items:center;justify-content:center;
    animation:acmBadgeBounce .8s infinite;
}
@keyframes acmBadgeBounce{
    0%,100%{transform:scale(1);}
    50%{transform:scale(1.15);}
}

/* ─── EMPTY ─── */
.acm-empty{
    display:flex;flex-direction:column;
    align-items:center;justify-content:center;
    padding:3rem 1.5rem;text-align:center;
    color:#94a3b8;gap:.75rem;
}
.acm-empty i{font-size:3rem;opacity:.3;}
.acm-empty .acm-empty-title{
    font-size:.95rem;font-weight:700;color:#475569;
}
[data-theme="dark"] .acm-empty .acm-empty-title{color:#cbd5e1;}
.acm-empty .acm-empty-desc{font-size:.8rem;max-width:300px;line-height:1.5;}

/* ─── LOADING ─── */
.acm-loading{
    display:flex;align-items:center;justify-content:center;
    padding:3rem;color:#94a3b8;gap:.5rem;
    font-size:.85rem;
}

/* ─── MOBILE ─── */
@media (max-width:768px){
    .acm-modal{padding:0;align-items:flex-end;}
    .acm-box{
        max-width:100%;
        height:92vh;
        border-radius:20px 20px 0 0;
        animation:acmSlideUp .3s cubic-bezier(.34,1.56,.64,1);
    }
    @keyframes acmSlideUp{
        from{transform:translateY(100%);}
        to{transform:translateY(0);}
    }
    .acm-stats{
        grid-template-columns:repeat(2,1fr);
        padding:.6rem .85rem;
    }
    .acm-list{padding:.6rem .85rem;}
    .acm-search{padding:.6rem .85rem;}
    .acm-user{padding:.65rem .7rem;}
    .acm-user-avatar{width:40px;height:40px;font-size:.9rem;}
    .acm-header{padding:.85rem 1rem;}
    .acm-header h3{font-size:.95rem;}
}

/* ─── FAB MỞ ADMIN CHAT MANAGER ─── */
.acm-fab{
    position:fixed;
    right:20px;
    bottom:calc(20px + env(safe-area-inset-bottom));
    z-index:9997;
    width:56px;height:56px;
    border-radius:50%;
    border:3px solid #fff;
    background:linear-gradient(135deg,#059669,#10b981);
    color:#fff;
    cursor:pointer;
    display:none;
    align-items:center;justify-content:center;
    font-size:1.3rem;
    box-shadow:0 8px 24px rgba(16,185,129,.5);
    transition:all .3s cubic-bezier(.34,1.56,.64,1);
}
.acm-fab.show{display:flex;}
.acm-fab:hover{transform:scale(1.1) rotate(-8deg);box-shadow:0 12px 32px rgba(16,185,129,.7);}
.acm-fab .acm-fab-badge{
    position:absolute;top:-6px;right:-6px;
    min-width:22px;height:22px;padding:0 .35rem;
    border-radius:50px;
    background:#dc2626;color:#fff;
    font-size:.65rem;font-weight:900;
    display:none;align-items:center;justify-content:center;
    border:2px solid #fff;
    animation:acmBadgeBounce .8s infinite;
}
.acm-fab .acm-fab-badge.show{display:flex;}

@media (max-width:768px){
    .acm-fab{
        width:48px;height:48px;
        right:12px;
        bottom:calc(12px + env(safe-area-inset-bottom));
        font-size:1.1rem;
    }
}
"""


def build_admin_chat_html():
    return r"""
<!-- ═══════════════════════════════════════════════════════════════
     📋 ADMIN CHAT MANAGER — Trình quản lý chat riêng cho admin
     ═══════════════════════════════════════════════════════════════ -->
<div class="acm-modal" id="acmModal">
    <div class="acm-box">

        <div class="acm-header">
            <h3><i class="fas fa-users-cog"></i> Quản lý Chat — Tất cả User</h3>
            <button class="acm-close" id="acmClose" type="button" title="Đóng">
                <i class="fas fa-times"></i>
            </button>
        </div>

        <div class="acm-stats" id="acmStats">
            <div class="acm-stat active" data-filter="all" id="acmStatAll">
                <span class="acm-stat-value" id="acmCountAll">0</span>
                <span class="acm-stat-label">Tất cả</span>
            </div>
            <div class="acm-stat" data-filter="unread" id="acmStatUnread">
                <span class="acm-stat-value" id="acmCountUnread">0</span>
                <span class="acm-stat-label">Chưa đọc</span>
            </div>
            <div class="acm-stat" data-filter="has-thread" id="acmStatHasThread">
                <span class="acm-stat-value" id="acmCountHasThread">0</span>
                <span class="acm-stat-label">Có tin nhắn</span>
            </div>
            <div class="acm-stat" data-filter="no-thread" id="acmStatNoThread">
                <span class="acm-stat-value" id="acmCountNoThread">0</span>
                <span class="acm-stat-label">Chưa nhắn</span>
            </div>
        </div>

        <div class="acm-search">
            <input type="text" class="acm-search-input" id="acmSearchInput"
                   placeholder="🔍 Tìm theo tên hoặc email..." autocomplete="off">
            <button class="acm-refresh-btn" id="acmRefreshBtn" type="button" title="Làm mới">
                <i class="fas fa-sync-alt"></i>
            </button>
        </div>

        <div class="acm-list" id="acmList">
            <div class="acm-loading">
                <i class="fas fa-spinner fa-pulse"></i>
                <span>Đang tải danh sách user...</span>
            </div>
        </div>

    </div>
</div>

<!-- FAB mở Admin Chat Manager (chỉ admin thấy) -->
<button class="acm-fab" id="acmFab" type="button" title="Quản lý Chat (Admin)">
    <i class="fas fa-users-cog"></i>
    <span class="acm-fab-badge" id="acmFabBadge">0</span>
</button>
"""


def build_admin_chat_js():
    return r"""
/* ═══════════════════════════════════════════════════════════════
   📋 ADMIN CHAT MANAGER — Trình quản lý chat cho admin
   Hiển thị TOÀN BỘ user (merge users + chat_threads)
   ═══════════════════════════════════════════════════════════════ */
(function() {
    'use strict';

    var ACM = {
        inited: false,
        isOpen: false,
        usersUnsub: null,
        threadsUnsub: null,
        allUsers: [],          // merge kết quả
        usersMap: {},          // { email: userData }
        threadsMap: {},        // { email: threadData }
        filter: 'all',         // all | unread | has-thread | no-thread
        searchTerm: '',
        renderTimer: null
    };

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
    function getDb() { return window.db || null; }
    function getCu() { return window.currentUser || null; }
    function isAdmin() { var u = getCu(); return u && u.role === 'admin'; }

    function timeAgo(ms) {
        if (ms < 60000) return 'Vừa xong';
        if (ms < 3600000) return Math.floor(ms/60000) + 'p';
        if (ms < 86400000) return Math.floor(ms/3600000) + 'h';
        if (ms < 2592000000) return Math.floor(ms/86400000) + 'd';
        return Math.floor(ms/2592000000) + 'th';
    }

    function getTierClass(tier) {
        tier = (tier || 'demo').toLowerCase();
        if (tier === 'active' || tier === 'premium') return 'active';
        if (tier === 'trial') return 'trial';
        if (tier === 'admin' || tier === 'super_admin') return 'admin';
        if (tier === 'expired') return 'expired';
        return 'demo';
    }
    function getTierLabel(tier) {
        tier = (tier || 'demo').toLowerCase();
        if (tier === 'super_admin') return 'ADMIN';
        if (tier === 'admin') return 'ADMIN';
        if (tier === 'active' || tier === 'premium') return 'ACTIVE';
        if (tier === 'trial') return 'TRIAL';
        if (tier === 'expired') return 'HẾT HẠN';
        return 'DEMO';
    }

    /* ═══════════════════════════════════════════════════════════
       ⭐ MERGE DATA: users collection + chat_threads collection
       ═══════════════════════════════════════════════════════════ */
    function rebuildList() {
        var map = {};   // { email: {...merged} }

        // 1. Từ users collection
        Object.keys(ACM.usersMap).forEach(function(email) {
            var u = ACM.usersMap[email];
            map[email] = {
                email: email,
                name: u.name || u.displayName || email.split('@')[0],
                role: u.role || 'user',
                tier: u.tier || u.plan || 'demo',
                thread: null,
                unread: 0,
                lastMessage: '',
                lastMessageAt: 0,
                lastMessageFrom: ''
            };
        });

        // 2. Merge với chat_threads
        Object.keys(ACM.threadsMap).forEach(function(email) {
            var t = ACM.threadsMap[email];
            if (!map[email]) {
                // User có thread nhưng chưa có trong users collection
                map[email] = {
                    email: email,
                    name: t.userName || email.split('@')[0],
                    role: 'user',
                    tier: 'demo',
                    thread: t,
                    unread: 0,
                    lastMessage: '',
                    lastMessageAt: 0,
                    lastMessageFrom: ''
                };
            }
            map[email].thread = t;
            map[email].unread = t.unreadByAdmin || 0;
            map[email].lastMessage = t.lastMessage || '';
            map[email].lastMessageAt = t.lastMessageAt
                ? (t.lastMessageAt.toMillis ? t.lastMessageAt.toMillis() : 0)
                : 0;
            map[email].lastMessageFrom = t.lastMessageFrom || '';
            if (t.userName && !map[email].name) map[email].name = t.userName;
        });

        // 3. Convert to array
        ACM.allUsers = Object.keys(map).map(function(k) { return map[k]; });

        // 4. Sort: unread trước, rồi tới có tin nhắn gần đây, rồi alphabet
        ACM.allUsers.sort(function(a, b) {
            if (a.unread > 0 && b.unread === 0) return -1;
            if (a.unread === 0 && b.unread > 0) return 1;
            if (a.lastMessageAt > 0 && b.lastMessageAt === 0) return -1;
            if (a.lastMessageAt === 0 && b.lastMessageAt > 0) return 1;
            if (a.lastMessageAt !== b.lastMessageAt) return b.lastMessageAt - a.lastMessageAt;
            return (a.name || '').localeCompare(b.name || '');
        });

        // 5. Update stats
        updateStats();

        // 6. Render
        scheduleRender();
    }

    function updateStats() {
        var all = ACM.allUsers.length;
        var unread = 0, hasThread = 0, noThread = 0;
        ACM.allUsers.forEach(function(u) {
            if (u.unread > 0) unread++;
            if (u.thread) hasThread++;
            else noThread++;
        });
        var el;
        if ((el = $id('acmCountAll'))) el.textContent = all;
        if ((el = $id('acmCountUnread'))) el.textContent = unread;
        if ((el = $id('acmCountHasThread'))) el.textContent = hasThread;
        if ((el = $id('acmCountNoThread'))) el.textContent = noThread;

        // FAB badge
        var fabBadge = $id('acmFabBadge');
        if (fabBadge) {
            if (unread > 0) {
                fabBadge.textContent = unread > 99 ? '99+' : unread;
                fabBadge.classList.add('show');
            } else {
                fabBadge.classList.remove('show');
            }
        }
    }

    function scheduleRender() {
        if (ACM.renderTimer) clearTimeout(ACM.renderTimer);
        ACM.renderTimer = setTimeout(renderList, 100);
    }

    /* ═══════════════════════════════════════════════════════════
       🎨 RENDER LIST
       ═══════════════════════════════════════════════════════════ */
    function renderList() {
        var el = $id('acmList');
        if (!el) return;

        // Filter
        var list = ACM.allUsers.filter(function(u) {
            // Filter by tab
            if (ACM.filter === 'unread' && u.unread === 0) return false;
            if (ACM.filter === 'has-thread' && !u.thread) return false;
            if (ACM.filter === 'no-thread' && u.thread) return false;

            // Search
            if (ACM.searchTerm) {
                var s = ACM.searchTerm.toLowerCase();
                var name = (u.name || '').toLowerCase();
                var email = (u.email || '').toLowerCase();
                if (name.indexOf(s) < 0 && email.indexOf(s) < 0) return false;
            }
            return true;
        });

        if (list.length === 0) {
            var emptyMsg = 'Chưa có user nào';
            if (ACM.searchTerm) emptyMsg = 'Không tìm thấy user phù hợp';
            else if (ACM.filter === 'unread') emptyMsg = 'Không có tin chưa đọc';
            else if (ACM.filter === 'has-thread') emptyMsg = 'Chưa có user nào nhắn tin';
            else if (ACM.filter === 'no-thread') emptyMsg = 'Tất cả user đều đã nhắn';

            el.innerHTML =
                '<div class="acm-empty">' +
                    '<i class="fas fa-inbox"></i>' +
                    '<div class="acm-empty-title">' + emptyMsg + '</div>' +
                    '<div class="acm-empty-desc">' +
                        (ACM.filter === 'no-thread'
                            ? 'Bấm "Tất cả" để xem toàn bộ user có thể chat'
                            : 'Thử đổi bộ lọc hoặc xóa từ khóa tìm kiếm') +
                    '</div>' +
                '</div>';
            return;
        }

        var html = '';
        list.forEach(function(u) {
            var hasUnread = u.unread > 0;
            var hasThread = !!u.thread;
            var initial = (u.name || u.email || '?').charAt(0).toUpperCase();
            var tierClass = getTierClass(u.role === 'admin' ? 'admin' : u.tier);
            var tierLabel = getTierLabel(u.role === 'admin' ? 'admin' : u.tier);
            var isMe = (getCu() && getCu().email === u.email);

            var preview = '';
            if (hasThread && u.lastMessage) {
                var prefix = (u.lastMessageFrom === 'admin') ? '<b>Bạn:</b> ' : '';
                preview = prefix + esc(u.lastMessage);
            } else if (hasThread) {
                preview = '<i>(chưa có tin nhắn)</i>';
            } else {
                preview = '<i>Chưa nhắn tin</i>';
            }

            var timeText = u.lastMessageAt > 0
                ? timeAgo(Date.now() - u.lastMessageAt)
                : '';

            html += '<div class="acm-user' +
                        (hasUnread ? ' has-unread' : '') +
                        (hasThread ? '' : ' no-thread') +
                    '" onclick="window.__acmOpenThread(\'' + jsStr(u.email) + '\')">' +
                '<div class="acm-user-avatar ' + (hasThread ? '' : 'no-thread') + '">' +
                    esc(initial) +
                '</div>' +
                '<div class="acm-user-info">' +
                    '<div class="acm-user-name">' +
                        esc(u.name) +
                        (isMe ? ' <span style="font-size:.6rem;color:#94a3b8;">(bạn)</span>' : '') +
                        ' <span class="acm-tier ' + tierClass + '">' + tierLabel + '</span>' +
                    '</div>' +
                    '<div class="acm-user-email">' + esc(u.email) + '</div>' +
                    '<div class="acm-user-preview">' + preview + '</div>' +
                '</div>' +
                '<div class="acm-user-meta">' +
                    (timeText ? '<span class="acm-user-time">' + timeText + '</span>' : '') +
                    (hasUnread ? '<span class="acm-user-badge">' +
                        (u.unread > 99 ? '99+' : u.unread) + '</span>' : '') +
                '</div>' +
            '</div>';
        });

        el.innerHTML = html;
    }

    /* ═══════════════════════════════════════════════════════════
       🔌 WATCHERS — onSnapshot cả users và chat_threads
       ═══════════════════════════════════════════════════════════ */
 function startWatchers() {
        stopWatchers();
        var db = getDb();
        if (!db || !isAdmin()) return;

        // ═══════════════════════════════════════════════════════════
        // 1. Watch allowed_users collection (toàn bộ user đăng ký)
        // ═══════════════════════════════════════════════════════════
        ACM.usersUnsub = db.collection('allowed_users')
            .onSnapshot(function(snap) {
                ACM.usersMap = {};
                snap.forEach(function(doc) {
                    var d = doc.data() || {};
                    var email = doc.id;   // allowed_users dùng email làm doc ID
                    if (email) {
                        // ⭐ Tính tier chính xác từ allowed_users data
                        var tier = 'demo';
                        if (d.role === 'admin') {
                            tier = 'admin';
                        } else if (d.isPermanent) {
                            tier = 'active';
                        } else if (d.expiresAt) {
                            var expTime = d.expiresAt.toMillis
                                ? d.expiresAt.toMillis()
                                : 0;
                            tier = expTime > Date.now() ? 'active' : 'expired';
                        } else if (d.tier) {
                            tier = d.tier;
                        }

                        ACM.usersMap[email] = {
                            email: email,
                            name: d.name || d.displayName || email.split('@')[0],
                            role: d.role || 'user',
                            tier: tier
                        };
                    }
                });
                console.log('✅ ACM: Loaded', Object.keys(ACM.usersMap).length, 'users');
                rebuildList();
            }, function(err) {
                console.error('ACM users watch error:', err);
            });

        // ═══════════════════════════════════════════════════════════
        // 2. Watch chat_threads collection
        // ═══════════════════════════════════════════════════════════
        ACM.threadsUnsub = db.collection('chat_threads')
            .onSnapshot(function(snap) {
                ACM.threadsMap = {};
                snap.forEach(function(doc) {
                    var d = doc.data() || {};
                    var email = d.userEmail || doc.id;
                    if (email) {
                        ACM.threadsMap[email] = {
                            userEmail: email,
                            userName: d.userName || email.split('@')[0],
                            lastMessage: d.lastMessage || '',
                            lastMessageAt: d.lastMessageAt,
                            lastMessageFrom: d.lastMessageFrom || '',
                            unreadByAdmin: d.unreadByAdmin || 0
                        };
                    }
                });
                console.log('✅ ACM: Loaded', Object.keys(ACM.threadsMap).length, 'threads');
                rebuildList();
            }, function(err) {
                console.error('ACM threads watch error:', err);
            });
    }
    function stopWatchers() {
        if (ACM.usersUnsub) { try { ACM.usersUnsub(); } catch(e){} ACM.usersUnsub = null; }
        if (ACM.threadsUnsub) { try { ACM.threadsUnsub(); } catch(e){} ACM.threadsUnsub = null; }
    }

    /* ═══════════════════════════════════════════════════════════
       🪟 OPEN / CLOSE
       ═══════════════════════════════════════════════════════════ */
    function openModal() {
        if (!isAdmin()) return;
        ACM.isOpen = true;
        $id('acmModal').classList.add('show');
        document.body.style.overflow = 'hidden';
        if (!ACM.usersUnsub && !ACM.threadsUnsub) {
            startWatchers();
        }
    }

    function closeModal() {
        ACM.isOpen = false;
        $id('acmModal').classList.remove('show');
        document.body.style.overflow = '';
        // Không stop watchers — để badge FAB vẫn cập nhật realtime
    }

    /* ═══════════════════════════════════════════════════════════
       🔗 MỞ CHAT VỚI USER (gọi hàm có sẵn trong chat_support)
       ═══════════════════════════════════════════════════════════ */
    window.__acmOpenThread = function(email) {
        closeModal();
        // Đợi modal đóng xong
        setTimeout(function() {
            if (typeof window.__chatOpen === 'function') {
                // Đảm bảo chat modal mở
                if (!document.getElementById('chatModal').classList.contains('show')) {
                    window.__chatOpen();
                }
            }
            // Đợi chat mở xong → mở thread
            setTimeout(function() {
                if (typeof window.__chatOpenThread === 'function') {
                    window.__chatOpenThread(email);
                }
            }, 400);
        }, 200);
    };
    /* ═══════════════════════════════════════════════════════════
       🚀 INIT
       ═══════════════════════════════════════════════════════════ */
    function init() {
        if (ACM.inited) return;
        ACM.inited = true;

        // Nút đóng
        var closeBtn = $id('acmClose');
        if (closeBtn) closeBtn.addEventListener('click', closeModal);

        // Click backdrop để đóng
        var modal = $id('acmModal');
        if (modal) modal.addEventListener('click', function(e) {
            if (e.target === this) closeModal();
        });

        // Phím Esc để đóng
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && ACM.isOpen) closeModal();
        });

        // FAB mở modal
        var fab = $id('acmFab');
        if (fab) fab.addEventListener('click', openModal);

        // Search input
        var searchInput = $id('acmSearchInput');
        if (searchInput) {
            var debounce;
            searchInput.addEventListener('input', function() {
                clearTimeout(debounce);
                var val = this.value;
                debounce = setTimeout(function() {
                    ACM.searchTerm = val.trim();
                    scheduleRender();
                }, 200);
            });
        }

        // Refresh button
        var refreshBtn = $id('acmRefreshBtn');
        if (refreshBtn) refreshBtn.addEventListener('click', function() {
            this.classList.add('spinning');
            var self = this;
            startWatchers();
            setTimeout(function() { self.classList.remove('spinning'); }, 800);
        });

        // Filter tabs
        document.querySelectorAll('.acm-stat').forEach(function(tab) {
            tab.addEventListener('click', function() {
                document.querySelectorAll('.acm-stat').forEach(function(t) {
                    t.classList.remove('active');
                });
                this.classList.add('active');
                ACM.filter = this.getAttribute('data-filter');
                scheduleRender();
            });
        });

        console.log('✅ Admin Chat Manager: init');
    }

    // Watch auth → show/hide FAB
    var _lastRole = null;
    setInterval(function() {
        var u = getCu();
        var role = u ? (u.role || 'user') : null;
        if (role === _lastRole) return;
        _lastRole = role;

        var fab = $id('acmFab');
        if (!fab) return;

        if (role === 'admin') {
            fab.classList.add('show');
            // Tự động start watchers để cập nhật badge
            if (!ACM.usersUnsub && !ACM.threadsUnsub) {
                startWatchers();
            }
        } else {
            fab.classList.remove('show');
            stopWatchers();
            if (ACM.isOpen) closeModal();
        }
    }, 2000);

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
"""
