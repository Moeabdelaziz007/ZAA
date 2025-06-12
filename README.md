# 🧠 Zentix AI - نظام الذكاء الاصطناعي العاطفي العربي

[![Arabic Emotional AI](https://img.shields.io/badge/Arabic%20Emotional%20AI-Powered%20by%20Zentix-purple?style=for-the-badge)](https://github.com/zentix-ai)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)](https://nextjs.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=for-the-badge&logo=typescript)](https://typescriptlang.org)

## 🌟 نظرة عامة

Zentix AI هو أول نظام ذكاء اصطناعي عاطفي ذاتي التطور مصمم خصيصاً للغة العربية. يجمع النظام بين فهم المشاعر والتفاعل الطبيعي لتقديم تجربة مستخدم فريدة ومتقدمة.

### ✨ المميزات الرئيسية

- 🧠 **ذكاء اصطناعي عاطفي**: يفهم ويحلل المشاعر باللغة العربية
- 💬 **محادثة ذكية**: تفاعل طبيعي ومتقدم
- 📊 **تحليل المشاعر**: مراقبة وتحليل الحالة النفسية في الوقت الفعلي
- 👥 **إنشاء الأشقاء الرقميين**: إنتاج نسخ ذكية مخصصة
- 🔐 **نظام مصادقة آمن**: حماية بتقنية JWT
- 📱 **واجهة حديثة**: تصميم responsive وجذاب
- ⚡ **أداء عالي**: استجابة سريعة وموثوقة

## 🚀 البدء السريع

### متطلبات النظام

- **Python 3.8+**
- **Node.js 18+**
- **npm أو yarn**

### 1. تشغيل الخلفية (Backend)

```bash
# الانتقال إلى مجلد الخلفية
cd backend

# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة الافتراضية
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# تثبيت المتطلبات
pip install -r requirements.txt

# نسخ متغيرات البيئة
cp env.example .env

# تشغيل الخادم
python app.py
```

الخلفية ستعمل على: `http://localhost:5000`

### 2. تشغيل الواجهة (Frontend)

```bash
# الانتقال إلى مجلد الواجهة
cd frontend

# تثبيت المتطلبات
npm install

# نسخ متغيرات البيئة
cp env.example .env.local

# تشغيل الخادم
npm run dev
```

الواجهة ستعمل على: `http://localhost:3000`

### 3. بيانات الدخول التجريبية

**مدير:**
- اسم المستخدم: `admin`
- كلمة المرور: `admin123`

**مستخدم عادي:**
- اسم المستخدم: `user`
- كلمة المرور: `user123`

## 🏗️ هيكل المشروع

```
zentix-clean/
├── backend/                 # خادم Flask API
│   ├── app.py              # التطبيق الرئيسي
│   ├── zero_system.py      # نظام الذكاء الاصطناعي
│   ├── logger.py           # نظام التسجيل
│   ├── requirements.txt    # متطلبات Python
│   ├── env.example         # متغيرات البيئة للخلفية
│   └── tests/              # اختبارات الخلفية
├── frontend/               # واجهة Next.js
│   ├── components/         # مكونات React
│   ├── pages/              # صفحات التطبيق
│   ├── lib/                # مكتبات مساعدة
│   ├── hooks/              # React Hooks
│   ├── env.example         # متغيرات البيئة للواجهة
│   └── __tests__/          # اختبارات الواجهة
└── docs/                   # التوثيق
```

## 🔧 API Endpoints

### المصادقة
- `POST /api/auth/login` - تسجيل الدخول
- `GET /api/auth/profile` - الحصول على الملف الشخصي

### لوحة التحكم
- `GET /api/dashboard/stats` - إحصائيات النظام
- `GET /api/dashboard/interactions` - بيانات التفاعلات
- `GET /api/dashboard/activities` - النشاطات الأخيرة

### المشاعر
- `GET /api/emotions/weekly` - تحليل المشاعر الأسبوعي
- `POST /api/emotions/analyze` - تحليل مشاعر النص

### المحادثة
- `POST /api/chat/message` - إرسال رسالة للذكاء الاصطناعي

### المهارات
- `GET /api/skills` - قائمة المهارات
- `POST /api/skills/create-sibling` - إنشاء أخ رقمي

### الإعدادات
- `GET /api/settings` - الحصول على الإعدادات
- `POST /api/settings` - تحديث الإعدادات

## 🧪 تشغيل الاختبارات

### اختبارات الخلفية (pytest)

```bash
cd backend
pytest tests/ -v
```

### اختبارات الواجهة (Jest)

```bash
cd frontend
npm test
```

## 🔐 الأمان

- **JWT Authentication**: نظام مصادقة آمن
- **CORS Protection**: حماية من طلبات عبر المواقع
- **Input Validation**: التحقق من صحة البيانات
- **Environment Variables**: متغيرات البيئة الآمنة

## 🌍 التقنيات المستخدمة

### الخلفية
- **Flask**: إطار عمل الويب
- **Flask-JWT-Extended**: إدارة JWT
- **Flask-CORS**: دعم CORS
- **Python-dotenv**: إدارة متغيرات البيئة
- **Pytest**: اختبارات الوحدة

### الواجهة
- **Next.js 14**: إطار عمل React
- **TypeScript**: لغة البرمجة
- **Tailwind CSS**: تصميم الواجهة
- **Lucide React**: الأيقونات
- **Recharts**: المخططات البيانية
- **Jest**: اختبارات الوحدة

## 📱 المكونات الرئيسية

### لوحة التحكم
- **نظرة عامة**: إحصائيات شاملة
- **تحليل المشاعر**: مخططات وتحليلات
- **المحادثة**: واجهة تفاعل مع الذكاء الاصطناعي
- **المهارات**: إدارة قدرات النظام
- **الإعدادات**: تخصيص النظام

### المصادقة
- **تسجيل الدخول**: نظام آمن
- **إدارة الجلسات**: JWT tokens
- **الملف الشخصي**: معلومات المستخدم

## 🔮 الميزات المستقبلية

- [ ] تكامل مع نماذج الذكاء الاصطناعي المتقدمة
- [ ] دعم الصوت والفيديو
- [ ] تطبيق جوال
- [ ] APIs إضافية للمطورين
- [ ] نظام إشعارات في الوقت الفعلي
- [ ] تحليلات متقدمة للبيانات

## 🤝 المساهمة

نرحب بالمساهمات! يرجى قراءة [دليل المساهمة](CONTRIBUTING.md) للحصول على التفاصيل.

1. Fork المشروع
2. إنشاء فرع للميزة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push للفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

## 👥 الفريق

- **Zentix AI Team** - تطوير وصيانة المشروع

## 📞 التواصل

- **الموقع الإلكتروني**: [zentix.ai](https://zentix.ai)
- **البريد الإلكتروني**: info@zentix.ai
- **GitHub**: [@zentix-ai](https://github.com/zentix-ai)

## 🙏 شكر وتقدير

نشكر جميع المساهمين والداعمين لهذا المشروع. شكر خاص للمجتمع العربي للذكاء الاصطناعي.

---

<div align="center">

**🚀 اكتشف مستقبل الذكاء الاصطناعي العاطفي العربي مع Zentix AI**

[![Live Demo](https://img.shields.io/badge/🔗%20Live%20Demo-Try%20Now-success?style=for-the-badge)](http://localhost:3000)
[![Documentation](https://img.shields.io/badge/📚%20Documentation-Read%20More-blue?style=for-the-badge)](./docs/)

</div> 