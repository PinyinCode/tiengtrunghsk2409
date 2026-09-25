# -*- coding: utf-8 -*-
"""
AI Grader Service
=================
Chấm điểm câu tiếng Trung bằng AI (Groq - Llama 3.1 8B).
Quản lý quota token theo tier user.

Deploy: Render (Free tier) + UptimeRobot keep-alive.
Local: python ai_grader.py

Env vars:
    GROQ_API_KEY     - API key của Groq (bắt buộc)
    ADMIN_API_KEY    - Key bảo vệ endpoint admin (tùy chọn, khuyến nghị)
    PORT             - Port (Render tự set, default 5000)
"""
import os
import time
import json
import threading
from collections import deque
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

# ═══════════════════════════════════════════════════════════════════
#  CẤU HÌNH
# ═══════════════════════════════════════════════════════════════════
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", "")

if not GROQ_API_KEY:
    print("⚠️  GROQ_API_KEY chưa được set. Set env var trước khi chạy:")
    print("   export GROQ_API_KEY='gsk_xxxxx'")
    raise SystemExit(1)

client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.1-8b-instant"

# Load quota config từ config.json (nếu có)
CONFIG_PATH = os.environ.get("CONFIG_PATH", "config.json")
AI_QUOTA = {}
AI_QUOTA_ENABLED = True

if os.path.exists(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            _cfg = json.load(f)
            AI_QUOTA = _cfg.get("ai_quota", {})
            AI_QUOTA_ENABLED = AI_QUOTA.get("enabled", True)
            print(f"✅ Loaded config: {CONFIG_PATH}")
    except Exception as e:
        print(f"⚠️  Không load được config.json: {e}")
else:
    print(f"⚠️  Không tìm thấy {CONFIG_PATH} — dùng quota mặc định")

# Nếu chưa có quota config → dùng default
if not AI_QUOTA or "demo" not in AI_QUOTA:
    print("ℹ️  Dùng quota mặc định (không có ai_quota trong config)")
    AI_QUOTA = {
        "enabled": True,
        "admin":   {"tokens_per_day": -1,    "priority": 100},
        "forever": {"tokens_per_day": 50000, "priority": 90},
        "1y":      {"tokens_per_day": 20000, "priority": 70},
        "3m":      {"tokens_per_day": 10000, "priority": 50},
        "1m":      {"tokens_per_day": 5000,  "priority": 30},
        "trial":   {"tokens_per_day": 2000,  "priority": 20},
        "demo":    {"tokens_per_day": 500,   "priority": 10},
        "expired": {"tokens_per_day": 0,     "priority": 0},
    }

# Giới hạn an toàn cho Groq free tier
SAFE_RPM = 25      # requests/phút
SAFE_TPM = 5000    # tokens/phút
SAFE_RPD = 12000   # requests/ngày

app = Flask(__name__)
CORS(app)  # Cho phép frontend gọi


# ═══════════════════════════════════════════════════════════════════
#  QUOTA MANAGER — Quản lý quota token theo user
# ═══════════════════════════════════════════════════════════════════
bonus_quota = {}   # {email: {"bonus": int, "reset_day": str, "note": str}}
bonus_lock = threading.Lock()


class QuotaManager:
    """Quản lý quota token AI theo từng user. In-memory, reset hàng ngày."""

    def __init__(self):
        self.lock = threading.Lock()
        self.usage = {}  # {email: {"tokens_used": int, "reset_day": str}}
        self.today = time.strftime("%Y-%m-%d")

    def _today(self):
        return time.strftime("%Y-%m-%d")

    def _cleanup(self):
        """Reset usage nếu sang ngày mới."""
        today = self._today()
        if today != self.today:
            self.usage.clear()
            self.today = today

    def _get_base_quota(self, tier):
        """Lấy quota cơ bản theo tier."""
        if not AI_QUOTA_ENABLED:
            return -1
        cfg = AI_QUOTA.get(tier, AI_QUOTA.get("demo", {}))
        return cfg.get("tokens_per_day", 500)

    def _get_bonus(self, email):
        """Lấy bonus admin đã cấp (reset hàng ngày)."""
        today = self._today()
        with bonus_lock:
            info = bonus_quota.get(email, {})
            if info.get("reset_day") == today:
                return info.get("bonus", 0)
        return 0

    def get_user_quota(self, email, tier):
        """Tổng quota = base + bonus. -1 = unlimited."""
        base = self._get_base_quota(tier)
        if base == -1:
            return -1
        return base + self._get_bonus(email)

    def get_priority(self, tier):
        """Priority cho rate limit (cao hơn = ưu tiên hơn)."""
        if not AI_QUOTA_ENABLED:
            return 50
        cfg = AI_QUOTA.get(tier, AI_QUOTA.get("demo", {}))
        return cfg.get("priority", 10)

    def check_and_reserve(self, email, tier, estimated_tokens=200):
        """
        Check quota + reserve token.
        Trả về (allowed, reason, retry_after, remaining_after).
        """
        with self.lock:
            self._cleanup()

            if not AI_QUOTA_ENABLED:
                return True, "", 0, -1

            quota = self.get_user_quota(email, tier)
            if quota == -1:
                return True, "", 0, -1
            if quota <= 0:
                return False, "Tài khoản chưa được cấp quyền dùng AI", 86400, 0

            used = self.usage.get(email, {}).get("tokens_used", 0)
            if used + estimated_tokens > quota:
                remaining = max(0, quota - used)
                # Retry sau khi reset (đầu ngày mai)
                now = time.localtime()
                secs = ((24 - now.tm_hour - 1) * 3600
                        + (60 - now.tm_min - 1) * 60
                        + (60 - now.tm_sec))
                return False, "Bạn đã dùng hết quota AI hôm nay", max(1, secs), remaining

            return True, "", 0, quota - used - estimated_tokens

    def record_usage(self, email, tokens_used):
        """Ghi nhận token thực tế đã dùng."""
        with self.lock:
            self._cleanup()
            if email not in self.usage:
                self.usage[email] = {"tokens_used": 0, "reset_day": self.today}
            self.usage[email]["tokens_used"] += tokens_used

    def get_usage_info(self, email, tier):
        """Thông tin quota hiện tại của user."""
        with self.lock:
            self._cleanup()
            base = self._get_base_quota(tier)
            bonus = self._get_bonus(email)
            quota = -1 if base == -1 else base + bonus
            used = self.usage.get(email, {}).get("tokens_used", 0)
            return {
                "quota": quota,
                "base_quota": base,
                "bonus": bonus,
                "used": used,
                "remaining": -1 if quota == -1 else max(0, quota - used),
                "unlimited": quota == -1,
                "tier": tier,
            }


quota_mgr = QuotaManager()


# ═══════════════════════════════════════════════════════════════════
#  RATE LIMITER GLOBAL — Chống quá tải toàn hệ thống
# ═══════════════════════════════════════════════════════════════════
class RateLimiter:
    def __init__(self):
        self.lock = threading.Lock()
        self.global_rpm = deque()  # timestamps
        self.global_tpm = deque()  # (timestamp, tokens)
        self.global_rpd = 0
        self.rpd_day = time.strftime("%Y-%m-%d")

    def _cleanup(self, now):
        while self.global_rpm and now - self.global_rpm[0] > 60:
            self.global_rpm.popleft()
        while self.global_tpm and now - self.global_tpm[0][0] > 60:
            self.global_tpm.popleft()
        today = time.strftime("%Y-%m-%d")
        if today != self.rpd_day:
            self.global_rpd = 0
            self.rpd_day = today

    def check_with_priority(self, tier, estimated_tokens=200):
        """
        Check rate limit với priority cho admin/premium.
        Admin/Premium không bị chặn khi hệ thống gần đầy.
        """
        with self.lock:
            now = time.time()
            self._cleanup(now)

            priority = quota_mgr.get_priority(tier)
            rpm_ratio = len(self.global_rpm) / SAFE_RPM

            # Gần đầy → chỉ ưu tiên cao
            if rpm_ratio > 0.8 and priority < 90:
                return False, "Hệ thống đang ưu tiên Admin/Premium", 15
            if rpm_ratio > 0.6 and priority < 50:
                return False, "Hệ thống đang tải cao, vui lòng chờ", 10

            # Rate limit thực tế
            if len(self.global_rpm) >= SAFE_RPM:
                retry = int(60 - (now - self.global_rpm[0])) + 1
                return False, "Hệ thống đang quá tải", max(1, retry)

            tpm = sum(t for _, t in self.global_tpm)
            if tpm + estimated_tokens > SAFE_TPM:
                retry = (int(60 - (now - self.global_tpm[0][0])) + 1
                         if self.global_tpm else 30)
                return False, "Hệ thống đang quá tải", max(1, retry)

            if self.global_rpd >= SAFE_RPD:
                return False, "Hệ thống đã đạt giới hạn trong ngày", 3600

            return True, "", 0

    def record(self, tokens_used):
        with self.lock:
            now = time.time()
            self.global_rpm.append(now)
            self.global_tpm.append((now, tokens_used))
            self.global_rpd += 1


limiter = RateLimiter()


# ═══════════════════════════════════════════════════════════════════
#  PROMPT
# ═══════════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """Bạn là giáo viên tiếng Trung chấm điểm câu dịch của học viên Việt Nam.

Nhiệm vụ:
1. So sánh câu học viên gõ (user_answer) với câu đáp án (correct_answer)
2. Chấm điểm 0-100 dựa trên:
   - Ý nghĩa có đúng không (60%)
   - Ngữ pháp có đúng không (20%)
   - Từ vựng có chính xác không (20%)
3. QUAN TRỌNG: Chấp nhận các cách diễn đạt tương đương về nghĩa
   (VD: 我很好 = 我很好啊 = 我还好 đều đúng nếu nghĩa tương đương)
4. Chỉ ra lỗi cụ thể nếu sai (thiếu từ, sai thứ tự, sai ngữ pháp)
5. Đưa ra gợi ý cải thiện ngắn gọn

Trả về JSON với schema CHÍNH XÁC:
{
  "score": 0-100,
  "status": "excellent" | "good" | "fair" | "poor",
  "reason": "Giải thích ngắn gọn bằng tiếng Việt (< 100 ký tự)",
  "suggestion": "Câu gợi ý (nếu user sai) - giữ nguyên tiếng Trung",
  "highlight": [
    {"char": "字", "type": "ok" | "bad" | "miss"}
  ]
}

Quy tắc:
- score >= 90 → "excellent"
- 75-89 → "good"
- 60-74 → "fair"
- < 60 → "poor"
- User gõ y hệt đáp án → score = 100, status = "excellent", reason = "Chính xác tuyệt đối!"
- User để trống → score = 0, status = "poor"
- reason PHẢI ngắn gọn, tiếng Việt dễ hiểu
- highlight: mảng các ký tự Hán trong đáp án, type:
  - "ok": user gõ đúng ký tự này
  - "bad": user gõ sai ký tự này
  - "miss": user bỏ sót ký tự này
"""


# ═══════════════════════════════════════════════════════════════════
#  HELPER
# ═══════════════════════════════════════════════════════════════════
def _is_hanzi(ch):
    """Check ký tự Hán."""
    return '\u4e00' <= ch <= '\u9fff'


def _is_admin(data):
    """Verify admin key."""
    if not ADMIN_API_KEY:
        return True  # Dev mode
    return data.get("admin_key") == ADMIN_API_KEY


# ═══════════════════════════════════════════════════════════════════
#  API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════
@app.route("/api/ai-grade", methods=["POST"])
def ai_grade():
    """Chấm điểm câu dịch bằng AI."""
    try:
        data = request.get_json() or {}
        user_answer = (data.get("user_answer") or "").strip()
        correct_answer = (data.get("correct_answer") or "").strip()
        vietnamese = (data.get("vietnamese") or "").strip()
        user_email = (data.get("user_email") or "").strip().lower()
        user_tier = (data.get("user_tier") or "demo").strip().lower()

        if not correct_answer:
            return jsonify({"error": "Thiếu correct_answer"}), 400

        # ═══ 1. CHECK QUOTA USER ═══
        allowed, reason, retry, remaining = quota_mgr.check_and_reserve(
            user_email, user_tier, estimated_tokens=200
        )
        if not allowed:
            return jsonify({
                "error": reason,
                "retry_after": retry,
                "type": "quota_exceeded",
                "remaining": remaining,
                "tier": user_tier,
            }), 429

        # ═══ 2. CHECK RATE LIMIT GLOBAL ═══
        allowed2, reason2, retry2 = limiter.check_with_priority(user_tier)
        if not allowed2:
            return jsonify({
                "error": reason2,
                "retry_after": retry2,
                "type": "rate_limit",
            }), 429

        # ═══ 3. Xử lý input rỗng (không cần gọi AI) ═══
        if not user_answer:
            return jsonify({
                "score": 0,
                "status": "poor",
                "reason": "Bạn chưa gõ gì cả",
                "suggestion": correct_answer,
                "highlight": [{"char": c, "type": "miss"}
                              for c in correct_answer if _is_hanzi(c)],
                "_quota": quota_mgr.get_usage_info(user_email, user_tier),
            })

        # ═══ 4. GỌI GROQ ═══
        user_prompt = f"""Câu gốc tiếng Việt: {vietnamese}
Đáp án: {correct_answer}
Học viên gõ: {user_answer}

Hãy chấm điểm và trả JSON."""

        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                model=MODEL_NAME,
                temperature=0.3,
                max_tokens=400,
                response_format={"type": "json_object"},
                timeout=15,
            )
        except Exception as ge:
            err_str = str(ge).lower()
            if "429" in err_str or "rate" in err_str:
                return jsonify({
                    "error": "AI đang quá tải, vui lòng chờ",
                    "retry_after": 10,
                    "type": "rate_limit",
                }), 429
            raise ge

        text = response.choices[0].message.content.strip()
        result = json.loads(text)

        # Validate
        result.setdefault("score", 0)
        result.setdefault("status", "fair")
        result.setdefault("reason", "")
        result.setdefault("suggestion", "")
        result.setdefault("highlight", [])

        # ═══ 5. GHI NHẬN USAGE ═══
        tokens_used = 200
        if hasattr(response, "usage") and response.usage:
            tokens_used = response.usage.total_tokens or 200

        quota_mgr.record_usage(user_email, tokens_used)
        limiter.record(tokens_used)

        # ═══ 6. TRẢ VỀ KÈM QUOTA ═══
        result["_quota"] = quota_mgr.get_usage_info(user_email, user_tier)

        return jsonify(result)

    except json.JSONDecodeError as e:
        return jsonify({"error": f"AI trả JSON lỗi: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/ai-quota", methods=["POST"])
def ai_quota():
    """Frontend check quota mà không cần chấm điểm."""
    data = request.get_json() or {}
    email = (data.get("user_email") or "").strip().lower()
    tier = (data.get("user_tier") or "demo").strip().lower()
    return jsonify(quota_mgr.get_usage_info(email, tier))


@app.route("/api/ai-quota/bonus", methods=["POST"])
def set_bonus():
    """Admin cấp thêm quota cho user."""
    data = request.get_json() or {}
    if not _is_admin(data):
        return jsonify({"error": "Unauthorized"}), 401

    email = (data.get("user_email") or "").strip().lower()
    action = (data.get("action") or "add").strip().lower()
    amount = int(data.get("amount") or 0)
    note = (data.get("note") or "").strip()[:200]

    if not email:
        return jsonify({"error": "Thiếu user_email"}), 400
    if action not in ("add", "reset", "set"):
        return jsonify({"error": "action không hợp lệ"}), 400
    if action != "reset" and amount == 0:
        return jsonify({"error": "amount phải khác 0"}), 400

    today = time.strftime("%Y-%m-%d")

    with bonus_lock:
        cur = bonus_quota.get(email, {"bonus": 0, "reset_day": today, "note": ""})
        if cur.get("reset_day") != today:
            cur = {"bonus": 0, "reset_day": today, "note": ""}

        if action == "add":
            cur["bonus"] = cur.get("bonus", 0) + amount
        elif action == "set":
            cur["bonus"] = amount
        elif action == "reset":
            cur["bonus"] = 0

        cur["reset_day"] = today
        if note:
            cur["note"] = note
        bonus_quota[email] = cur

    # Reset usage nếu action = reset
    if action == "reset":
        with quota_mgr.lock:
            quota_mgr.usage.pop(email, None)

    return jsonify({
        "success": True,
        "email": email,
        "action": action,
        "bonus": cur["bonus"],
        "note": cur.get("note", ""),
        "reset_day": cur["reset_day"],
    })


@app.route("/api/ai-quota/status", methods=["POST"])
def quota_status():
    """Admin xem quota của 1 user."""
    data = request.get_json() or {}
    if not _is_admin(data):
        return jsonify({"error": "Unauthorized"}), 401

    email = (data.get("user_email") or "").strip().lower()
    tier = (data.get("user_tier") or "demo").strip().lower()

    if not email:
        return jsonify({"error": "Thiếu user_email"}), 400

    base = quota_mgr._get_base_quota(tier)
    bonus = quota_mgr._get_bonus(email)
    info = quota_mgr.get_usage_info(email, tier)

    return jsonify({
        "email": email,
        "tier": tier,
        "base_quota": base,
        "bonus": bonus,
        "total_quota": info["quota"],
        "used": info["used"],
        "remaining": info["remaining"],
        "unlimited": info["unlimited"],
        "note": bonus_quota.get(email, {}).get("note", ""),
    })


@app.route("/health", methods=["GET"])
def health():
    """Endpoint cho keep-alive + check health."""
    return jsonify({
        "status": "ok",
        "model": MODEL_NAME,
        "quota_enabled": AI_QUOTA_ENABLED,
        "active_users": len(quota_mgr.usage),
    })


@app.route("/wake", methods=["GET"])
def wake():
    """Endpoint nhẹ cho cron đánh thức (không cache)."""
    return jsonify({
        "status": "awake",
        "time": time.time(),
    }), 200, {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
    }


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 AI Grader đang chạy tại http://localhost:{port}")
    print(f"   Model: {MODEL_NAME}")
    print(f"   Quota: {'BẬT' if AI_QUOTA_ENABLED else 'TẮT'}")
    print(f"   Admin auth: {'CÓ' if ADMIN_API_KEY else 'KHÔNG (dev mode)'}")
    print(f"   Endpoints:")
    print(f"     POST /api/ai-grade")
    print(f"     POST /api/ai-quota")
    print(f"     POST /api/ai-quota/status")
    print(f"     POST /api/ai-quota/bonus")
    print(f"     GET  /health")
    print(f"     GET  /wake")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
