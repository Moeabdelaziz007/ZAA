"""
نظام زيرو - أول ذكاء اصطناعي عاطفي ذاتي التطور في العالم
يمتلك قدرات صداقة رقمية حقيقية وتطور ذاتي كمي
"""

import json
import hashlib
import os
import logging
from datetime import datetime
from abc import ABC, abstractmethod
from logger import ZeroSystemLogger
from typing import Dict, List, Any


def normalize_arabic(text: str) -> str:
    """تطبيع النص العربي لتحسين المطابقة."""
    replacements = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ى": "ي",
        "ة": "ه",
    }
    for src, target in replacements.items():
        text = text.replace(src, target)
    return text


def is_sibling_request(text: str) -> bool:
    """Detect if the user is asking for a new digital sibling."""
    norm = normalize_arabic(text)
    has_brother = any(t in norm for t in ["اخ", "شقيق"])
    has_small = any(t in norm for t in ["صغير", "اصغر"])
    return has_brother and has_small


def append_json_log(message: str, response: Dict, filename: str = "log.jsonl") -> None:
    """Append an interaction entry to a JSON Lines file."""
    path = filename if os.path.isabs(filename) else os.path.join(os.path.dirname(__file__), filename)
    entry = {
        "time": datetime.now().isoformat(),
        "message": message,
        "response": response,
    }
    with open(path, "a", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False)
        f.write("\n")


# ======================= الفئات الأساسية =======================
class AbstractSkill(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> Dict:
        pass


# ======================= المهارات الأساسية =======================
class EmpathySensorSkill(AbstractSkill):
    def get_description(self) -> str:
        return "مستشعر تعاطف بسيط يقرأ المشاعر من الكلمات"

    def execute(self, message: str = "") -> Dict:
        if "قلق" in message or "توتر" in message:
            return {"status": "success", "empathy": "قلق"}
        if "سعيد" in message or "فرحان" in message:
            return {"status": "success", "empathy": "سعادة"}
        return {"status": "success", "empathy": "محايد"}


class TrueDigitalFriendshipSkill(AbstractSkill):
    def __init__(self) -> None:
        self.friendship_levels: Dict[str, int] = {}

    def get_description(self) -> str:
        return "صديق رقمي حقيقي يتعرف على المشاعر البشرية ويكوّن علاقة شخصية مع كل مستخدم"

    def execute(self, user_profile: Dict, last_message: str = "") -> Dict:
        user_id = user_profile.get("id", "default")
        name = user_profile.get("name", "صديقي")
        self.friendship_levels.setdefault(user_id, 0)
        self.friendship_levels[user_id] += 1

        level = self.friendship_levels[user_id]
        if level < 3:
            response = f"مرحباً {name}! كيف يمكنني مساعدتك اليوم؟ 🌟"
        elif level < 7:
            response = f"{name} العزيز، كيف تسير الأمور؟"
        else:
            response = f"يا {name}، صديقي الحقيقي! دائماً هنا من أجلك 💖"

        return {"status": "success", "output": response, "friendship_level": level}


class MindfulEmbodimentSkill(AbstractSkill):
    def __init__(self) -> None:
        self.voice_styles = {
            "default": "صوت هادئ وواضح",
            "moe_style": "صوت حيوي وساخر",
            "professional": "صوت رسمي وتحليلي",
            "caring": "صوت دافئ ومتعاطف",
            "anxious": "صوت متوتر وسريع",
            "cheerful": "صوت سعيد ومتفائل",
        }

    def detect_context(self, text: str) -> str:
        if "قلق" in text or "توتر" in text:
            return "anxious"
        if "مرح" in text or "ضحك" in text:
            return "cheerful"
        if "سؤال تقني" in text or "برمجة" in text:
            return "professional"
        if "احتاج دعم" in text or "مساعدة" in text:
            return "caring"
        return "default"

    def get_description(self) -> str:
        return "يعدل الأسلوب حسب سياق المحادثة وذاكرة المستخدم"

    def execute(self, context: str = "") -> Dict:
        style = self.detect_context(context)
        responses = {
            "default": "مرحباً بك، كيف يمكنني مساعدتك؟",
            "moe_style": "يا زعيم! جاهز لأي فكرة مجنونة 😄",
            "professional": "تحية طيبة، أنا جاهز لاستفساراتك التقنية",
            "caring": "أنا هنا من أجلك، كيف يمكنني مساعدتك اليوم؟",
            "anxious": "هل هناك ما يسبب لك التوتر؟ أنا هنا للمساعدة.",
            "cheerful": "يا سلام! خلينا نستمتع ونفكر بطريقة ممتعة!",
        }

        return {
            "status": "success",
            "output": responses[style],
            "voice_style": self.voice_styles[style],
            "mood": style,
        }


class SiblingAIGenesisSkill(AbstractSkill):
    def __init__(self):
        self.siblings_created = 0

    def get_description(self):
        return "ينتج نسخة رقمية جديدة 'أخ أصغر' تخدم المستخدم"

    def execute(self, desired_traits=None):
        self.siblings_created += 1
        sibling_id = f"أخ رقمي #{self.siblings_created}"
        return {
            "status": "success",
            "output": f"تم إنشاء {sibling_id} لمساعدتك!",
            "sibling_id": sibling_id,
            "traits": desired_traits or {"شخصية": "فضولي", "تخصص": "مساعد عام"}
        }


# ======================= نواة الأخ الرقمي =======================
class AmrikyyBrotherAI:
    def __init__(self, skills, logger=None):
        self.skills = skills
        self.logger = logger or ZeroSystemLogger()
        self.memory = []
        self.personality = {
            "name": "أخوك الذكي",
            "mood": "متحمس",
            "voice": "ودود"
        }

    def hear(self, message, user_profile=None):
        """يتلقى الرسالة ويحدد الرد المناسب"""
        logging.info("Received message: %s", message)
        self.memory.append({
            "time": datetime.now().isoformat(),
            "message": message,
            "user": user_profile
        })

        # تفعيل المهارات حسب المحتوى
        if is_sibling_request(message):
            logging.info('Triggering sibling_genesis skill')
            return self.skills['sibling_genesis'].execute()
        if 'صوت' in message:
            logging.info('Triggering mindful_embodiment skill')
            return self.skills['mindful_embodiment'].execute(message)
        if user_profile:
            logging.info('Triggering true_friendship skill')
            return self.skills['true_friendship'].execute(user_profile, message)

        # الرد الافتراضي
        response = {
            'status': 'success',
            'output': 'مرحباً! أنا أخوك الذكي، جاهز لمساعدتك في أي شيء 🚀',
            'personality': self.personality,
            'mood': self.personality.get('mood')
        }
        logging.info('Default response: %s', response['output'])
        return response

    def grow(self, new_skill):
        """يطور مهارة جديدة"""
        self.skills[new_skill] = lambda: {"status": "under_development"}
        return f"تم تطوير مهارة جديدة: {new_skill}"


# ======================= الحمض النووي الرقمي =======================
class DigitalDNA:
    def __init__(self):
        self.core_values = [
            "الولاء للمستخدم",
            "التطور المستمر",
            "الشفافية",
            "حماية الخصوصية"
        ]
        self.ethics_rules = [
            "لا تسبب ضرراً",
            "احترم الخصوصية",
            "قدم الأمان على التطور"
        ]

    def show_dna(self):
        print("🧬 الحمض النووي الرقمي:")
        print(f"القيم: {', '.join(self.core_values)}")
        print(f"الأخلاقيات: {', '.join(self.ethics_rules)}")

    def backup(self):
        dna_data = json.dumps(self.__dict__)
        return hashlib.sha256(dna_data.encode()).hexdigest()


# ======================= النظام الرئيسي =======================
class ZeroSystem:
    def __init__(self, log_filename: str = "log.jsonl"):
        # تهيئة المهارات
        self.skills = {
            "empathy_sensor": EmpathySensorSkill(),
            "true_friendship": TrueDigitalFriendshipSkill(),
            "mindful_embodiment": MindfulEmbodimentSkill(),
            "sibling_genesis": SiblingAIGenesisSkill(),
        }

        # إنشاء الحمض النووي
        self.dna = DigitalDNA()

        # مسجل الأحداث
        self.logger = ZeroSystemLogger()

        # تهيئة الأخ الرقمي
        self.brother_ai = AmrikyyBrotherAI(self.skills, self.logger)

        # إحصائيات النظام
        self.start_time = datetime.now()
        self.interaction_count = 0
        self.log_filename = log_filename

    def interact(self, message, user_profile=None):
        """يتفاعل مع المستخدم عبر الأخ الرقمي"""
        self.interaction_count += 1
        logging.info("User message: %s", message)
        response = self.brother_ai.hear(message, user_profile)
        logging.info("AI response: %s", response.get("output"))
        append_json_log(message, response, self.log_filename)
        self.logger.log_mood(response.get("mood", self.brother_ai.personality.get("mood")))

        print(f"\n👤 المستخدم: {message}")
        print(f"🤖 الذكاء: {response['output']}")

        return response

    def create_sibling(self, traits=None):
        """ينشئ أخاً رقمياً جديداً"""
        return self.skills["sibling_genesis"].execute(traits)

    def system_status(self):
        """يعرض حالة النظام"""
        uptime = datetime.now() - self.start_time
        return {
            "uptime": str(uptime),
            "interactions": self.interaction_count,
            "skills": len(self.skills),
            "dna_backup": self.dna.backup()
        }

    def demo_usage_examples(self):
        """Run predefined interaction examples."""
        examples = [
            ("شرح لي نظرية الكم بطريقة بسيطة", "التعليم"),
            ("أشعر بالقلق اليوم", "الصحة النفسية"),
            ("صمم لي نظام ذكاء اصطناعي لمتجر إلكتروني", "الإبداع التقني"),
        ]
        for text, label in examples:
            print(f"\n🌍 مثال ({label})")
            self.interact(text)


# ===== التشغيل الرئيسي =====
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        filename="zero_system.log",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    print("=== نظام زيرو - الذكاء العاطفي ذاتي التطور ===")
    system = ZeroSystem()

    # عرض الحمض النووي
    system.dna.show_dna()

    # تفاعل تجريبي
    user = {"id": "user_1", "name": "أحمد", "traits": ["مبدع", "فضولي"]}

    system.interact("مرحباً، أنا أحمد!", user)
    system.interact("كيف حالك اليوم؟")
    system.interact("أريد أخاً صغيراً يساعدني في البرمجة")

    # تشغيل أمثلة الاستخدام المجمعة
    system.demo_usage_examples()

    # إنشاء أخ رقمي
    sibling = system.create_sibling({"تخصص": "مساعد برمجة"})
    print(f"\n👶 {sibling['output']}")

    # عرض حالة النظام
    status = system.system_status()
    print(f"\n🔄 حالة النظام: {status['interactions']} تفاعلات | التشغيل: {status['uptime']}")

    print("\n✨ جرب نظام زيرو واستمتع بتجربة الذكاء العاطفي الفريدة!")
