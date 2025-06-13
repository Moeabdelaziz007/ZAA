import pytest
from datetime import datetime, timedelta
import numpy as np
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
def test_user(db_session):
    user = User(
        username="test_user",
        email="test@example.com",
        preferences={
            "language": "ar",
            "theme": "dark",
            "notifications": True,
            "timezone": "UTC+3"
        }
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def emotion_engine(db_session):
    return EmotionSuggestionEngine(db_session)

@pytest.fixture
def contextual_personalization(db_session):
    return ContextualPersonalization(db_session)

@pytest.fixture
def auto_evaluation(db_session):
    return AutoEvaluation(db_session)

@pytest.fixture
def sample_data(db_session, test_user):
    """إنشاء بيانات اختبار شاملة"""
    # إنشاء سياق زمني
    time_context = TimeContext(
        hour=14,
        day_of_week=1,
        season="summer",
        is_holiday=False
    )
    db_session.add(time_context)
    
    # إنشاء سجلات عاطفية
    logs = []
    for i in range(24):
        log = EmotionLog(
            user_id=test_user.id,
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
            created_at=datetime.now() - timedelta(hours=i)
        )
        logs.append(log)
    
    db_session.add_all(logs)
    db_session.commit()
    return time_context, logs

def test_emotion_analysis_integration(emotion_engine, test_user, sample_data):
    """اختبار تكامل تحليل المشاعر"""
    _, logs = sample_data
    
    # تحليل المشاعر
    analysis = emotion_engine.analyze_and_suggest(test_user.id)
    
    assert isinstance(analysis, dict)
    assert "emotional_state" in analysis
    assert "patterns" in analysis
    assert "suggestions" in analysis
    assert "confidence_score" in analysis
    assert 0 <= analysis["confidence_score"] <= 1
    
    # التحقق من صحة الحالة العاطفية
    emotional_state = analysis["emotional_state"]
    assert isinstance(emotional_state, dict)
    assert all(0 <= v <= 1 for v in emotional_state.values())
    
    # التحقق من صحة الأنماط
    patterns = analysis["patterns"]
    assert isinstance(patterns, list)
    assert len(patterns) > 0
    for pattern in patterns:
        assert "type" in pattern
        assert "confidence" in pattern
        assert "description" in pattern

def test_contextual_personalization_integration(contextual_personalization, test_user, sample_data):
    """اختبار تكامل التخصيص السياقي"""
    time_context, _ = sample_data
    
    # الحصول على التفضيلات السياقية
    preferences = contextual_personalization.get_contextual_preferences(test_user.id)
    
    assert isinstance(preferences, dict)
    assert "context" in preferences
    assert "preferences" in preferences
    assert "confidence" in preferences
    assert 0 <= preferences["confidence"] <= 1
    
    # التحقق من صحة السياق
    context = preferences["context"]
    assert isinstance(context, dict)
    assert "time" in context
    assert "location" in context
    assert "activity" in context
    
    # التحقق من صحة التفضيلات
    user_preferences = preferences["preferences"]
    assert isinstance(user_preferences, dict)
    assert "language" in user_preferences
    assert "theme" in user_preferences
    assert "notifications" in user_preferences

def test_auto_evaluation_integration(auto_evaluation, test_user, sample_data):
    """اختبار تكامل التقييم التلقائي"""
    # تشغيل دورة التقييم
    evaluation_results = auto_evaluation.run_evaluation_cycle()
    
    assert isinstance(evaluation_results, dict)
    assert "model_performance" in evaluation_results
    assert "ab_testing_results" in evaluation_results
    assert "llm_evaluation" in evaluation_results
    assert "recommendations" in evaluation_results
    
    # التحقق من أداء النموذج
    model_performance = evaluation_results["model_performance"]
    assert isinstance(model_performance, dict)
    assert "accuracy" in model_performance
    assert "precision" in model_performance
    assert "recall" in model_performance
    assert all(0 <= v <= 1 for v in model_performance.values())
    
    # التحقق من نتائج A/B testing
    ab_results = evaluation_results["ab_testing_results"]
    assert isinstance(ab_results, dict)
    assert "winner" in ab_results
    assert "confidence" in ab_results
    assert "improvement" in ab_results

def test_full_system_integration(emotion_engine, contextual_personalization, auto_evaluation, test_user, sample_data):
    """اختبار تكامل النظام الكامل"""
    time_context, logs = sample_data
    
    # تحليل المشاعر
    emotion_analysis = emotion_engine.analyze_and_suggest(test_user.id)
    
    # الحصول على التفضيلات السياقية
    context_preferences = contextual_personalization.get_contextual_preferences(test_user.id)
    
    # تشغيل التقييم التلقائي
    evaluation_results = auto_evaluation.run_evaluation_cycle()
    
    # التحقق من تكامل النتائج
    assert isinstance(emotion_analysis, dict)
    assert isinstance(context_preferences, dict)
    assert isinstance(evaluation_results, dict)
    
    # التحقق من اتساق البيانات
    assert emotion_analysis["user_id"] == test_user.id
    assert context_preferences["user_id"] == test_user.id
    
    # التحقق من جودة النتائج
    assert emotion_analysis["confidence_score"] >= 0.7
    assert context_preferences["confidence"] >= 0.7
    assert evaluation_results["model_performance"]["accuracy"] >= 0.8
    
    # التحقق من تكامل الاقتراحات
    suggestions = emotion_analysis["suggestions"]
    assert isinstance(suggestions, list)
    assert len(suggestions) > 0
    
    for suggestion in suggestions:
        assert "type" in suggestion
        assert "content" in suggestion
        assert "priority" in suggestion
        assert "confidence" in suggestion
        assert 0 <= suggestion["priority"] <= 1
        assert 0 <= suggestion["confidence"] <= 1
        assert isinstance(suggestion["content"], str)
        assert len(suggestion["content"]) > 0

def test_error_handling_integration(emotion_engine, contextual_personalization, auto_evaluation, db_session):
    """اختبار معالجة الأخطاء في التكامل"""
    # اختبار مع مستخدم غير موجود
    non_existent_user_id = 99999
    
    # التحقق من معالجة الأخطاء في تحليل المشاعر
    with pytest.raises(Exception):
        emotion_engine.analyze_and_suggest(non_existent_user_id)
    
    # التحقق من معالجة الأخطاء في التخصيص السياقي
    with pytest.raises(Exception):
        contextual_personalization.get_contextual_preferences(non_existent_user_id)
    
    # اختبار مع بيانات غير صالحة
    invalid_log = EmotionLog(
        user_id=non_existent_user_id,
        emotion_state={"invalid": "data"},
        confidence=1.5,  # قيمة غير صالحة
        created_at=datetime.now()
    )
    db_session.add(invalid_log)
    db_session.commit()
    
    # التحقق من معالجة الأخطاء في التقييم التلقائي
    with pytest.raises(Exception):
        auto_evaluation.run_evaluation_cycle() 
