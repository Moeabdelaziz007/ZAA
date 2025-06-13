# Monitoring Stack for Zentix AI

## 📦 المكونات:

- Prometheus (metrics scraping)
- Grafana (visual dashboards)
- Node Exporter (system metrics)
- cAdvisor (Docker/container metrics)
- Redis/Postgres Exporter (DB metrics)
- AlertManager (alerts via Slack/Email)
- قواعد تنبيه جاهزة في `rules.yml`

## 🚀 خطوات التشغيل:
1. تأكد من إضافة Slack webhook في `infrastructure/prometheus/alertmanager.yml`
2. شغّل النظام:
   ```bash
   docker-compose up -d
   ```

## ⚡ للوصول السريع:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001
- AlertManager: http://localhost:9093
- cAdvisor: http://localhost:8080

## 📊 لوحات المعلومات:
1. قم بتسجيل الدخول إلى Grafana (admin/admin)
2. أضف Prometheus كمصدر بيانات
3. استورد لوحات المعلومات التالية:
   - Node Exporter Full
   - Docker & System Monitoring
   - Redis Dashboard
   - PostgreSQL Dashboard

## 🔔 التنبيهات:
يتم إرسال التنبيهات إلى:
- قناة Slack #alerts
- البريد الإلكتروني (قابل للتكوين)

## 📈 المقاييس الرئيسية:
- معدل الأخطاء
- زمن الاستجابة
- استخدام الذاكرة
- استخدام CPU
- مساحة القرص
- صحة الخدمات

## 🛠️ الصيانة:
- النسخ الاحتياطي التلقائي للبيانات
- تنظيف البيانات القديمة
- تحديث القواعد والتنبيهات

## 🔧 التكوين:
- `infrastructure/prometheus/prometheus.yml`: تكوين Prometheus
- `infrastructure/prometheus/alertmanager.yml`: تكوين التنبيهات
- `infrastructure/prometheus/rules.yml`: قواعد التنبيهات
- `docker-compose.yml`: تكوين الخدمات

## 📝 ملاحظات:
- تأكد من تحديث كلمات المرور الافتراضية
- قم بتعديل قواعد التنبيه حسب احتياجاتك
- راقب استخدام الموارد بانتظام 