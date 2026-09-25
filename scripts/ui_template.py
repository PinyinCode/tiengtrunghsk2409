function showOnboardingActiveBanner(topics, count) {
    var old = $('onboardingActiveBanner');
    if (old) old.remove();

    var mainContent = $('mainContent');
    if (!mainContent) return;
    var container = mainContent.querySelector('.container');
    if (!container) return;

    var info = getTierInfo();
    var totalAvailable = RAW_DATA.length;

    var cfg = getOnboardingConfig();
    var isUnlimitedTier = (info.tier === 'active')
                       || (cfg && (cfg.max_questions === -1 || cfg.max_questions === Infinity));

    var lockedCount = isUnlimitedTier ? 0 : Math.max(0, totalAvailable - count);
    var isLimited = (info.tier !== 'active');

    var lockedIndustryCount = 0;
    if (typeof DATASET_REGISTRY !== 'undefined' && DATASET_REGISTRY) {
        Object.keys(DATASET_REGISTRY).forEach(function(id) {
            if (id === 'tonghop') return;
            if (!canAccessChuyenNganh()) lockedIndustryCount++;
        });
    }

    var allowedHskForStats;
    if (cfg && cfg.hsk_allowed && Array.isArray(cfg.hsk_allowed) && cfg.hsk_allowed.length > 0) {
        allowedHskForStats = cfg.hsk_allowed.map(function(n) { return 'HSK' + n; });
    } else {
        allowedHskForStats = getAllowedHskList();
    }
    var maxQForStats = (cfg && cfg.max_questions > 0) ? cfg.max_questions : info.maxQuestions;
    var lockStats = computeLockStats(topics, allowedHskForStats, maxQForStats, isUnlimitedTier);

    var banner = document.createElement('div');
    banner.id = 'onboardingActiveBanner';
    banner.className = 'onboarding-active-banner';

    var isAuto = !!window.__onboardingAutoPicked;
    var iconHtml = isAuto ? '<i class="fas fa-magic"></i>' : '<i class="fas fa-star"></i>';
    var labelText = isAuto ? 'Chủ đề gợi ý cho bạn:' : 'Chủ đề của bạn:';

    var iconSpan = document.createElement('span');
    iconSpan.className = 'ob-icon';
    iconSpan.innerHTML = iconHtml;
    banner.appendChild(iconSpan);

    var labelSpan = document.createElement('span');
    labelSpan.className = 'ob-label';
    labelSpan.textContent = labelText;
    banner.appendChild(labelSpan);

    var MAX_VISIBLE_CHIPS = 5;
    var visibleTopics = topics.slice(0, MAX_VISIBLE_CHIPS);
    var hiddenCount = Math.max(0, topics.length - MAX_VISIBLE_CHIPS);

    var chipsWrap = document.createElement('span');
    chipsWrap.className = 'ob-chips';

    visibleTopics.forEach(function(t) {
        var chip = document.createElement('span');
        chip.className = 'ob-chip';
        chip.textContent = t.normalize ? t.normalize('NFC') : t;
        chipsWrap.appendChild(chip);
    });

    if (hiddenCount > 0) {
        var moreChip = document.createElement('span');
        moreChip.className = 'ob-chip ob-chip-more';
        moreChip.textContent = '+' + hiddenCount + ' chủ đề khác';
        moreChip.title = topics.join(' · ');
        moreChip.setAttribute('data-tooltip', topics.join(' · '));
        moreChip.style.cursor = 'help';
        chipsWrap.appendChild(moreChip);
    }

    banner.appendChild(chipsWrap);

    var countSpan = document.createElement('span');
    countSpan.className = 'ob-count';
    if (isUnlimitedTier) {
        countSpan.textContent = '(toàn bộ ' + count + ' câu)';
    } else {
        countSpan.textContent = '(' + count + ' câu)';
    }
    banner.appendChild(countSpan);

    var changeBtn = document.createElement('button');
    changeBtn.type = 'button';
    changeBtn.id = 'onboardingChangeBtn';
    changeBtn.className = 'ob-change-btn';
    changeBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Đổi';
    changeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        onChangeTopicsClick();
    });
    banner.appendChild(changeBtn);

    if (isLimited) {
        var statsBar = document.createElement('div');
        statsBar.className = 'ob-stats-bar ob-stats-inline';

        /* STAT 1: Số câu đang có / tổng */
        if (lockedCount > 0) {
            var stat1 = document.createElement('span');
            stat1.className = 'ob-stat-inline';
            stat1.innerHTML =
                '<i class="fas fa-database"></i>' +
                '<b>' + count + '</b>/' + totalAvailable + ' câu';
            statsBar.appendChild(stat1);
        }

        /* STAT 2: Số chủ đề chưa mở khoá */
        if (lockStats.lockedTopics > 0) {
            var stat2 = document.createElement('span');
            stat2.className = 'ob-stat-inline ob-stat-inline-topics';
            stat2.innerHTML =
                '<i class="fas fa-folder-minus"></i>' +
                '<b>' + lockStats.lockedTopics + '</b> chủ đề khoá';
            statsBar.appendChild(stat2);
        }

        /* STAT 3: Số chuyên ngành chưa mở */
        if (lockedIndustryCount > 0) {
            var stat3 = document.createElement('span');
            stat3.className = 'ob-stat-inline ob-stat-inline-industry';
            stat3.innerHTML =
                '<i class="fas fa-industry"></i>' +
                '<b>' + lockedIndustryCount + '</b> chuyên ngành khoá';
            statsBar.appendChild(stat3);
        }

        /* CTA */
        var shouldShowCta = false;
        var ctaLabel = '';
        var ctaIcon = '';
        var ctaAction = null;

        if (info.tier === 'trial') {
            var expiryEl = $('expiryBanner');
            var expiryVisible = false;
            if (expiryEl) {
                var displayStyle = window.getComputedStyle(expiryEl).display;
                expiryVisible = (expiryEl.style.display !== 'none' && displayStyle !== 'none');
            }
            if (!expiryVisible) {
                shouldShowCta = true;
                ctaLabel = 'Nâng cấp';
                ctaIcon = 'fas fa-gem';
                ctaAction = function() {
                    if (typeof openRenewalModal === 'function') openRenewalModal();
                };
            }
        }

        var hasAnyLock = (lockedCount > 0) || (lockedIndustryCount > 0) || (lockStats.lockedTopics > 0);

        if (hasAnyLock && shouldShowCta) {
            var ctaBtn = document.createElement('button');
            ctaBtn.type = 'button';
            ctaBtn.className = 'ob-cta-btn';
            ctaBtn.innerHTML = '<i class="' + ctaIcon + '"></i> ' + ctaLabel;
            ctaBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                if (typeof ctaAction === 'function') ctaAction();
            });
            statsBar.appendChild(ctaBtn);
        }

        if (statsBar.children.length > 0) {
            banner.appendChild(statsBar);
        }
    }

    container.insertBefore(banner, container.firstChild);
}
function initOnboarding() {
    var startBtn = $('onboardingStartBtn');
    var skipBtn = $('onboardingSkipBtn');
    var closeBtn = $('onboardingCloseBtn');

    if (startBtn) startBtn.addEventListener('click', onOnboardingStart);
    if (skipBtn)  skipBtn.addEventListener('click', onOnboardingSkip);

    if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            onOnboardingSkip();
        });
    }

    document.addEventListener('keydown', function(e) {
        if (e.key !== 'Escape') return;
        var modal = $('onboardingModal');
        if (modal && modal.classList.contains('show')) {
            onOnboardingSkip();
        }
    });

    var modal = $('onboardingModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                onOnboardingSkip();
            }
        });
    }

    setTimeout(maybeShowOnboarding, 500);
}

window.maybeShowOnboarding = maybeShowOnboarding;
window.showOnboardingModal = showOnboardingModal;
window.applyOnboardingSelection = applyOnboardingSelection;
window.onChangeTopicsClick = onChangeTopicsClick;

/* ============================================================ */
/* TIKTOK BAR RESPONSIVE                                         */
/* ============================================================ */
function moveTikTokBarToHeader() {
    try {
        if (window.innerWidth < 769) return;
        var headerInner = document.querySelector('.header-inner');
        var headerActions = document.querySelector('.header-actions');
        var tiktokBar = document.querySelector('.sticky-top .container > .tiktok-bar');
        if (!headerInner || !headerActions || !tiktokBar) return;
        headerInner.insertBefore(tiktokBar, headerActions);
        setTimeout(function() { checkHeaderOverflow(); }, 100);
    } catch(e) {}
}

function moveTikTokBarBelowHeader() {
    try {
        var headerInner = document.querySelector('.header-inner');
        var tiktokBar = headerInner ? headerInner.querySelector('.tiktok-bar') : null;
        var container = document.querySelector('.sticky-top .container');
        var header = container ? container.querySelector('.header') : null;
        if (!tiktokBar || !container || !header) return;
        if (header.nextSibling) {
            container.insertBefore(tiktokBar, header.nextSibling);
        } else {
            container.appendChild(tiktokBar);
        }
    } catch(e) {}
}

function checkHeaderOverflow() {
    try {
        if (window.innerWidth < 769) return;
        var headerInner = document.querySelector('.header-inner');
        if (!headerInner) return;
        var tiktok = headerInner.querySelector('.tiktok-bar');
        if (!tiktok) return;
        tiktok.style.display = '';
    } catch(e) {}
}

var _lastWidthMode = null;
function handleResponsiveTikTok() {
    var currentMode = window.innerWidth >= 769 ? 'desktop' : 'mobile';
    if (currentMode === _lastWidthMode) return;
    _lastWidthMode = currentMode;
    if (currentMode === 'desktop') moveTikTokBarToHeader();
    else moveTikTokBarBelowHeader();
}

function populateTikTokFloat() {
    try {
        var pfTiktok = $('pfTiktokFloat');
        if (!pfTiktok) return;
        var tiktokUrl = (typeof TIKTOK_URL !== 'undefined' && TIKTOK_URL) ? TIKTOK_URL : '';
        if (!tiktokUrl) { pfTiktok.style.display = 'none'; return; }
        pfTiktok.href = tiktokUrl;
        var avatarUrl = (typeof TIKTOK_AVATAR !== 'undefined' && TIKTOK_AVATAR) ? TIKTOK_AVATAR : '';
        var avatarEl = $('pfTiktokAvatar');
        if (avatarEl) {
            if (avatarUrl) { avatarEl.src = avatarUrl; avatarEl.style.display = ''; }
            else { avatarEl.style.display = 'none'; }
        }
        var displayName = '';
        if (typeof TIKTOK_NICKNAME !== 'undefined' && TIKTOK_NICKNAME) displayName = TIKTOK_NICKNAME;
        else if (typeof TIKTOK_USERNAME !== 'undefined' && TIKTOK_USERNAME) displayName = TIKTOK_USERNAME;
        else displayName = 'TikTok';
        var nameEl = $('pfTiktokName');
        if (nameEl) nameEl.textContent = displayName;
        pfTiktok.title = 'Theo dõi TikTok: ' + displayName;
    } catch(e) {}
}

/* ============================================================ */
/* INIT APP                                                      */
/* ============================================================ */
function initApp() {
    mobileWrapper = $('mobileWrapper');
    $('loadingScreen').classList.add('hidden');
    $('stickyTop').style.display = 'block';
    $('fabGroup').style.display = 'flex';
    $('mainContent').style.display = 'block';

    loadVoiceSettings();
    initDatasetSelector();

    if (typeof initSocial === 'function') initSocial();
    if (typeof updateFloatingLeftVisibility === 'function') updateFloatingLeftVisibility();
    if (typeof initAuthUI === 'function') initAuthUI();
    initScrollDetection();
    initFabGroup();
    initTheme();
    initDisplayState();
    initSpeech();
    initWriter();
    initPracticeFull();
    initVoiceSettings();
    initOnboarding();

    _lastWidthMode = window.innerWidth >= 769 ? 'desktop' : 'mobile';
    if (_lastWidthMode === 'desktop') moveTikTokBarToHeader();
    populateTikTokFloat();

    var _resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(_resizeTimer);
        _resizeTimer = setTimeout(function() {
            handleResponsiveTikTok();
            checkHeaderOverflow();
        }, 200);
    });

    $('searchInput').addEventListener('input', applyFilter);
    $('resetBtn').addEventListener('click', function() {
        $('searchInput').value = '';
        $('hskFilter').value = '';
        $('subjectFilter').value = '';
        window.__onboardingOverride = null;
        var obBanner = $('onboardingActiveBanner');
        if (obBanner) obBanner.remove();
        applyFilter();
    });
    $('clearSearchBtn').addEventListener('click', function() {
        $('searchInput').value = '';
        state.search = '';
        $('searchInput').focus();
        applyFilter();
        this.classList.remove('show');
    });
    $('hskFilter').addEventListener('change', function() {
        var val = this.value;
        var allowed = getAllowedHskList();
        if (val && allowed.indexOf(val) === -1) {
            var info = getTierInfo();
            var msg = info.tier === 'trial'
                ? 'Bản Trial chỉ cho phép lọc HSK1-' + info.maxHSK + '.'
                : 'Bản Demo chỉ cho phép lọc HSK1-' + info.maxHSK + '.';
            alert(msg);
            this.value = '';
            applyFilter();
            return;
        }
        applyFilter();
    });
    $('subjectFilter').addEventListener('change', function() {
        var val = this.value;
        var allowed = getAllowedSubjectList();
        if (val && allowed.indexOf(val) === -1) {
            var info = getTierInfo();
            var msg = info.tier === 'trial'
                ? 'Chủ đề này chưa có trong ' + info.maxQuestions + ' câu Trial.'
                : 'Chủ đề này chưa có trong ' + info.maxQuestions + ' câu Demo.';
            alert(msg);
            this.value = '';
            applyFilter();
            return;
        }
        applyFilter();
    });

    try { buildFilters(); applyFilter(); }
    catch(e) { console.error('Init error:', e); }
}

function refreshApp() {
    buildFilters();
    applyFilter();
    applyDisplayState();
    updateToggleButtons();
    updateResultCount();
    updateTierBadge();
    updateDemoBanner();

    if (typeof maybeShowOnboarding === 'function') {
        setTimeout(maybeShowOnboarding, 800);
    }
}

function updateTierBadge() {
    var badge = $('trialBadge');
    if (!badge) return;
    var info = getTierInfo();
    if (info.tier === 'trial') {
        badge.classList.add('show');
        var daysLeft = null;
        if (typeof getDaysRemaining === 'function'
            && typeof currentUser !== 'undefined'
            && currentUser) {
            daysLeft = getDaysRemaining(currentUser);
        }
        var badgeText = $('trialBadgeText');
        if (badgeText) {
            if (daysLeft !== null && daysLeft > 0) {
                badgeText.textContent = 'Trial · ' + daysLeft + ' ngày';
            } else {
                badgeText.textContent = 'Trial';
            }
        }
    } else {
        badge.classList.remove('show');
    }
}

function updateDemoBanner() {
    var info = getTierInfo();
    var banner = $('demoBanner');
    if (!banner) return;
    if (info.tier !== 'demo' && info.tier !== 'expired') return;
    var titleEl = $('demoBannerTitle');
    var descEl  = $('demoBannerDesc');
    var btnEl   = $('demoBannerBtn');
    var btnText = $('demoBannerBtnText');
    var iconEl  = banner.querySelector('.demo-banner-icon');

    if (info.tier === 'expired') {
        if (titleEl) titleEl.innerHTML = 'Tài khoản đã hết hạn';
        if (descEl) {
            descEl.innerHTML = 'Bạn đang xem chế độ giới hạn (' +
                info.maxQuestions + ' câu đầu, HSK1-' + info.maxHSK + ', ' +
                DEMO_DAILY_LIMIT + ' lượt/ngày).<br>Gia hạn để mở khóa toàn bộ ' +
                (typeof RAW_DATA !== 'undefined' ? RAW_DATA.length : '') + ' câu!';
        }
        if (btnEl) {
            btnEl.onclick = function() {
                if (typeof openRenewalModal === 'function') openRenewalModal();
            };
            btnEl.setAttribute('onclick', '');
        }
        if (btnText) btnText.textContent = 'Gia hạn ngay';
        if (iconEl) iconEl.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
        banner.style.background = 'linear-gradient(135deg, #fecaca, #fca5a5)';
        banner.style.borderColor = '#dc2626';
    } else {
        if (titleEl) titleEl.innerHTML = 'Đăng nhập miễn phí để mở khóa toàn bộ';
        if (descEl) {
            descEl.innerHTML = 'Đăng nhập bằng <b>Gmail</b> để xem <b>toàn bộ kho câu</b>, ' +
                'không giới hạn nghe và luyện viết.<br>' +
                'Nghe + Luyện viết còn lại hôm nay: ' +
                '<b id="demoRemainingText" style="color:#16a34a">' + getDemoRemaining() + '</b> lượt.';
        }
        if (btnText) btnText.textContent = 'Đăng nhập bằng Gmail';
        if (iconEl) iconEl.innerHTML = '<i class="fas fa-gift"></i>';
        banner.style.background = '';
        banner.style.borderColor = '';
    }
}

/* ============================================================ */
/* SCROLL / FAB / THEME / DISPLAY                                */
/* ============================================================ */
function initScrollDetection() {
    var sticky = $('stickyTop');
    if (!sticky) return;
    var ticking = false;
    function update() {
        if (window.scrollY > 5) sticky.classList.add('scrolled');
        else sticky.classList.remove('scrolled');
        ticking = false;
    }
    window.addEventListener('scroll', function() {
        if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
}

function initFabGroup() {
    var fabGroup = $('fabGroup');
    var fabMainBtn = $('fabMainBtn');
    if (!fabGroup || !fabMainBtn) return;

    var closedFlag = null;
    try { closedFlag = sessionStorage.getItem('fabClosed'); } catch(_e) {}

    var fabOpen = (closedFlag !== '1');
    fabGroup.classList.toggle('open', fabOpen);

    fabMainBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        fabOpen = !fabOpen;
        fabGroup.classList.toggle('open', fabOpen);
        try { sessionStorage.setItem('fabClosed', fabOpen ? '0' : '1'); } catch(_e) {}
    });

    document.addEventListener('click', function(e) {
        if (!fabGroup.contains(e.target) && fabOpen && window.innerWidth > 768) {
            fabOpen = false;
            fabGroup.classList.remove('open');
            try { sessionStorage.setItem('fabClosed', '1'); } catch(_e) {}
        }
    });
}

function initTheme() {
    try {
        var saved = localStorage.getItem('theme');
        if (saved) document.documentElement.setAttribute('data-theme', saved);
        else document.documentElement.setAttribute('data-theme', 'light');
    } catch(e) {}
    updateThemeIcon();
    $('themeToggle').addEventListener('click', function() {
        var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        var newTheme = isDark ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        try { localStorage.setItem('theme', newTheme); } catch(e) {}
        updateThemeIcon();
    });
}

function updateThemeIcon() {
    var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    var icon = $('themeToggle').querySelector('i');
    icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
}

function initDisplayState() {
    try {
        var saved = localStorage.getItem('displayState');
        if (saved) {
            var parsed = JSON.parse(saved);
            displayState.vi = parsed.vi !== false;
            displayState.pinyin = !!parsed.pinyin;
            displayState.practice = !!parsed.practice;
        }
    } catch(e) {}
    var focusHidden = false;
    try { focusHidden = localStorage.getItem('focusHidden') === 'true'; } catch(e) {}
    if (focusHidden) document.body.classList.add('hide-floating');
    updateFocusBtnIcon();
    if (displayState.practice) { displayState.pinyin = false; displayState.vi = true; }
    applyDisplayState();
    updateToggleButtons();

    $('toggleViBtn').addEventListener('click', function(e) {
        e.stopPropagation();
        displayState.vi = !displayState.vi;
        applyDisplayState(); saveDisplayState(); updateToggleButtons();
    });
    $('togglePinyinBtn').addEventListener('click', function(e) {
        e.stopPropagation();
        displayState.pinyin = !displayState.pinyin;
        if (displayState.pinyin && displayState.practice) displayState.practice = false;
        applyDisplayState(); saveDisplayState(); updateToggleButtons();
    });
    $('togglePracticeBtn').addEventListener('click', function(e) {
        e.stopPropagation();
        displayState.practice = !displayState.practice;
        if (displayState.practice) { displayState.pinyin = false; displayState.vi = true; }
        applyDisplayState(); saveDisplayState(); updateToggleButtons();
    });
    var toggleFocusBtn = $('toggleFocusBtn');
    if (toggleFocusBtn) {
        toggleFocusBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            var isHidden = document.body.classList.toggle('hide-floating');
            try { localStorage.setItem('focusHidden', isHidden ? 'true' : 'false'); } catch(e) {}
            updateFocusBtnIcon();
        });
    }
}

function updateFocusBtnIcon() {
    var btn = $('toggleFocusBtn');
    if (!btn) return;
    var isHidden = document.body.classList.contains('hide-floating');
    var icon = btn.querySelector('i');
    if (isHidden) {
        icon.className = 'fas fa-bell-slash';
        btn.classList.remove('active');
    } else {
        icon.className = 'fas fa-bell';
        btn.classList.add('active');
    }
}

function applyDisplayState() {
    document.body.classList.toggle('show-vi', displayState.vi);
    document.body.classList.toggle('show-pinyin', displayState.pinyin);
    document.body.classList.toggle('show-practice', displayState.practice);
    if (displayState.practice) {
        document.querySelectorAll('.card-check').forEach(function(c) { c.innerHTML = ''; });
        document.querySelectorAll('.practice-input').forEach(function(i) {
            i.value = '';
            var answer = i.dataset.answer || '';
            updateInlinePreview(i, answer);
        });
    }
}

function saveDisplayState() {
    try { localStorage.setItem('displayState', JSON.stringify(displayState)); } catch(e) {}
}

function updateToggleButtons() {
    $('toggleViBtn').classList.toggle('active', displayState.vi);
    $('togglePinyinBtn').classList.toggle('active', displayState.pinyin);
    $('togglePracticeBtn').classList.toggle('active', displayState.practice);
    updateFocusBtnIcon();
}

window.toggleFocus = function(stt, element) {
    if (focusedStt === stt) { clearFocus(); return; }
    clearFocus();
    focusedStt = stt;
    element.classList.add('focused', 'tapped');
    setTimeout(function() { if (element) element.classList.remove('tapped'); }, 600);
};

window.clearFocus = function() {
    document.querySelectorAll('.focused').forEach(function(el) {
        el.classList.remove('focused', 'tapped');
    });
    focusedStt = null;
};

document.addEventListener('click', function(e) {
    if (e.target.closest('.card')) return;
    if (e.target.closest('.practice-input') || e.target.closest('.audio-btn') ||
        e.target.closest('.write-btn') || e.target.closest('.chip') ||
        e.target.closest('.fab-group') || e.target.closest('.icon-btn') ||
        e.target.closest('.search-bar') || e.target.closest('.filters') ||
        e.target.closest('.search-filter-row') ||
        e.target.closest('.writer-modal') || e.target.closest('.user-menu') ||
        e.target.closest('.login-modal') || e.target.closest('.admin-modal') ||
        e.target.closest('.practice-full-modal') || e.target.closest('.import-modal') ||
        e.target.closest('.edit-modal') || e.target.closest('.zalo-btn') ||
        e.target.closest('.tiktok-float-wrap') || e.target.closest('.tiktok-bar') ||
        e.target.closest('.renewal-modal') || e.target.closest('.voice-modal') ||
        e.target.closest('.dataset-selector') ||
        e.target.closest('.onboarding-modal') ||
        e.target.closest('.onboarding-active-banner') ||
        e.target.closest('.tag-clickable') ||
        e.target.closest('.toggle-check-btn')) return;
    clearFocus();
}, true);

/* ============================================================ */
/* SPEECH                                                        */
/* ============================================================ */
function initSpeech() {
    if ('speechSynthesis' in window) {
        speechSynthesis.getVoices();
        if (speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = function(){
                populateVoiceSelect();
            };
        }
    }
}

window.speakText = function(text, btn, evt) {
    if (evt) evt.stopPropagation();
    if (!canUseFeature()) { showLimitMessage(); return; }
    if (!('speechSynthesis' in window)) { alert('Trình duyệt không hỗ trợ phát âm.'); return; }
    if (shouldCountUsage()) { incDemoUsage(); updateDemoRemaining(); }
    speechSynthesis.cancel();
    if (currentBtn) currentBtn.classList.remove('speaking');
    if (btn) { btn.classList.add('speaking'); currentBtn = btn; }
    var utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'zh-CN';
    applyVoiceSettings(utterance);
    utterance.onend = utterance.onerror = function() {
        if (currentBtn) { currentBtn.classList.remove('speaking'); currentBtn = null; }
    };
    setTimeout(function(){ speechSynthesis.speak(utterance); }, 50);
};

document.addEventListener('visibilitychange', function() {
    if (document.hidden && 'speechSynthesis' in window) {
        speechSynthesis.cancel();
        if (currentBtn) { currentBtn.classList.remove('speaking'); currentBtn = null; }
    }
});

function populateVoiceSelect() {
    if (!('speechSynthesis' in window)) return;
    var sel = $('voiceSelect');
    if (!sel) return;
    var voices = speechSynthesis.getVoices();
    var zhVoices = voices.filter(function(v) {
        return v.lang && v.lang.toLowerCase().indexOf('zh') === 0;
    });
    if (!zhVoices.length) {
        sel.innerHTML = '<option value="">-- Đang tải giọng đọc... --</option>';
        return;
    }
    sel.innerHTML = '';
    var defaultOpt = document.createElement('option');
    defaultOpt.value = '';
    defaultOpt.textContent = '-- Tự động (mặc định) --';
    sel.appendChild(defaultOpt);

    zhVoices.forEach(function(v) {
        var opt = document.createElement('option');
        opt.value = v.voiceURI;
        var label = v.name + ' (' + v.lang + ')' + (v.localService ? '' : ' - online');
        opt.textContent = label;
        sel.appendChild(opt);
    });
    sel.value = voiceState.voiceURI || '';
}

function updateVoiceUI() {
    var rateSlider = $('voiceRateSlider');
    var rateVal    = $('voiceRateValue');
    var pitchSlider = $('voicePitchSlider');
    var pitchVal   = $('voicePitchValue');
    var volSlider  = $('voiceVolumeSlider');
    var volVal     = $('voiceVolumeValue');
    if (rateSlider)  rateSlider.value  = voiceState.rate;
    if (rateVal)     rateVal.textContent = voiceState.rate.toFixed(2) + '×';
    if (pitchSlider) pitchSlider.value = voiceState.pitch;
    if (pitchVal)    pitchVal.textContent = voiceState.pitch.toFixed(2);
    if (volSlider)   volSlider.value   = voiceState.volume;
    if (volVal)      volVal.textContent = Math.round(voiceState.volume * 100) + '%';

    document.querySelectorAll('.voice-preset-btn').forEach(function(b) {
        var r = parseFloat(b.dataset.rate);
        b.classList.toggle('active', Math.abs(r - voiceState.rate) < 0.001);
    });
}

function voiceTestSpeak() {
    if (!('speechSynthesis' in window)) { alert('Trình duyệt không hỗ trợ phát âm.'); return; }
    speechSynthesis.cancel();
    var btn = $('voiceTestBtn');
    if (btn) {
        btn.classList.add('speaking');
        btn.innerHTML = '<i class="fas fa-stop"></i> Đang đọc...';
    }
    var u = new SpeechSynthesisUtterance('你好，欢迎学习中文。');
    u.lang = 'zh-CN';
    applyVoiceSettings(u);
    var finish = function() {
        if (btn) {
            btn.classList.remove('speaking');
            btn.innerHTML = '<i class="fas fa-play"></i> Nghe thử';
        }
    };
    u.onend = finish;
    u.onerror = finish;
    setTimeout(function(){ try { speechSynthesis.speak(u); } catch(e) { finish(); } }, 30);
}

function initVoiceSettings() {
    var modal = $('voiceModal');
    if (!modal) return;

    populateVoiceSelect();

    var rateSlider = $('voiceRateSlider');
    var pitchSlider = $('voicePitchSlider');
    var volSlider = $('voiceVolumeSlider');

    updateVoiceUI();

    if (rateSlider) rateSlider.addEventListener('input', function() {
        voiceState.rate = parseFloat(this.value);
        $('voiceRateValue').textContent = voiceState.rate.toFixed(2) + '×';
        document.querySelectorAll('.voice-preset-btn').forEach(function(b) {
            b.classList.toggle('active', Math.abs(parseFloat(b.dataset.rate) - voiceState.rate) < 0.001);
        });
        saveVoiceSettings();
    });
    if (pitchSlider) pitchSlider.addEventListener('input', function() {
        voiceState.pitch = parseFloat(this.value);
        $('voicePitchValue').textContent = voiceState.pitch.toFixed(2);
        saveVoiceSettings();
    });
    if (volSlider) volSlider.addEventListener('input', function() {
        voiceState.volume = parseFloat(this.value);
        $('voiceVolumeValue').textContent = Math.round(voiceState.volume * 100) + '%';
        saveVoiceSettings();
    });

    function adjust(key, delta, min, max) {
        voiceState[key] = Math.max(min, Math.min(max, +(voiceState[key] + delta).toFixed(2)));
        updateVoiceUI();
        saveVoiceSettings();
    }
    if ($('voiceRateMinus'))  $('voiceRateMinus').addEventListener('click',  function(){ adjust('rate',   -0.05, 0.5, 1.5); });
    if ($('voiceRatePlus'))   $('voiceRatePlus').addEventListener('click',   function(){ adjust('rate',    0.05, 0.5, 1.5); });
    if ($('voicePitchMinus')) $('voicePitchMinus').addEventListener('click', function(){ adjust('pitch',  -0.05, 0.5, 1.5); });
    if ($('voicePitchPlus'))  $('voicePitchPlus').addEventListener('click',  function(){ adjust('pitch',   0.05, 0.5, 1.5); });
    if ($('voiceVolumeMinus'))$('voiceVolumeMinus').addEventListener('click',function(){ adjust('volume', -0.05, 0, 1); });
    if ($('voiceVolumePlus')) $('voiceVolumePlus').addEventListener('click', function(){ adjust('volume',  0.05, 0, 1); });

    document.querySelectorAll('.voice-preset-btn').forEach(function(b) {
        b.addEventListener('click', function() {
            voiceState.rate = parseFloat(this.dataset.rate);
            updateVoiceUI();
            saveVoiceSettings();
        });
    });

    var sel = $('voiceSelect');
    if (sel) sel.addEventListener('change', function() {
        voiceState.voiceURI = this.value;
        saveVoiceSettings();
    });

    if ($('voiceTestBtn')) $('voiceTestBtn').addEventListener('click', voiceTestSpeak);

    if ($('voiceResetBtn')) $('voiceResetBtn').addEventListener('click', function() {
        voiceState.rate    = DEFAULT_VOICE.rate;
        voiceState.pitch   = DEFAULT_VOICE.pitch;
        voiceState.volume  = DEFAULT_VOICE.volume;
        voiceState.voiceURI = DEFAULT_VOICE.voiceURI;
        if ($('voiceSelect')) $('voiceSelect').value = '';
        updateVoiceUI();
        saveVoiceSettings();
    });

    if ($('pfVoiceBtn')) {
        $('pfVoiceBtn').addEventListener('click', function(e) {
            e.stopPropagation();
            e.preventDefault();
            populateVoiceSelect();
            updateVoiceUI();
            modal.classList.add('show');
        });
    }
    if ($('toggleVoiceBtn')) {
        $('toggleVoiceBtn').addEventListener('click', function(e) {
            e.stopPropagation();
            populateVoiceSelect();
            updateVoiceUI();
            modal.classList.add('show');
            if ($('fabGroup')) $('fabGroup').classList.remove('open');
        });
    }
    if ($('voiceClose')) $('voiceClose').addEventListener('click', function() { modal.classList.remove('show'); });
    modal.addEventListener('click', function(e) { if (e.target === this) modal.classList.remove('show'); });
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('show')) modal.classList.remove('show');
    });
}

/* ============================================================ */
/* BUILD FILTERS                                                 */
/* ============================================================ */
function buildFilters() {
    var hskSelect = $('hskFilter');
    var subjectSelect = $('subjectFilter');
    var info = getTierInfo();
    var isLimited = info.tier !== 'active';

    if (isLimited) {
        var allowedHsk = getAllowedHskList();
        var hskHtml = '<option value="">Tất cả (HSK1-' + info.maxHSK + ')</option>';
        allowedHsk.forEach(function(h) {
            hskHtml += '<option value="' + h + '">' + h + '</option>';
        });
        var allHskList = ['HSK1','HSK2','HSK3','HSK4','HSK5','HSK6'];
        allHskList.forEach(function(h) {
            if (allowedHsk.indexOf(h) === -1) {
                var lockLabel = info.tier === 'trial' ? '(gia hạn)' : '(đăng nhập)';
                hskHtml += '<option value="' + h + '" disabled>' + h + ' ' + lockLabel + '</option>';
            }
        });
        hskSelect.innerHTML = hskHtml;

        var allowedSubjects = getAllowedSubjectList();
        var allSubjectSet = {};
        RAW_DATA.forEach(function(r) { if (r.subject) allSubjectSet[r.subject] = 1; });
        var allSubjects = Object.keys(allSubjectSet).sort();
        var unlocked = [], locked = [];
        allSubjects.forEach(function(s) {
            if (allowedSubjects.indexOf(s) !== -1) unlocked.push(s);
            else locked.push(s);
        });
        var subjHtml = '<option value="">Tất cả chủ đề</option>';
        unlocked.forEach(function(s) {
            subjHtml += '<option value="' + escapeHtml(s) + '">' + escapeHtml(s) + '</option>';
        });
        locked.forEach(function(s) {
            var lockLabel = info.tier === 'trial' ? '(gia hạn)' : '(đăng nhập)';
            subjHtml += '<option value="' + escapeHtml(s) + '" disabled>' + escapeHtml(s) + ' ' + lockLabel + '</option>';
        });
        subjectSelect.innerHTML = subjHtml;
    } else {
        hskSelect.innerHTML =
            '<option value="">Tất cả</option>' +
            '<option value="HSK1">HSK1</option>' +
            '<option value="HSK2">HSK2</option>' +
            '<option value="HSK3">HSK3</option>' +
            '<option value="HSK4">HSK4</option>' +
            '<option value="HSK5">HSK5</option>' +
            '<option value="HSK6">HSK6</option>';
        var allSubjectSet2 = {};
        RAW_DATA.forEach(function(r) { if (r.subject) allSubjectSet2[r.subject] = 1; });
        var allSubjects2 = Object.keys(allSubjectSet2).sort();
        subjectSelect.innerHTML = '<option value="">Tất cả chủ đề</option>' +
            allSubjects2.map(function(v){ return '<option value="'+escapeHtml(v)+'">'+escapeHtml(v)+'</option>'; }).join('');
    }
}

function updateFilterUI() {
    var hsk = $('hskFilter').value;
    var subject = $('subjectFilter').value;
    $('hskValue').textContent = hsk || 'Tất cả';
    $('subjectValue').textContent = subject || 'Tất cả';
    $('hskChip').classList.toggle('has-value', !!hsk);
    $('subjectChip').classList.toggle('has-value', !!subject);
    var info = getTierInfo();
    var limited = info.tier === 'demo' || info.tier === 'expired';
    $('hskChip').classList.toggle('demo-limited', limited);
    $('subjectChip').classList.toggle('demo-limited', limited);
    var count = 0;
    if (state.search) count++;
    if (hsk) count++;
    if (subject) count++;
    var resetBtn = $('resetBtn');
    var badge = $('resetBadge');
    if (count > 0) {
        resetBtn.classList.remove('hidden');
        resetBtn.classList.add('has-badge');
        badge.textContent = count;
    } else {
        resetBtn.classList.add('hidden');
    }
    updateResultCount();
}

function updateResultCount() {
    var el = $('resultCount');
    if (!el) return;
    var total = filtered ? filtered.length : 0;
    var hasFilter = !!(state.search || state.hsk || state.subject);
    if (!hasFilter) { el.classList.remove('show', 'empty'); return; }
    el.classList.add('show');
    el.classList.toggle('empty', total === 0);
    var spanEl = el.querySelector('span');
    if (spanEl) {
        if (total === 0) spanEl.innerHTML = 'Không tìm thấy kết quả nào';
        else spanEl.innerHTML = 'Tìm thấy <b>' + total + '</b> kết quả';
    }
}

function applyFilter() {
    state.search = $('searchInput').value.trim().toLowerCase();
    state.hsk = $('hskFilter').value;
    state.subject = $('subjectFilter').value;
    updateFilterUI();
    var clearBtn = $('clearSearchBtn');
    if (state.search) clearBtn.classList.add('show');
    else clearBtn.classList.remove('show');
    var baseData = getLimitedData();
    filtered = baseData.filter(function(r) {
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
        return true;
    });
    updateResultCount();
    render(true);
    if (state.hsk || state.subject) {
        setTimeout(function() {
            var mainEl = $('mainContent');
            if (mainEl) {
                var yOffset = mainEl.getBoundingClientRect().top + window.scrollY - 100;
                window.scrollTo({ top: yOffset, behavior: 'smooth' });
            }
        }, 150);
    }
}

/* ============================================================ */
/* RENDER CARDS                                                  */
/* ============================================================ */
function render(reset) {
    if (reset) { renderedCount = 0; focusedStt = null; }
    if (!filtered.length) {
        mobileWrapper.innerHTML = '<div class="no-data"><i class="fas fa-search"></i>Không tìm thấy câu nào</div>';
        return;
    }
    if (reset) mobileWrapper.innerHTML = '';
    var end = Math.min(renderedCount + PAGE_SIZE, filtered.length);
    var mobHtml = '';
    for (var i = renderedCount; i < end; i++) {
        var r = filtered[i];
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
        var practiceInput = '<input type="text" class="practice-input" placeholder="Gõ tiếng Trung..." data-answer="' + zhHtml + '" data-vi-hint="' + viHtml + '" data-stt="' + sttSafe + '" oninput="checkInput(this)" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">';
        var toggleCheckBtn = '<button class="toggle-check-btn" onclick="toggleInlineCheck(this, event)" title="Ẩn/hiện kết quả kiểm tra" data-visible="0"><i class="fas fa-eye"></i></button>';

        var excelBadge = '';
        if (r.excelRow !== undefined && r.excelRow !== null && r.excelRow !== '') {
            excelBadge = '<span class="card-excel-row" title="Dòng ' + escapeHtml(r.excelRow) + ' trong file Excel">' +
                         '<i class="fas fa-file-excel"></i> ' + escapeHtml(r.excelRow) +
                         '</span>';
        }

        var topicTag = '';
        if (r.topic) {
            topicTag = '<span class="card-tag topic tag-clickable" ' +
                       'onclick="searchByTag(event, \'topic\', \'' + escapeJs(r.topic) + '\')" ' +
                       'title="Lọc theo chủ điểm này">' +
                       escapeHtml(r.topic) + '</span>';
        }
        var subjectTag = '';
        if (r.subject) {
            subjectTag = '<span class="card-tag subject tag-clickable" ' +
                         'onclick="searchByTag(event, \'subject\', \'' + escapeJs(r.subject) + '\')" ' +
                         'title="Lọc theo chủ đề này">' +
                         escapeHtml(r.subject) + '</span>';
        }

        mobHtml += '<div class="card" data-hsk="' + (r.hsk || '') + '" onclick="toggleFocus(\'' + sttJs + '\', this)" data-stt="' + sttSafe + '">' +
            '<div class="card-header">' +
                '<div class="card-stt">' + sttSafe + '</div>' +
                '<div class="card-meta">' +
                    (r.hsk ? '<span class="card-tag hsk">' + escapeHtml(r.hsk) + '</span>' : '') +
                    topicTag +
                    subjectTag +
                    excelBadge +
                '</div>' +
                '<div onclick="event.stopPropagation()" class="action-group">' + audio + writeBtn + fullBtn + '</div>' +
            '</div>' +
            '<div class="card-body">' +
                (r.vi ? '<div class="card-vi">' + viHtml + '</div>' : '') +
                '<div class="card-zh">' + zhHtml + '</div>' +
                (r.pinyin ? '<div class="card-pinyin">' + escapeHtml(r.pinyin) + '</div>' : '') +
            '</div>' +
            '<div class="card-practice" onclick="event.stopPropagation()">' +
                practiceInput +
                toggleCheckBtn +
                '<div class="card-check" data-check-stt="' + sttSafe + '" style="display:none"></div>' +
            '</div>' +
            '</div>';
    }
    mobileWrapper.insertAdjacentHTML('beforeend', mobHtml);
    renderedCount = end;

    var oldMobileBtn = mobileWrapper.querySelector('.load-more');
    if (oldMobileBtn) oldMobileBtn.remove();
    var oldEndNote = mobileWrapper.querySelector('.end-note');
    if (oldEndNote) oldEndNote.remove();

    if (renderedCount < filtered.length) {
        var info = getTierInfo();
        var limited = info.tier !== 'active';
        var limitedDataLen = limited ? getLimitedData().length : RAW_DATA.length;
        var isTierLocked = limited && (renderedCount >= limitedDataLen) && (filtered.length >= limitedDataLen);

        if (!isTierLocked) {
            var btnMobile = document.createElement('button');
            btnMobile.className = 'load-more';
            btnMobile.innerHTML = '<i class="fas fa-chevron-down"></i> Xem thêm (' + renderedCount + '/' + filtered.length + ')';
            btnMobile.onclick = function() { render(false); };
            mobileWrapper.appendChild(btnMobile);
        } else {
            var lockedBtn = document.createElement('button');
            lockedBtn.className = 'load-more locked';
            if (info.tier === 'expired') {
                lockedBtn.classList.add('expired');
                lockedBtn.innerHTML = '<i class="fas fa-gem"></i> Gia hạn để xem toàn bộ ' + RAW_DATA.length + ' câu';
                lockedBtn.onclick = function() {
                    if (typeof openRenewalModal === 'function') openRenewalModal();
                };
            } else if (info.tier === 'trial') {
                lockedBtn.innerHTML = '<i class="fas fa-crown"></i> Gia hạn để xem toàn bộ ' + RAW_DATA.length + ' câu';
                lockedBtn.onclick = function() {
                    if (typeof openRenewalModal === 'function') openRenewalModal();
                };
            } else {
                lockedBtn.innerHTML = '<i class="fas fa-lock"></i> Đăng nhập để xem toàn bộ ' + RAW_DATA.length + ' câu';
                lockedBtn.onclick = function() {
                    if (typeof showLoginModal === 'function') showLoginModal();
                };
            }
            mobileWrapper.appendChild(lockedBtn);
        }
    } else if (filtered.length > PAGE_SIZE) {
        var endNote = document.createElement('div');
        endNote.className = 'end-note';
        endNote.innerHTML = '<i class="fas fa-check-circle"></i> Đã hiển thị tất cả ' + filtered.length + ' câu';
        mobileWrapper.appendChild(endNote);
    }
}

/* ============================================================ */
/* ANSWER CHECKING                                               */
/* ============================================================ */
function normalizeAnswer(str) {
    if (!str) return '';
    return String(str)
        .replace(/[。，！？、；：""''「」『』（）《》〈〉【】〔〕]/g, '')
        .replace(/[.,!?;:'"()\[\]{}\-~`@#$%^&*+=|\\/<>]/g, '')
        .replace(/\s+/g, '')
        .toLowerCase()
        .trim();
}

function removeTones(str) {
    if (!str) return '';
    var map = {
        'ā':'a','á':'a','ǎ':'a','à':'a','ē':'e','é':'e','ě':'e','è':'e',
        'ī':'i','í':'i','ǐ':'i','ì':'i','ō':'o','ó':'o','ǒ':'o','ò':'o',
        'ū':'u','ú':'u','ǔ':'u','ù':'u','ǖ':'v','ǘ':'v','ǚ':'v','ǜ':'v','ü':'v'
    };
    return str.replace(/[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]/g, function(c) { return map[c] || c; });
}

function removeFillers(str) {
    if (!str) return '';
    var result = str;
    FILLER_WORDS.forEach(function(w) { result = result.split(w).join(''); });
    return result;
}

function expandSynonyms(str) {
    var results = [str];
    var keys = Object.keys(SYNONYMS);
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        if (str.indexOf(key) !== -1) {
            var values = SYNONYMS[key];
            for (var j = 0; j < values.length; j++) results.push(str.split(key).join(values[j]));
        }
    }
    return results;
}

function levenshtein(a, b) {
    if (a === b) return 0;
    if (!a.length) return b.length;
    if (!b.length) return a.length;
    var matrix = [];
    for (var i = 0; i <= b.length; i++) matrix[i] = [i];
    for (var j = 0; j <= a.length; j++) matrix[0][j] = j;
    for (var i = 1; i <= b.length; i++) {
        for (var j = 1; j <= a.length; j++) {
            if (b.charAt(i-1) === a.charAt(j-1)) matrix[i][j] = matrix[i-1][j-1];
            else matrix[i][j] = Math.min(matrix[i-1][j-1] + 1, matrix[i][j-1] + 1, matrix[i-1][j] + 1);
        }
    }
    return matrix[b.length][a.length];
}

function similarity(a, b) {
    var maxLen = Math.max(a.length, b.length);
    if (maxLen === 0) return 1;
    return 1 - (levenshtein(a, b) / maxLen);
}

function smartCheck(userAnswer, correctAnswer) {
    var user = normalizeAnswer(userAnswer);
    var correct = normalizeAnswer(correctAnswer);
    if (!user) return { status: 'wrong', reason: '' };
    if (user === correct) return { status: 'correct', reason: 'Chính xác' };
    var userNoTone = removeTones(user);
    var correctNoTone = removeTones(correct);
    if (userNoTone === correctNoTone) return { status: 'correct', reason: 'Đúng (thiếu dấu thanh)' };
    var userNoFill = removeFillers(user);
    var correctNoFill = removeFillers(correct);
    if (userNoFill === correctNoFill) return { status: 'correct', reason: 'Đúng (bỏ qua từ phụ)' };
    var uNF = removeTones(userNoFill);
    var cNF = removeTones(correctNoFill);
    if (uNF === cNF) return { status: 'correct', reason: 'Đúng (từ phụ + dấu thanh)' };
    var userVariants = expandSynonyms(userNoFill);
    var correctVariants = expandSynonyms(correctNoFill);
    for (var i = 0; i < userVariants.length; i++) {
        for (var j = 0; j < correctVariants.length; j++) {
            if (userVariants[i] === correctVariants[j]) return { status: 'correct', reason: 'Đúng (từ đồng nghĩa)' };
        }
    }
    var maxSim = 0;
    for (var k = 0; k < correctVariants.length; k++) {
        var sim = similarity(userNoFill, correctVariants[k]);
        if (sim > maxSim) maxSim = sim;
    }
    for (var m = 0; m < userVariants.length; m++) {
        var sim2 = similarity(userVariants[m], correctNoFill);
        if (sim2 > maxSim) maxSim = sim2;
    }
    if (maxSim >= 0.85) return { status: 'partial', reason: 'Gần đúng (' + Math.round(maxSim * 100) + '%)' };
    if (user.indexOf(correct) !== -1 || correct.indexOf(user) !== -1) return { status: 'partial', reason: 'Thiếu/thừa từ' };
    return { status: 'wrong', reason: 'Không khớp' };
}

function countSyllables(pinyinWord) {
    if (!pinyinWord) return 0;
    var cleaned = pinyinWord
        .replace(/[.,!?;:'"()\[\]{}\-~`@#$%^&*+=|\\/<>。，！？、；：\s]/g, '')
        .toLowerCase();
    if (!cleaned) return 0;
    var map = {
        'ā':'a','á':'a','ǎ':'a','à':'a','ē':'e','é':'e','ě':'e','è':'e',
        'ī':'i','í':'i','ǐ':'i','ì':'i','ō':'o','ó':'o','ǒ':'o','ò':'o',
        'ū':'u','ú':'u','ǔ':'u','ù':'u','ǖ':'v','ǘ':'v','ǚ':'v','ǜ':'v','ü':'v'
    };
    cleaned = cleaned.replace(/[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]/g, function(c) { return map[c] || c; });
    var vowels = 'aeiouv';
    var count = 0;
    var i = 0;
    while (i < cleaned.length) {
        if (vowels.indexOf(cleaned[i]) !== -1) {
            count++;
            while (i < cleaned.length && vowels.indexOf(cleaned[i]) !== -1) {
                i++;
            }
        } else {
            i++;
        }
    }
    return count || 1;
}

function splitByPinyin(zh, pinyin) {
    if (!zh) return [];
    var hanziChars = [];
    for (var i = 0; i < zh.length; i++) {
        var c = zh[i];
        if (/[\u4e00-\u9fa5]/.test(c)) hanziChars.push(c);
    }
    if (hanziChars.length === 0) return [];

    if (!pinyin || !pinyin.trim()) {
        return hanziChars.map(function(c) { return { text: c, type: 'single', pinyin: '' }; });
    }

    var normalizedPinyin = pinyin
        .replace(/[.,!?;:'"()\[\]{}\-~`@#$%^&*+=|\\/<>。，！？、；：""'']/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();

    var pinyinWords = normalizedPinyin.split(/\s+/).filter(function(w) { return w.length > 0; });
    var syllableCounts = pinyinWords.map(function(w) { return countSyllables(w); });
    var totalSyllables = syllableCounts.reduce(function(a, b) { return a + b; }, 0);

    if (totalSyllables === hanziChars.length) {
        var result = [];
        var charIdx = 0;
        for (var j = 0; j < syllableCounts.length; j++) {
            var cnt = syllableCounts[j];
            if (cnt <= 0) continue;
            var phrase = hanziChars.slice(charIdx, charIdx + cnt).join('');
            if (phrase) {
                result.push({
                    text: phrase,
                    type: 'phrase',
                    pinyin: pinyinWords[j] || ''
                });
            }
            charIdx += cnt;
        }
        if (charIdx < hanziChars.length) {
            var remaining = hanziChars.slice(charIdx).join('');
            if (result.length > 0) {
                result[result.length - 1].text += remaining;
                if (charIdx < pinyinWords.length) {
                    result[result.length - 1].pinyin += ' ' + pinyinWords.slice(charIdx).join(' ');
                }
            } else {
                result.push({ text: remaining, type: 'single', pinyin: '' });
            }
        }
        return result;
    }

    return hanziChars.map(function(c) { return { text: c, type: 'single', pinyin: '' }; });
}

function updateInlinePreview(input, answer) {
    var wrapper = input.parentElement;
    var preview = wrapper.querySelector('.inline-char-preview');
    if (!preview) {
        preview = document.createElement('div');
        preview.className = 'inline-char-preview';
        input.insertAdjacentElement('afterend', preview);
    }
    var userVal = input.value.replace(/\s+/g, '');
    var cleanAnswer = (answer || '').replace(/\s+/g, '');
    if (!cleanAnswer) { preview.innerHTML = ''; return; }
    var html = '';
    var maxLen = Math.max(userVal.length, cleanAnswer.length);
    for (var i = 0; i < maxLen; i++) {
        var userChar = userVal[i] || '';
        var answerChar = cleanAnswer[i] || '';
        var cls = 'char-slot';
        var display = '';
        var clickable = false;
        if (userChar && answerChar) {
            if (userChar === answerChar) {
                cls += ' correct';
                display = userChar;
            } else {
                cls += ' wrong';
                display = userChar;
                clickable = true;
            }
        } else if (!userChar && answerChar) {
            cls += ' ghost-missing';
            display = '·';
            clickable = true;
        } else if (userChar && !answerChar) {
            cls += ' extra';
            display = userChar;
            clickable = true;
        } else {
            continue;
        }
        if (clickable) {
            html += '<span class="' + cls + '" data-idx="' + i + '" onclick="fixInlineChar(this, event)">' + escapeHtml(display) + '</span>';
        } else {
            html += '<span class="' + cls + '">' + escapeHtml(display) + '</span>';
        }
    }
    preview.innerHTML = html;
}

window.fixInlineChar = function(el, evt) {
    evt.stopPropagation();
    if (evt.preventDefault) evt.preventDefault();
    var wrap = el.closest('.card-practice');
    var input = wrap ? wrap.querySelector('.practice-input') : null;
    if (!input) return;
    var strippedIdx = parseInt(el.dataset.idx);
    var rawVal = input.value;
    var rawIdx = -1;
    var strippedCount = -1;
    for (var i = 0; i < rawVal.length; i++) {
        if (!/\s/.test(rawVal[i])) {
            strippedCount++;
            if (strippedCount === strippedIdx) {
                rawIdx = i;
                break;
            }
        }
    }
    if (rawIdx === -1) rawIdx = rawVal.length;
    while (rawIdx < rawVal.length && /\s/.test(rawVal[rawIdx])) {
        rawIdx++;
    }
    input.focus();
    setTimeout(function() {
        try {
            var endIdx = Math.min(rawIdx + 1, rawVal.length);
            input.setSelectionRange(rawIdx, endIdx);
        } catch(e) {
            input.selectionStart = rawIdx;
            input.selectionEnd = Math.min(rawIdx + 1, rawVal.length);
        }
        el.classList.add('highlight');
        setTimeout(function() { el.classList.remove('highlight'); }, 1200);
    }, 10);
};

function showInlineCheckWithAnswer(input) {
    if (!input) return;
    var stt = input.dataset.stt;
    var answer = input.dataset.answer;
    var cells = document.querySelectorAll('[data-check-stt="' + stt + '"]');
    var val = input.value.trim();
    if (!answer) { cells.forEach(function(c) { c.innerHTML = ''; }); return; }
    var answerHtml = '<div class="answer-inline-display">' +
        '<span class="answer-inline-label"><i class="fas fa-check-circle"></i> Đáp án:</span>' +
        '<span class="answer-inline-text">' + escapeHtml(answer) + '</span>' +
        '</div>';
    var resultHtml = '';
    if (val) {
        var result = smartCheck(val, answer);
        if (result.status === 'correct') resultHtml = '<span class="ai-correct">ĐÚNG</span>';
        else if (result.status === 'partial') resultHtml = '<span class="ai-partial">GẦN ĐÚNG</span>';
        else resultHtml = '<span class="ai-wrong">SAI</span>';
        if (result.reason) resultHtml += '<span class="ai-reason">' + escapeHtml(result.reason) + '</span>';
    } else {
        resultHtml = '<span class="ai-reason">Chưa gõ gì cả</span>';
    }
    cells.forEach(function(c) { c.innerHTML = resultHtml + answerHtml; });
}

window.checkInput = function(input) {
    var stt = input.dataset.stt;
    var answer = input.dataset.answer;
    var cells = document.querySelectorAll('[data-check-stt="' + stt + '"]');
    var val = input.value.trim();
    updateInlinePreview(input, answer);
    var wrap = input.closest('.card-practice');
    var btn = wrap ? wrap.querySelector('.toggle-check-btn') : null;
    var isVisible = btn && btn.dataset.visible === '1';
    if (!isVisible) return;
    var answerHtml = '<div class="answer-inline-display">' +
        '<span class="answer-inline-label"><i class="fas fa-check-circle"></i> Đáp án:</span>' +
        '<span class="answer-inline-text">' + escapeHtml(answer) + '</span>' +
        '</div>';
    var resultHtml = '';
    if (val) {
        var result = smartCheck(val, answer);
        if (result.status === 'correct') resultHtml = '<span class="ai-correct">ĐÚNG</span>';
        else if (result.status === 'partial') resultHtml = '<span class="ai-partial">GẦN ĐÚNG</span>';
        else resultHtml = '<span class="ai-wrong">SAI</span>';
        if (result.reason) resultHtml += '<span class="ai-reason">' + escapeHtml(result.reason) + '</span>';
    } else {
        resultHtml = '<span class="ai-reason">Chưa gõ gì cả</span>';
    }
    cells.forEach(function(c) { c.innerHTML = resultHtml + answerHtml; });
};

window.toggleInlineCheck = function(btn, evt) {
    if (evt) { evt.stopPropagation(); if (evt.preventDefault) evt.preventDefault(); }
    var wrap = btn.closest('.card-practice');
    if (!wrap) return;
    var checkEl = wrap.querySelector('.card-check');
    var input = wrap.querySelector('.practice-input');
    if (!checkEl) return;
    var isVisible = btn.dataset.visible === '1';
    if (isVisible) {
        checkEl.style.display = 'none';
        btn.dataset.visible = '0';
        btn.innerHTML = '<i class="fas fa-eye"></i>';
        btn.classList.remove('active');
    } else {
        checkEl.style.display = 'block';
        btn.dataset.visible = '1';
        btn.innerHTML = '<i class="fas fa-eye-slash"></i>';
        btn.classList.add('active');
        showInlineCheckWithAnswer(input);
    }
};

/* ============================================================ */
/* PRACTICE FULL MODAL — expired dùng được như Demo              */
/* ============================================================ */
var pfCurrentStt = null;
var pfCurrentAnswer = '';
var pfCurrentVi = '';
var pfCurrentPinyin = '';
var pfHintEnabled = false;
var pfRandomMode = false;

window.openPracticeFull = function(stt, evt) {
    if (evt) { evt.stopPropagation(); if (evt.preventDefault) evt.preventDefault(); }

    if (!canUseFeature()) { showLimitMessage(); return; }

    if (typeof pfBuildDatasetSelect === 'function') pfBuildDatasetSelect();
    pfBuildFilterOptions();
    pfBuildQuickNav();
    var idx = -1;
    for (var i = 0; i < filtered.length; i++) {
        if (String(filtered[i].stt) === String(stt)) { idx = i; break; }
    }
    if (idx === -1) { alert('Không tìm thấy câu!'); return; }
    pfCurrentStt = stt;
    document.body.classList.add('practice-full-open');
    if (typeof updateFloatingLeftVisibility === 'function') updateFloatingLeftVisibility();
    document.body.style.overflow = 'hidden';
    $('practiceFullModal').classList.add('show');
    loadPracticeFull(stt);
};

window.closePracticeFull = function() {
    if (window._isSpeakingFull) stopSpeakFull();
    if (window._isQuickSpeaking) stopQuickSpeak();
    $('practiceFullModal').classList.remove('show');
    document.body.style.overflow = '';
    document.body.classList.remove('practice-full-open');
    if (typeof updateFloatingLeftVisibility === 'function') updateFloatingLeftVisibility();
    pfCurrentStt = null;
    if ('speechSynthesis' in window) speechSynthesis.cancel();
};

function loadPracticeFull(stt) {
    var idx = -1;
    for (var i = 0; i < filtered.length; i++) {
        if (String(filtered[i].stt) === String(stt)) { idx = i; break; }
    }
    if (idx === -1) return;
    if (!$('pfSearchInput').value && !$('pfHskFilter').value && !$('pfSubjectFilter').value) {
        $('pfSearchInput').value = $('searchInput').value;
        $('pfHskFilter').value = $('hskFilter').value;
        $('pfSubjectFilter').value = $('subjectFilter').value;
    }
    pfUpdateFilterUI();
    var r = filtered[idx];
    pfCurrentStt = stt;
    pfCurrentAnswer = r.zh || '';
    pfCurrentVi = r.vi || '';
    pfCurrentPinyin = r.pinyin || '';

    var sttRaw = (r.stt !== undefined && r.stt !== null && String(r.stt).trim() !== '')
                 ? String(r.stt).trim()
                 : '';
    var sttLabel = sttRaw ? '#' + sttRaw + '  ·  ' : '';
    $('pfCounter').textContent = sttLabel + 'Câu ' + (idx + 1) + ' / ' + filtered.length;

    var tagsHtml = '';
    if (r.hsk) tagsHtml += '<span class="card-tag hsk">' + escapeHtml(r.hsk) + '</span>';
    if (r.topic) {
        tagsHtml += '<span class="card-tag topic tag-clickable" ' +
                    'onclick="searchByTag(event, \'topic\', \'' + escapeJs(r.topic) + '\')" ' +
                    'title="Lọc theo chủ điểm này">' +
                    escapeHtml(r.topic) + '</span>';
    }
    if (r.subject) {
        tagsHtml += '<span class="card-tag tag-clickable" ' +
                    'onclick="searchByTag(event, \'subject\', \'' + escapeJs(r.subject) + '\')" ' +
                    'title="Lọc theo chủ đề này">' +
                    escapeHtml(r.subject) + '</span>';
    }
    if (r.excelRow !== undefined && r.excelRow !== null && r.excelRow !== '') {
        tagsHtml += '<span class="card-tag excel-tag" title="Dòng ' + escapeHtml(r.excelRow) + ' trong file Excel">' +
                    '<i class="fas fa-file-excel"></i> Excel: ' + escapeHtml(r.excelRow) +
                    '</span>';
    }
    $('pfTags').innerHTML = tagsHtml;
    $('pfVi').textContent = pfCurrentVi;
    $('pfInput').value = '';
    $('pfStatus').textContent = '';
    $('pfStatus').className = 'practice-full-status';
    $('pfAnswer').classList.remove('show');
    var revealBtn = $('pfRevealBtn');
    revealBtn.classList.remove('revealed', 'hidden');
    revealBtn.innerHTML = '<i class="fas fa-eye"></i> Xem đáp án';
    pfHintEnabled = false;
    $('pfHintBtn').classList.remove('active');
    updateCharPreview();
    $('pfPrevBtn').disabled = (idx === 0);
    $('pfNextBtn').disabled = (idx === filtered.length - 1);
    var quickNav = $('pfQuickNav');
    if (quickNav && quickNav.value !== stt) quickNav.value = stt;

    if (window._isSpeakingFull) {
        stopSpeakFull();
    } else {
        _setSpeakBtnState(false);
    }
    if (window._isQuickSpeaking) {
        stopQuickSpeak();
    } else {
        _setQuickSpeakBtnState(false);
    }

    setTimeout(function() {
        var active = document.activeElement;
        if (active && (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA' || active.tagName === 'SELECT')) return;
        $('pfInput').focus();
    }, 200);
}

window.pfNext = function() {
    if (!pfCurrentStt || filtered.length === 0) return;
    var idx = -1;
    for (var i = 0; i < filtered.length; i++) {
        if (String(filtered[i].stt) === String(pfCurrentStt)) { idx = i; break; }
    }
    if (idx === -1) return;

    if (pfRandomMode && filtered.length > 1) {
        var newIdx = idx;
        var tries = 0;
        while (newIdx === idx && tries < 20) {
            newIdx = Math.floor(Math.random() * filtered.length);
            tries++;
        }
        if (newIdx === idx) newIdx = (idx + 1) % filtered.length;

        var rndBtn = $('pfRandomToggleBtn');
        if (rndBtn) {
            var icon = rndBtn.querySelector('i');
            if (icon) {
                icon.style.animation = 'none';
                void icon.offsetWidth;
                icon.style.animation = 'diceShake 0.6s ease-in-out';
            }
        }
        loadPracticeFull(filtered[newIdx].stt);
        return;
    }

    if (idx >= filtered.length - 1) return;
    loadPracticeFull(filtered[idx + 1].stt);
};

window.pfToggleRandom = function() {
    pfRandomMode = !pfRandomMode;
    var btn = $('pfRandomToggleBtn');
    if (btn) {
        btn.classList.toggle('active', pfRandomMode);
        btn.title = pfRandomMode
            ? 'ĐANG BẬT: Nút Next sẽ nhảy câu ngẫu nhiên'
            : 'Bật/tắt chế độ nhảy câu ngẫu nhiên';
    }
    try { localStorage.setItem('pfRandomMode', pfRandomMode ? '1' : '0'); } catch(e) {}
};

window.pfPrev = function() {
    if (!pfCurrentStt) return;
    var idx = -1;
    for (var i = 0; i < filtered.length; i++) {
        if (String(filtered[i].stt) === String(pfCurrentStt)) { idx = i; break; }
    }
    if (idx <= 0) return;
    loadPracticeFull(filtered[idx - 1].stt);
};

function pfBuildQuickNav() {
    var sel = $('pfQuickNav');
    if (!sel) return;
    var html = '<option value="">-- Chọn câu (' + filtered.length + ') --</option>';
    filtered.forEach(function(r, i) {
        var vi = (r.vi || '').substring(0, 45);
        var sttRaw = (r.stt !== undefined && r.stt !== null && String(r.stt).trim() !== '')
                     ? '#' + String(r.stt).trim() + ' · '
                     : '';
        var label = sttRaw + 'Câu ' + (i + 1) + ': ' + vi;
        html += '<option value="' + escapeHtml(r.stt) + '">' + escapeHtml(label) + '</option>';
    });
    sel.innerHTML = html;
    if (pfCurrentStt) sel.value = pfCurrentStt;
}

function pfQuickNavChange() {
    var sel = $('pfQuickNav');
    if (!sel) return;
    var stt = sel.value;
    if (!stt) return;
    loadPracticeFull(stt);
}

function pfBuildFilterOptions() {
    var hskSel = $('pfHskFilter');
    var subjSel = $('pfSubjectFilter');
    var info = getTierInfo();
    var isLimited = info.tier !== 'active';
    if (isLimited) {
        var allowedHsk = getAllowedHskList();
        var hskHtml = '<option value="">Tất cả</option>';
        allowedHsk.forEach(function(h) { hskHtml += '<option value="' + h + '">' + h + '</option>'; });
        var allHskList = ['HSK1','HSK2','HSK3','HSK4','HSK5','HSK6'];
        allHskList.forEach(function(h) {
            if (allowedHsk.indexOf(h) === -1) {
                var lockLabel = info.tier === 'trial' ? '(gia hạn)' : '(đăng nhập)';
                hskHtml += '<option value="' + h + '" disabled>' + h + ' ' + lockLabel + '</option>';
            }
        });
        hskSel.innerHTML = hskHtml;
        var allowedSubjects = getAllowedSubjectList();
        var allSubjectSet = {};
        RAW_DATA.forEach(function(r) { if (r.subject) allSubjectSet[r.subject] = 1; });
        var allSubjects = Object.keys(allSubjectSet).sort();
        var unlocked = [], locked = [];
        allSubjects.forEach(function(s) {
            if (allowedSubjects.indexOf(s) !== -1) unlocked.push(s);
            else locked.push(s);
        });
        var subjHtml = '<option value="">Tất cả chủ đề</option>';
        unlocked.forEach(function(s) { subjHtml += '<option value="' + escapeHtml(s) + '">' + escapeHtml(s) + '</option>'; });
        locked.forEach(function(s) {
            var lockLabel = info.tier === 'trial' ? '(gia hạn)' : '(đăng nhập)';
            subjHtml += '<option value="' + escapeHtml(s) + '" disabled>' + escapeHtml(s) + ' ' + lockLabel + '</option>';
        });
        subjSel.innerHTML = subjHtml;
    } else {
        hskSel.innerHTML =
            '<option value="">Tất cả</option>' +
            '<option value="HSK1">HSK1</option>' +
            '<option value="HSK2">HSK2</option>' +
            '<option value="HSK3">HSK3</option>' +
            '<option value="HSK4">HSK4</option>' +
            '<option value="HSK5">HSK5</option>' +
            '<option value="HSK6">HSK6</option>';
        var allSubjectSet2 = {};
        RAW_DATA.forEach(function(r) { if (r.subject) allSubjectSet2[r.subject] = 1; });
        var allSubjects2 = Object.keys(allSubjectSet2).sort();
        subjSel.innerHTML = '<option value="">Tất cả chủ đề</option>' +
            allSubjects2.map(function(v){ return '<option value="'+escapeHtml(v)+'">'+escapeHtml(v)+'</option>'; }).join('');
    }
    hskSel.value = $('hskFilter').value;
    subjSel.value = $('subjectFilter').value;
    $('pfSearchInput').value = $('searchInput').value;
    pfUpdateFilterUI();
}

function pfUpdateFilterUI() {
    var hsk = $('pfHskFilter').value;
    var subject = $('pfSubjectFilter').value;
    $('pfHskValue').textContent = hsk || 'Tất cả';
    $('pfSubjectValue').textContent = subject || 'Tất cả';
    $('pfHskChip').classList.toggle('has-value', !!hsk);
    $('pfSubjectChip').classList.toggle('has-value', !!subject);
    var search = $('pfSearchInput').value.trim();
    if (search) $('pfClearSearchBtn').classList.add('show');
    else $('pfClearSearchBtn').classList.remove('show');
}

function pfApplyFilter() {
    $('searchInput').value = $('pfSearchInput').value;
    $('hskFilter').value = $('pfHskFilter').value;
    $('subjectFilter').value = $('pfSubjectFilter').value;
    state.search = $('pfSearchInput').value.trim().toLowerCase();
    state.hsk = $('pfHskFilter').value;
    state.subject = $('pfSubjectFilter').value;
    var baseData = getLimitedData();
    filtered = baseData.filter(function(r) {
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
        return true;
    });
    updateFilterUI();
    pfUpdateFilterUI();
    pfBuildQuickNav();
    render(true);
    if (state.hsk || state.subject) {
        setTimeout(function() {
            var bodyEl = document.querySelector('.practice-full-body');
            if (bodyEl) bodyEl.scrollTo({ top: 0, behavior: 'smooth' });
        }, 100);
    }
    var activeEl = document.activeElement;
    var isTypingInSearch = activeEl && activeEl.id === 'pfSearchInput';
    var currentStillValid = false;
    if (pfCurrentStt) {
        for (var i = 0; i < filtered.length; i++) {
            if (String(filtered[i].stt) === String(pfCurrentStt)) { currentStillValid = true; break; }
        }
    }
    if (filtered.length > 0) {
        if (isTypingInSearch && currentStillValid) {
            var idx = -1;
            for (var j = 0; j < filtered.length; j++) {
                if (String(filtered[j].stt) === String(pfCurrentStt)) { idx = j; break; }
            }
            if (idx !== -1) {
                var rNow = filtered[idx];
                var sttNow = (rNow.stt !== undefined && rNow.stt !== null && String(rNow.stt).trim() !== '')
                             ? '#' + String(rNow.stt).trim() + '  ·  '
                             : '';
                $('pfCounter').textContent = sttNow + 'Câu ' + (idx + 1) + ' / ' + filtered.length;
            }
            return;
        }
        loadPracticeFull(filtered[0].stt);
    } else {
        pfCurrentStt = null;
        pfCurrentAnswer = '';
        pfCurrentVi = 'Không tìm thấy câu nào';
        pfCurrentPinyin = '';
        $('pfVi').textContent = 'Không tìm thấy câu nào';
        $('pfInput').value = '';
        $('pfCounter').textContent = 'Câu 0 / 0';
        $('pfTags').innerHTML = '';
        $('pfAnswer').classList.remove('show');
        $('pfPreview').innerHTML = '';
        $('pfStatus').textContent = '';
        $('pfPrevBtn').disabled = true;
        $('pfNextBtn').disabled = true;
    }
}

function updateCharPreview() {
    var input = $('pfInput');
    var preview = $('pfPreview');
    var userVal = input.value;
    var cleanUser = userVal.replace(/\s+/g, '');
    var cleanAnswer = pfCurrentAnswer.replace(/\s+/g, '');
    if (!cleanAnswer) { preview.innerHTML = ''; return; }
    var html = '';
    var maxLen = Math.max(cleanUser.length, cleanAnswer.length);
    for (var i = 0; i < maxLen; i++) {
        var userChar = cleanUser[i] || '';
        var answerChar = cleanAnswer[i] || '';
        var cls = 'char-slot';
        var display = '';
        var clickable = false;
        if (userChar && answerChar) {
            if (userChar === answerChar) { cls += ' correct'; display = userChar; }
            else { cls += ' wrong'; display = userChar; clickable = true; }
        } else if (!userChar && answerChar) {
            if (pfHintEnabled) { cls += ' ghost'; display = answerChar; }
            else { continue; }
        } else if (userChar && !answerChar) {
            cls += ' extra'; display = userChar; clickable = true;
        } else { continue; }
        if (clickable) {
            html += '<span class="' + cls + '" data-idx="' + i + '" onclick="fixCharAt(' + i + ', this)">' + escapeHtml(display) + '</span>';
        } else {
            html += '<span class="' + cls + '">' + escapeHtml(display) + '</span>';
        }
    }
    preview.innerHTML = html;
}

window.fixCharAt = function(idx, el) {
    var input = $('pfInput');
    if (!input) return;
    input.focus();
    setTimeout(function() {
        try { input.setSelectionRange(idx, idx + 1); }
        catch(e) { input.selectionStart = idx; input.selectionEnd = idx + 1; }
        if (el) {
            el.classList.add('highlight');
            setTimeout(function() { el.classList.remove('highlight'); }, 1200);
        }
    }, 10);
};

function toggleHint() {
    pfHintEnabled = !pfHintEnabled;
    var btn = $('pfHintBtn');
    if (pfHintEnabled) btn.classList.add('active');
    else btn.classList.remove('active');
    updateCharPreview();
}

function checkFullAnswer() {
    var input = $('pfInput');
    var statusEl = $('pfStatus');
    var val = input.value.trim();
    if (!val) {
        statusEl.textContent = '';
        statusEl.className = 'practice-full-status';
        return;
    }
    var result = smartCheck(val, pfCurrentAnswer);
    if (result.status === 'correct') {
        statusEl.textContent = 'ĐÚNG';
        statusEl.className = 'practice-full-status correct';
    } else if (result.status === 'partial') {
        statusEl.textContent = (result.reason || 'GẦN ĐÚNG');
        statusEl.className = 'practice-full-status partial';
    } else {
        statusEl.textContent = 'SAI';
        statusEl.className = 'practice-full-status wrong';
    }
}

var _activeTooltipWrap = null;

function togglePhraseTooltip(wrapEl) {
    if (!wrapEl) return;
    var tip = wrapEl.querySelector('.answer-phrase-tooltip');
    if (!tip) return;

    if (_activeTooltipWrap && _activeTooltipWrap !== wrapEl) {
        var oldTip = _activeTooltipWrap.querySelector('.answer-phrase-tooltip');
        if (oldTip) oldTip.classList.remove('show');
    }

    if (tip.classList.contains('show')) {
        tip.classList.remove('show');
        _activeTooltipWrap = null;
    } else {
        tip.classList.add('show');
        _activeTooltipWrap = wrapEl;
    }
}

document.addEventListener('click', function(e) {
    if (!e.target.closest('.answer-phrase-wrap')) {
        document.querySelectorAll('.answer-phrase-tooltip.show').forEach(function(t) {
            t.classList.remove('show');
        });
        _activeTooltipWrap = null;
    }
});

function revealFullAnswer() {
    var answerEl = $('pfAnswer');
    var revealBtn = $('pfRevealBtn');
    if (answerEl.classList.contains('show')) {
        answerEl.classList.remove('show');
        revealBtn.classList.remove('revealed');
        revealBtn.innerHTML = '<i class="fas fa-eye"></i> Xem đáp án';
        return;
    }
    var charsEl = $('pfAnswerChars');
    var pinyinEl = $('pfAnswerPinyin');
    charsEl.innerHTML = '';
    var phrases = splitByPinyin(pfCurrentAnswer, pfCurrentPinyin);
    if (phrases.length === 0) {
        pfCurrentAnswer.split('').forEach(function(c) {
            if (/[\u4e00-\u9fa5]/.test(c)) phrases.push({ text: c, type: 'single', pinyin: '' });
        });
    }
    window._pfPhrases = phrases;

    phrases.forEach(function(item, idx) {
        var wrap = document.createElement('span');
        wrap.className = 'answer-phrase-wrap';
        wrap.dataset.idx = idx;
        wrap.dataset.text = item.text;
        wrap.dataset.pinyin = item.pinyin || '';

        var btn = document.createElement('button');
        btn.className = 'answer-phrase-btn';
        btn.textContent = item.text;
        btn.title = item.pinyin ? (item.text + ' - ' + item.pinyin) : item.text;
        btn.onclick = (function(text, pinyin, el, wrapEl) {
            return function(e) {
                e.stopPropagation();
                el.classList.add('zoom-in');
                setTimeout(function() { el.classList.remove('zoom-in'); }, 700);
                togglePhraseTooltip(wrapEl);
                speakPhrase(text, el);
            };
        })(item.text, item.pinyin, btn, wrap);
        wrap.appendChild(btn);

        var tip = document.createElement('span');
        tip.className = 'answer-phrase-tooltip';
        tip.textContent = item.pinyin || item.text;
        wrap.appendChild(tip);

        if (item.pinyin) {
            wrap.addEventListener('mouseenter', function() {
                tip.classList.add('show');
            });
            wrap.addEventListener('mouseleave', function() {
                tip.classList.remove('show');
            });
        }

        charsEl.appendChild(wrap);
    });

    pinyinEl.textContent = pfCurrentPinyin;
    answerEl.classList.add('show');
    revealBtn.classList.add('revealed');
    revealBtn.innerHTML = '<i class="fas fa-eye-slash"></i> Ẩn đáp án';
}

window.speakPhrase = function(phrase, btn) {
    if (!canUseFeature()) { showLimitMessage(); return; }
    if (!('speechSynthesis' in window)) { alert('Trình duyệt không hỗ trợ phát âm.'); return; }
    if (shouldCountUsage()) { incDemoUsage(); updateDemoRemaining(); }
    speechSynthesis.cancel();
    document.querySelectorAll('.answer-phrase-btn.speaking').forEach(function(b) { b.classList.remove('speaking'); });
    btn.classList.add('speaking');
    var utterance = new SpeechSynthesisUtterance(phrase);
    utterance.lang = 'zh-CN';
    applyVoiceSettings(utterance);
    utterance.onend = utterance.onerror = function() { btn.classList.remove('speaking'); };
    setTimeout(function(){ speechSynthesis.speak(utterance); }, 30);
};

window._isSpeakingFull = false;
window._speakToken = 0;

function _setSpeakBtnState(speaking) {
    window._isSpeakingFull = speaking;
    var btn = $('pfSpeakBtn');
    if (!btn) return;
    if (speaking) {
        btn.classList.add('speaking');
        btn.setAttribute('title', 'Nhấn để dừng');
        btn.setAttribute('aria-label', 'Nhấn để dừng');
        var i = btn.querySelector('i');
        if (i) i.className = 'fas fa-stop';
    } else {
        btn.classList.remove('speaking');
        btn.setAttribute('title', 'Nghe câu này');
        btn.setAttribute('aria-label', 'Nghe câu này');
        var i2 = btn.querySelector('i');
        if (i2) i2.className = 'fas fa-volume-up';
    }
}

window.stopSpeakFull = function() {
    window._speakToken++;
    window._isSpeakingFull = false;
    if ('speechSynthesis' in window) {
        try { speechSynthesis.cancel(); } catch(e) {}
    }
    var charsContainer = $('pfAnswerChars');
    if (charsContainer) {
        charsContainer.querySelectorAll('.answer-phrase-btn.reading, .answer-phrase-btn.speaking').forEach(function(b) {
            b.classList.remove('reading', 'speaking');
        });
        charsContainer.querySelectorAll('.answer-phrase-tooltip.show').forEach(function(t) {
            t.classList.remove('show');
        });
        charsContainer.querySelectorAll('.answer-phrase-wrap.active-wrap').forEach(function(w) {
            w.classList.remove('active-wrap');
        });
    }
    _activeTooltipWrap = null;
    _setSpeakBtnState(false);
};

window.toggleSpeakFull = function() {
    if (!pfCurrentAnswer) return;
    if (window._isSpeakingFull) { stopSpeakFull(); return; }
    if (window._isQuickSpeaking) stopQuickSpeak();
    if (!canUseFeature()) { showLimitMessage(); return; }
    if (!('speechSynthesis' in window)) {
        alert('Trình duyệt không hỗ trợ phát âm.');
        return;
    }
    if (shouldCountUsage()) { incDemoUsage(); updateDemoRemaining(); }
    if ('speechSynthesis' in window) {
        try { speechSynthesis.cancel(); } catch(e) {}
    }
    var token = ++window._speakToken;
    _setSpeakBtnState(true);

    var answerVisible = $('pfAnswer').classList.contains('show');
    if (answerVisible) {
        _speakWithHighlightKaraoke(token);
    } else {
        _speakNormal(token);
    }
};

function _speakNormal(token) {
    var u = new SpeechSynthesisUtterance(pfCurrentAnswer);
    u.lang = 'zh-CN';
    applyVoiceSettings(u);
    var done = false;
    function finish() {
        if (done) return;
        done = true;
        if (token !== window._speakToken) return;
        _setSpeakBtnState(false);
    }
    u.onend = finish;
    u.onerror = finish;
    setTimeout(function() {
        if (token !== window._speakToken) return;
        try { speechSynthesis.speak(u); } catch(e) { finish(); }
    }, 30);
}

function _speakWithHighlightKaraoke(token) {
    var phrases = window._pfPhrases || [];
    var charsContainer = $('pfAnswerChars');
    if (!charsContainer) { _setSpeakBtnState(false); return; }
    var wraps = charsContainer.querySelectorAll('.answer-phrase-wrap');
    var buttons = charsContainer.querySelectorAll('.answer-phrase-btn');
    if (phrases.length === 0) { _speakNormal(token); return; }
    var idx = 0;

    function cleanupAll() {
        buttons.forEach(function(b) { b.classList.remove('reading'); });
        charsContainer.querySelectorAll('.answer-phrase-tooltip.show').forEach(function(t) {
            t.classList.remove('show');
        });
        charsContainer.querySelectorAll('.answer-phrase-wrap.active-wrap').forEach(function(w) {
            w.classList.remove('active-wrap');
        });
        _activeTooltipWrap = null;
    }

    function speakNext() {
        if (token !== window._speakToken) { cleanupAll(); return; }
        if (idx >= phrases.length) {
            cleanupAll();
            _setSpeakBtnState(false);
            return;
        }
        var phrase = phrases[idx];
        var btn = buttons[idx];
        var wrap = wraps[idx];

        if (btn) btn.classList.add('reading');
        if (wrap) {
            wrap.classList.add('active-wrap');
            charsContainer.querySelectorAll('.answer-phrase-tooltip.show').forEach(function(t) {
                t.classList.remove('show');
            });
            var tip = wrap.querySelector('.answer-phrase-tooltip');
            if (tip) {
                tip.classList.add('show');
                _activeTooltipWrap = wrap;
            }
        }

        var u = new SpeechSynthesisUtterance(phrase.text);
        u.lang = 'zh-CN';
        applyVoiceSettings(u);

        var handled = false;
        function next() {
            if (handled) return;
            handled = true;
            if (btn) btn.classList.remove('reading');
            if (wrap) wrap.classList.remove('active-wrap');
            if (token !== window._speakToken) { cleanupAll(); return; }
            idx++;
            setTimeout(speakNext, 120);
        }
        u.onend = next;
        u.onerror = next;
        setTimeout(function() {
            if (token !== window._speakToken) { next(); return; }
            try { speechSynthesis.speak(u); } catch(e) { next(); }
        }, 30);
    }

    setTimeout(speakNext, 100);
}

window._isQuickSpeaking = false;
window._quickSpeakToken = 0;

function _setQuickSpeakBtnState(speaking) {
    window._isQuickSpeaking = speaking;
    var btn = $('pfQuickSpeakBtn');
    if (!btn) return;
    if (speaking) {
        btn.classList.add('speaking');
        btn.setAttribute('title', 'Nhấn để dừng');
        btn.setAttribute('aria-label', 'Nhấn để dừng');
        var i = btn.querySelector('i');
        if (i) i.className = 'fas fa-stop';
    } else {
        btn.classList.remove('speaking');
        btn.setAttribute('title', 'Đọc cả câu');
        btn.setAttribute('aria-label', 'Đọc cả câu');
        var i2 = btn.querySelector('i');
        if (i2) i2.className = 'fas fa-volume-up';
    }
}

window.stopQuickSpeak = function() {
    window._quickSpeakToken++;
    window._isQuickSpeaking = false;
    if ('speechSynthesis' in window) {
        try { speechSynthesis.cancel(); } catch(e) {}
    }
    _setQuickSpeakBtnState(false);
};

window.toggleQuickSpeakFull = function() {
    if (!pfCurrentAnswer) return;
    if (window._isQuickSpeaking) { stopQuickSpeak(); return; }
    if (window._isSpeakingFull) stopSpeakFull();
    if (!canUseFeature()) { showLimitMessage(); return; }
    if (!('speechSynthesis' in window)) {
        alert('Trình duyệt không hỗ trợ phát âm.');
        return;
    }
    if (shouldCountUsage()) { incDemoUsage(); updateDemoRemaining(); }
    if ('speechSynthesis' in window) {
        try { speechSynthesis.cancel(); } catch(e) {}
    }
    var token = ++window._quickSpeakToken;
    _setQuickSpeakBtnState(true);
    _quickSpeakNormal(token);
};

function _quickSpeakNormal(token) {
    var u = new SpeechSynthesisUtterance(pfCurrentAnswer);
    u.lang = 'zh-CN';
    applyVoiceSettings(u);
    var done = false;
    function finish() {
        if (done) return;
        done = true;
        if (token !== window._quickSpeakToken) return;
        _setQuickSpeakBtnState(false);
    }
    u.onend = finish;
    u.onerror = finish;
    setTimeout(function() {
        if (token !== window._quickSpeakToken) return;
        try { speechSynthesis.speak(u); } catch(e) { finish(); }
    }, 30);
}

function initPracticeFull() {
    try {
        var savedRandom = localStorage.getItem('pfRandomMode') === '1';
        if (savedRandom) {
            pfRandomMode = true;
            var rBtnInit = $('pfRandomToggleBtn');
            if (rBtnInit) {
                rBtnInit.classList.add('active');
                rBtnInit.title = 'ĐANG BẬT: Nút Next sẽ nhảy câu ngẫu nhiên';
            }
        }
    } catch(e) {}

    var randomToggleBtn = $('pfRandomToggleBtn');
    if (randomToggleBtn) {
        randomToggleBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            e.preventDefault();
            pfToggleRandom();
        });
    }

    $('pfClose').addEventListener('click', closePracticeFull);
    $('pfPrevBtn').addEventListener('click', pfPrev);
    $('pfNextBtn').addEventListener('click', pfNext);
    $('pfRevealBtn').addEventListener('click', revealFullAnswer);
    $('pfHintBtn').addEventListener('click', toggleHint);
    $('pfInput').addEventListener('input', function() {
        updateCharPreview();
        checkFullAnswer();
    });
    $('pfQuickNav').addEventListener('change', pfQuickNavChange);
    $('pfSearchInput').addEventListener('input', function() { pfApplyFilter(); });
    $('pfClearSearchBtn').addEventListener('click', function() {
        $('pfSearchInput').value = '';
        $('pfSearchInput').focus();
        pfApplyFilter();
    });
    $('pfHskFilter').addEventListener('change', function() {
        var val = this.value;
        var allowed = getAllowedHskList();
        if (val && allowed.indexOf(val) === -1) {
            var info = getTierInfo();
            var msg = info.tier === 'trial'
                ? 'Bản Trial chỉ cho phép lọc HSK1-' + info.maxHSK + '.'
                : 'Bản Demo chỉ cho phép lọc HSK1-' + info.maxHSK + '.';
            alert(msg);
            this.value = '';
            return;
        }
        pfApplyFilter();
    });
    $('pfSubjectFilter').addEventListener('change', function() {
        var val = this.value;
        var allowed = getAllowedSubjectList();
        if (val && allowed.indexOf(val) === -1) {
            var info = getTierInfo();
            var msg = info.tier === 'trial'
                ? 'Chủ đề này chưa có trong ' + info.maxQuestions + ' câu Trial.'
                : 'Chủ đề này chưa có trong ' + info.maxQuestions + ' câu Demo.';
            alert(msg);
            this.value = '';
            return;
        }
        pfApplyFilter();
    });

    document.addEventListener('keydown', function(e) {
        if (!$('practiceFullModal').classList.contains('show')) return;
        var active = document.activeElement;
        var isTyping = active && (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA' || active.tagName === 'SELECT');
        if (e.key === 'Escape') { closePracticeFull(); return; }
        if (isTyping) return;
        if (e.key === 'ArrowRight' && e.ctrlKey) pfNext();
        if (e.key === 'ArrowLeft' && e.ctrlKey) pfPrev();
        if (e.key === 'r' || e.key === 'R') pfToggleRandom();
    });

    var modal = $('practiceFullModal');
    var touchStartX = 0;
    modal.addEventListener('touchstart', function(e) {
        touchStartX = e.touches[0].clientX;
    }, { passive: true });
    modal.addEventListener('touchend', function(e) {
        var dx = e.changedTouches[0].clientX - touchStartX;
        if (Math.abs(dx) > 100) {
            if (dx < 0) pfNext();
            else pfPrev();
        }
    }, { passive: true });

    if (!window._pfSpeakBound) {
        window._pfSpeakBound = true;
        var speakBtn = $('pfSpeakBtn');
        if (speakBtn) {
            speakBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                e.preventDefault();
                toggleSpeakFull();
            });
        }
    }
    if (!window._pfQuickSpeakBound) {
        window._pfQuickSpeakBound = true;
        var quickBtn = $('pfQuickSpeakBtn');
        if (quickBtn) {
            quickBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                e.preventDefault();
                toggleQuickSpeakFull();
            });
        }
    }
}

function pfBuildDatasetSelect() {
    var sel = $('pfDatasetSelect');
    var row = $('pfDatasetRow');
    if (!sel || typeof DATASET_REGISTRY === 'undefined') return;

    var canAccessAll = canAccessChuyenNganh();
    var current = (typeof CURRENT_DATASET !== 'undefined') ? CURRENT_DATASET : 'tonghop';

    sel.innerHTML = '';

    Object.keys(DATASET_REGISTRY).forEach(function(id) {
        var ds = DATASET_REGISTRY[id];
        var isTonghop = (id === 'tonghop');
        var isLocked = !isTonghop && !canAccessAll;

        var opt = document.createElement('option');
        opt.value = id;
        if (isLocked) {
            opt.dataset.locked = '1';
            opt.className = 'locked-opt';
        }

        var dsName = ds.name && ds.name.normalize ? ds.name.normalize('NFC') : ds.name;
        if (isTonghop) {
            opt.textContent = (ds.count || 0) + ' câu - Tổng hợp VPCX';
        } else {
            opt.textContent = (isLocked ? '[Khoá] ' : '') +
                              dsName + ' (' + (ds.count || 0) + ' câu)';
        }

        sel.appendChild(opt);
    });

    sel.value = (current !== 'tonghop' && !canAccessAll) ? 'tonghop' : current;

    if (row) {
        var hasLock = !canAccessAll && Object.keys(DATASET_REGISTRY).length > 1;
        row.classList.toggle('has-locked-options', hasLock);
    }
}

document.addEventListener('change', function(e) {
    if (!e.target || e.target.id !== 'pfDatasetSelect') return;

    var sel = e.target;
    var val = sel.value;
    var opt = sel.options[sel.selectedIndex];
    var currentDataset = (typeof CURRENT_DATASET !== 'undefined') ? CURRENT_DATASET : 'tonghop';

    if (opt && opt.dataset.locked === '1') {
        sel.value = currentDataset;
        showPracticeFullLockMessage();
        return;
    }

    if (val !== 'tonghop' && !canAccessChuyenNganh()) {
        sel.value = currentDataset;
        showPracticeFullLockMessage();
        return;
    }

    var ok = (typeof window.__switchRawData === 'function')
             ? window.__switchRawData(val)
             : false;
    if (!ok) {
        sel.value = currentDataset;
        return;
    }

    window.__onboardingOverride = null;
    var obBanner = $('onboardingActiveBanner');
    if (obBanner) obBanner.remove();

    state = { search:'', hsk:'', subject:'' };
    if ($('pfSearchInput')) $('pfSearchInput').value = '';
    if ($('pfHskFilter')) $('pfHskFilter').value = '';
    if ($('pfSubjectFilter')) $('pfSubjectFilter').value = '';
    if ($('searchInput')) $('searchInput').value = '';
    if ($('hskFilter')) $('hskFilter').value = '';
    if ($('subjectFilter')) $('subjectFilter').value = '';

    if (typeof pfBuildFilterOptions === 'function') pfBuildFilterOptions();

    if (typeof pfApplyFilter === 'function') {
        pfApplyFilter();
    } else if (typeof applyFilter === 'function') {
        applyFilter();
    }

    if (typeof filtered !== 'undefined' && filtered.length > 0) {
        if (typeof loadPracticeFull === 'function') {
            loadPracticeFull(filtered[0].stt);
        }
    }

    pfBuildDatasetSelect();
});

/* ============================================================ */
/* WRITER (Luyện viết chữ Hán) — expired dùng được như Demo      */
/* ============================================================ */
var writerInstance = null;
var currentWriteZh = '';
var currentWriteVi = '';
var currentWritePinyin = '';
var currentCharIndex = 0;

function initWriter() {
    $('writerAnimate').addEventListener('click', function() {
        if (!writerInstance) return;
        $('writerScore').textContent = '';
        $('writerScore').className = 'writer-score';
        writerInstance.cancelQuiz();
        writerInstance.animateCharacter();
    });
    $('writerQuiz').addEventListener('click', function() {
        if (!writerInstance) return;
        $('writerScore').textContent = 'Vẽ chữ bằng ngón tay...';
        $('writerScore').className = 'writer-score';
        writerInstance.quiz({
            onMistake: function(strokeData) {
                $('writerScore').textContent = 'Sai nét ' + (strokeData.strokeNum + 1) + ' - thử lại';
                $('writerScore').className = 'writer-score error';
            },
            onComplete: function(summary) {
                if (summary.totalMistakes === 0) {
                    $('writerScore').textContent = 'Tuyệt vời! Viết đúng tất cả các nét!';
                    $('writerScore').className = 'writer-score success';
                } else {
                    $('writerScore').textContent = 'Hoàn thành! Số nét sai: ' + summary.totalMistakes;
                    $('writerScore').className = 'writer-score';
                }
            }
        });
    });
    $('writerReset').addEventListener('click', function() {
        if (!writerInstance) return;
        $('writerScore').textContent = '';
        $('writerScore').className = 'writer-score';
        writerInstance.cancelQuiz();
        var chars = currentWriteZh.split('').filter(function(c) { return /[\u4e00-\u9fa5]/.test(c); });
        var currentChar = chars[currentCharIndex];
        if (currentChar) showWriterChar(currentChar);
    });
    $('writerClose').addEventListener('click', closeWriter);
    $('writerModal').addEventListener('click', function(e) {
        if (e.target === this) closeWriter();
    });
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeWriter();
    });
}

window.openWriter = function(zh, vi, pinyin, evt) {
    if (evt) { evt.stopPropagation(); if (evt.preventDefault) evt.preventDefault(); }
    if (!canUseFeature()) { showLimitMessage(); return; }
    if (typeof HanziWriter === 'undefined') { alert('Thư viện chưa tải xong.'); return; }
    if (shouldCountUsage()) { incDemoUsage(); updateDemoRemaining(); }
    currentWriteZh = zh || '';
    currentWriteVi = vi || '';
    currentWritePinyin = pinyin || '';
    currentCharIndex = 0;
    var chars = currentWriteZh.split('').filter(function(c) { return /[\u4e00-\u9fa5]/.test(c); });
    if (chars.length === 0) { alert('Câu này không có chữ Hán.'); return; }
    $('writerModal').classList.add('show');
    $('writerScore').textContent = '';
    $('writerScore').className = 'writer-score';
    $('writerViSmall').textContent = currentWriteVi;
    $('writerPinyinSmall').textContent = currentWritePinyin;
    renderWriterChars(chars);
    showWriterChar(chars[0]);
};

window.closeWriter = function() {
    $('writerModal').classList.remove('show');
    writerInstance = null;
};

function renderWriterChars(chars) {
    var container = $('writerChars');
    if (chars.length <= 1) { container.innerHTML = ''; return; }
    container.innerHTML = chars.map(function(c, i) {
        return '<button class="writer-char-btn' + (i === 0 ? ' active' : '') + '" data-idx="' + i + '" data-char="' + c + '">' + c + '</button>';
    }).join('');
    container.querySelectorAll('.writer-char-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var idx = parseInt(this.dataset.idx);
            var ch = this.dataset.char;
            container.querySelectorAll('.writer-char-btn').forEach(function(b) { b.classList.remove('active'); });
            this.classList.add('active');
            currentCharIndex = idx;
            $('writerScore').textContent = '';
            $('writerScore').className = 'writer-score';
            showWriterChar(ch);
        });
    });
}

function showWriterChar(char) {
    var target = $('writerTarget');
    target.innerHTML = '<div class="writer-loading"><i class="fas fa-spinner fa-pulse"></i>Đang tải...</div>';
    writerInstance = null;
    setTimeout(function() {
        try {
            target.innerHTML = '';
            var targetSize = target.offsetWidth || 280;
            var padSize = Math.round(targetSize * 0.06);
            var drawWidth = Math.round(targetSize * 0.07);
            writerInstance = HanziWriter.create('writerTarget', char, {
                width: targetSize, height: targetSize, padding: padSize,
                strokeColor: '#1e293b', radicalColor: '#7c3aed',
                highlightColor: '#f59e0b', outlineColor: '#cbd5e1',
                drawingColor: '#7c3aed', drawingWidth: drawWidth,
                showOutline: true, strokeAnimationSpeed: 1, delayBetweenStrokes: 250,
                charDataLoader: function(ch, onComplete, onError) {
                    fetch('https://cdn.jsdelivr.net/npm/hanzi-writer-data@2.0/' + encodeURIComponent(ch) + '.json')
                        .then(function(res) { if (!res.ok) throw new Error('Không có dữ liệu'); return res.json(); })
                        .then(onComplete)
                        .catch(function(err) {
                            if (onError) onError(err);
                            target.innerHTML = '<div class="writer-loading"><i class="fas fa-exclamation-triangle" style="color:#dc2626"></i>Không tải được dữ liệu.</div>';
                        });
                }
            });
        } catch(e) {
            target.innerHTML = '<div class="writer-loading"><i class="fas fa-exclamation-triangle"></i>Lỗi tạo khung vẽ</div>';
        }
    }, 100);
}
"""
