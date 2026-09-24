# -*- coding: utf-8 -*-
"""Load + validate config.json."""
import json
import os
import sys

CONFIG_FILE = "scripts/config.json"

DEFAULT_SYNONYMS = {
    "我": ["俺", "本人", "咱"], "你": ["您", "阁下"], "他": ["她", "它"],
    "是": ["系", "为"], "的": ["之"], "不": ["没", "未"],
    "很": ["非常", "十分", "特别"], "好": ["棒", "优秀", "不错"],
    "说": ["讲", "谈"], "看": ["瞧", "望"], "吃": ["食", "用"],
    "给": ["送", "赠"], "想要": ["想", "要"],
    "越南": ["越南"], "中国": ["中华"],
    "谢谢": ["感谢", "多谢"], "对不起": ["抱歉", "不好意思"],
    "再见": ["拜拜", "再会"], "请": ["麻烦", "拜托"],
}
DEFAULT_FILLERS = ["了", "的", "吗", "呢", "吧", "啊", "呀", "哦", "嘛", "哈", "哪", "着", "过"]


def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Không tìm thấy file cấu hình: {CONFIG_FILE}")
        sys.exit(1)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    if not cfg.get("firebase_config", {}).get("apiKey"):
        print(f"❌ Firebase config chưa được cấu hình trong {CONFIG_FILE}")
        sys.exit(1)

    # ═══════════════════════════════════════════════════
    # Defaults cơ bản
    # ═══════════════════════════════════════════════════
    cfg.setdefault("excel_file", "data/input.xlsx")
    cfg.setdefault("output_html", "index.html")
    cfg.setdefault("sheet_index", 0)

    # ═══════════════════════════════════════════════════
    # DEMO tier — chưa đăng nhập
    # ═══════════════════════════════════════════════════
    cfg.setdefault("demo_limit", 25)
    cfg.setdefault("demo_daily_limit", 50)
    cfg.setdefault("demo_hsk_max", 3)

    # ═══════════════════════════════════════════════════
    # TRIAL tier — user mới đăng ký
    # ═══════════════════════════════════════════════════
    cfg.setdefault("trial_days", 3)
    cfg.setdefault("trial_max_questions", 50)
    cfg.setdefault("trial_max_hsk", 5)
    cfg.setdefault("trial_unlimited_writing", True)

    # ═══════════════════════════════════════════════════
    # Admin
    # ═══════════════════════════════════════════════════
    cfg.setdefault("target_admins", 2)
    cfg.setdefault("super_admin", "hoanginvest@gmail.com")

    # ═══════════════════════════════════════════════════
    # Social
    # ═══════════════════════════════════════════════════
    cfg.setdefault("zalo_phone", "")
    cfg.setdefault("zalo_name", "Hỗ trợ")
    cfg.setdefault("tiktok_username", "thaonoizhongwen")
    cfg.setdefault("tiktok_nickname", "Thảo nói 中文")
    cfg.setdefault("tiktok_avatar", "")
    cfg.setdefault("tiktok_url",
                   f"https://www.tiktok.com/@{cfg['tiktok_username']}")

    # ═══════════════════════════════════════════════════
    # Smart check
    # ═══════════════════════════════════════════════════
    cfg.setdefault("synonyms", DEFAULT_SYNONYMS)
    cfg.setdefault("filler_words", DEFAULT_FILLERS)

    # ═══════════════════════════════════════════════════
    # Gia hạn — bank + packages
    # ═══════════════════════════════════════════════════
    cfg.setdefault("bank_config", {
        "bank_id": "970418",
        "bank_name": "BIDV",
        "account_no": "8897014076",
        "account_name": "NGUYEN THI THAO"
    })
    cfg.setdefault("packages", [
        {"id": "1m", "label": "1 tháng", "amount": 50000, "days": 30, "popular": False},
        {"id": "3m", "label": "3 tháng", "amount": 100000, "days": 90,
         "popular": True, "save": "Tiết kiệm 33%"},
        {"id": "1y", "label": "1 năm", "amount": 250000, "days": 365,
         "popular": False, "save": "Tiết kiệm 58%"},
        {"id": "forever", "label": "Premium", "amount": 1000000, "days": 36500,
         "popular": False, "save": "Dùng mãi mãi", "permanent": True}
    ])
    cfg.setdefault("renewal_support_zalo", cfg["zalo_phone"])

    # ═══════════════════════════════════════════════════
    # Telegram
    # ═══════════════════════════════════════════════════
    cfg.setdefault("telegram_bot_token", "")
    cfg.setdefault("telegram_chat_id", "")

    # ═══════════════════════════════════════════════════
    # Onboarding — chọn chủ đề quan tâm (Demo + Trial)
    # ═══════════════════════════════════════════════════
    # Mỗi tier có config riêng. Có thể tinh chỉnh trong config.json:
    #   - enabled:          bật/tắt onboarding
    #   - max_questions:    số câu tối đa sẽ gợi ý (chia đều theo HSK)
    #   - hsk_allowed:      danh sách HSK số [1,2,3] → JS tự map thành HSK1,HSK2,HSK3
    #   - topics_per_user:  số chủ đề tối đa user được chọn
    #   - title/subtitle:   text hiển thị trên modal
    cfg.setdefault("onboarding", {
        "demo": {
            "enabled": True,
            "max_questions": cfg.get("demo_limit", 25),
            "hsk_allowed": list(range(1, cfg.get("demo_hsk_max", 3) + 1)),
            "topics_per_user": 3,
            "title": "Bạn quan tâm chủ đề nào?",
            "subtitle": "Chọn tối đa 3 chủ đề — chúng tôi sẽ gợi ý câu phù hợp nhất"
        },
        "trial": {
            "enabled": True,
            "max_questions": cfg.get("trial_max_questions", 50),
            "hsk_allowed": list(range(1, cfg.get("trial_max_hsk", 5) + 1)),
            "topics_per_user": 5,
            "title": "Bạn quan tâm chủ đề nào?",
            "subtitle": "Chọn tối đa 5 chủ đề — chúng tôi sẽ gợi ý câu phù hợp nhất"
        }
    })

    return cfg


def print_banner(CONFIG):
    """In thông tin config khi build. Dùng .get() để tránh KeyError."""
    print(f"⚙️  Đã đọc cấu hình từ: {CONFIG_FILE}")
    print(f"   📄 Excel: {CONFIG.get('excel_file', 'N/A')}")
    print(f"   📤 Output: {CONFIG.get('output_html', 'N/A')}")
    print(f"   📞 Zalo: {CONFIG.get('zalo_phone', 'N/A')} ({CONFIG.get('zalo_name', '')})")
    print(f"   🎵 TikTok: @{CONFIG.get('tiktok_username', 'N/A')} ({CONFIG.get('tiktok_nickname', '')})")
    print(f"   🖼️  TikTok Avatar: {'Có' if CONFIG.get('tiktok_avatar') else 'Không (dùng fallback)'}")
    print(f"   🎁 Demo: {CONFIG.get('demo_limit', 25)} câu + HSK1-{CONFIG.get('demo_hsk_max', 3)} "
          f"+ {CONFIG.get('demo_daily_limit', 50)} lượt/ngày")
    print(f"   👑 Super admin: {CONFIG.get('super_admin', 'N/A')}")
    print(f"   🎉 Trial {CONFIG.get('trial_days', 3)} ngày cho user mới đăng ký")
    print(f"   📚 Trial limits: {CONFIG.get('trial_max_questions', 50)} câu, "
          f"HSK1-{CONFIG.get('trial_max_hsk', 5)}, "
          f"nghe viết {'KHÔNG' if CONFIG.get('trial_unlimited_writing', True) else 'CÓ'} giới hạn")

    # ─── Onboarding ───
    onb = CONFIG.get('onboarding', {})
    if onb.get('demo', {} 🎯).get('enabled'):
        d = On onb['demo']
       boarding print(f"   🎯 Onboarding Demo Demo: {d.get('max_questions', 0)} câu, "
              f"HSK {d.get('hsk_allowed', [])}, "
              f"tối đa {d.get('topics_per_user', 3)} chủ đề")
    else:
        print(f"  : TẮT")

    if onb.get('trial', {}).get('enabled'):
        t = onb['trial']
        print(f"   🎯 Onboarding Trial: {t.get('max_questions', 0)} câu, "
              f"HSK {t.get('hsk_allowed', [])}, "
              f"tối đa {t.get('topics_per_user', 5)} chủ đề")
    else:
        print(f"   🎯 Onboarding Trial: TẮT")

    bank = CONFIG.get('bank_config', {})
    print(f"   🏦 Bank: {bank.get('bank_name', 'N/A')} - {bank.get('account_no', 'N/A')}")
    packages = CONFIG.get('packages', [])
    print(f"   💰 Packages: {len(packages)} gói")
    permanent_count = sum(1 for p in packages if p.get("permanent"))
    if permanent_count:
        print(f"   💎 Có {permanent_count} gói VĨNH VIỄN")
    # Telegram
    if CONFIG.get('telegram_bot_token') and CONFIG.get('telegram_chat_id'):
        print(f"   📲 Telegram: ĐÃ bật (chat_id: {CONFIG['telegram_chat_id']})")
    else:
        print(f"   📲 Telegram: CHƯA cấu hình (thiếu token hoặc chat_id)")
