# التوثيق التقني - Zentix

## نظرة عامة
Zentix هو تطبيق ويب متقدم مبني باستخدام Next.js و TypeScript، مع التركيز على الأداء العالي وتجربة المستخدم المتميزة.

## الهيكل التقني

### الواجهة الأمامية
- **Next.js 13+**: استخدام App Router للتنقل
- **TypeScript**: للسلامة النوعية
- **Tailwind CSS**: للتصميم
- **Framer Motion**: للرسوم المتحركة
- **Jest & React Testing Library**: للاختبارات

ملف `package.json` الخاص بالواجهة وكل أوامر `npm` موجودة داخل مجلد **frontend**.

### الخلفية
- **FastAPI**: لبناء API
- **PostgreSQL**: قاعدة البيانات الرئيسية
- **Redis**: للتخزين المؤقت
- **Celery**: للمهام الخلفية

## تحسينات الأداء

### First Contentful Paint (FCP)
- تحسين تحميل الصور باستخدام Next.js Image
- تقسيم الكود (Code Splitting)
- التحميل الكسول (Lazy Loading)
- التخزين المؤقت (Caching)

### Time to Interactive (TTI)
- تحسين حجم الحزمة
- تحسين تحميل الخطوط
- تحسين تحميل JavaScript
- تحسين تحميل CSS

### Service Worker
- تخزين الموارد الثابتة
- دعم وضع عدم الاتصال
- مزامنة البيانات في الخلفية
- إشعارات الدفع

## الاختبارات

### اختبارات الوحدة
```bash
 codex/decide-on-root-package.json-usage
cd frontend
npm run test
=======
cd frontend && npm run test
 main
```

### اختبارات التكامل
```bash
 codex/decide-on-root-package.json-usage
cd frontend
npm run test:integration
=======
cd frontend && npm run test:integration
 main
```

### اختبارات الأداء
```bash
 codex/decide-on-root-package.json-usage
cd frontend
npm run test:performance
=======
cd frontend && npm run test:performance
 main
```

## CI/CD

### مراحل CI/CD
1. **الاختبار**
   - اختبارات الوحدة
   - اختبارات التكامل
   - فحص النوع
   - فحص التنسيق

2. **البناء**
   - بناء التطبيق
   - تحليل الحزمة
   - تحسين الصور

3. **النشر**
   - النشر التلقائي
   - التحقق من الصحة
   - التراجع التلقائي

## الأمان

### أفضل الممارسات
- حماية CSRF
- حماية XSS
- حماية SQL Injection
- حماية Clickjacking

### التشفير
- تشفير البيانات الحساسة
- تشفير الاتصالات
- تشفير كلمات المرور

## المراقبة

### الأدوات
- Sentry: لتتبع الأخطاء
- Prometheus: لقياس الأداء
- Grafana: للتصور
- ELK Stack: للسجلات

## التوسع

### الاستراتيجيات
- التخزين المؤقت
- تحميل التوازن
- التخزين المؤقت الموزع
- التخزين المؤقت للاستعلامات

## الصيانة

### المهام الدورية
- تحديث التبعيات
- تنظيف السجلات
- تحسين قاعدة البيانات
- نسخ احتياطي للبيانات

## المساهمة

### إرشادات المساهمة
1. Fork المشروع
2. إنشاء فرع للميزة
3. إضافة الاختبارات
4. تحديث التوثيق
5. إنشاء طلب سحب

### معايير الكود
- ESLint
- Prettier
- TypeScript
- Jest

## الترخيص
MIT License 