from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime
from app.core.logger import logger
from app.core.quantum_brain.emotion_module import EmotionModule
from app.core.quantum_brain.time_module import TimeModule

class EmotionTimeIntegrator:
    """وحدة تكامل المشاعر والزمن"""
    
    def __init__(self):
        self.emotion_module = EmotionModule()
        self.time_module = TimeModule()
        self.integrated_state = self._initialize_integrated_state()
        
    def _initialize_integrated_state(self) -> Dict:
        """تهيئة الحالة المتكاملة"""
        return {
            'emotion_time_matrix': np.zeros((len(self.emotion_module.emotion_states), 24)),
            'quantum_correlation': np.zeros((len(self.emotion_module.emotion_states), 24)),
            'temporal_emotion_patterns': {}
        }
        
    async def update_integrated_state(self, text: str, timezone: str = 'UTC'):
        """تحديث الحالة المتكاملة"""
        try:
            # تحديث وحدة المشاعر
            emotion_state = await self.emotion_module.analyze_emotion(text)
            
            # تحديث وحدة الزمن
            self.time_module.update_time_context(timezone)
            
            # تحديث المصفوفة المتكاملة
            self._update_emotion_time_matrix(emotion_state)
            
            # تحديث الارتباط الكوانتمي
            self._update_quantum_correlation()
            
            # تحديث الأنماط الزمنية للمشاعر
            self._update_temporal_patterns()
            
        except Exception as e:
            logger.error(f"خطأ في تحديث الحالة المتكاملة: {str(e)}")
            
    def _update_emotion_time_matrix(self, emotion_state: Dict[str, float]):
        """تحديث مصفوفة المشاعر-الزمن"""
        try:
            hour = self.time_module.current_time.hour
            
            # تحديث المصفوفة
            for i, emotion in enumerate(self.emotion_module.emotion_states.keys()):
                self.integrated_state['emotion_time_matrix'][i, hour] = emotion_state[emotion]
                
        except Exception as e:
            logger.error(f"خطأ في تحديث مصفوفة المشاعر-الزمن: {str(e)}")
            
    def _update_quantum_correlation(self):
        """تحديث الارتباط الكوانتمي"""
        try:
            # حساب الارتباط الكوانتمي بين المشاعر والزمن
            emotion_state = self.emotion_module.quantum_state
            time_state = self.time_module.quantum_state
            
            # تطبيق تداخل كوانتمي
            correlation = np.tensordot(emotion_state, time_state, axes=([0, 1], [0, 1]))
            
            # تطبيق تحويل فورييه الكوانتمي
            fft_correlation = np.fft.fft2(correlation)
            
            self.integrated_state['quantum_correlation'] = np.abs(fft_correlation)
            
        except Exception as e:
            logger.error(f"خطأ في تحديث الارتباط الكوانتمي: {str(e)}")
            
    def _update_temporal_patterns(self):
        """تحديث الأنماط الزمنية للمشاعر"""
        try:
            # تحليل الأنماط الزمنية
            emotion_trends = self.emotion_module.get_emotion_trend()
            time_trends = self.time_module.get_time_trend()
            
            # تحديد الأنماط المتكررة
            patterns = {}
            for emotion, values in emotion_trends.items():
                if values:
                    # حساب الارتباط مع الوقت
                    correlation = np.corrcoef(values, time_trends['hour'])[0, 1]
                    patterns[emotion] = {
                        'correlation': correlation,
                        'trend': np.mean(np.diff(values)),
                        'peak_hour': np.argmax(values)
                    }
                    
            self.integrated_state['temporal_emotion_patterns'] = patterns
            
        except Exception as e:
            logger.error(f"خطأ في تحديث الأنماط الزمنية: {str(e)}")
            
    def get_emotional_context(self) -> Dict:
        """الحصول على السياق العاطفي الحالي"""
        try:
            current_hour = self.time_module.current_time.hour
            
            # استخراج المشاعر السائدة في هذا الوقت
            hour_emotions = self.integrated_state['emotion_time_matrix'][:, current_hour]
            dominant_emotion = list(self.emotion_module.emotion_states.keys())[np.argmax(hour_emotions)]
            
            # تحليل الأنماط الزمنية
            patterns = self.integrated_state['temporal_emotion_patterns']
            
            return {
                'current_emotion': dominant_emotion,
                'emotion_intensity': float(np.max(hour_emotions)),
                'temporal_patterns': patterns,
                'time_context': self.time_module.time_context
            }
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على السياق العاطفي: {str(e)}")
            return {}
            
    def predict_emotional_state(self, hours_ahead: int) -> Dict:
        """التنبؤ بالحالة العاطفية المستقبلية"""
        try:
            # التنبؤ بحالة الزمن المستقبلية
            future_time = self.time_module.predict_future_state(hours_ahead)
            
            # استخراج المشاعر المتوقعة
            future_hour = future_time['hour']
            future_emotions = self.integrated_state['emotion_time_matrix'][:, future_hour]
            
            # تحليل الأنماط
            patterns = self.integrated_state['temporal_emotion_patterns']
            
            return {
                'predicted_emotion': list(self.emotion_module.emotion_states.keys())[np.argmax(future_emotions)],
                'confidence': float(np.max(future_emotions)),
                'temporal_factors': patterns,
                'future_time_context': future_time
            }
            
        except Exception as e:
            logger.error(f"خطأ في التنبؤ بالحالة العاطفية: {str(e)}")
            return {}
            
    def get_quantum_integrated_state(self) -> Tuple[np.ndarray, Dict]:
        """الحصول على الحالة الكوانتمية المتكاملة"""
        return self.integrated_state['quantum_correlation'], self.integrated_state['temporal_emotion_patterns']
        
    def reset_integrated_state(self):
        """إعادة تعيين الحالة المتكاملة"""
        self.emotion_module.reset_emotion_state()
        self.time_module.reset_time_state()
        self.integrated_state = self._initialize_integrated_state() 