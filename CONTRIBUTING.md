# 🤝 دليل المساهمة في Zero System

نرحب بمساهماتكم في تطوير Zero System! هذا الدليل سيساعدك على البدء.

## 🚀 كيفية المساهمة

### 1. إعداد البيئة التطويرية

```bash
# نسخ المشروع
git clone https://github.com/cryptojoker710/zentix-clean.git
cd zentix-clean

# إعداد بيئة Python
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r backend/requirements.txt

# إعداد Frontend
cd frontend/
npm install
```

### 2. تشغيل الاختبارات

```bash
# اختبارات Backend
cd backend/
pytest

# اختبارات Frontend (قريباً)
cd frontend/
npm test
```

### 3. إرشادات الكود

#### Python (Backend)
- استخدم **Type Hints** دائماً
- اتبع **PEP 8** للتنسيق
- أضف **docstrings** للدوال
- اكتب **اختبارات** لأي كود جديد

```python
def analyze_emotion(text: str) -> Dict[str, Any]:
    """تحليل المشاعر من النص العربي.
    
    Args:
        text: النص المراد تحليله
        
    Returns:
        قاموس يحتوي على نتائج التحليل
    """
    pass
```

#### TypeScript/React (Frontend)
- استخدم **TypeScript** دائماً
- اتبع **React best practices**
- استخدم **ShadCN UI components**
- دعم **RTL** للعربية

```typescript
interface EmotionAnalysis {
  emotion: string;
  confidence: number;
  suggestions: string[];
}

const analyzeEmotion = (text: string): EmotionAnalysis => {
  // Implementation
};
```

## 🐛 الإبلاغ عن المشاكل

عند إنشاء Issue جديد، يرجى تضمين:

1. **وصف المشكلة** بوضوح
2. **خطوات إعادة الإنتاج**
3. **السلوك المتوقع**
4. **السلوك الفعلي**
5. **معلومات البيئة** (OS, Python version, etc.)

## ✨ اقتراح ميزات جديدة

نرحب بالأفكار الجديدة! يرجى:

1. التحقق من عدم وجود اقتراح مشابه
2. شرح **الحاجة** للميزة
3. وصف **كيفية العمل** المقترحة
4. تقديم **أمثلة** إن أمكن

## 📝 عملية المراجعة

1. **Fork** المشروع
2. إنشاء **فرع جديد**: `git checkout -b feature/amazing-feature`
3. **التطوير** مع اتباع الإرشادات
4. **اختبار** التغييرات
5. **Commit**: `git commit -m 'Add amazing feature'`
6. **Push**: `git push origin feature/amazing-feature`
7. إنشاء **Pull Request**

## 🎯 أولويات التطوير

### أولوية عالية
- حل merge conflicts في `zero_system.py`
- ربط Frontend مع Backend API
- إضافة اختبارات Frontend

### أولوية متوسطة
- تحسين خوارزميات تحليل المشاعر
- إضافة المزيد من المهارات (Skills)
- تحسين واجهة المستخدم

### أولوية منخفضة
- دعم لغات إضافية
- تحسين الأداء
- إضافة ميزات متقدمة

## 🏷️ نظام التسميات

- `bug` - مشاكل تحتاج إصلاح
- `enhancement` - تحسينات على ميزات موجودة
- `feature` - ميزات جديدة
- `help wanted` - نحتاج مساعدة
- `good first issue` - مناسب للمبتدئين
- `documentation` - تحسين التوثيق

## 🌟 نصائح للمساهمين الجدد

1. ابدأ بـ `good first issue`
2. اقرأ الكود الموجود أولاً
3. لا تتردد في طرح الأسئلة
4. اختبر تغييراتك جيداً
5. اكتب commit messages واضحة

## 📞 التواصل

- **GitHub Issues** للأسئلة التقنية
- **Email**: mohamed.abdelaziz@example.com
- **Discord**: قريباً

## 🙏 شكراً

شكراً لاهتمامك بالمساهمة في Zero System! كل مساهمة، مهما كانت صغيرة، تساعد في تطوير الذكاء الاصطناعي العربي.

---

**مع التقدير،**  
فريق Zero System 🧠 