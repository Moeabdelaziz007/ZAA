from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import os
from datetime import datetime, timedelta
import json
from zero_system import ZeroSystem
import hashlib

app = Flask(__name__)

# إعدادات البيئة
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'zentix-ai-secret-key-2024')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# تهيئة JWT و CORS
jwt = JWTManager(app)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

# إنشاء نظام Zero
zero_system = ZeroSystem()

# بيانات المستخدمين الوهمية (في التطبيق الحقيقي استخدم قاعدة بيانات)
users_db = {
    "admin": {
        "id": "user_1", 
        "username": "admin", 
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "name": "المدير",
        "email": "admin@zentix.ai",
        "role": "admin"
    },
    "user": {
        "id": "user_2",
        "username": "user",
        "password": hashlib.sha256("user123".encode()).hexdigest(), 
        "name": "مستخدم تجريبي",
        "email": "user@zentix.ai",
        "role": "user"
    }
}

# ========================= Auth Endpoints =========================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """تسجيل الدخول باستخدام JWT"""
    try:
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({"error": "اسم المستخدم وكلمة المرور مطلوبان"}), 400
            
        # التحقق من المستخدم
        user = users_db.get(username)
        if not user or user['password'] != hashlib.sha256(password.encode()).hexdigest():
            return jsonify({"error": "بيانات تسجيل الدخول غير صحيحة"}), 401
            
        # إنشاء JWT token
        access_token = create_access_token(
            identity=user['id'],
            additional_claims={
                "username": user['username'],
                "name": user['name'],
                "role": user['role']
            }
        )
        
        return jsonify({
            "access_token": access_token,
            "user": {
                "id": user['id'],
                "username": user['username'], 
                "name": user['name'],
                "email": user['email'],
                "role": user['role']
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في تسجيل الدخول: {str(e)}"}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """الحصول على بيانات المستخدم الحالي"""
    try:
        current_user_id = get_jwt_identity()
        
        # البحث عن المستخدم
        user = None
        for u in users_db.values():
            if u['id'] == current_user_id:
                user = u
                break
                
        if not user:
            return jsonify({"error": "المستخدم غير موجود"}), 404
            
        return jsonify({
            "user": {
                "id": user['id'],
                "username": user['username'],
                "name": user['name'], 
                "email": user['email'],
                "role": user['role']
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في الحصول على البيانات: {str(e)}"}), 500

# ========================= Dashboard Endpoints =========================

@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """إحصائيات Dashboard الرئيسية"""
    try:
        stats = zero_system.system_status()
        
        return jsonify({
            "total_interactions": stats.get("interactions", 1247),
            "active_users": 89,
            "happiness_level": 92,
            "response_time": "0.3s",
            "uptime": stats.get("uptime", "15 أيام، 3 ساعات"),
            "skills_count": stats.get("skills", 4),
            "dna_backup": stats.get("dna_backup", "")
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في الحصول على الإحصائيات: {str(e)}"}), 500

@app.route('/api/dashboard/interactions', methods=['GET'])
@jwt_required()
def get_interactions_data():
    """بيانات التفاعلات اليومية"""
    try:
        # بيانات وهمية - في التطبيق الحقيقي احصل عليها من قاعدة البيانات
        interactions_data = [
            {"time": "09:00", "تفاعلات": 12},
            {"time": "12:00", "تفاعلات": 25},
            {"time": "15:00", "تفاعلات": 18},
            {"time": "18:00", "تفاعلات": 32},
            {"time": "21:00", "تفاعلات": 28},
        ]
        
        return jsonify({"data": interactions_data}), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في الحصول على بيانات التفاعلات: {str(e)}"}), 500

@app.route('/api/dashboard/activities', methods=['GET'])
@jwt_required()
def get_recent_activities():
    """النشاطات الأخيرة"""
    try:
        activities = [
            {"user": "أحمد محمد", "action": "طلب دعم نفسي", "time": "منذ دقيقتين", "status": "success"},
            {"user": "فاطمة علي", "action": "سؤال تقني", "time": "منذ 5 دقائق", "status": "active"},
            {"user": "محمد حسن", "action": "إنشاء أخ رقمي", "time": "منذ 10 دقائق", "status": "success"},
            {"user": "سارة أحمد", "action": "محادثة عامة", "time": "منذ 15 دقيقة", "status": "success"},
        ]
        
        return jsonify({"activities": activities}), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في الحصول على النشاطات: {str(e)}"}), 500

# ========================= Emotions Endpoints =========================

@app.route('/api/emotions/weekly', methods=['GET'])
@jwt_required()
def get_weekly_emotions():
    """تحليل المشاعر الأسبوعي"""
    try:
        emotion_data = [
            {"name": "الاثنين", "سعادة": 80, "قلق": 20, "حياد": 30},
            {"name": "الثلاثاء", "سعادة": 65, "قلق": 35, "حياد": 25},
            {"name": "الأربعاء", "سعادة": 90, "قلق": 15, "حياد": 40},
            {"name": "الخميس", "سعادة": 75, "قلق": 25, "حياد": 35},
            {"name": "الجمعة", "سعادة": 95, "قلق": 10, "حياد": 45},
            {"name": "السبت", "سعادة": 85, "قلق": 20, "حياد": 50},
            {"name": "الأحد", "سعادة": 70, "قلق": 30, "حياد": 30},
        ]
        
        return jsonify({"data": emotion_data}), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في الحصول على بيانات المشاعر: {str(e)}"}), 500

@app.route('/api/emotions/analyze', methods=['POST'])
@jwt_required()
def analyze_emotion():
    """تحليل مشاعر نص معين"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "النص مطلوب"}), 400
            
        # استخدام مهارة تحليل المشاعر من Zero System
        result = zero_system.skills['empathy_sensor'].execute(text)
        
        return jsonify({
            "emotion": result.get('empathy', 'محايد'),
            "confidence": 0.85,
            "analysis": result
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في تحليل المشاعر: {str(e)}"}), 500

# ========================= Chat Endpoints =========================

@app.route('/api/chat/message', methods=['POST'])
@jwt_required()
def send_message():
    """إرسال رسالة للذكاء الاصطناعي"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({"error": "الرسالة مطلوبة"}), 400
            
        # البحث عن بيانات المستخدم
        user_profile = None
        for u in users_db.values():
            if u['id'] == current_user_id:
                user_profile = {
                    "id": u['id'],
                    "name": u['name']
                }
                break
                
        # إرسال الرسالة لنظام Zero
        response = zero_system.interact(message, user_profile)
        
        return jsonify({
            "response": response.get('output', 'عذراً، لم أستطع فهم طلبك'),
            "mood": response.get('mood', 'محايد'),
            "personality": response.get('personality', {}),
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في إرسال الرسالة: {str(e)}"}), 500

# ========================= Skills Endpoints =========================

@app.route('/api/skills', methods=['GET'])
@jwt_required()
def get_skills():
    """الحصول على جميع المهارات وحالتها"""
    try:
        skills_data = [
            {"name": "مستشعر التعاطف", "status": "نشط", "performance": 95, "description": "يحلل المشاعر من النص"},
            {"name": "الصداقة الرقمية", "status": "نشط", "performance": 88, "description": "يكون علاقات شخصية مع المستخدمين"},
            {"name": "التجسيد الذهني", "status": "نشط", "performance": 92, "description": "يعدل الأسلوب حسب السياق"},
            {"name": "إنشاء الأشقاء", "status": "تطوير", "performance": 78, "description": "ينشئ أشقاء رقميين جدد"},
        ]
        
        skills_performance = [
            {"skill": "التعاطف", "فعالية": 95},
            {"skill": "الصداقة الرقمية", "فعالية": 88},
            {"skill": "التجسيد الذهني", "فعالية": 92},
            {"skill": "إنشاء الأشقاء", "فعالية": 78},
        ]
        
        return jsonify({
            "skills": skills_data,
            "performance": skills_performance
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في الحصول على المهارات: {str(e)}"}), 500

@app.route('/api/skills/create-sibling', methods=['POST'])
@jwt_required()
def create_sibling():
    """إنشاء أخ رقمي جديد"""
    try:
        data = request.get_json()
        traits = data.get('traits', {})
        
        # إنشاء أخ رقمي باستخدام Zero System
        result = zero_system.create_sibling(traits)
        
        return jsonify({
            "success": True,
            "sibling": result,
            "message": "تم إنشاء الأخ الرقمي بنجاح!"
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في إنشاء الأخ الرقمي: {str(e)}"}), 500

# ========================= Settings Endpoints =========================

@app.route('/api/settings', methods=['GET'])
@jwt_required()
def get_settings():
    """الحصول على إعدادات النظام"""
    try:
        settings = {
            "logging_enabled": True,
            "emotion_analysis": True,
            "auto_backup": True,
            "language": "ar",
            "theme": "dark",
            "notifications": True
        }
        
        return jsonify({"settings": settings}), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في الحصول على الإعدادات: {str(e)}"}), 500

@app.route('/api/settings', methods=['POST'])
@jwt_required()
def update_settings():
    """تحديث إعدادات النظام"""
    try:
        data = request.get_json()
        # في التطبيق الحقيقي، احفظ الإعدادات في قاعدة البيانات
        
        return jsonify({
            "success": True,
            "message": "تم تحديث الإعدادات بنجاح"
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في تحديث الإعدادات: {str(e)}"}), 500

# ========================= Health Check =========================

@app.route('/api/health', methods=['GET'])
def health_check():
    """فحص صحة الخدمة"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Zentix AI Backend",
        "version": "0.1.0"
    }), 200

# ========================= Error Handlers =========================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "المسار غير موجود"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "خطأ داخلي في الخادم"}), 500

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "انتهت صلاحية الجلسة، يرجى تسجيل الدخول مرة أخرى"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "رمز مصادقة غير صالح"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"error": "رمز المصادقة مطلوب"}), 401

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print("🚀 تشغيل Zentix AI Backend API...")
    print(f"📡 الخادم يعمل على البورت: {port}")
    print(f"🌍 الوضع: {'تطوير' if debug else 'إنتاج'}")
    
    app.run(host='0.0.0.0', port=port, debug=debug) 