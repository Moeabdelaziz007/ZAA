import pytest
import time
import numpy as np
from datetime import datetime, timedelta
from backend.core.emotion_engine import EmotionSuggestionEngine
from backend.core.contextual_personalization import ContextualPersonalization
from backend.core.auto_evaluation import AutoEvaluation
from backend.models.emotion import EmotionLog, EmotionPattern
from backend.models.user import User
from backend.models.time_context import TimeContext

@pytest.fixture
def db_session():
    from backend.database import SessionLocal
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def large_dataset(db_session):
    """إنشاء مجموعة بيانات كبيرة للاختبار"""
    users = []
    logs = []
    
    # إنشاء 100 مستخدم
    for i in range(100):
        user = User(
            username=f"test_user_{i}",
            email=f"test_{i}@example.com",
            preferences={
                "language": "ar",
                "theme": "dark",
                "notifications": True,
                "timezone": "UTC+3"
            }
        )
        users.append(user)
    
    db_session.add_all(users)
    db_session.commit()
    
    # إنشاء 1000 سجل عاطفي لكل مستخدم
    for user in users:
        for j in range(1000):
            log = EmotionLog(
                user_id=user.id,
                emotion_state={
                    "happiness": np.random.random(),
                    "sadness": np.random.random(),
                    "anger": np.random.random(),
                    "fear": np.random.random(),
                    "surprise": np.random.random()
                },
                confidence=np.random.random(),
                context={
                    "activity": np.random.choice(["work", "home", "social"]),
                    "location": np.random.choice(["office", "home", "cafe"]),
                    "weather": np.random.choice(["sunny", "rainy", "cloudy"])
                },
                created_at=datetime.now() - timedelta(hours=j)
            )
            logs.append(log)
    
    db_session.add_all(logs)
    db_session.commit()
    
    return users, logs

def test_emotion_analysis_performance(emotion_engine, large_dataset):
    """اختبار أداء تحليل المشاعر"""
    users, _ = large_dataset
    
    # قياس وقت تحليل المشاعر لـ 10 مستخدمين
    start_time = time.time()
    for user in users[:10]:
        analysis = emotion_engine.analyze_and_suggest(user.id)
        assert isinstance(analysis, dict)
    end_time = time.time()
    
    # التحقق من أن متوسط وقت التحليل أقل من 1 ثانية لكل مستخدم
    average_time = (end_time - start_time) / 10
    assert average_time < 1.0
    
    # قياس استخدام الذاكرة
    import psutil
    import os
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # بالميجابايت
    assert memory_usage < 500  # أقل من 500 ميجابايت

def test_contextual_personalization_performance(contextual_personalization, large_dataset):
    """اختبار أداء التخصيص السياقي"""
    users, _ = large_dataset
    
    # قياس وقت التخصيص السياقي لـ 10 مستخدمين
    start_time = time.time()
    for user in users[:10]:
        preferences = contextual_personalization.get_contextual_preferences(user.id)
        assert isinstance(preferences, dict)
    end_time = time.time()
    
    # التحقق من أن متوسط وقت التخصيص أقل من 0.5 ثانية لكل مستخدم
    average_time = (end_time - start_time) / 10
    assert average_time < 0.5
    
    # قياس استخدام الذاكرة
    import psutil
    import os
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # بالميجابايت
    assert memory_usage < 300  # أقل من 300 ميجابايت

def test_auto_evaluation_performance(auto_evaluation, large_dataset):
    """اختبار أداء التقييم التلقائي"""
    # قياس وقت دورة التقييم الكاملة
    start_time = time.time()
    evaluation_results = auto_evaluation.run_evaluation_cycle()
    end_time = time.time()
    
    # التحقق من أن وقت التقييم أقل من 5 ثواني
    evaluation_time = end_time - start_time
    assert evaluation_time < 5.0
    assert isinstance(evaluation_results, dict)
    
    # قياس استخدام الذاكرة
    import psutil
    import os
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # بالميجابايت
    assert memory_usage < 400  # أقل من 400 ميجابايت

def test_memory_usage(emotion_engine, large_dataset):
    """اختبار استخدام الذاكرة"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # تحليل المشاعر لـ 10 مستخدمين
    users, _ = large_dataset
    for user in users[:10]:
        analysis = emotion_engine.analyze_and_suggest(user.id)
    
    final_memory = process.memory_info().rss
    memory_increase = (final_memory - initial_memory) / 1024 / 1024  # بالميجابايت
    
    # التحقق من أن زيادة استخدام الذاكرة أقل من 100 ميجابايت
    assert memory_increase < 100

def test_concurrent_requests(emotion_engine, large_dataset):
    """اختبار الطلبات المتزامنة"""
    import concurrent.futures
    
    users, _ = large_dataset
    test_users = users[:20]  # اختبار 20 مستخدم متزامن
    
    def analyze_user(user):
        return emotion_engine.analyze_and_suggest(user.id)
    
    # تنفيذ التحليلات بشكل متزامن
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(analyze_user, test_users))
    end_time = time.time()
    
    # التحقق من النتائج
    assert len(results) == 20
    assert all(isinstance(result, dict) for result in results)
    
    # التحقق من أن متوسط وقت المعالجة المتزامنة أقل من 5 ثواني
    total_time = end_time - start_time
    assert total_time < 5.0

def test_database_performance(db_session, large_dataset):
    """اختبار أداء قاعدة البيانات"""
    users, logs = large_dataset
    
    # قياس وقت استعلام قاعدة البيانات
    start_time = time.time()
    
    # استعلام بسيط
    user_count = db_session.query(User).count()
    assert user_count == 100
    
    # استعلام مع join
    user_logs = db_session.query(User, EmotionLog).join(EmotionLog).limit(1000).all()
    assert len(user_logs) == 1000
    
    end_time = time.time()
    query_time = end_time - start_time
    
    # التحقق من أن وقت الاستعلام أقل من 1 ثانية
    assert query_time < 1.0

def test_caching_performance(emotion_engine, large_dataset):
    """اختبار أداء التخزين المؤقت"""
    users, _ = large_dataset
    test_user = users[0]
    
    # قياس وقت التحليل بدون تخزين مؤقت
    start_time = time.time()
    first_analysis = emotion_engine.analyze_and_suggest(test_user.id)
    first_time = time.time() - start_time
    
    # قياس وقت التحليل مع تخزين مؤقت
    start_time = time.time()
    second_analysis = emotion_engine.analyze_and_suggest(test_user.id)
    second_time = time.time() - start_time
    
    # التحقق من أن التحليل الثاني أسرع
    assert second_time < first_time
    assert second_analysis == first_analysis

def test_batch_processing_performance(emotion_engine, large_dataset):
    """اختبار أداء المعالجة المجمعة"""
    users, _ = large_dataset
    test_users = users[:50]  # اختبار 50 مستخدم
    
    # قياس وقت المعالجة المجمعة
    start_time = time.time()
    results = emotion_engine.batch_analyze([user.id for user in test_users])
    end_time = time.time()
    
    # التحقق من النتائج
    assert len(results) == 50
    assert all(isinstance(result, dict) for result in results)
    
    # التحقق من أن متوسط وقت المعالجة المجمعة أقل من 10 ثواني
    total_time = end_time - start_time
    assert total_time < 10.0 
