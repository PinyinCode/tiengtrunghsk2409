# -*- coding: utf-8 -*-
"""
Intro Template — Tính năng giới thiệu & hướng dẫn sử dụng.

Cung cấp 3 hàm:
  - build_intro_css()   → CSS cho intro modal + quick banner
  - build_intro_html()  → HTML cho intro modal + quick banner
  - build_intro_js()    → JS điều khiển intro modal + quick banner

Cách dùng trong main.py:
    from intro_template import build_intro_css, build_intro_html, build_intro_js

    full_css = build_ui_css() + build_intro_css() + ...
    ui_html = build_ui_html().replace("<!-- __QUICK_INTRO_BANNER__ -->", build_intro_html())
    full_js  = build_ui_js() + build_intro_js() + ...
"""


# ═══════════════════════════════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════════════════════════════
def build_intro_css():
    return r"""
/* ═══════════════════════════════════════════════════════════════ */
/* QUICK INTRO BANNER — Giới thiệu nhanh trên trang chủ            */
/* ═══════════════════════════════════════════════════════════════ */
.quick-intro-banner {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: .9rem 1.1rem;
    margin-bottom: 1rem;
    background: linear-gradient(135deg,
        rgba(99, 102, 241, .08) 0%,
        rgba(139, 92, 246, .08) 50%,
        rgba(217, 70, 239, .06) 100%);
    border: 1.5px solid rgba(139, 92, 246, .3);
    border-radius: 16px;
    position: relative;
    overflow: hidden;
    animation: qibSlideDown .5s cubic-bezier(.34, 1.56, .64, 1);
    flex-wrap: wrap;
    box-shadow: 0 4px 16px rgba(139, 92, 246, .08);
}
.quick-intro-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(115deg,
        transparent 40%,
        rgba(255, 255, 255, .3) 50%,
        transparent 60%);
    transform: translateX(-100%) rotate(25deg);
    animation: qibShine 6s ease-in-out infinite;
    pointer-events: none;
}
@keyframes qibShine {
    0% { transform: translateX(-100%) rotate(25deg); }
    40%, 100% { transform: translateX(100%) rotate(25deg); }
}
@keyframes qibSlideDown {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
}

.quick-intro-banner.dismissed {
    display: none !important;
}

.qib-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6 40%, #d946ef);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
    box-shadow: 0 6px 18px rgba(139, 92, 246, .4);
    animation: qibIconFloat 3s ease-in-out infinite;
    position: relative;
    z-index: 2;
}
@keyframes qibIconFloat {
    0%, 100% { transform: translateY(0) rotate(0); }
    50% { transform: translateY(-3px) rotate(-5deg); }
}

.qib-content {
    flex: 1 1 300px;
    min-width: 0;
    position: relative;
    z-index: 2;
}

.qib-title {
    font-size: .92rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: .5rem;
    line-height: 1.35;
}
.qib-title strong {
    background: linear-gradient(135deg, #4f46e5, #7c3aed 50%, #d946ef);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
    font-weight: 900;
}

.qib-features {
    display: flex;
    flex-wrap: wrap;
    gap: .35rem;
}
.qib-feature {
    display: inline-flex;
    align-items: center;
    gap: .3rem;
    padding: .22rem .6rem;
    border-radius: 50px;
    background: var(--surface);
    border: 1px solid rgba(139, 92, 246, .2);
    color: var(--text-2);
    font-size: .72rem;
    font-weight: 700;
    white-space: nowrap;
    transition: all .2s ease;
}
.qib-feature i {
    color: #7c3aed;
    font-size: .78rem;
}
.qib-feature:hover {
    transform: translateY(-1px);
    border-color: rgba(139, 92, 246, .5);
    box-shadow: 0 2px 8px rgba(139, 92, 246, .2);
}
[data-theme="dark"] .qib-feature {
    background: rgba(30, 41, 59, .6);
    border-color: rgba(167, 139, 250, .3);
}
[data-theme="dark"] .qib-feature i { color: #c4b5fd; }

.qib-actions {
    display: flex;
    align-items: center;
    gap: .5rem;
    flex-shrink: 0;
    position: relative;
    z-index: 2;
}

.qib-btn {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    padding: .55rem 1rem;
    border-radius: 50px;
    border: none;
    font-size: .82rem;
    font-weight: 800;
    cursor: pointer;
    font-family: inherit;
    transition: all .2s cubic-bezier(.34, 1.56, .64, 1);
    white-space: nowrap;
}
.qib-btn-primary {
    background: linear-gradient(135deg, #4f46e5, #7c3aed 50%, #a855f7);
    color: #fff;
    box-shadow: 0 4px 14px rgba(124, 58, 237, .35);
    animation: qibBtnPulse 2.5s ease-in-out infinite;
}
.qib-btn-primary:hover {
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 8px 22px rgba(124, 58, 237, .6);
}
@keyframes qibBtnPulse {
    0%, 100% { box-shadow: 0 4px 14px rgba(124, 58, 237, .35); }
    50%      { box-shadow: 0 4px 20px rgba(124, 58, 237, .65); }
}
.qib-btn-primary i { font-size: .9rem; }

.qib-btn-ghost {
    width: 34px;
    height: 34px;
    padding: 0;
    background: var(--surface);
    color: var(--text-3);
    border: 1px solid var(--border);
    justify-content: center;
}
.qib-btn-ghost:hover {
    background: var(--danger-light);
    color: var(--danger);
    border-color: var(--danger);
    transform: rotate(90deg);
}

/* ═══ Mobile quick banner ═══ */
@media (max-width: 640px) {
    .quick-intro-banner {
        padding: .75rem .85rem;
        gap: .65rem;
        flex-wrap: wrap;
    }
    .qib-icon {
        width: 38px;
        height: 38px;
        font-size: 1.05rem;
        border-radius: 11px;
    }
    .qib-content {
        flex: 1 1 100%;
        order: 3;
        margin-top: .15rem;
    }
    .qib-title {
        font-size: .82rem;
        margin-bottom: .4rem;
    }
    .qib-features { gap: .25rem; }
    .qib-feature {
        font-size: .65rem;
        padding: .18rem .5rem;
        gap: .22rem;
    }
    .qib-feature i { font-size: .7rem; }
    .qib-actions {
        order: 2;
        margin-left: auto;
    }
    .qib-btn-primary {
        padding: .5rem .85rem;
        font-size: .75rem;
    }
    .qib-btn-primary span { display: none; }
    .qib-btn-primary::after {
        content: 'Hướng dẫn';
        margin-left: .15rem;
    }
    .qib-btn-ghost {
        width: 30px;
        height: 30px;
    }
}
@media (max-width: 400px) {
    .qib-title strong {
        display: block;
        margin-top: .15rem;
    }
    .qib-feature:nth-child(n+5) { display: none; }
}

/* ═══════════════════════════════════════════════════════════════ */
/* INTRO SLIDES — Modal giới thiệu                                 */
/* ═══════════════════════════════════════════════════════════════ */
.intro-modal {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, .88);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    z-index: 6000;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    animation: introFadeIn .3s ease;
}
.intro-modal.show { display: flex; }
@keyframes introFadeIn { from { opacity: 0; } to { opacity: 1; } }

.intro-box {
    background: var(--surface);
    border-radius: 24px;
    width: 100%;
    max-width: 960px;
    max-height: min(92vh, 720px);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
    box-shadow: 0 30px 80px rgba(0, 0, 0, .5),
                0 0 0 1px rgba(139, 92, 246, .2);
    animation: introSlideUp .4s cubic-bezier(.34, 1.56, .64, 1);
}
@keyframes introSlideUp {
    from { transform: translateY(40px) scale(.95); opacity: 0; }
    to   { transform: translateY(0) scale(1);      opacity: 1; }
}

.intro-close {
    position: absolute;
    top: 14px;
    right: 14px;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: none;
    background: rgba(255,255,255,.85);
    color: #475569;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: .95rem;
    z-index: 20;
    transition: .15s;
    font-family: inherit;
    box-shadow: 0 2px 8px rgba(0,0,0,.15);
}
.intro-close:hover {
    background: var(--danger);
    color: #fff;
    transform: scale(1.08) rotate(90deg);
}
[data-theme="dark"] .intro-close {
    background: rgba(30,41,59,.9);
    color: #cbd5e1;
}

.intro-slides {
    flex: 1 1 auto;
    min-height: 0;
    position: relative;
    overflow: hidden;
}
.intro-slide {
    position: absolute;
    inset: 0;
    opacity: 0;
    transform: translateX(30px);
    pointer-events: none;
    transition: opacity .35s ease, transform .35s ease;
    overflow-y: auto;
    padding: 2.5rem 3rem;
    display: flex;
    align-items: center;
    justify-content: center;
    -webkit-overflow-scrolling: touch;
}
.intro-slide.active {
    opacity: 1;
    transform: translateX(0);
    pointer-events: auto;
    position: relative;
}
.intro-slide.prev {
    transform: translateX(-30px);
}
.intro-slide-content {
    width: 100%;
    max-width: 780px;
    margin: 0 auto;
}

/* ═══ Slide 1: Cover ═══ */
.cover-slide { text-align: center; }
.cover-icon {
    width: 96px;
    height: 96px;
    margin: 0 auto 1.25rem;
    border-radius: 24px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6 40%, #d946ef);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 2.5rem;
    box-shadow: 0 16px 40px rgba(139, 92, 246, .5);
    animation: coverIconFloat 3s ease-in-out infinite;
    position: relative;
    overflow: hidden;
}
.cover-icon::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(115deg, transparent 30%, rgba(255,255,255,.35) 50%, transparent 70%);
    transform: translateX(-100%) rotate(25deg);
    animation: coverShine 3s ease-in-out infinite;
}
@keyframes coverIconFloat {
    0%, 100% { transform: translateY(0) rotate(0); }
    50% { transform: translateY(-6px) rotate(-3deg); }
}
@keyframes coverShine {
    0% { transform: translateX(-100%) rotate(25deg); }
    60%, 100% { transform: translateX(100%) rotate(25deg); }
}

.cover-title {
    font-size: clamp(1.75rem, 3.5vw, 2.5rem);
    font-weight: 900;
    letter-spacing: -.025em;
    background: linear-gradient(135deg, #1e293b 0%, #4f46e5 50%, #7c3aed 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
    margin-bottom: .5rem;
    line-height: 1.15;
}
[data-theme="dark"] .cover-title {
    background: linear-gradient(135deg, #f1f5f9 0%, #a5b4fc 50%, #c4b5fd 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.cover-subtitle {
    font-size: clamp(1.1rem, 2vw, 1.4rem);
    font-weight: 800;
    color: #7c3aed;
    margin-bottom: 1rem;
    letter-spacing: .02em;
}
[data-theme="dark"] .cover-subtitle { color: #c4b5fd; }

.cover-desc {
    font-size: clamp(.85rem, 1.1vw, .95rem);
    color: var(--text-2);
    line-height: 1.7;
    margin-bottom: 1.75rem;
}

.cover-tags {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: .5rem;
}
.cover-tag {
    display: inline-flex;
    align-items: center;
    gap: .35rem;
    padding: .4rem .85rem;
    border-radius: 50px;
    background: linear-gradient(135deg, rgba(99,102,241,.12), rgba(139,92,246,.08));
    border: 1px solid rgba(139,92,246,.3);
    color: #7c3aed;
    font-size: .78rem;
    font-weight: 700;
}
.cover-tag i { font-size: .85rem; }
[data-theme="dark"] .cover-tag {
    background: linear-gradient(135deg, rgba(139,92,246,.25), rgba(139,92,246,.12));
    color: #c4b5fd;
    border-color: rgba(167,139,250,.4);
}

/* ═══ Slide 2-4: Badge + Title ═══ */
.slide-badge {
    display: inline-flex;
    align-items: center;
    gap: .35rem;
    padding: .3rem .75rem;
    border-radius: 50px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #fff;
    font-size: .7rem;
    font-weight: 800;
    letter-spacing: .5px;
    text-transform: uppercase;
    margin-bottom: .85rem;
    box-shadow: 0 4px 12px rgba(124,58,237,.35);
}
.slide-badge i { font-size: .8rem; }

.slide-title {
    font-size: clamp(1.35rem, 2.5vw, 1.85rem);
    font-weight: 900;
    color: var(--text);
    margin-bottom: 1.5rem;
    line-height: 1.2;
    letter-spacing: -.02em;
}

/* ═══ Feature items (Slide 2) ═══ */
.slide-body.two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    align-items: start;
}
@media (max-width: 640px) {
    .slide-body.two-col {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
}

.feature-item {
    display: flex;
    gap: .75rem;
    padding: .85rem;
    border-radius: 12px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    margin-bottom: .65rem;
    transition: transform .2s ease, border-color .2s ease;
}
.feature-item:hover {
    transform: translateX(4px);
    border-color: rgba(139,92,246,.4);
}
.feature-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    color: #fff;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(0,0,0,.15);
}
.feature-icon.blue   { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.feature-icon.purple { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }
.feature-icon.green  { background: linear-gradient(135deg, #10b981, #059669); }
.feature-text { flex: 1; min-width: 0; }
.feature-title {
    font-weight: 800;
    font-size: .88rem;
    color: var(--text);
    margin-bottom: .2rem;
}
.feature-desc {
    font-size: .78rem;
    color: var(--text-2);
    line-height: 1.5;
}

.slide-preview { display: flex; align-items: center; justify-content: center; }
.preview-mockup {
    width: 100%;
    max-width: 280px;
    padding: 1rem;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(99,102,241,.08), rgba(139,92,246,.05));
    border: 1px solid rgba(139,92,246,.25);
    display: flex;
    flex-direction: column;
    gap: .6rem;
}
.preview-bar {
    height: 10px;
    border-radius: 50px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    opacity: .8;
}
.preview-bar.short { width: 60%; opacity: .5; }
.preview-card {
    padding: .75rem;
    border-radius: 10px;
    background: var(--surface);
    border: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    gap: .4rem;
}
.preview-line {
    height: 8px;
    border-radius: 50px;
    background: var(--border-strong);
    opacity: .5;
}
.preview-line.short { width: 70%; }
.preview-line.tiny { width: 40%; }

/* ═══════════════════════════════════════════════════════════════ */
/* GUIDE STEPS — Slide hướng dẫn                                    */
/* ═══════════════════════════════════════════════════════════════ */
.guide-steps {
    display: flex;
    flex-direction: column;
    gap: .75rem;
}

.guide-step {
    display: flex;
    gap: .75rem;
    padding: .85rem 1rem;
    border-radius: 12px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    transition: all .25s ease;
    animation: guideStepFadeIn .4s ease backwards;
}
.guide-step:nth-child(1) { animation-delay: .05s; }
.guide-step:nth-child(2) { animation-delay: .1s; }
.guide-step:nth-child(3) { animation-delay: .15s; }
.guide-step:nth-child(4) { animation-delay: .2s; }
.guide-step:nth-child(5) { animation-delay: .25s; }
.guide-step:nth-child(6) { animation-delay: .3s; }
.guide-step:nth-child(7) { animation-delay: .35s; }
@keyframes guideStepFadeIn {
    from { opacity: 0; transform: translateX(-8px); }
    to   { opacity: 1; transform: translateX(0); }
}

.guide-step:hover {
    border-color: rgba(139, 92, 246, .4);
    transform: translateX(4px);
    box-shadow: 0 4px 14px rgba(139, 92, 246, .12);
}

.guide-step-num {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: .88rem;
    font-weight: 900;
    flex-shrink: 0;
    box-shadow: 0 4px 10px rgba(124, 58, 237, .35);
}

.guide-step-content { flex: 1; min-width: 0; }

.guide-step-title {
    font-weight: 800;
    font-size: .88rem;
    color: var(--text);
    margin-bottom: .35rem;
    display: flex;
    align-items: center;
    gap: .4rem;
}
.guide-step-title i {
    color: #7c3aed;
    font-size: .95rem;
}

.guide-step-desc {
    font-size: .76rem;
    color: var(--text-2);
    line-height: 1.55;
    margin-bottom: .5rem;
}
.guide-step-desc b {
    color: var(--text);
    font-weight: 800;
}

.guide-step-visual {
    display: flex;
    flex-wrap: wrap;
    gap: .35rem;
    align-items: center;
    margin-top: .4rem;
}

.guide-mock-chip {
    display: inline-flex;
    align-items: center;
    gap: .25rem;
    padding: .22rem .55rem;
    border-radius: 50px;
    background: var(--surface);
    border: 1px solid var(--border);
    font-size: .7rem;
    font-weight: 700;
    color: var(--text-2);
}
.guide-mock-chip.active {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #fff;
    border-color: transparent;
}

.guide-mock-btn {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: var(--surface);
    border: 1px solid var(--border);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: .78rem;
    color: var(--text-2);
}
.guide-mock-btn.primary {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #fff;
    border-color: transparent;
}

.guide-mock-arrow {
    color: #7c3aed;
    font-weight: 900;
    font-size: .85rem;
}

.guide-mock-input {
    flex: 1;
    min-width: 100px;
    padding: .35rem .65rem;
    border-radius: 8px;
    background: var(--surface);
    border: 1px solid var(--border);
    font-size: .72rem;
    color: var(--text-3);
    font-style: italic;
}

.guide-mock-result {
    padding: .3rem .6rem;
    border-radius: 6px;
    font-size: .72rem;
    font-weight: 800;
    font-family: var(--font-zh);
}
.guide-mock-result.correct {
    background: rgba(22, 163, 74, .15);
    color: #15803d;
}
.guide-mock-result.wrong {
    background: rgba(220, 38, 38, .15);
    color: #dc2626;
}

.guide-mock-nav {
    display: inline-flex;
    gap: .25rem;
    padding: .25rem .5rem;
    border-radius: 50px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text-2);
    font-size: .7rem;
}
.guide-mock-nav i {
    padding: .15rem .3rem;
    border-radius: 50%;
    background: var(--surface-2);
}
.guide-mock-nav i:nth-child(2) {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #fff;
}

.guide-mock-canvas {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    background: #fff;
    border: 1.5px solid var(--border-strong);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-zh);
    font-size: 1.4rem;
    font-weight: 700;
    color: #1e293b;
    background-image:
        linear-gradient(to right, transparent calc(50% - .5px), #e2e8f0 calc(50% - .5px), #e2e8f0 calc(50% + .5px), transparent calc(50% + .5px)),
        linear-gradient(to bottom, transparent calc(50% - .5px), #e2e8f0 calc(50% - .5px), #e2e8f0 calc(50% + .5px), transparent calc(50% + .5px));
}

.guide-mock-toggle {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: var(--surface);
    border: 1px solid var(--border);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: .7rem;
    color: var(--text-3);
    opacity: .4;
}
.guide-mock-toggle.active {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #fff;
    border-color: transparent;
    opacity: 1;
    box-shadow: 0 2px 6px rgba(124, 58, 237, .35);
}

.guide-step-tip {
    background: linear-gradient(135deg, rgba(251, 191, 36, .1), rgba(245, 158, 11, .06));
    border-color: rgba(245, 158, 11, .35);
    margin-top: .25rem;
}
.guide-step-tip:hover {
    border-color: rgba(245, 158, 11, .6);
    box-shadow: 0 4px 14px rgba(245, 158, 11, .15);
}
.guide-tip-icon {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: .95rem;
    flex-shrink: 0;
    box-shadow: 0 4px 10px rgba(245, 158, 11, .4);
    animation: tipBulbPulse 2s ease-in-out infinite;
}
@keyframes tipBulbPulse {
    0%, 100% { transform: scale(1); box-shadow: 0 4px 10px rgba(245, 158, 11, .4); }
    50%      { transform: scale(1.08); box-shadow: 0 6px 16px rgba(245, 158, 11, .7); }
}
.guide-step-tip .guide-step-title { color: #92400e; }
[data-theme="dark"] .guide-step-tip .guide-step-title { color: #fcd34d; }

/* ═══ Trial cards (Slide Trial) ═══ */
.trial-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}
@media (max-width: 700px) {
    .trial-cards { grid-template-columns: 1fr; }
}
.trial-card {
    padding: 1.1rem 1rem;
    border-radius: 14px;
    background: var(--surface-2);
    border: 1.5px solid var(--border);
    position: relative;
    transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
}
.trial-card:hover {
    transform: translateY(-4px);
    border-color: rgba(139,92,246,.5);
    box-shadow: 0 12px 28px rgba(139,92,246,.18);
}
.trial-card-badge {
    position: absolute;
    top: -10px;
    left: 14px;
    padding: .15rem .55rem;
    border-radius: 50px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #fff;
    font-size: .6rem;
    font-weight: 900;
    letter-spacing: .5px;
    text-transform: uppercase;
    box-shadow: 0 4px 10px rgba(124,58,237,.4);
}
.trial-card-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(99,102,241,.15), rgba(139,92,246,.1));
    color: #7c3aed;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.15rem;
    margin-bottom: .75rem;
}
[data-theme="dark"] .trial-card-icon {
    background: linear-gradient(135deg, rgba(139,92,246,.3), rgba(139,92,246,.15));
    color: #c4b5fd;
}
.trial-card-title {
    font-weight: 800;
    font-size: .88rem;
    color: var(--text);
    margin-bottom: .35rem;
}
.trial-card-desc {
    font-size: .75rem;
    color: var(--text-2);
    line-height: 1.5;
}

/* ═══ Package items (Slide Gói) ═══ */
.package-item {
    display: flex;
    gap: .7rem;
    padding: .75rem .85rem;
    border-radius: 12px;
    background: var(--surface-2);
    border: 1.5px solid var(--border);
    margin-bottom: .55rem;
    transition: transform .2s ease, border-color .2s ease;
    align-items: flex-start;
}
.package-item:hover {
    transform: translateX(4px);
    border-color: rgba(139,92,246,.4);
}
.package-item.premium {
    background: linear-gradient(135deg, rgba(251,191,36,.1), rgba(245,158,11,.05));
    border-color: rgba(245,158,11,.4);
}
.package-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: .95rem;
    flex-shrink: 0;
}
.package-icon.hot { background: linear-gradient(135deg, #f59e0b, #d97706); }
.package-icon.premium { background: linear-gradient(135deg, #fbbf24, #f59e0b); }
.package-info { flex: 1; min-width: 0; }
.package-title {
    font-weight: 800;
    font-size: .85rem;
    color: var(--text);
    margin-bottom: .15rem;
    display: flex;
    align-items: center;
    gap: .4rem;
    flex-wrap: wrap;
}
.package-price {
    color: #dc2626;
    font-weight: 900;
    font-size: .95rem;
}
.package-badge {
    padding: .1rem .4rem;
    border-radius: 50px;
    background: linear-gradient(135deg, #16a34a, #22c55e);
    color: #fff;
    font-size: .58rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: .3px;
}
.package-badge.save { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.package-badge.forever {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    color: #fde68a;
}
.package-desc {
    font-size: .72rem;
    color: var(--text-2);
    line-height: 1.4;
}

.qr-preview {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: .5rem;
}
.qr-box {
    width: 140px;
    height: 140px;
    border-radius: 14px;
    background: #fff;
    border: 2px dashed var(--border-strong);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
    color: #4f46e5;
    box-shadow: 0 8px 24px rgba(0,0,0,.1);
}
.qr-caption {
    font-size: .75rem;
    color: var(--text-2);
    text-align: center;
    line-height: 1.5;
}
.qr-caption strong { color: #16a34a; }

/* ═══ Slide CTA ═══ */
.cta-slide { text-align: center; }
.cta-icon {
    width: 88px;
    height: 88px;
    margin: 0 auto 1.5rem;
    border-radius: 50%;
    background: linear-gradient(135deg, #4f46e5, #7c3aed 50%, #a855f7);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 2.2rem;
    box-shadow: 0 16px 40px rgba(124,58,237,.5);
    animation: ctaIconPulse 2s ease-in-out infinite;
}
@keyframes ctaIconPulse {
    0%, 100% { transform: scale(1); box-shadow: 0 16px 40px rgba(124,58,237,.5); }
    50% { transform: scale(1.06); box-shadow: 0 20px 50px rgba(124,58,237,.7); }
}
.cta-title {
    font-size: clamp(1.5rem, 3vw, 2.1rem);
    font-weight: 900;
    background: linear-gradient(135deg, #4f46e5, #7c3aed 50%, #d946ef);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
    margin-bottom: 1rem;
    line-height: 1.2;
    letter-spacing: -.02em;
}
.cta-desc {
    font-size: clamp(.85rem, 1.1vw, 1rem);
    color: var(--text-2);
    line-height: 1.6;
    max-width: 500px;
    margin: 0 auto 1.25rem;
}
.cta-message {
    display: inline-flex;
    align-items: center;
    gap: .5rem;
    padding: .65rem 1.2rem;
    border-radius: 50px;
    background: linear-gradient(135deg, rgba(99,102,241,.1), rgba(139,92,246,.08));
    border: 1.5px solid rgba(139,92,246,.3);
    color: #7c3aed;
    font-size: .85rem;
    font-weight: 700;
    margin-bottom: 2rem;
}
[data-theme="dark"] .cta-message {
    background: linear-gradient(135deg, rgba(139,92,246,.25), rgba(139,92,246,.12));
    color: #c4b5fd;
    border-color: rgba(167,139,250,.4);
}
.cta-message i { color: #d946ef; font-size: 1rem; }

.cta-actions {
    display: flex;
    gap: .75rem;
    justify-content: center;
    flex-wrap: wrap;
}
.cta-btn {
    padding: .9rem 1.75rem;
    border-radius: 50px;
    border: none;
    font-size: .92rem;
    font-weight: 800;
    font-family: inherit;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: .5rem;
    transition: all .25s cubic-bezier(.34,1.56,.64,1);
    text-transform: uppercase;
    letter-spacing: .5px;
}
.cta-btn.secondary {
    background: var(--surface-2);
    color: var(--text-2);
    border: 1.5px solid var(--border);
}
.cta-btn.secondary:hover {
    background: var(--surface);
    border-color: var(--primary);
    color: var(--primary);
    transform: translateY(-2px);
}
.cta-btn.primary {
    background: linear-gradient(135deg, #4f46e5, #7c3aed 50%, #a855f7);
    color: #fff;
    box-shadow: 0 8px 24px rgba(124,58,237,.4);
}
.cta-btn.primary:hover {
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 12px 32px rgba(124,58,237,.65);
}

/* ═══ Navigation buttons ═══ */
.intro-nav {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: none;
    background: var(--surface);
    color: var(--text-2);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: .95rem;
    box-shadow: 0 4px 16px rgba(0,0,0,.15);
    transition: all .2s ease;
    z-index: 15;
    font-family: inherit;
}
.intro-nav:hover {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #fff;
    transform: translateY(-50%) scale(1.1);
    box-shadow: 0 8px 24px rgba(124,58,237,.5);
}
.intro-nav.prev { left: 12px; }
.intro-nav.next { right: 12px; }
.intro-nav:disabled {
    opacity: .3;
    cursor: not-allowed;
    pointer-events: none;
}
@media (max-width: 640px) {
    .intro-nav { display: none; }
}

/* ═══ Footer: counter + dots ═══ */
.intro-footer {
    flex: 0 0 auto;
    padding: .85rem 1.5rem;
    background: var(--surface-2);
    border-top: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}
.intro-counter {
    font-size: .78rem;
    font-weight: 800;
    color: var(--text-2);
    letter-spacing: .5px;
}
.intro-counter #introCurrent {
    color: #7c3aed;
    font-size: 1rem;
}
.intro-dots {
    display: flex;
    gap: .4rem;
    align-items: center;
}
.intro-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    border: none;
    background: var(--border-strong);
    cursor: pointer;
    padding: 0;
    transition: all .25s ease;
    font-family: inherit;
}
.intro-dot:hover {
    background: #7c3aed;
    transform: scale(1.2);
}
.intro-dot.active {
    width: 26px;
    border-radius: 50px;
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    box-shadow: 0 2px 8px rgba(124,58,237,.5);
}

/* ═══ Mobile modal ═══ */
@media (max-width: 640px) {
    .intro-modal { padding: .5rem; align-items: flex-end; }
    .intro-box {
        max-width: 100%;
        max-height: 94vh;
        border-radius: 20px 20px 0 0;
    }
    .intro-slide { padding: 2rem 1.25rem 1.5rem; }
    .intro-close { top: 10px; right: 10px; width: 32px; height: 32px; }
    .cover-icon { width: 72px; height: 72px; font-size: 1.9rem; border-radius: 20px; }
    .cover-title { font-size: 1.5rem; }
    .cover-subtitle { font-size: 1rem; }
    .cover-desc { font-size: .8rem; margin-bottom: 1.25rem; }
    .cover-tags { gap: .35rem; }
    .cover-tag { font-size: .7rem; padding: .3rem .65rem; }
    .slide-title { font-size: 1.2rem; margin-bottom: 1rem; }
    .feature-item, .package-item { padding: .65rem .75rem; }
    .feature-icon, .package-icon { width: 36px; height: 36px; font-size: .9rem; }
    .trial-cards { gap: .75rem; }
    .trial-card { padding: .85rem .75rem; }
    .cta-icon { width: 72px; height: 72px; font-size: 1.8rem; }
    .cta-title { font-size: 1.35rem; }
    .cta-desc { font-size: .82rem; }
    .cta-message { font-size: .78rem; padding: .5rem .9rem; }
    .cta-btn { padding: .75rem 1.25rem; font-size: .82rem; }
    .cta-actions { flex-direction: column-reverse; }
    .cta-btn { width: 100%; justify-content: center; }
    .intro-footer { padding: .7rem 1rem; }
    .qr-box { width: 110px; height: 110px; font-size: 3rem; }

    .guide-step { padding: .7rem .75rem; gap: .55rem; }
    .guide-step-num { width: 26px; height: 26px; font-size: .78rem; }
    .guide-step-title { font-size: .8rem; }
    .guide-step-desc { font-size: .7rem; line-height: 1.5; }
    .guide-mock-btn { width: 26px; height: 26px; font-size: .7rem; }
    .guide-mock-chip { font-size: .64rem; padding: .18rem .45rem; }
    .guide-mock-input { font-size: .66rem; }
    .guide-mock-canvas { width: 34px; height: 34px; font-size: 1.2rem; }
}

[data-theme="dark"] .intro-footer {
    background: rgba(15,23,42,.6);
}
"""


# ═══════════════════════════════════════════════════════════════════
#  HTML
# ═══════════════════════════════════════════════════════════════════
def build_intro_html():
    return r"""
<!-- ═══════════════════════════════════════════════════════════ -->
<!-- QUICK INTRO BANNER                                          -->
<!-- ═══════════════════════════════════════════════════════════ -->
<div class="quick-intro-banner" id="quickIntroBanner">
    <div class="qib-icon">
        <i class="fas fa-rocket"></i>
    </div>
    <div class="qib-content">
        <div class="qib-title">
            🎉 Chào mừng đến với <strong>Học Tiếng Trung · Văn Phòng &amp; Công Xưởng</strong>
        </div>
        <div class="qib-features">
            <span class="qib-feature"><i class="fas fa-database"></i> 1750+ câu</span>
            <span class="qib-feature"><i class="fas fa-graduation-cap"></i> HSK1-6</span>
            <span class="qib-feature"><i class="fas fa-industry"></i> 8 chuyên ngành</span>
            <span class="qib-feature"><i class="fas fa-volume-up"></i> Audio chuẩn</span>
            <span class="qib-feature"><i class="fas fa-pen-fancy"></i> Luyện viết</span>
            <span class="qib-feature"><i class="fas fa-robot"></i> AI chấm điểm</span>
            <span class="qib-feature"><i class="fas fa-book-open"></i> Hướng dẫn chi tiết</span>
        </div>
    </div>
    <div class="qib-actions">
        <button class="qib-btn qib-btn-primary" onclick="openIntroModal()">
            <i class="fas fa-play-circle"></i> <span>Hướng dẫn 30s</span>
        </button>
        <button class="qib-btn qib-btn-ghost" id="quickIntroDismiss" title="Đóng">
            <i class="fas fa-times"></i>
        </button>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════ -->
<!-- INTRO MODAL — 6 SLIDES                                      -->
<!-- ═══════════════════════════════════════════════════════════ -->
<div class="intro-modal" id="introModal">
    <div class="intro-box">
        <button class="intro-close" id="introClose" aria-label="Đóng">
            <i class="fas fa-times"></i>
        </button>

        <div class="intro-slides" id="introSlides">

            <!-- ═══ SLIDE 1: Cover ═══ -->
            <div class="intro-slide active" data-slide="0">
                <div class="intro-slide-content cover-slide">
                    <div class="cover-icon">
                        <i class="fas fa-language"></i>
                    </div>
                    <h1 class="cover-title">Học Tiếng Trung</h1>
                    <h2 class="cover-subtitle">Văn Phòng · Công Xưởng</h2>
                    <p class="cover-desc">
                        Giải pháp luyện phản xạ giao tiếp chuyên sâu,<br>
                        hỗ trợ đắc lực cho công việc văn phòng,<br>
                        xưởng sản xuất và quản lý nhân sự.
                    </p>
                    <div class="cover-tags">
                        <span class="cover-tag"><i class="fas fa-fire"></i> 1750+ câu</span>
                        <span class="cover-tag"><i class="fas fa-graduation-cap"></i> HSK1-6</span>
                        <span class="cover-tag"><i class="fas fa-volume-up"></i> Audio</span>
                        <span class="cover-tag"><i class="fas fa-pen-fancy"></i> Luyện viết</span>
                    </div>
                </div>
            </div>

            <!-- ═══ SLIDE 2: Tổng quan ═══ -->
            <div class="intro-slide" data-slide="1">
                <div class="intro-slide-content">
                    <div class="slide-badge"><i class="fas fa-star"></i> Tổng quan</div>
                    <h2 class="slide-title">Tổng Quan Giao Diện &amp; Dữ Liệu</h2>

                    <div class="slide-body two-col">
                        <div class="slide-col">
                            <div class="feature-item">
                                <div class="feature-icon blue"><i class="fas fa-database"></i></div>
                                <div class="feature-text">
                                    <div class="feature-title">Kho dữ liệu lớn</div>
                                    <div class="feature-desc">1750+ câu phản xạ tổng hợp VPCX cùng bộ lọc chủ đề chuyên ngành.</div>
                                </div>
                            </div>
                            <div class="feature-item">
                                <div class="feature-icon purple"><i class="fas fa-list-check"></i></div>
                                <div class="feature-text">
                                    <div class="feature-title">Chủ đề thực chiến</div>
                                    <div class="feature-desc">Tiến độ, mua hàng, sản xuất, IQC/IPQC/FQC và nhân sự HR.</div>
                                </div>
                            </div>
                            <div class="feature-item">
                                <div class="feature-icon green"><i class="fas fa-user-check"></i></div>
                                <div class="feature-text">
                                    <div class="feature-title">Đăng nhập nhanh</div>
                                    <div class="feature-desc">Tài khoản Google giúp đồng bộ tiến trình học tập dễ dàng.</div>
                                </div>
                            </div>
                        </div>
                        <div class="slide-col slide-preview">
                            <div class="preview-mockup">
                                <div class="preview-bar"></div>
                                <div class="preview-bar short"></div>
                                <div class="preview-card">
                                    <div class="preview-line"></div>
                                    <div class="preview-line short"></div>
                                    <div class="preview-line tiny"></div>
                                </div>
                                <div class="preview-card">
                                    <div class="preview-line"></div>
                                    <div class="preview-line short"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ═══ SLIDE 3: Hướng dẫn ═══ -->
            <div class="intro-slide" data-slide="2">
                <div class="intro-slide-content">
                    <div class="slide-badge"><i class="fas fa-book-open"></i> Hướng dẫn</div>
                    <h2 class="slide-title">Cách Sử Dụng Hiệu Quả</h2>

                    <div class="guide-steps">
                        <div class="guide-step">
                            <div class="guide-step-num">1</div>
                            <div class="guide-step-content">
                                <div class="guide-step-title"><i class="fas fa-search"></i> Tìm câu theo chủ đề</div>
                                <div class="guide-step-desc">Dùng <b>thanh tìm kiếm</b> hoặc bộ lọc <b>HSK</b> / <b>Chủ đề</b>. Bấm trực tiếp vào <b>tag chủ đề</b> trên mỗi câu để lọc nhanh.</div>
                                <div class="guide-step-visual">
                                    <span class="guide-mock-chip"><i class="fas fa-filter"></i> HSK3</span>
                                    <span class="guide-mock-chip active"><i class="fas fa-industry"></i> Máy tính &amp; IT</span>
                                    <span class="guide-mock-chip"><i class="fas fa-search"></i> Tìm kiếm...</span>
                                </div>
                            </div>
                        </div>

                        <div class="guide-step">
                            <div class="guide-step-num">2</div>
                            <div class="guide-step-content">
                                <div class="guide-step-title"><i class="fas fa-volume-up"></i> Nghe phát âm chuẩn</div>
                                <div class="guide-step-desc">Bấm biểu tượng <b>🔊 loa</b> để nghe câu. Chỉnh <b>tốc độ, giọng đọc, cao độ, âm lượng</b> trong cài đặt giọng (nút tai nghe 🎧).</div>
                                <div class="guide-step-visual">
                                    <span class="guide-mock-btn primary"><i class="fas fa-volume-up"></i></span>
                                    <span class="guide-mock-arrow">→</span>
                                    <span class="guide-mock-btn"><i class="fas fa-headphones"></i></span>
                                </div>
                            </div>
                        </div>

                        <div class="guide-step">
                            <div class="guide-step-num">3</div>
                            <div class="guide-step-content">
                                <div class="guide-step-title"><i class="fas fa-keyboard"></i> Luyện gõ phản xạ</div>
                                <div class="guide-step-desc">Bật nút <b>⌨️ bàn phím</b> để hiện ô luyện tập. Gõ câu tiếng Trung → hệ thống <b>chấm điểm tự động</b> từng ký tự.</div>
                                <div class="guide-step-visual">
                                    <span class="guide-mock-input">Gõ tiếng Trung...</span>
                                    <span class="guide-mock-arrow">→</span>
                                    <span class="guide-mock-result correct">我吃饭了 ✓</span>
                                    <span class="guide-mock-result wrong">我喝水 ✗</span>
                                </div>
                            </div>
                        </div>

                        <div class="guide-step">
                            <div class="guide-step-num">4</div>
                            <div class="guide-step-content">
                                <div class="guide-step-title"><i class="fas fa-expand"></i> Luyện tập full màn hình</div>
                                <div class="guide-step-desc">Bấm nút <b>⛶ mở rộng</b> trên mỗi câu. Có thể <b>nhảy câu ngẫu nhiên</b> 🎲, <b>gợi ý 💡</b>, <b>xem đáp án</b>, chấm điểm tự động.</div>
                                <div class="guide-step-visual">
                                    <span class="guide-mock-btn"><i class="fas fa-expand"></i></span>
                                    <span class="guide-mock-arrow">→</span>
                                    <span class="guide-mock-nav">
                                        <i class="fas fa-chevron-left"></i>
                                        <i class="fas fa-chevron-right"></i>
                                        <i class="fas fa-volume-up"></i>
                                        <i class="fas fa-dice"></i>
                                    </span>
                                </div>
                            </div>
                        </div>

                        <div class="guide-step">
                            <div class="guide-step-num">5</div>
                            <div class="guide-step-content">
                                <div class="guide-step-title"><i class="fas fa-pen-fancy"></i> Luyện viết chữ Hán</div>
                                <div class="guide-step-desc">Bấm nút <b>✍️ bút</b> trên mỗi câu → mở công cụ luyện viết. Xem <b>动画 nét viết</b> hoặc <b>tự viết theo nét</b>.</div>
                                <div class="guide-step-visual">
                                    <span class="guide-mock-btn"><i class="fas fa-pen-fancy"></i></span>
                                    <span class="guide-mock-arrow">→</span>
                                    <span class="guide-mock-canvas">字</span>
                                </div>
                            </div>
                        </div>

                        <div class="guide-step">
                            <div class="guide-step-num">6</div>
                            <div class="guide-step-content">
                                <div class="guide-step-title"><i class="fas fa-sliders-h"></i> Tùy chỉnh hiển thị</div>
                                <div class="guide-step-desc">Bấm <b>⚙️ tùy chọn</b> góc phải màn hình để bật/tắt <b>Tiếng Việt</b>, <b>Pinyin</b>, <b>Ô luyện tập</b>, và bật <b>Silent mode</b> 🔕.</div>
                                <div class="guide-step-visual">
                                    <span class="guide-mock-btn"><i class="fas fa-sliders-h"></i></span>
                                    <span class="guide-mock-arrow">→</span>
                                    <span class="guide-mock-toggle active"><i class="fas fa-language"></i></span>
                                    <span class="guide-mock-toggle active"><i class="fas fa-spell-check"></i></span>
                                    <span class="guide-mock-toggle"><i class="fas fa-keyboard"></i></span>
                                    <span class="guide-mock-toggle"><i class="fas fa-bell"></i></span>
                                </div>
                            </div>
                        </div>

                        <div class="guide-step guide-step-tip">
                            <div class="guide-tip-icon"><i class="fas fa-lightbulb"></i></div>
                            <div class="guide-step-content">
                                <div class="guide-step-title">💡 Mẹo học nhanh</div>
                                <div class="guide-step-desc">
                                    • Học <b>10-15 câu/ngày</b>, ôn lại sau 1 ngày → 3 ngày → 7 ngày<br>
                                    • Luôn <b>nghe trước khi gõ</b> để luyện phản xạ âm thanh<br>
                                    • Bấm <b>tag chủ đề</b> để học theo nhóm chủ điểm cùng lúc<br>
                                    • Dùng <b>chế độ ngẫu nhiên 🎲</b> để tránh học vẹt theo thứ tự
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ═══ SLIDE 4: Trial ═══ -->
            <div class="intro-slide" data-slide="3">
                <div class="intro-slide-content">
                    <div class="slide-badge"><i class="fas fa-gift"></i> Dùng thử</div>
                    <h2 class="slide-title">Chương Trình Trải Nghiệm (Trial)</h2>

                    <div class="trial-cards">
                        <div class="trial-card">
                            <div class="trial-card-badge">Ưu đãi</div>
                            <div class="trial-card-icon"><i class="fas fa-calendar-check"></i></div>
                            <div class="trial-card-title">Tặng 3 Ngày Dùng Thử</div>
                            <div class="trial-card-desc">Tài khoản mới được tặng ngay 3 ngày trải nghiệm toàn bộ hệ thống (200 câu đầu tiên, HSK1-5).</div>
                        </div>
                        <div class="trial-card">
                            <div class="trial-card-badge">Tính năng</div>
                            <div class="trial-card-icon"><i class="fas fa-infinity"></i></div>
                            <div class="trial-card-title">Không Giới Hạn</div>
                            <div class="trial-card-desc">Tự do luyện nghe và luyện viết không giới hạn số lần trong suốt thời gian dùng thử.</div>
                        </div>
                        <div class="trial-card">
                            <div class="trial-card-badge">Lưu ý</div>
                            <div class="trial-card-icon"><i class="fas fa-shield-halved"></i></div>
                            <div class="trial-card-title">Cảnh Báo Trình Duyệt</div>
                            <div class="trial-card-desc">Đảm bảo trình duyệt cho phép popup đăng nhập để quá trình xác thực Google diễn ra mượt mà.</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ═══ SLIDE 5: Gói gia hạn ═══ -->
            <div class="intro-slide" data-slide="4">
                <div class="intro-slide-content">
                    <div class="slide-badge"><i class="fas fa-crown"></i> Nâng cấp</div>
                    <h2 class="slide-title">Gói Gia Hạn &amp; Mở Khóa Toàn Bộ</h2>

                    <div class="slide-body two-col">
                        <div class="slide-col">
                            <div class="package-item">
                                <div class="package-icon"><i class="fas fa-calendar-day"></i></div>
                                <div class="package-info">
                                    <div class="package-title">Gói 1 tháng <span class="package-price">50.000đ</span></div>
                                    <div class="package-desc">Phù hợp học thử ngắn hạn hoặc ôn tập.</div>
                                </div>
                            </div>
                            <div class="package-item">
                                <div class="package-icon hot"><i class="fas fa-fire"></i></div>
                                <div class="package-info">
                                    <div class="package-title">Gói 3 tháng <span class="package-price">120.000đ</span><span class="package-badge">Phổ biến</span></div>
                                    <div class="package-desc">Tiết kiệm 33%, lựa chọn phổ biến cho người học đều đặn.</div>
                                </div>
                            </div>
                            <div class="package-item">
                                <div class="package-icon"><i class="fas fa-calendar-alt"></i></div>
                                <div class="package-info">
                                    <div class="package-title">Gói 1 năm <span class="package-price">300.000đ</span><span class="package-badge save">Tiết kiệm 58%</span></div>
                                    <div class="package-desc">Tiết kiệm 58% cho lộ trình dài hạn.</div>
                                </div>
                            </div>
                            <div class="package-item premium">
                                <div class="package-icon premium"><i class="fas fa-crown"></i></div>
                                <div class="package-info">
                                    <div class="package-title">Gói Premium Vĩnh Viễn <span class="package-price">1.000.000đ</span><span class="package-badge forever">Vĩnh viễn</span></div>
                                    <div class="package-desc">Sở hữu mãi mãi, Admin hỗ trợ trực tiếp.</div>
                                </div>
                            </div>
                        </div>
                        <div class="slide-col slide-preview">
                            <div class="qr-preview">
                                <div class="qr-box"><i class="fas fa-qrcode"></i></div>
                                <div class="qr-caption">Thanh toán qua QR ngân hàng<br><strong>Xác nhận tự động</strong></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ═══ SLIDE 6: CTA ═══ -->
            <div class="intro-slide" data-slide="5">
                <div class="intro-slide-content cta-slide">
                    <div class="cta-icon"><i class="fas fa-rocket"></i></div>
                    <h2 class="cta-title">Bắt Đầu Học Ngay Hôm Nay!</h2>
                    <p class="cta-desc">Nâng cấp tài khoản để mở khóa toàn bộ nội dung và chinh phục tiếng Trung văn phòng - công xưởng.</p>
                    <div class="cta-message">
                        <i class="fas fa-graduation-cap"></i>
                        Chúc bạn học tốt &amp; thành công trong công việc!
                    </div>
                    <div class="cta-actions">
                        <button class="cta-btn secondary" onclick="closeIntroModal()">
                            <i class="fas fa-times"></i> Đóng
                        </button>
                        <button class="cta-btn primary" id="ctaMainBtn" onclick="handleCtaAction()">
                            <i class="fas fa-sign-in-alt"></i> <span id="ctaBtnText">Đăng nhập ngay</span>
                        </button>
                    </div>
                </div>
            </div>

        </div>

        <button class="intro-nav prev" id="introPrev" aria-label="Trước">
            <i class="fas fa-chevron-left"></i>
        </button>
        <button class="intro-nav next" id="introNext" aria-label="Sau">
            <i class="fas fa-chevron-right"></i>
        </button>

        <div class="intro-footer">
            <div class="intro-counter">
                <span id="introCurrent">1</span> / <span id="introTotal">6</span>
            </div>
            <div class="intro-dots" id="introDots">
                <button class="intro-dot active" data-index="0"></button>
                <button class="intro-dot" data-index="1"></button>
                <button class="intro-dot" data-index="2"></button>
                <button class="intro-dot" data-index="3"></button>
                <button class="intro-dot" data-index="4"></button>
                <button class="intro-dot" data-index="5"></button>
            </div>
        </div>
    </div>
</div>
"""


# ═══════════════════════════════════════════════════════════════════
#  JS
# ═══════════════════════════════════════════════════════════════════
def build_intro_js():
    return r"""
/* ═══════════════════════════════════════════════════════════════ */
/* QUICK INTRO BANNER                                              */
/* ═══════════════════════════════════════════════════════════════ */
function initQuickIntroBanner() {
    var banner = $('quickIntroBanner');
    var dismiss = $('quickIntroDismiss');
    if (!banner) return;

    var hidden = false;
    try { hidden = localStorage.getItem('quick_intro_dismissed') === '1'; } catch(e) {}
    if (hidden) { banner.classList.add('dismissed'); return; }

    if (dismiss) {
        dismiss.addEventListener('click', function() {
            banner.classList.add('dismissed');
            try { localStorage.setItem('quick_intro_dismissed', '1'); } catch(e) {}
        });
    }
}

function resetQuickIntroBanner() {
    try { localStorage.removeItem('quick_intro_dismissed'); } catch(e) {}
    var banner = $('quickIntroBanner');
    if (banner) banner.classList.remove('dismissed');
}

/* ═══════════════════════════════════════════════════════════════ */
/* INTRO SLIDES — Điều khiển modal giới thiệu                       */
/* ═══════════════════════════════════════════════════════════════ */
var introCurrentSlide = 0;
var introTotalSlides = 6;

window.openIntroModal = function() {
    var modal = $('introModal');
    if (!modal) return;
    introCurrentSlide = 0;
    updateIntroSlides();
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
    updateIntroCta();
};

window.closeIntroModal = function() {
    var modal = $('introModal');
    if (!modal) return;
    modal.classList.remove('show');
    document.body.style.overflow = '';
};

function updateIntroSlides() {
    var slides = document.querySelectorAll('.intro-slide');
    slides.forEach(function(s, i) {
        s.classList.remove('active', 'prev');
        if (i === introCurrentSlide) s.classList.add('active');
        else if (i < introCurrentSlide) s.classList.add('prev');
    });

    document.querySelectorAll('.intro-dot').forEach(function(dot, i) {
        dot.classList.toggle('active', i === introCurrentSlide);
    });

    var curEl = $('introCurrent');
    if (curEl) curEl.textContent = introCurrentSlide + 1;

    var prevBtn = $('introPrev');
    var nextBtn = $('introNext');
    if (prevBtn) prevBtn.disabled = (introCurrentSlide === 0);
    if (nextBtn) nextBtn.disabled = (introCurrentSlide === introTotalSlides - 1);
}

window.introGoTo = function(index) {
    if (index < 0 || index >= introTotalSlides) return;
    introCurrentSlide = index;
    updateIntroSlides();
};

window.introNext = function() {
    if (introCurrentSlide < introTotalSlides - 1) {
        introCurrentSlide++;
        updateIntroSlides();
    }
};

window.introPrev = function() {
    if (introCurrentSlide > 0) {
        introCurrentSlide--;
        updateIntroSlides();
    }
};

function updateIntroCta() {
    var btn = $('ctaMainBtn');
    var btnText = $('ctaBtnText');
    if (!btn || !btnText) return;

    var isLoggedIn = (typeof currentUser !== 'undefined' && currentUser);

    if (isLoggedIn) {
        btn.innerHTML = '<i class="fas fa-play"></i> <span id="ctaBtnText">Bắt đầu học</span>';
        btn.onclick = function() { closeIntroModal(); };
    } else {
        btn.innerHTML = '<i class="fas fa-sign-in-alt"></i> <span id="ctaBtnText">Đăng nhập ngay</span>';
        btn.onclick = function() {
            closeIntroModal();
            if (typeof showLoginModal === 'function') {
                setTimeout(showLoginModal, 300);
            }
        };
    }
}

window.handleCtaAction = function() {
    var isLoggedIn = (typeof currentUser !== 'undefined' && currentUser);
    closeIntroModal();
    if (!isLoggedIn && typeof showLoginModal === 'function') {
        setTimeout(showLoginModal, 300);
    }
};

function initIntroModal() {
    var btn = $('introBtn');
    var modal = $('introModal');
    var closeBtn = $('introClose');
    var prevBtn = $('introPrev');
    var nextBtn = $('introNext');

    if (btn) btn.addEventListener('click', openIntroModal);
    if (closeBtn) closeBtn.addEventListener('click', closeIntroModal);
    if (prevBtn) prevBtn.addEventListener('click', introPrev);
    if (nextBtn) nextBtn.addEventListener('click', introNext);

    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) closeIntroModal();
        });
    }

    document.querySelectorAll('.intro-dot').forEach(function(dot) {
        dot.addEventListener('click', function() {
            introGoTo(parseInt(this.dataset.index));
        });
    });

    document.addEventListener('keydown', function(e) {
        if (!modal || !modal.classList.contains('show')) return;
        if (e.key === 'Escape') { closeIntroModal(); return; }
        if (e.key === 'ArrowRight') introNext();
        if (e.key === 'ArrowLeft') introPrev();
    });

    var touchStartX = 0;
    var touchStartY = 0;
    if (modal) {
        modal.addEventListener('touchstart', function(e) {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        }, { passive: true });

        modal.addEventListener('touchend', function(e) {
            var dx = e.changedTouches[0].clientX - touchStartX;
            var dy = e.changedTouches[0].clientY - touchStartY;
            if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy)) {
                if (dx < 0) introNext();
                else introPrev();
            }
        }, { passive: true });
    }

    updateIntroSlides();
}

function maybeAutoOpenIntro() {
    try {
        var seen = localStorage.getItem('intro_seen');
        if (seen === '1') return;
        var isGuest = !(typeof currentUser !== 'undefined' && currentUser);
        if (!isGuest) return;
        setTimeout(function() {
            openIntroModal();
            try { localStorage.setItem('intro_seen', '1'); } catch(e) {}
        }, 1500);
    } catch(e) {}
}

/* Init khi DOM ready */
if (typeof window.initApp === 'function') {
    var _origInitApp = window.initApp;
    window.initApp = function() {
        _origInitApp.apply(this, arguments);
        initIntroModal();
        initQuickIntroBanner();
        maybeAutoOpenIntro();
    };
}
"""
