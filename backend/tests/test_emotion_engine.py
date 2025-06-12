import pytest
import numpy as np
from datetime import datetime, timedelta
from backend.core.emotion_engine import EmotionSuggestionEngine
from backend.models.emotion import EmotionLog, EmotionPattern
from backend.models.user import User
from backend.models.time_context import TimeContext

@pytest.fixture
def db_session():
    # إنشاء جلسة قاعدة بيانات للاختبار
    from backend.database import SessionLocal
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def emotion_engine(db_session):
    # إنشاء نسخة من محرك المشاعر للاختبار
    return EmotionSuggestionEngine(db_session)

@pytest.fixture
def test_user(db_session):
    user = User(
        username="test_user",
        email="test@example.com",
        preferences={"language": "ar", "theme": "dark"}
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def sample_emotion_logs():
    # إنشاء بيانات اختبار للسجلات العاطفية
    return [
        EmotionLog(
            user_id=1,
            emotion_state={"happiness": 0.8, "sadness": 0.1},
            confidence=0.9,
            context={"activity": "work", "location": "office"},
            created_at=datetime.now() - timedelta(hours=i)
        )
        for i in range(24)
    ]

@pytest.fixture
def sample_time_context():
    # إنشاء سياق زمني للاختبار
    return TimeContext(
        hour=14,
        day_of_week=1,
        season="summer",
        is_holiday=False
    )

def test_analyze_daily_patterns(emotion_engine, sample_emotion_logs):
    """اختبار تحليل الأنماط اليومية"""
    patterns = emotion_engine._analyze_daily_patterns(sample_emotion_logs)
    
    assert isinstance(patterns, list)
    assert len(patterns) > 0
    
    for pattern in patterns:
        assert pattern["type"] == "daily"
        assert "hour" in pattern
        assert "average_state" in pattern
        assert "std_dev" in pattern
        assert "confidence" in pattern
        assert "sample_size" in pattern
        assert 0 <= pattern["confidence"] <= 1
        assert pattern["sample_size"] > 0

def test_analyze_weekly_patterns(emotion_engine, sample_emotion_logs):
    """اختبار تحليل الأنماط الأسبوعية"""
    patterns = emotion_engine._analyze_weekly_patterns(sample_emotion_logs)
    
    assert isinstance(patterns, list)
    assert len(patterns) > 0
    
    for pattern in patterns:
        assert pattern["type"] == "weekly"
        assert "day" in pattern
        assert "average_state" in pattern
        assert "std_dev" in pattern
        assert "confidence" in pattern
        assert "sample_size" in pattern
        assert 0 <= pattern["confidence"] <= 1
        assert pattern["sample_size"] > 0

def test_analyze_seasonal_patterns(emotion_engine, sample_emotion_logs):
    """اختبار تحليل الأنماط الموسمية"""
    patterns = emotion_engine._analyze_seasonal_patterns(sample_emotion_logs)
    
    assert isinstance(patterns, list)
    assert len(patterns) > 0
    
    for pattern in patterns:
        assert pattern["type"] == "seasonal"
        assert "season" in pattern
        assert "average_state" in pattern
        assert "std_dev" in pattern
        assert "trends" in pattern
        assert "confidence" in pattern
        assert "sample_size" in pattern
        assert 0 <= pattern["confidence"] <= 1
        assert pattern["sample_size"] > 0

def test_calculate_pattern_confidence(emotion_engine):
    """اختبار حساب ثقة الأنماط"""
    sample_states = [
        {"happiness": 0.8, "sadness": 0.1},
        {"happiness": 0.7, "sadness": 0.2},
        {"happiness": 0.9, "sadness": 0.1}
    ]
    
    confidence = emotion_engine._calculate_pattern_confidence(sample_states)
    
    assert isinstance(confidence, float)
    assert 0 <= confidence <= 1

def test_pattern_analysis_edge_cases(emotion_engine):
    """اختبار حالات الحدود في تحليل الأنماط"""
    # اختبار قائمة فارغة
    empty_patterns = emotion_engine._analyze_daily_patterns([])
    assert isinstance(empty_patterns, list)
    assert len(empty_patterns) == 0
    
    # اختبار بيانات غير كافية
    insufficient_data = [
        EmotionLog(
            user_id=1,
            emotion_state={"happiness": 0.8},
            confidence=0.9,
            created_at=datetime.now()
        )
    ]
    patterns = emotion_engine._analyze_daily_patterns(insufficient_data)
    assert isinstance(patterns, list)
    assert len(patterns) == 0

def test_analyze_seasonal_trends(emotion_engine, sample_emotion_logs):
    """اختبار تحليل الاتجاهات الموسمية"""
    trends = emotion_engine._analyze_seasonal_trends(sample_emotion_logs)
    
    assert isinstance(trends, dict)
    assert "trend" in trends
    assert "seasonal_change" in trends
    assert "seasonal_strength" in trends
    assert 0 <= trends["seasonal_strength"] <= 1

def test_seasonal_analysis_edge_cases(emotion_engine):
    """اختبار حالات الحدود في التحليل الموسمي"""
    # اختبار قائمة فارغة
    empty_trends = emotion_engine._analyze_seasonal_trends([])
    assert isinstance(empty_trends, dict)
    assert empty_trends["trend"] == 0
    assert empty_trends["seasonal_change"] == 0
    assert empty_trends["seasonal_strength"] == 0
    
    # اختبار بيانات غير كافية
    insufficient_data = [
        EmotionLog(
            user_id=1,
            emotion_state={"happiness": 0.8},
            confidence=0.9,
            created_at=datetime.now()
        )
    ]
    trends = emotion_engine._analyze_seasonal_trends(insufficient_data)
    assert isinstance(trends, dict)
    assert trends["trend"] == 0
    assert trends["seasonal_change"] == 0
    assert trends["seasonal_strength"] == 0

def test_emotion_state_validation(emotion_engine):
    """اختبار التحقق من صحة الحالة العاطفية"""
    # اختبار حالة عاطفية صالحة
    valid_state = {"happiness": 0.8, "sadness": 0.1, "anger": 0.0}
    assert emotion_engine._validate_emotion_state(valid_state)
    
    # اختبار حالة عاطفية غير صالحة (قيم خارج النطاق)
    invalid_state = {"happiness": 1.5, "sadness": -0.1}
    assert not emotion_engine._validate_emotion_state(invalid_state)
    
    # اختبار حالة عاطفية غير صالحة (نوع بيانات غير صحيح)
    invalid_type = {"happiness": "high", "sadness": "low"}
    assert not emotion_engine._validate_emotion_state(invalid_type)

def test_context_validation(emotion_engine):
    """اختبار التحقق من صحة السياق"""
    # اختبار سياق صالح
    valid_context = {
        "activity": "work",
        "location": "office",
        "weather": "sunny",
        "time_of_day": "morning"
    }
    assert emotion_engine._validate_context(valid_context)
    
    # اختبار سياق غير صالح (قيم غير متوقعة)
    invalid_context = {
        "activity": "unknown_activity",
        "location": "unknown_location"
    }
    assert not emotion_engine._validate_context(invalid_context)

def test_pattern_confidence_calculation(emotion_engine):
    """اختبار حساب ثقة الأنماط"""
    # اختبار حساب الثقة مع بيانات متناسقة
    consistent_states = [
        {"happiness": 0.8, "sadness": 0.1},
        {"happiness": 0.8, "sadness": 0.1},
        {"happiness": 0.8, "sadness": 0.1}
    ]
    high_confidence = emotion_engine._calculate_pattern_confidence(consistent_states)
    assert high_confidence > 0.8
    
    # اختبار حساب الثقة مع بيانات غير متناسقة
    inconsistent_states = [
        {"happiness": 0.8, "sadness": 0.1},
        {"happiness": 0.2, "sadness": 0.9},
        {"happiness": 0.5, "sadness": 0.5}
    ]
    low_confidence = emotion_engine._calculate_pattern_confidence(inconsistent_states)
    assert low_confidence < 0.5

def test_pattern_discovery(emotion_engine, sample_emotion_logs):
    """اختبار اكتشاف الأنماط"""
    patterns = emotion_engine._discover_patterns(sample_emotion_logs)
    
    assert isinstance(patterns, list)
    assert len(patterns) > 0
    
    for pattern in patterns:
        assert "type" in pattern
        assert "confidence" in pattern
        assert "description" in pattern
        assert "impact" in pattern
        assert 0 <= pattern["confidence"] <= 1
        assert isinstance(pattern["impact"], float)
        assert pattern["impact"] > 0

def test_emotion_suggestion_generation(emotion_engine, test_user, sample_emotion_logs):
    """اختبار توليد الاقتراحات العاطفية"""
    suggestions = emotion_engine._generate_suggestions(test_user.id, sample_emotion_logs)
    
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