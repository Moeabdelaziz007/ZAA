# 🧠 Zero System - نظام الذكاء الاصطناعي العاطفي

<div align="center">

![Zero System Logo](https://img.shields.io/badge/Zero%20System-AI%20Emotional%20Intelligence-purple?style=for-the-badge&logo=brain&logoColor=white)

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14.2+-black.svg)](https://nextjs.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Arabic Support](https://img.shields.io/badge/Arabic-RTL%20Support-red.svg)](README.md)

**أول نظام ذكاء اصطناعي عاطفي مع دعم كامل للغة العربية**

[🚀 التشغيل السريع](#-التشغيل-السريع) • [📋 الميزات](#-الميزات-الرئيسية) • [🛠️ التطوير](#️-تطوير-المشروع) • [📖 التوثيق](#-التوثيق)

</div>

---

## 🌟 نظرة عامة

Zero System هو نظام ذكاء اصطناعي رائد يركز على **الذكاء العاطفي** و**التفاعل الإنساني الطبيعي**. يتميز بدعم كامل للغة العربية ونظام إضافات قابل للتوسع.

### 🎯 الهدف
إنشاء "صديق رقمي" حقيقي قادر على:
- فهم المشاعر البشرية وتحليلها
- التكيف مع سياق المحادثة
- تطوير علاقات شخصية مع المستخدمين
- التطور الذاتي من خلال التفاعل

---

## 🏗️ هيكل المشروع

```
zentix-clean/
├── 🐍 backend/              # النظام الأساسي (Python)
│   ├── zero_system.py       # محرك الذكاء الاصطناعي الرئيسي
│   ├── cli.py              # واجهة سطر الأوامر
│   ├── dashboard.py        # خادم Flask للـ API
│   ├── plugin_example.py   # نظام الإضافات التوضيحي
│   ├── logger.py           # نظام التسجيل المتقدم
│   ├── sss/                # الحزمة الأساسية للنظام
│   ├── templates/          # قوالب HTML للواجهات
│   ├── static/             # الملفات الثابتة
│   └── tests/              # اختبارات شاملة (11 ملف اختبار)
├── ⚛️ frontend/             # واجهة المستخدم (Next.js)
│   ├── ai-dashboard.tsx    # لوحة التحكم الذكية الرئيسية
│   ├── components/         # مكونات UI متقدمة (ShadCN)
│   ├── hooks/              # React Hooks مخصصة
│   ├── lib/                # مكتبات مساعدة
│   └── pages/              # صفحات التطبيق
└── 📚 docs/                # التوثيق الشامل
```

---

## ✨ الميزات الرئيسية

### 🧠 الذكاء العاطفي
- **تحليل المشاعر** من النصوص العربية
- **اكتشاف السياق** العاطفي للمحادثات
- **تكييف الردود** حسب الحالة النفسية للمستخدم

### 🤝 الصداقة الرقمية
- **تتبع علاقات المستخدمين** وتطورها
- **ذاكرة شخصية** لكل مستخدم
- **تطوير مستوى الثقة** تدريجياً

### 🔧 نظام الإضافات
- **هيكل Plugin قابل للتوسع**
- **مهارات قابلة للإضافة** ديناميكياً
- **API مرن** للتطوير

### 🎨 واجهة متطورة
- **لوحة تحكم تفاعلية** مع Next.js
- **رسوم بيانية حية** لتحليل المشاعر
- **دعم RTL كامل** للعربية
- **تصميم متجاوب** لجميع الأجهزة

---

## 🚀 التشغيل السريع

### متطلبات النظام
- Python 3.8+ 🐍
- Node.js 16+ ⚡
- Git 📦

### 1️⃣ استنساخ المشروع
```bash
git clone https://github.com/cryptojoker710/zentix-clean.git
cd zentix-clean
```

### 2️⃣ تشغيل النظام الخلفي
```bash
cd backend/
pip install -r requirements.txt

# تشغيل الواجهة النصية
python cli.py interactive

# أو تشغيل خادم الويب
python dashboard.py
```

### 3️⃣ تشغيل الواجهة الأمامية
```bash
cd frontend/
npm install
npm run dev
```

### 4️⃣ فتح التطبيق
- **واجهة الويب**: [http://localhost:3000](http://localhost:3000)
- **API البيانات**: [http://localhost:5000](http://localhost:5000)

---

## 💻 أمثلة الاستخدام

### تفاعل عبر CLI
```bash
# بدء جلسة تفاعلية
python cli.py interactive

# عرض حالة النظام
python cli.py status

# تشغيل الأمثلة التوضيحية
python cli.py demo
```

### تفاعل برمجي
```python
from zero_system import ZeroSystem

# إنشاء نظام جديد
system = ZeroSystem()

# تفاعل مع المستخدم
response = system.interact(
    "أشعر بالقلق اليوم", 
    user_profile={"id": "user_1", "name": "أحمد"}
)

print(response["output"])
# 🤖 أتفهم شعورك، دعنا نتنفس معاً... 💆‍♂️
```

### إنشاء إضافة جديدة
```python
from zero_system import AbstractSkill

class MyCustomSkill(AbstractSkill):
    def get_description(self):
        return "مهارة مخصصة جديدة"
    
    def execute(self, **kwargs):
        return {"status": "success", "output": "نجح التنفيذ!"}
```

---

## 🛠️ تطوير المشروع

### هيكل التطوير
```bash
# إعداد بيئة التطوير
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### تشغيل الاختبارات
```bash
# اختبارات Python
cd backend/
pytest

# اختبارات Frontend (قادمة)
cd frontend/
npm test
```

### المساهمة في المشروع
1. Fork المشروع
2. إنشاء فرع جديد (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push للفرع (`git push origin feature/amazing-feature`)
5. إنشاء Pull Request

---

## 📊 الإحصائيات

| المقياس | القيمة |
|---------|--------|
| 📝 أسطر الكود | 2000+ |
| 🧪 الاختبارات | 11 ملف |
| 🎨 مكونات UI | 13 مكون |
| 🌐 دعم اللغات | العربية + الإنجليزية |
| 📱 المنصات | Web + Desktop + Mobile |

---

## 🎯 خارطة الطريق

### 🔥 النسخة الحالية (v0.2.0)
- ✅ نظام الذكاء العاطفي الأساسي
- ✅ واجهة ويب متطورة
- ✅ دعم اللغة العربية
- ✅ نظام الإضافات

### 🚀 النسخة القادمة (v0.3.0)
- 🔄 ربط Frontend مع Backend
- 🧪 إضافة اختبارات Frontend
- 🌙 دعم الثيمات المتعددة
- 📊 تحسين الرسوم البيانية

### 🌟 المستقبل (v1.0.0)
- 🤖 تحسين خوارزميات الذكاء
- 🗣️ دعم الصوت والكلام
- 🌍 دعم لغات إضافية
- ☁️ نشر سحابي

---

## 📖 التوثيق

- [📘 دليل المطور](docs/developer-guide.md)
- [🎨 دليل UI/UX](docs/ui-guide.md)
- [🔌 تطوير الإضافات](docs/plugins.md)
- [🌐 دليل API](docs/api-reference.md)

---

## 👥 الفريق

- **Mohamed H. Abdelaziz** - المطور الرئيسي - [@cryptojoker710](https://github.com/cryptojoker710)

---

## 📄 الترخيص

هذا المشروع مرخص تحت [MIT License](LICENSE) - راجع ملف الترخيص للتفاصيل.

---

## 🙏 الشكر والتقدير

- [ShadCN UI](https://ui.shadcn.com/) للمكونات الرائعة
- [Next.js](https://nextjs.org/) لإطار العمل المتقدم
- [Recharts](https://recharts.org/) للرسوم البيانية
- المجتمع العربي للذكاء الاصطناعي

---

<div align="center">

**⭐ إذا أعجبك المشروع، لا تنس إعطاؤه نجمة! ⭐**

صُنع بـ ❤️ للمجتمع العربي

</div> 