from typing import Dict, List, Optional
from datetime import datetime
import numpy as np
from sqlalchemy.orm import Session
from app.models.recommendation import Recommendation
from app.models.user_interaction import UserInteraction
from app.core.metrics import calculate_metrics
from app.core.logger import logger

class SelfEvaluationSystem:
    """نظام التقييم الذاتي للتوصيات"""
    
    def __init__(self, db: Session):
        self.db = db
        self.metrics = {
            'precision': 0.0,
            'recall': 0.0,
            'ndcg': 0.0,
            'diversity': 0.0,
            'novelty': 0.0,
            'coverage': 0.0
        }
        
    def evaluate_recommendations(self, user_id: int, recommendations: List[Dict]) -> Dict:
        """تقييم جودة التوصيات لمستخدم معين"""
        try:
            # جمع التفاعلات السابقة
            interactions = self.db.query(UserInteraction).filter(
                UserInteraction.user_id == user_id
            ).all()
            
            # حساب المقاييس
            self.metrics = calculate_metrics(recommendations, interactions)
            
            # تسجيل النتائج
            self._log_evaluation_results(user_id)
            
            return self.metrics
            
        except Exception as e:
            logger.error(f"خطأ في تقييم التوصيات: {str(e)}")
            raise
            
    def _log_evaluation_results(self, user_id: int):
        """تسجيل نتائج التقييم"""
        try:
            evaluation = {
                'user_id': user_id,
                'timestamp': datetime.utcnow(),
                'metrics': self.metrics
            }
            
            # حفظ النتائج في قاعدة البيانات
            # TODO: إنشاء نموذج EvaluationResult
            
            logger.info(f"تم تسجيل نتائج التقييم للمستخدم {user_id}")
            
        except Exception as e:
            logger.error(f"خطأ في تسجيل نتائج التقييم: {str(e)}")
            raise
            
    def generate_evaluation_report(self, start_date: datetime, end_date: datetime) -> Dict:
        """توليد تقرير تقييم لفترة زمنية"""
        try:
            # جمع جميع التقييمات في الفترة المحددة
            evaluations = self.db.query(Recommendation).filter(
                Recommendation.created_at.between(start_date, end_date)
            ).all()
            
            # حساب المتوسطات
            report = {
                'period': {
                    'start': start_date,
                    'end': end_date
                },
                'metrics': {
                    'precision': np.mean([e.metrics['precision'] for e in evaluations]),
                    'recall': np.mean([e.metrics['recall'] for e in evaluations]),
                    'ndcg': np.mean([e.metrics['ndcg'] for e in evaluations]),
                    'diversity': np.mean([e.metrics['diversity'] for e in evaluations]),
                    'novelty': np.mean([e.metrics['novelty'] for e in evaluations]),
                    'coverage': np.mean([e.metrics['coverage'] for e in evaluations])
                },
                'total_recommendations': len(evaluations),
                'active_users': len(set(e.user_id for e in evaluations))
            }
            
            return report
            
        except Exception as e:
            logger.error(f"خطأ في توليد تقرير التقييم: {str(e)}")
            raise
            
    def get_user_feedback(self, user_id: int) -> Dict:
        """جمع وتجميع ملاحظات المستخدم"""
        try:
            # جمع التفاعلات والملاحظات
            interactions = self.db.query(UserInteraction).filter(
                UserInteraction.user_id == user_id
            ).all()
            
            feedback = {
                'total_interactions': len(interactions),
                'positive_feedback': len([i for i in interactions if i.rating > 3]),
                'negative_feedback': len([i for i in interactions if i.rating <= 3]),
                'average_rating': np.mean([i.rating for i in interactions]),
                'last_interaction': max(i.created_at for i in interactions)
            }
            
            return feedback
            
        except Exception as e:
            logger.error(f"خطأ في جمع ملاحظات المستخدم: {str(e)}")
            raise
