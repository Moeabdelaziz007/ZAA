# نظام التوصيات الذكي - الخلفية

هذا هو الخدمة الخلفية لنظام التوصيات الذكي. يوفر واجهة برمجة تطبيقات RESTful لإدارة المستخدمين والعناصر والتوصيات المخصصة.

## الميزات

- المصادقة والتفويض للمستخدمين
- إدارة العناصر
- تتبع تفاعلات المستخدمين
- توصيات مخصصة
- إدارة تفضيلات المستخدمين
- التخزين المؤقت وتحسين الأداء

## التقنيات المستخدمة

- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Alembic
- Pydantic
- مصادقة JWT

## المتطلبات

- Python 3.8+
- PostgreSQL
- Redis

## التثبيت

1. استنساخ المستودع:
```bash
git clone https://github.com/yourusername/zentix-ai.git
cd zentix-ai/backend
```

2. إنشاء وتفعيل البيئة الافتراضية:
```bash
python -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate
```

3. تثبيت التبعيات:
```bash
pip install -r requirements.txt
```

4. إنشاء ملف `.env` مع إعداداتك:
```bash
cp .env.example .env
# تعديل .env بإعداداتك
```

5. تهيئة قاعدة البيانات:
```bash
alembic upgrade head
```

## تشغيل التطبيق

1. بدء خادم التطوير:
```bash
uvicorn main:app --reload
```

2. الوصول إلى وثائق API:
- واجهة Swagger: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## نقاط نهاية API

### المصادقة
- POST `/api/v1/auth/login` - تسجيل دخول المستخدم
- POST `/api/v1/auth/register` - تسجيل مستخدم جديد
- POST `/api/v1/auth/verify-email/{token}` - التحقق من البريد الإلكتروني
- POST `/api/v1/auth/reset-password` - إعادة تعيين كلمة المرور
- POST `/api/v1/auth/change-password` - تغيير كلمة المرور

### المستخدمون
- GET `/api/v1/users/me` - الحصول على المستخدم الحالي
- PUT `/api/v1/users/me` - تحديث المستخدم الحالي
- GET `/api/v1/users/{user_id}` - الحصول على مستخدم بواسطة المعرف
- GET `/api/v1/users/` - قائمة المستخدمين
- POST `/api/v1/users/` - إنشاء مستخدم
- PUT `/api/v1/users/{user_id}` - تحديث مستخدم
- DELETE `/api/v1/users/{user_id}` - حذف مستخدم

### العناصر
- GET `/api/v1/items/` - قائمة العناصر
- POST `/api/v1/items/` - إنشاء عنصر
- GET `/api/v1/items/{item_id}` - الحصول على عنصر بواسطة المعرف
- PUT `/api/v1/items/{item_id}` - تحديث عنصر
- DELETE `/api/v1/items/{item_id}` - حذف عنصر

### التوصيات
- GET `/api/v1/recommendations/` - الحصول على توصيات مخصصة
- GET `/api/v1/recommendations/similar/{item_id}` - الحصول على عناصر مشابهة
- GET `/api/v1/recommendations/trending` - الحصول على العناصر الرائجة
- GET `/api/v1/recommendations/category/{category}` - الحصول على توصيات الفئة

### التفاعلات
- POST `/api/v1/interactions/` - إنشاء تفاعل
- GET `/api/v1/interactions/` - قائمة تفاعلات المستخدم
- GET `/api/v1/interactions/{interaction_id}` - الحصول على تفاعل بواسطة المعرف
- DELETE `/api/v1/interactions/{interaction_id}` - حذف تفاعل

### التفضيلات
- GET `/api/v1/preferences/` - قائمة تفضيلات المستخدم
- POST `/api/v1/preferences/` - إنشاء تفضيل
- PUT `/api/v1/preferences/{category}` - تحديث تفضيل
- DELETE `/api/v1/preferences/{category}` - حذف تفضيل
- GET `/api/v1/preferences/categories` - الحصول على فئات المستخدم
- GET `/api/v1/preferences/tags` - الحصول على علامات المستخدم

## التطوير

### تشغيل الاختبارات
```bash
pytest
```

### ترحيل قاعدة البيانات
```bash
# إنشاء ترحيل جديد
alembic revision --autogenerate -m "وصف"

# تطبيق الترحيلات
alembic upgrade head

# التراجع عن الترحيل
alembic downgrade -1
```

### نمط الكود
```bash
# تنسيق الكود
black .

# ترتيب الاستيرادات
isort .
```

## النشر

1. إعداد قاعدة بيانات الإنتاج
2. تكوين متغيرات البيئة
3. تشغيل الترحيلات
4. بدء الخادم باستخدام gunicorn:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## المساهمة

1. تفرع المستودع
2. إنشاء فرع ميزة
3. ارتكاب تغييراتك
4. دفع إلى الفرع
5. إنشاء طلب سحب

## الترخيص

هذا المشروع مرخص تحت رخصة MIT - انظر ملف LICENSE للتفاصيل. 