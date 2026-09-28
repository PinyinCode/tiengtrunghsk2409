# -*- coding: utf-8 -*-
"""
Admin Chat Manager — Trình quản lý chat riêng cho admin.
- Hiển thị TOÀN BỘ user (kể cả chưa nhắn tin)
- Merge: allowed_users + chat_threads
- Filter: Tất cả / Online / Chưa đọc / Có tin nhắn / Chưa nhắn
- Search: tìm theo tên / email
- Click user → xem lịch sử hoạt động HOẶC chat
- ⭐ MỚI: Xem lịch sử hoạt động của user (login, chat, renewal, ...)
- ⭐ MỚI: Hiển thị thời gian hoạt động gần nhất (từ login_logs)
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
.acm-header-back{
    width:36px;height:36px;border-radius:50%;
    border:none;background:rgba(255,255,255,.2);
    color:#fff;cursor:pointer;
    display:none;align-items:center;justify-content:center;
    font-size:1rem;flex-shrink:0;transition:.15s;
}
.acm-header-back.show{display:flex;}
.acm-header-back:hover{background:rgba(255,255,255,.35);transform:scale(1.05);}
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
.acm-stat[data-filter="online"] .acm-stat-value{color:#16a34a;}
.acm-stat[data-filter="online"].active{background:linear-gradient(135deg,#16a34a,#22c55e);}
.acm-stat[data-filter="online"].active .acm-stat-value{color:#fff;}

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

/* ⭐ Thời gian hoạt động — Online / Recent login */
.acm-user-time.online-now{
    color:#16a34a;
    font-weight:800;
    animation:acmOnlinePulse 2s ease-in-out infinite;
}
@keyframes acmOnlinePulse{
    0%,100%{opacity:1;}
    50%{opacity:.6;}
}
.acm-user-time.recent-login{
    color:#4f46e5;
    font-weight:700;
}
[data-theme="dark"] .acm-user-time.online-now{color:#22c55e;}
[data-theme="dark"] .acm-user-time.recent-login{color:#a5b4fc;}

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

/* ⭐ Actions cho mỗi user (chat + history) */
.acm-user-actions{
    display:flex;gap:.3rem;flex-shrink:0;margin-left:.5rem;
}
.acm-user-btn{
    width:32px;height:32px;border-radius:8px;
    border:none;cursor:pointer;
    display:flex;align-items:center;justify-content:center;
    font-size:.8rem;transition:.15s;
    background:#f1f5f9;color:#64748b;
}
.acm-user-btn:hover{transform:scale(1.1);}
.acm-user-btn.chat{background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;}
.acm-user-btn.chat:hover{box-shadow:0 4px 12px rgba(79,70,229,.4);}
.acm-user-btn.history{background:#eff6ff;color:#4f46e5;}
.acm-user-btn.history:hover{background:#4f46e5;color:#fff;box-shadow:0 4px 12px rgba(79,70,229,.4);}

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

/* ═══════════════════════════════════════════════════════════════
   📜 HISTORY VIEW — Lịch sử hoạt động của user
   ═══════════════════════════════════════════════════════════════ */
.acm-history{
    display:none;
    flex:1;min-height:0;overflow-y:auto;
    padding:1rem 1.25rem;
    background:#f8fafc;
}
.acm-history.show{display:block;}
[data-theme="dark"] .acm-history{background:#0f172a;}

/* Header của user trong history */
.acm-hist-header{
    display:flex;align-items:center;gap:1rem;
    padding:1rem;
    background:#fff;
    border-radius:12px;
    margin-bottom:1rem;
    border:1px solid #e2e8f0;
}
[data-theme="dark"] .acm-hist-header{background:#1e293b;border-color:#334155;}
.acm-hist-avatar{
    width:60px;height:60px;border-radius:50%;
    background:linear-gradient(135deg,#4f46e5,#7c3aed);
    color:#fff;
    display:flex;align-items:center;justify-content:center;
    font-weight:900;font-size:1.5rem;flex-shrink:0;
    position:relative;
}
.acm-hist-info{flex:1;min-width:0;}
.acm-hist-name{
    font-size:1.1rem;font-weight:900;
    color:#0f172a;margin-bottom:.2rem;
    display:flex;align-items:center;gap:.4rem;
    flex-wrap:wrap;
}
[data-theme="dark"] .acm-hist-name{color:#f1f5f9;}
.acm-hist-email{
    font-size:.8rem;color:#64748b;margin-bottom:.3rem;
}
.acm-hist-meta{
    font-size:.7rem;color:#94a3b8;
    display:flex;flex-wrap:wrap;gap:.75rem;
}

/* ── Filter tabs history ── */
.acm-hist-filters{
    display:flex;gap:.4rem;flex-wrap:wrap;
    margin-bottom:1rem;
}
.acm-hist-filter{
    padding:.35rem .85rem;
    border-radius:50px;
    border:1.5px solid #e2e8f0;
    background:#fff;color:#64748b;
    font-size:.75rem;font-weight:700;
    cursor:pointer;transition:.15s;
    font-family:inherit;
    display:inline-flex;align-items:center;gap:.3rem;
}
[data-theme="dark"] .acm-hist-filter{background:#1e293b;border-color:#334155;color:#94a3b8;}
.acm-hist-filter:hover{border-color:#4f46e5;color:#4f46e5;}
.acm-hist-filter.active{background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;border-color:transparent;}

/* ── Timeline ── */
.acm-timeline{
    position:relative;
    padding-left:2rem;
}
.acm-timeline::before{
    content:'';
    position:absolute;
    left:8px;top:0;bottom:0;
    width:2px;
    background:linear-gradient(180deg,#4f46e5,#7c3aed,#a855f7);
    opacity:.3;
}

.acm-tl-item{
    position:relative;
    margin-bottom:1rem;
    padding:.75rem 1rem;
    background:#fff;
    border-radius:10px;
    border-left:3px solid #4f46e5;
    transition:.15s;
}
[data-theme="dark"] .acm-tl-item{background:#1e293b;border-color:#4f46e5;}
.acm-tl-item:hover{box-shadow:0 4px 12px rgba(79,70,229,.1);transform:translateX(2px);}

/* Chấm tròn trên timeline */
.acm-tl-item::before{
    content:'';
    position:absolute;
    left:-1.65rem;top:1rem;
    width:12px;height:12px;border-radius:50%;
    background:#4f46e5;
    border:2px solid #fff;
    box-shadow:0 0 0 3px rgba(79,70,229,.15);
}
[data-theme="dark"] .acm-tl-item::before{border-color:#1e293b;}

/* Màu theo type */
.acm-tl-item[data-type="login"]{border-left-color:#16a34a;}
.acm-tl-item[data-type="login"]::before{background:#16a34a;box-shadow:0 0 0 3px rgba(22,163,74,.15);}
.acm-tl-item[data-type="logout"]{border-left-color:#94a3b8;}
.acm-tl-item[data-type="logout"]::before{background:#94a3b8;box-shadow:0 0 0 3px rgba(148,163,184,.15);}
.acm-tl-item[data-type="chat"]{border-left-color:#4f46e5;}
.acm-tl-item[data-type="chat"]::before{background:#4f46e5;box-shadow:0 0 0 3px rgba(79,70,229,.15);}
.acm-tl-item[data-type="renewal"]{border-left-color:#f59e0b;}
.acm-tl-item[data-type="renewal"]::before{background:#f59e0b;box-shadow:0 0 0 3px rgba(245,158,11,.15);}
.acm-tl-item[data-type="favorite"]{border-left-color:#dc2626;}
.acm-tl-item[data-type="favorite"]::before{background:#dc2626;box-shadow:0 0 0 3px rgba(220,38,38,.15);}
.acm-tl-item[data-type="practice"]{border-left-color:#7c3aed;}
.acm-tl-item[data-type="practice"]::before{background:#7c3aed;box-shadow:0 0 0 3px rgba(124,58,237,.15);}
.acm-tl-item[data-type="admin"]{border-left-color:#0ea5e9;}
.acm-tl-item[data-type="admin"]::before{background:#0ea5e9;box-shadow:0 0 0 3px rgba(14,165,233,.15);}

.acm-tl-head{
    display:flex;align-items:center;
    justify-content:space-between;gap:.5rem;
    margin-bottom:.3rem;
}
.acm-tl-title{
    font-size:.85rem;font-weight:800;
    color:#0f172a;
    display:flex;align-items:center;gap:.35rem;
}
[data-theme="dark"] .acm-tl-title{color:#f1f5f9;}
.acm-tl-icon{
    width:20px;height:20px;border-radius:50%;
    background:#eff6ff;color:#4f46e5;
    display:flex;align-items:center;justify-content:center;
    font-size:.65rem;flex-shrink:0;
}
.acm-tl-item[data-type="login"] .acm-tl-icon{background:#dcfce7;color:#16a34a;}
.acm-tl-item[data-type="logout"] .acm-tl-icon{background:#f1f5f9;color:#64748b;}
.acm-tl-item[data-type="renewal"] .acm-tl-icon{background:#fef3c7;color:#d97706;}
.acm-tl-item[data-type="favorite"] .acm-tl-icon{background:#fee2e2;color:#dc2626;}
.acm-tl-item[data-type="practice"] .acm-tl-icon{background:#ede9fe;color:#7c3aed;}
.acm-tl-item[data-type="admin"] .acm-tl-icon{background:#e0f2fe;color:#0284c7;}

.acm-tl-time{
    font-size:.7rem;color:#94a3b8;
    white-space:nowrap;flex-shrink:0;
}
.acm-tl-body{
    font-size:.8rem;color:#475569;
    line-height:1.5;padding-left:1.6rem;
}
[data-theme="dark"] .acm-tl-body{color:#cbd5e1;}
.acm-tl-body b{color:#4f46e5;font-weight:700;}
.acm-tl-body code{
    background:#f1f5f9;color:#dc2626;
    padding:.1rem .35rem;border-radius:4px;
    font-size:.75rem;
}
[data-theme="dark"] .acm-tl-body code{background:#0f172a;color:#f87171;}

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
    .acm-user{padding:.65rem .7rem;flex-wrap:wrap;}
    .acm-user-avatar{width:40px;height:40px;font-size:.9rem;}
    .acm-header{padding:.85rem 1rem;}
    .acm-header h3{font-size:.95rem;}
    .acm-user-actions{width:100%;justify-content:flex-end;margin-top:.4rem;margin-left:0;}
    .acm-history{padding:.75rem;}
    .acm-hist-header{padding:.75rem;}
    .acm-hist-avatar{width:48px;height:48px;font-size:1.2rem;}
    .acm-timeline{padding-left:1.5rem;}
    .acm-tl-item{padding:.6rem .75rem;}
}

/* ─── FAB MỞ ADMIN CHAT MANAGER ─── */
.acm-fab{
    position:fixed;
    right:80px;
    bottom:calc(30px + env(safe-area-inset-bottom));
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
        right:70px;
        bottom:calc(16px + env(safe-area-inset-bottom));
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

        <!-- ═══ VIEW 1: DANH SÁCH USER ═══ -->
        <div class="acm-header" id="acmHeaderList">
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
            <div class="acm-stat" data-filter="online" id="acmStatOnline">
                <span class="acm-stat-value" id="acmCountOnline">0</span>
                <span class="acm-stat-label">Online</span>
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

        <div class="acm-search" id="acmSearchBar">
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

        <!-- ═══ VIEW 2: LỊCH SỬ HOẠT ĐỘNG ═══ -->
        <div class="acm-header" id="acmHeaderHistory" style="display:none;">
            <button class="acm-header-back show" id="acmHistoryBack" type="button" title="Quay lại">
                <i class="fas fa-arrow-left"></i>
            </button>
            <h3><i class="fas fa-history"></i> Lịch sử hoạt động</h3>
            <button class="acm-close" id="acmCloseHistory" type="button" title="Đóng">
                <i class="fas fa-times"></i>
            </button>
        </div>

        <div class="acm-history" id="acmHistory">
            <div class="acm-loading">
                <i class="fas fa-spinner fa-pulse"></i>
                <span>Đang tải lịch sử...</span>
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
   📋 ADMIN CHAT MANAGER — Trình quản lý chat + Lịch sử hoạt động
   ═══════════════════════════════════════════════════════════════ */
(function() {
    'use strict';

    var ACM = {
        inited: false,
        isOpen: false,
        view: 'list',           // 'list' | 'history'
        usersUnsub: null,
        threadsUnsub: null,
        presenceUnsub: null,    // RTDB presence
        historyUnsub: null,     // Firestore activity logs
        loginLogsUnsub: null,   // ⭐ MỚI: watch login_logs
        currentHistoryEmail: null,
        allUsers: [],
        usersMap: {},
        threadsMap: {},
        onlineMap: {},          // { email: true } — RTDB
        loginLogsMap: {},       // ⭐ MỚI: { email: timestamp } — login_logs
        activityMap: {},
        filter: 'all',
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
    function formatDateTime(ms) {
        if (!ms) return '';
        try {
            var d = new Date(ms);
            return d.toLocaleDateString('vi-VN') + ' ' +
                   d.toLocaleTimeString('vi-VN', {hour:'2-digit',minute:'2-digit'});
        } catch(e) { return ''; }
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
       MERGE DATA
       ═══════════════════════════════════════════════════════════ */
    function rebuildList() {
        var map = {};

        // 1. Từ allowed_users
        Object.keys(ACM.usersMap).forEach(function(email) {
            var u = ACM.usersMap[email];
            var emailLower = (email || '').toLowerCase();
            map[email] = {
                email: email,
                name: u.name || u.displayName || email.split('@')[0],
                role: u.role || 'user',
                tier: u.tier || u.plan || 'demo',
                thread: null,
                unread: 0,
                lastMessage: '',
                lastMessageAt: 0,
                lastMessageFrom: '',
                lastLoginAt: ACM.loginLogsMap[emailLower] || 0   // ⭐ MỚI
            };
        });

        // 2. Merge với chat_threads
        Object.keys(ACM.threadsMap).forEach(function(email) {
            var t = ACM.threadsMap[email];
            if (!map[email]) {
                map[email] = {
                    email: email,
                    name: t.userName || email.split('@')[0],
                    role: 'user',
                    tier: 'demo',
                    thread: t,
                    unread: 0,
                    lastMessage: '',
                    lastMessageAt: 0,
                    lastMessageFrom: '',
                    lastLoginAt: 0
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

            // ⭐ Fallback: nếu chưa có login log → dùng last message time
            if (!map[email].lastLoginAt && map[email].lastMessageAt) {
                map[email].lastLoginAt = map[email].lastMessageAt;
            }
        });

        // 3. Array
        ACM.allUsers = Object.keys(map).map(function(k) { return map[k]; });

        // 4. Sort: unread > online > login gần đây > có tin gần đây > alphabet
        ACM.allUsers.sort(function(a, b) {
            // Ưu tiên 1: unread
            if (a.unread > 0 && b.unread === 0) return -1;
            if (a.unread === 0 && b.unread > 0) return 1;

            // Ưu tiên 2: đang online (RTDB presence)
            var aOn = ACM.onlineMap[a.email] ? 1 : 0;
            var bOn = ACM.onlineMap[b.email] ? 1 : 0;
            if (aOn !== bOn) return bOn - aOn;

            // ⭐ Ưu tiên 3: login gần đây (login_logs)
            if (a.lastLoginAt !== b.lastLoginAt) {
                return b.lastLoginAt - a.lastLoginAt;
            }

            // Ưu tiên 4: có tin nhắn gần đây
            if (a.lastMessageAt > 0 && b.lastMessageAt === 0) return -1;
            if (a.lastMessageAt === 0 && b.lastMessageAt > 0) return 1;
            if (a.lastMessageAt !== b.lastMessageAt) return b.lastMessageAt - a.lastMessageAt;

            // Cuối: alphabet
            return (a.name || '').localeCompare(b.name || '');
        });

        // 5. Stats
        updateStats();

        // 6. Render
        scheduleRender();
    }

    function updateStats() {
        var all = ACM.allUsers.length;
        var unread = 0, hasThread = 0, noThread = 0, online = 0;
        ACM.allUsers.forEach(function(u) {
            if (u.unread > 0) unread++;
            if (u.thread) hasThread++;
            else noThread++;
            if (ACM.onlineMap[u.email]) online++;
        });
        var el;
        if ((el = $id('acmCountAll'))) el.textContent = all;
        if ((el = $id('acmCountOnline'))) el.textContent = online;
        if ((el = $id('acmCountUnread'))) el.textContent = unread;
        if ((el = $id('acmCountHasThread'))) el.textContent = hasThread;
        if ((el = $id('acmCountNoThread'))) el.textContent = noThread;

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

        var list = ACM.allUsers.filter(function(u) {
            if (ACM.filter === 'online' && !ACM.onlineMap[u.email]) return false;
            if (ACM.filter === 'unread' && u.unread === 0) return false;
            if (ACM.filter === 'has-thread' && !u.thread) return false;
            if (ACM.filter === 'no-thread' && u.thread) return false;

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
            else if (ACM.filter === 'online') emptyMsg = 'Không có user nào online';
            else if (ACM.filter === 'unread') emptyMsg = 'Không có tin chưa đọc';
            else if (ACM.filter === 'has-thread') emptyMsg = 'Chưa có user nào nhắn tin';
            else if (ACM.filter === 'no-thread') emptyMsg = 'Tất cả user đều đã nhắn';

            el.innerHTML =
                '<div class="acm-empty">' +
                    '<i class="fas fa-inbox"></i>' +
                    '<div class="acm-empty-title">' + emptyMsg + '</div>' +
                    '<div class="acm-empty-desc">Thử đổi bộ lọc hoặc xóa từ khóa tìm kiếm</div>' +
                '</div>';
            return;
        }

        var html = '';
        list.forEach(function(u) {
            var hasUnread = u.unread > 0;
            var hasThread = !!u.thread;
            var isOnline = !!ACM.onlineMap[u.email];
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

            // ⭐ Thời gian hoạt động gần nhất — Ưu tiên: Online > Login > Chat
            var timeText = '';
            var timeClass = '';
            if (isOnline) {
                timeText = '🟢 Online';
                timeClass = 'online-now';
            } else if (u.lastLoginAt > 0) {
                timeText = '🕐 ' + timeAgo(Date.now() - u.lastLoginAt);
                timeClass = 'recent-login';
            } else if (u.lastMessageAt > 0) {
                timeText = '💬 ' + timeAgo(Date.now() - u.lastMessageAt);
            }

            html += '<div class="acm-user' +
                        (hasUnread ? ' has-unread' : '') +
                        (hasThread ? '' : ' no-thread') +
                    '">' +
                '<div class="acm-user-avatar' +
                    (hasThread ? '' : ' no-thread') +
                    (isOnline ? ' online' : '') +
                '">' +
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
                    (timeText ? '<span class="acm-user-time ' + timeClass + '">' + timeText + '</span>' : '') +
                    (hasUnread ? '<span class="acm-user-badge">' +
                        (u.unread > 99 ? '99+' : u.unread) + '</span>' : '') +
                '</div>' +
                '<div class="acm-user-actions">' +
                    '<button class="acm-user-btn history" type="button" ' +
                        'onclick="window.__acmShowHistory(\'' + jsStr(u.email) + '\')" ' +
                        'title="Xem lịch sử hoạt động">' +
                        '<i class="fas fa-history"></i>' +
                    '</button>' +
                    '<button class="acm-user-btn chat" type="button" ' +
                        'onclick="window.__acmOpenThread(\'' + jsStr(u.email) + '\')" ' +
                        'title="Mở chat">' +
                        '<i class="fas fa-comments"></i>' +
                    '</button>' +
                '</div>' +
            '</div>';
        });

        el.innerHTML = html;
    }

    /* ═══════════════════════════════════════════════════════════
       📜 LỊCH SỬ HOẠT ĐỘNG
       ═══════════════════════════════════════════════════════════ */
    function showHistory(email) {
        if (!email) return;
        var db = getDb();
        if (!db) return;

        ACM.view = 'history';
        ACM.currentHistoryEmail = email;

        $id('acmHeaderList').style.display = 'none';
        $id('acmStats').style.display = 'none';
        $id('acmSearchBar').style.display = 'none';
        $id('acmList').style.display = 'none';

        $id('acmHeaderHistory').style.display = 'flex';
        $id('acmHistory').classList.add('show');

        $id('acmHistory').innerHTML =
            '<div class="acm-loading">' +
                '<i class="fas fa-spinner fa-pulse"></i>' +
                '<span>Đang tải lịch sử...</span>' +
            '</div>';

        if (ACM.historyUnsub) {
            try { ACM.historyUnsub(); } catch(e) {}
            ACM.historyUnsub = null;
        }

        var logsRef = db.collection('activity_logs')
            .where('email', '==', email)
            .orderBy('at', 'desc')
            .limit(100);

        ACM.historyUnsub = logsRef.onSnapshot(function(snap) {
            var activities = [];
            snap.forEach(function(doc) {
                var d = doc.data() || {};
                activities.push({
                    id: doc.id,
                    type: d.type || 'other',
                    title: d.title || '',
                    detail: d.detail || '',
                    at: d.at ? (d.at.toMillis ? d.at.toMillis() : 0) : 0,
                    metadata: d.metadata || {}
                });
            });
            renderHistory(email, activities);
        }, function(err) {
            console.error('History watch error:', err);
            renderHistory(email, []);
        });
    }

    function renderHistory(email, activities) {
        var el = $id('acmHistory');
        if (!el) return;

        var userInfo = ACM.usersMap[email] || {};
        var threadInfo = ACM.threadsMap[email] || {};
        var name = userInfo.name || threadInfo.userName || email.split('@')[0];
        var initial = (name || '?').charAt(0).toUpperCase();
        var tier = userInfo.tier || 'demo';
        var role = userInfo.role || 'user';
        var tierClass = getTierClass(role === 'admin' ? 'admin' : tier);
        var tierLabel = getTierLabel(role === 'admin' ? 'admin' : tier);
        var isOnline = !!ACM.onlineMap[email];

        // ⭐ Thời gian login gần nhất
        var lastLoginMs = ACM.loginLogsMap[(email || '').toLowerCase()] || 0;
        var lastLoginText = lastLoginMs > 0 ? formatDateTime(lastLoginMs) : '';

        var counts = { login: 0, chat: 0, renewal: 0, favorite: 0, practice: 0, other: 0 };
        activities.forEach(function(a) {
            var t = a.type || 'other';
            if (counts[t] !== undefined) counts[t]++;
            else counts.other++;
        });

        var html =
            '<div class="acm-hist-header">' +
                '<div class="acm-hist-avatar">' +
                    (isOnline ? '<span style="position:absolute;bottom:0;right:0;width:14px;height:14px;border-radius:50%;background:#16a34a;border:2px solid #fff;"></span>' : '') +
                    esc(initial) +
                '</div>' +
                '<div class="acm-hist-info">' +
                    '<div class="acm-hist-name">' +
                        esc(name) +
                        ' <span class="acm-tier ' + tierClass + '">' + tierLabel + '</span>' +
                        (isOnline ? ' <span style="color:#16a34a;font-size:.7rem;font-weight:700;">🟢 Online</span>' : '') +
                    '</div>' +
                    '<div class="acm-hist-email">' + esc(email) + '</div>' +
                    '<div class="acm-hist-meta">' +
                        '<span><i class="fas fa-list"></i> ' + activities.length + ' hoạt động</span>' +
                        (threadInfo.userEmail ? '<span><i class="fas fa-comments"></i> Có tin nhắn</span>' : '') +
                        // ⭐ Hiển thị lần login cuối
                        (lastLoginText ? '<span><i class="fas fa-sign-in-alt"></i> Login cuối: ' + esc(lastLoginText) + '</span>' : '') +
                    '</div>' +
                '</div>' +
                '<button class="acm-user-btn chat" type="button" ' +
                    'onclick="window.__acmOpenThread(\'' + jsStr(email) + '\')" ' +
                    'title="Mở chat">' +
                    '<i class="fas fa-comments"></i>' +
                '</button>' +
            '</div>';

        html +=
            '<div class="acm-hist-filters">' +
                '<button class="acm-hist-filter active" data-type="all">' +
                    '<i class="fas fa-list"></i> Tất cả (' + activities.length + ')' +
                '</button>' +
                '<button class="acm-hist-filter" data-type="login">' +
                    '<i class="fas fa-sign-in-alt"></i> Đăng nhập (' + counts.login + ')' +
                '</button>' +
                '<button class="acm-hist-filter" data-type="chat">' +
                    '<i class="fas fa-comments"></i> Chat (' + counts.chat + ')' +
                '</button>' +
                '<button class="acm-hist-filter" data-type="renewal">' +
                    '<i class="fas fa-money-bill"></i> Gia hạn (' + counts.renewal + ')' +
                '</button>' +
                '<button class="acm-hist-filter" data-type="practice">' +
                    '<i class="fas fa-pen"></i> Luyện tập (' + counts.practice + ')' +
                '</button>' +
                '<button class="acm-hist-filter" data-type="favorite">' +
                    '<i class="fas fa-heart"></i> Yêu thích (' + counts.favorite + ')' +
                '</button>' +
            '</div>';

        if (activities.length === 0) {
            html +=
                '<div class="acm-empty">' +
                    '<i class="fas fa-history"></i>' +
                    '<div class="acm-empty-title">Chưa có hoạt động nào</div>' +
                    '<div class="acm-empty-desc">' +
                        'Khi user đăng nhập, chat, gia hạn... sẽ được ghi lại ở đây' +
                    '</div>' +
                '</div>';
        } else {
            html += '<div class="acm-timeline" id="acmTimeline">';
            activities.forEach(function(a) {
                html += buildActivityItem(a);
            });
            html += '</div>';
        }

        el.innerHTML = html;

        el.querySelectorAll('.acm-hist-filter').forEach(function(btn) {
            btn.addEventListener('click', function() {
                el.querySelectorAll('.acm-hist-filter').forEach(function(b) {
                    b.classList.remove('active');
                });
                this.classList.add('active');
                var type = this.getAttribute('data-type');
                filterTimeline(type);
            });
        });
    }

    function buildActivityItem(a) {
        var icon = 'fa-circle';
        var title = a.title || 'Hoạt động';
        var detail = a.detail || '';

        switch (a.type) {
            case 'login':   icon = 'fa-sign-in-alt'; break;
            case 'logout':  icon = 'fa-sign-out-alt'; break;
            case 'chat':    icon = 'fa-comments'; break;
            case 'renewal': icon = 'fa-money-bill'; break;
            case 'favorite':icon = 'fa-heart'; break;
            case 'practice':icon = 'fa-pen'; break;
            case 'admin':   icon = 'fa-shield-alt'; break;
            default:        icon = 'fa-circle';
        }

        return '<div class="acm-tl-item" data-type="' + esc(a.type) + '">' +
            '<div class="acm-tl-head">' +
                '<div class="acm-tl-title">' +
                    '<span class="acm-tl-icon"><i class="fas ' + icon + '"></i></span>' +
                    esc(title) +
                '</div>' +
                '<span class="acm-tl-time">' + formatDateTime(a.at) + '</span>' +
            '</div>' +
            (detail ? '<div class="acm-tl-body">' + detail + '</div>' : '') +
        '</div>';
    }

    function filterTimeline(type) {
        var tl = $id('acmTimeline');
        if (!tl) return;
        tl.querySelectorAll('.acm-tl-item').forEach(function(item) {
            if (type === 'all' || item.getAttribute('data-type') === type) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    }

    function hideHistory() {
        ACM.view = 'list';
        ACM.currentHistoryEmail = null;

        $id('acmHeaderHistory').style.display = 'none';
        $id('acmHistory').classList.remove('show');
        $id('acmHistory').innerHTML = '';

        $id('acmHeaderList').style.display = 'flex';
        $id('acmStats').style.display = 'grid';
        $id('acmSearchBar').style.display = 'flex';
        $id('acmList').style.display = 'block';

        if (ACM.historyUnsub) {
            try { ACM.historyUnsub(); } catch(e) {}
            ACM.historyUnsub = null;
        }
    }

    /* ═══════════════════════════════════════════════════════════
       🔌 WATCHERS
       ═══════════════════════════════════════════════════════════ */
    function startWatchers() {
        stopWatchers();
        var db = getDb();
        if (!db || !isAdmin()) return;

        // 1. Watch allowed_users
        ACM.usersUnsub = db.collection('allowed_users')
            .onSnapshot(function(snap) {
                ACM.usersMap = {};
                snap.forEach(function(doc) {
                    var d = doc.data() || {};
                    var email = doc.id;
                    if (email) {
                        var tier = 'demo';
                        if (d.role === 'admin') tier = 'admin';
                        else if (d.isPermanent) tier = 'active';
                        else if (d.expiresAt) {
                            var expTime = d.expiresAt.toMillis ? d.expiresAt.toMillis() : 0;
                            tier = expTime > Date.now() ? 'active' : 'expired';
                        } else if (d.tier) tier = d.tier;

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

        // 2. Watch chat_threads
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

        // 3. Watch RTDB presence
        if (typeof firebase !== 'undefined' && firebase.database) {
            try {
                var presenceRef = firebase.database().ref('presence');
                var PRESENCE_CUTOFF = 3 * 60 * 1000;

                var handler = presenceRef.on('value', function(snap) {
                    var val = snap.val() || {};
                    var now = Date.now();
                    ACM.onlineMap = {};

                    Object.keys(val).forEach(function(key) {
                        var u = val[key];
                        if (u && u.at && (now - u.at) < PRESENCE_CUTOFF) {
                            var email = u.email || decodeURIComponent(key);
                            ACM.onlineMap[email] = true;
                        }
                    });

                    console.log('👥 ACM: Online users:', Object.keys(ACM.onlineMap).length);
                    rebuildList();
                }, function(err) {
                    console.error('ACM presence watch error:', err);
                });

                ACM.presenceUnsub = function() {
                    try { presenceRef.off('value', handler); } catch(e) {}
                };
            } catch(e) {
                console.warn('ACM: Không thể watch presence:', e);
            }
        }

        // ⭐ 4. Watch login_logs — lần đăng nhập cuối
        ACM.loginLogsUnsub = db.collection('login_logs')
            .orderBy('time', 'desc')
            .limit(500)
            .onSnapshot(function(snap) {
                ACM.loginLogsMap = {};
                snap.forEach(function(doc) {
                    var d = doc.data() || {};
                    var email = (d.email || '').toLowerCase();
                    if (!email) return;
                    // Chỉ lấy log mới nhất của mỗi user
                    if (!ACM.loginLogsMap[email] && d.time) {
                        var ts = d.time.toMillis ? d.time.toMillis() : 
                                 (d.time.seconds ? d.time.seconds * 1000 : 0);
                        ACM.loginLogsMap[email] = ts;
                    }
                });
                console.log('✅ ACM: Loaded', Object.keys(ACM.loginLogsMap).length, 'login logs');
                rebuildList();
            }, function(err) {
                console.error('ACM login_logs watch error:', err);
            });
    }

    function stopWatchers() {
        if (ACM.usersUnsub) { try { ACM.usersUnsub(); } catch(e){} ACM.usersUnsub = null; }
        if (ACM.threadsUnsub) { try { ACM.threadsUnsub(); } catch(e){} ACM.threadsUnsub = null; }
        if (ACM.presenceUnsub) { try { ACM.presenceUnsub(); } catch(e){} ACM.presenceUnsub = null; }
        if (ACM.historyUnsub) { try { ACM.historyUnsub(); } catch(e){} ACM.historyUnsub = null; }
        if (ACM.loginLogsUnsub) { try { ACM.loginLogsUnsub(); } catch(e){} ACM.loginLogsUnsub = null; }
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
        if (ACM.view === 'history') hideHistory();
    }

    function toggleModal() {
        if (ACM.isOpen) closeModal();
        else openModal();
    }

    /* ═══════════════════════════════════════════════════════════
       🔗 EXPOSE GLOBAL
       ═══════════════════════════════════════════════════════════ */
    window.__acmOpenThread = function(email) {
        closeModal();
        setTimeout(function() {
            if (typeof window.__chatOpen === 'function') {
                if (!document.getElementById('chatModal').classList.contains('show')) {
                    window.__chatOpen();
                }
            }
            setTimeout(function() {
                if (typeof window.__chatOpenThread === 'function') {
                    window.__chatOpenThread(email);
                }
            }, 400);
        }, 200);
    };

    window.__acmShowHistory = function(email) {
        showHistory(email);
    };

    /* ═══════════════════════════════════════════════════════════
       🚀 INIT
       ═══════════════════════════════════════════════════════════ */
    function init() {
        if (ACM.inited) return;
        ACM.inited = true;

        var closeBtn = $id('acmClose');
        if (closeBtn) closeBtn.addEventListener('click', closeModal);

        var closeHistBtn = $id('acmCloseHistory');
        if (closeHistBtn) closeHistBtn.addEventListener('click', closeModal);

        var backBtn = $id('acmHistoryBack');
        if (backBtn) backBtn.addEventListener('click', hideHistory);

        var modal = $id('acmModal');
        if (modal) modal.addEventListener('click', function(e) {
            if (e.target === this) closeModal();
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && ACM.isOpen) {
                if (ACM.view === 'history') hideHistory();
                else closeModal();
            }
        });

        var fab = $id('acmFab');
        if (fab) fab.addEventListener('click', toggleModal);

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

        var refreshBtn = $id('acmRefreshBtn');
        if (refreshBtn) refreshBtn.addEventListener('click', function() {
            this.classList.add('spinning');
            var self = this;
            startWatchers();
            setTimeout(function() { self.classList.remove('spinning'); }, 800);
        });

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
