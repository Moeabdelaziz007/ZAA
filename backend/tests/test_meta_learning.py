import pytest
import numpy as np
from datetime import datetime, timedelta
from backend.core.meta_learning import MetaLearning
from backend.models.emotion import EmotionLog, EmotionPattern
from backend.models.user import User
from backend.models.learning import LearningState, ImprovementLog

@pytest.fixture
def db_session():
    from backend.database import SessionLocal
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def meta_learning(db_session):
    return MetaLearning(db_session)

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
def sample_data(db_session, test_user):
    """إنشاء بيانات اختبار"""
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
    return logs

def test_learning_cycle(meta_learning, test_user, sample_data):
    """اختبار دورة التعلم"""
    results = meta_learning.run_learning_cycle()
    
    assert isinstance(results, dict)
    assert results["status"] == "success"
    assert "data_analysis" in results
    assert "performance_evaluation" in results
    assert "improvement_areas" in results
    assert "applied_improvements" in results
    assert "results" in results

def test_data_analysis(meta_learning, sample_data):
    """اختبار تحليل البيانات"""
    analysis = meta_learning._analyze_system_data()
    
    assert isinstance(analysis, dict)
    assert "emotion_analysis" in analysis
    assert "user_patterns" in analysis
    assert "system_performance" in analysis
    
    # التحقق من تحليل المشاعر
    emotion_analysis = analysis["emotion_analysis"]
    assert isinstance(emotion_analysis, dict)
    assert len(emotion_analysis) > 0
    
    # التحقق من أنماط المستخدمين
    user_patterns = analysis["user_patterns"]
    assert isinstance(user_patterns, dict)
    assert len(user_patterns) > 0

def test_performance_evaluation(meta_learning, sample_data):
    """اختبار تقييم الأداء"""
    evaluation = meta_learning._evaluate_current_performance()
    
    assert isinstance(evaluation, dict)
    assert "emotion_accuracy" in evaluation
    assert "suggestion_quality" in evaluation
    assert "personalization_performance" in evaluation
    
    # التحقق من قيم التقييم
    assert 0 <= evaluation["emotion_accuracy"] <= 1
    assert 0 <= evaluation["suggestion_quality"] <= 1
    assert 0 <= evaluation["personalization_performance"] <= 1

def test_improvement_identification(meta_learning, sample_data):
    """اختبار تحديد مجالات التحسين"""
    data_analysis = meta_learning._analyze_system_data()
    performance_evaluation = meta_learning._evaluate_current_performance()
    
    improvement_areas = meta_learning._identify_improvement_areas(
        data_analysis,
        performance_evaluation
    )
    
    assert isinstance(improvement_areas, list)
    
    for area in improvement_areas:
        assert "area" in area
        assert "current_performance" in area
        assert "target_performance" in area
        assert "improvement_strategy" in area
        assert 0 <= area["current_performance"] <= 1
        assert 0 <= area["target_performance"] <= 1

def test_improvement_application(meta_learning, sample_data):
    """اختبار تطبيق التحسينات"""
    data_analysis = meta_learning._analyze_system_data()
    performance_evaluation = meta_learning._evaluate_current_performance()
    improvement_areas = meta_learning._identify_improvement_areas(
        data_analysis,
        performance_evaluation
    )
    
    improvements = meta_learning._apply_improvements(improvement_areas)
    
    assert isinstance(improvements, list)
    
    for improvement in improvements:
        assert "area" in improvement
        assert "result" in improvement
        assert isinstance(improvement["result"], dict)

def test_improvement_evaluation(meta_learning, sample_data):
    """اختبار تقييم التحسينات"""
    data_analysis = meta_learning._analyze_system_data()
    performance_evaluation = meta_learning._evaluate_current_performance()
    improvement_areas = meta_learning._identify_improvement_areas(
        data_analysis,
        performance_evaluation
    )
    improvements = meta_learning._apply_improvements(improvement_areas)
    
    results = meta_learning._evaluate_improvements(improvements)
    
    assert isinstance(results, dict)
    assert "successful_improvements" in results
    assert "failed_improvements" in results
    assert "overall_impact" in results
    assert 0 <= results["overall_impact"] <= 1

def test_learning_state_update(meta_learning, sample_data):
    """اختبار تحديث حالة التعلم"""
    data_analysis = meta_learning._analyze_system_data()
    performance_evaluation = meta_learning._evaluate_current_performance()
    improvement_areas = meta_learning._identify_improvement_areas(
        data_analysis,
        performance_evaluation
    )
    improvements = meta_learning._apply_improvements(improvement_areas)
    results = meta_learning._evaluate_improvements(improvements)
    
    meta_learning._update_learning_state(results)
    
    # التحقق من تحديث حالة التعلم
    learning_state = meta_learning.db.query(LearningState).order_by(
        LearningState.last_learning_cycle.desc()
    ).first()
    
    assert learning_state is not None
    assert learning_state.successful_improvements >= 0
    assert learning_state.failed_improvements >= 0
    assert 0 <= learning_state.overall_impact <= 1
    assert 0.001 <= learning_state.learning_rate <= 0.1

def test_emotion_pattern_analysis(meta_learning, sample_data):
    """اختبار تحليل أنماط المشاعر"""
    patterns = meta_learning._analyze_emotion_patterns(sample_data)
    
    assert isinstance(patterns, dict)
    assert len(patterns) > 0
    
    for emotion, data in patterns.items():
        assert "count" in data
        assert "total" in data
        assert "contexts" in data
        assert data["count"] > 0
        assert 0 <= data["total"] <= data["count"]

def test_user_pattern_analysis(meta_learning, test_user):
    """اختبار تحليل أنماط المستخدمين"""
    patterns = meta_learning._analyze_user_patterns()
    
    assert isinstance(patterns, dict)
    assert test_user.id in patterns
    
    user_pattern = patterns[test_user.id]
    assert "preferences" in user_pattern
    assert "behavior" in user_pattern
    assert isinstance(user_pattern["preferences"], dict)
    assert isinstance(user_pattern["behavior"], dict)

def test_system_performance_analysis(meta_learning, sample_data):
    """اختبار تحليل أداء النظام"""
    performance = meta_learning._analyze_system_performance()
    
    assert isinstance(performance, dict)
    assert "emotion_accuracy" in performance
    assert "suggestion_quality" in performance
    assert "personalization_performance" in performance
    
    assert 0 <= performance["emotion_accuracy"] <= 1
    assert 0 <= performance["suggestion_quality"] <= 1
    assert 0 <= performance["personalization_performance"] <= 1

def test_learning_rate_update(meta_learning):
    """اختبار تحديث معدل التعلم"""
    # اختبار زيادة معدل التعلم
    meta_learning._update_learning_rate({"overall_impact": 0.6})
    assert meta_learning.learning_rate > 0.01
    
    # اختبار تقليل معدل التعلم
    meta_learning._update_learning_rate({"overall_impact": 0.1})
    assert meta_learning.learning_rate < 0.01
    
    # اختبار الحدود
    meta_learning.learning_rate = 0.001
    meta_learning._update_learning_rate({"overall_impact": 0.1})
    assert meta_learning.learning_rate >= 0.001
    
    meta_learning.learning_rate = 0.1
    meta_learning._update_learning_rate({"overall_impact": 0.6})
    assert meta_learning.learning_rate <= 0.1 