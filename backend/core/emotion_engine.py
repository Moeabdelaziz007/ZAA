from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.logger import logger
from app.core.llm import LLMService
from app.core.cache import cache
from app.models.user import User
from app.models.interaction import Interaction
from app.models.emotion_log import EmotionLog
from app.models.pattern import Pattern
from app.core.visualization import VisualizationService
from app.core.quantum_brain.emotion_module import EmotionModule
from app.core.quantum_brain.time_module import TimeModule

class EmotionSuggestionEngine:
    """محرك الاقتراح العاطفي الذكي"""
    
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = LLMService()
        self.visualization = VisualizationService()
        self.emotion_module = EmotionModule()
        self.time_module = TimeModule()
        self.confidence_threshold = 0.7
        
    async def analyze_and_suggest(
        self,
        user_id: int,
        context: Optional[Dict] = None
    ) -> Dict:
        """تحليل وتقديم اقتراحات عاطفية"""
        try:
            # تحليل الحالة العاطفية
            emotion_analysis = await self._analyze_emotion_state(user_id, context)
            
            # اكتشاف الأنماط
            patterns = await self._discover_patterns(user_id)
            
            # حساب مؤشر الثقة
            confidence_score = self._calculate_confidence(emotion_analysis, patterns)
            
            # إنشاء الاقتراحات
            suggestions = await self._generate_suggestions(
                emotion_analysis,
                patterns,
                confidence_score
            )
            
            # إنشاء التصورات
            visualizations = self._create_visualizations(
                emotion_analysis,
                patterns,
                confidence_score
            )
            
            # تحديث السجل
            await self._update_emotion_log(
                user_id,
                emotion_analysis,
                patterns,
                confidence_score
            )
            
            return {
                'emotion_analysis': emotion_analysis,
                'patterns': patterns,
                'confidence_score': confidence_score,
                'suggestions': suggestions,
                'visualizations': visualizations,
                'timestamp': datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل وتقديم الاقتراحات: {str(e)}")
            return {}
            
    async def _analyze_emotion_state(
        self,
        user_id: int,
        context: Optional[Dict]
    ) -> Dict:
        """تحليل الحالة العاطفية"""
        try:
            # جمع البيانات
            user = self.db.query(User).filter(User.id == user_id).first()
            recent_interactions = self._get_recent_interactions(user_id)
            
            # تحليل النص
            text_analysis = await self._analyze_text(recent_interactions)
            
            # تحليل السياق
            context_analysis = await self._analyze_context(context)
            
            # تحليل الحالة العاطفية الكمية
            quantum_state = await self.emotion_module.analyze_emotion(
                text_analysis,
                context_analysis
            )
            
            # تحليل الاتجاهات
            trends = self._analyze_emotion_trends(user_id)
            
            return {
                'current_state': quantum_state,
                'text_analysis': text_analysis,
                'context_analysis': context_analysis,
                'trends': trends,
                'timestamp': datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل الحالة العاطفية: {str(e)}")
            return {}
            
    async def _discover_patterns(self, user_id: int) -> List[Dict]:
        """اكتشاف الأنماط"""
        try:
            # جمع البيانات التاريخية
            emotion_logs = self._get_emotion_logs(user_id)
            time_contexts = self._get_time_contexts(user_id)
            
            # تحليل الأنماط الزمنية
            temporal_patterns = self._analyze_temporal_patterns(
                emotion_logs,
                time_contexts
            )
            
            # تحليل أنماط السلوك
            behavioral_patterns = self._analyze_behavioral_patterns(
                emotion_logs
            )
            
            # تحليل الأنماط الخفية
            hidden_patterns = self._analyze_hidden_patterns(
                emotion_logs,
                time_contexts
            )
            
            # تحليل الأنماط الموسمية
            seasonal_patterns = self._analyze_seasonal_patterns(
                emotion_logs,
                time_contexts
            )
            
            # تحديث قاعدة البيانات
            await self._update_patterns(user_id, {
                'temporal': temporal_patterns,
                'behavioral': behavioral_patterns,
                'hidden': hidden_patterns,
                'seasonal': seasonal_patterns
            })
            
            return {
                'temporal': temporal_patterns,
                'behavioral': behavioral_patterns,
                'hidden': hidden_patterns,
                'seasonal': seasonal_patterns
            }
            
        except Exception as e:
            logger.error(f"خطأ في اكتشاف الأنماط: {str(e)}")
            return []
            
    def _calculate_confidence(
        self,
        emotion_analysis: Dict,
        patterns: List[Dict]
    ) -> float:
        """حساب مؤشر الثقة"""
        try:
            # حساب ثقة التحليل العاطفي
            emotion_confidence = self._calculate_emotion_confidence(
                emotion_analysis
            )
            
            # حساب ثقة الأنماط
            pattern_confidence = self._calculate_pattern_confidence(patterns)
            
            # حساب الثقة النهائية
            final_confidence = (emotion_confidence + pattern_confidence) / 2
            
            return min(max(final_confidence, 0), 1)
            
        except Exception as e:
            logger.error(f"خطأ في حساب مؤشر الثقة: {str(e)}")
            return 0.0
            
    async def _generate_suggestions(
        self,
        emotion_analysis: Dict,
        patterns: List[Dict],
        confidence_score: float
    ) -> List[Dict]:
        """إنشاء الاقتراحات"""
        try:
            suggestions = []
            
            # اقتراحات عاطفية
            emotion_suggestions = await self._generate_emotion_suggestions(
                emotion_analysis,
                confidence_score
            )
            suggestions.extend(emotion_suggestions)
            
            # اقتراحات سلوكية
            behavioral_suggestions = await self._generate_behavioral_suggestions(
                patterns,
                confidence_score
            )
            suggestions.extend(behavioral_suggestions)
            
            # اقتراحات سياقية
            contextual_suggestions = await self._generate_contextual_suggestions(
                emotion_analysis,
                patterns,
                confidence_score
            )
            suggestions.extend(contextual_suggestions)
            
            return suggestions
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء الاقتراحات: {str(e)}")
            return []
            
    def _create_visualizations(
        self,
        emotion_analysis: Dict,
        patterns: List[Dict],
        confidence_score: float
    ) -> Dict:
        """إنشاء التصورات"""
        try:
            visualizations = {}
            
            # تصور الحالة العاطفية
            visualizations['emotion_state'] = self._create_emotion_visualization(
                emotion_analysis
            )
            
            # تصور الأنماط
            visualizations['patterns'] = self._create_pattern_visualization(
                patterns
            )
            
            # تصور الثقة
            visualizations['confidence'] = self._create_confidence_visualization(
                confidence_score
            )
            
            # تصور الاتجاهات
            visualizations['trends'] = self._create_trend_visualization(
                emotion_analysis['trends']
            )
            
            return visualizations
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء التصورات: {str(e)}")
            return {}
            
    async def _update_emotion_log(
        self,
        user_id: int,
        emotion_analysis: Dict,
        patterns: List[Dict],
        confidence_score: float
    ):
        """تحديث سجل العواطف"""
        try:
            log = EmotionLog(
                user_id=user_id,
                emotion_state=emotion_analysis['current_state'],
                patterns=patterns,
                confidence_score=confidence_score,
                timestamp=datetime.utcnow()
            )
            
            self.db.add(log)
            self.db.commit()
            
        except Exception as e:
            logger.error(f"خطأ في تحديث سجل العواطف: {str(e)}")
            
    def _get_recent_interactions(self, user_id: int) -> List[Dict]:
        """الحصول على التفاعلات الأخيرة"""
        try:
            interactions = self.db.query(Interaction)\
                .filter(Interaction.user_id == user_id)\
                .order_by(Interaction.timestamp.desc())\
                .limit(100)\
                .all()
                
            return [
                {
                    'type': i.interaction_type,
                    'content': i.content,
                    'timestamp': i.timestamp,
                    'rating': i.rating
                }
                for i in interactions
            ]
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على التفاعلات الأخيرة: {str(e)}")
            return []
            
    async def _analyze_text(self, interactions: List[Dict]) -> Dict:
        """تحليل النص"""
        try:
            # تجميع النصوص
            texts = [i['content'] for i in interactions if i['content']]
            
            # تحليل المشاعر
            sentiment = await self.llm_service.analyze_sentiment(texts)
            
            # تحليل السياق
            context = await self.llm_service.analyze_context(texts)
            
            return {
                'sentiment': sentiment,
                'context': context,
                'text_count': len(texts)
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل النص: {str(e)}")
            return {}
            
    async def _analyze_context(self, context: Optional[Dict]) -> Dict:
        """تحليل السياق"""
        try:
            if not context:
                return {}
                
            # تحليل الوقت
            time_context = self.time_module.get_time_context()
            
            # تحليل الموقع
            location_context = self._analyze_location(context.get('location'))
            
            # تحليل الجهاز
            device_context = self._analyze_device(context.get('device'))
            
            return {
                'time': time_context,
                'location': location_context,
                'device': device_context
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل السياق: {str(e)}")
            return {}
            
    def _analyze_emotion_trends(self, user_id: int) -> Dict:
        """تحليل اتجاهات العواطف"""
        try:
            # الحصول على السجلات
            logs = self._get_emotion_logs(user_id)
            
            # تحليل الاتجاهات اليومية
            daily_trends = self._analyze_daily_trends(logs)
            
            # تحليل الاتجاهات الأسبوعية
            weekly_trends = self._analyze_weekly_trends(logs)
            
            # تحليل الاتجاهات الشهرية
            monthly_trends = self._analyze_monthly_trends(logs)
            
            return {
                'daily': daily_trends,
                'weekly': weekly_trends,
                'monthly': monthly_trends
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل اتجاهات العواطف: {str(e)}")
            return {}
            
    def _get_emotion_logs(
        self,
        user_id: int,
        days: int = 30
    ) -> List[Dict]:
        """الحصول على سجلات العواطف"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            logs = self.db.query(EmotionLog)\
                .filter(
                    EmotionLog.user_id == user_id,
                    EmotionLog.timestamp >= start_date
                )\
                .order_by(EmotionLog.timestamp.asc())\
                .all()
                
            return [
                {
                    'emotion_state': log.emotion_state,
                    'patterns': log.patterns,
                    'confidence_score': log.confidence_score,
                    'timestamp': log.timestamp
                }
                for log in logs
            ]
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على سجلات العواطف: {str(e)}")
            return []
            
    def _get_time_contexts(
        self,
        user_id: int,
        days: int = 30
    ) -> List[Dict]:
        """الحصول على السياقات الزمنية"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            logs = self.db.query(EmotionLog)\
                .filter(
                    EmotionLog.user_id == user_id,
                    EmotionLog.timestamp >= start_date
                )\
                .order_by(EmotionLog.timestamp.asc())\
                .all()
                
            return [
                {
                    'hour': log.timestamp.hour,
                    'day': log.timestamp.weekday(),
                    'month': log.timestamp.month,
                    'season': self._get_season(log.timestamp)
                }
                for log in logs
            ]
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على السياقات الزمنية: {str(e)}")
            return []
            
    def _analyze_temporal_patterns(
        self,
        emotion_logs: List[Dict],
        time_contexts: List[Dict]
    ) -> List[Dict]:
        """تحليل الأنماط الزمنية"""
        try:
            patterns = []
            
            # تحليل الأنماط اليومية
            daily_patterns = self._analyze_daily_patterns(
                emotion_logs,
                time_contexts
            )
            patterns.extend(daily_patterns)
            
            # تحليل الأنماط الأسبوعية
            weekly_patterns = self._analyze_weekly_patterns(
                emotion_logs,
                time_contexts
            )
            patterns.extend(weekly_patterns)
            
            # تحليل الأنماط الموسمية
            seasonal_patterns = self._analyze_seasonal_patterns(
                emotion_logs,
                time_contexts
            )
            patterns.extend(seasonal_patterns)
            
            return patterns
            
        except Exception as e:
            logger.error(f"خطأ في تحليل الأنماط الزمنية: {str(e)}")
            return []
            
    def _analyze_behavioral_patterns(
        self,
        emotion_logs: List[Dict]
    ) -> List[Dict]:
        """تحليل أنماط السلوك"""
        try:
            patterns = []
            
            # تحليل أنماط التفاعل
            interaction_patterns = self._analyze_interaction_patterns(
                emotion_logs
            )
            patterns.extend(interaction_patterns)
            
            # تحليل أنماط الاستجابة
            response_patterns = self._analyze_response_patterns(
                emotion_logs
            )
            patterns.extend(response_patterns)
            
            # تحليل أنماط التفضيل
            preference_patterns = self._analyze_preference_patterns(
                emotion_logs
            )
            patterns.extend(preference_patterns)
            
            return patterns
            
        except Exception as e:
            logger.error(f"خطأ في تحليل أنماط السلوك: {str(e)}")
            return []
            
    def _analyze_hidden_patterns(
        self,
        emotion_logs: List[Dict],
        time_contexts: List[Dict]
    ) -> List[Dict]:
        """تحليل الأنماط الخفية"""
        try:
            patterns = []
            
            # تحليل الارتباطات
            correlations = self._analyze_correlations(
                emotion_logs,
                time_contexts
            )
            patterns.extend(correlations)
            
            # تحليل السببية
            causations = self._analyze_causations(
                emotion_logs,
                time_contexts
            )
            patterns.extend(causations)
            
            # تحليل التوقعات
            predictions = self._analyze_predictions(
                emotion_logs,
                time_contexts
            )
            patterns.extend(predictions)
            
            return patterns
            
        except Exception as e:
            logger.error(f"خطأ في تحليل الأنماط الخفية: {str(e)}")
            return []
            
    async def _update_patterns(
        self,
        user_id: int,
        patterns: Dict
    ):
        """تحديث الأنماط"""
        try:
            pattern = Pattern(
                user_id=user_id,
                temporal_patterns=patterns['temporal'],
                behavioral_patterns=patterns['behavioral'],
                hidden_patterns=patterns['hidden'],
                seasonal_patterns=patterns['seasonal'],
                timestamp=datetime.utcnow()
            )
            
            self.db.add(pattern)
            self.db.commit()
            
        except Exception as e:
            logger.error(f"خطأ في تحديث الأنماط: {str(e)}")
            
    def _calculate_emotion_confidence(self, emotion_analysis: Dict) -> float:
        """حساب ثقة التحليل العاطفي"""
        try:
            # حساب ثقة النص
            text_confidence = self._calculate_text_confidence(
                emotion_analysis['text_analysis']
            )
            
            # حساب ثقة السياق
            context_confidence = self._calculate_context_confidence(
                emotion_analysis['context_analysis']
            )
            
            # حساب ثقة الحالة الكمية
            quantum_confidence = self._calculate_quantum_confidence(
                emotion_analysis['current_state']
            )
            
            # حساب الثقة النهائية
            final_confidence = (
                text_confidence * 0.4 +
                context_confidence * 0.3 +
                quantum_confidence * 0.3
            )
            
            return min(max(final_confidence, 0), 1)
            
        except Exception as e:
            logger.error(f"خطأ في حساب ثقة التحليل العاطفي: {str(e)}")
            return 0.0
            
    def _calculate_pattern_confidence(self, patterns: List[Dict]) -> float:
        """حساب ثقة الأنماط"""
        try:
            if not patterns:
                return 0.0
                
            # حساب ثقة الأنماط الزمنية
            temporal_confidence = self._calculate_temporal_confidence(
                patterns['temporal']
            )
            
            # حساب ثقة أنماط السلوك
            behavioral_confidence = self._calculate_behavioral_confidence(
                patterns['behavioral']
            )
            
            # حساب ثقة الأنماط الخفية
            hidden_confidence = self._calculate_hidden_confidence(
                patterns['hidden']
            )
            
            # حساب ثقة الأنماط الموسمية
            seasonal_confidence = self._calculate_seasonal_confidence(
                patterns['seasonal']
            )
            
            # حساب الثقة النهائية
            final_confidence = (
                temporal_confidence * 0.3 +
                behavioral_confidence * 0.3 +
                hidden_confidence * 0.2 +
                seasonal_confidence * 0.2
            )
            
            return min(max(final_confidence, 0), 1)
            
        except Exception as e:
            logger.error(f"خطأ في حساب ثقة الأنماط: {str(e)}")
            return 0.0
            
    async def _generate_emotion_suggestions(
        self,
        emotion_analysis: Dict,
        confidence_score: float
    ) -> List[Dict]:
        """إنشاء اقتراحات عاطفية"""
        try:
            suggestions = []
            
            # اقتراحات بناءً على الحالة الحالية
            current_suggestions = await self._generate_current_suggestions(
                emotion_analysis['current_state'],
                confidence_score
            )
            suggestions.extend(current_suggestions)
            
            # اقتراحات بناءً على الاتجاهات
            trend_suggestions = await self._generate_trend_suggestions(
                emotion_analysis['trends'],
                confidence_score
            )
            suggestions.extend(trend_suggestions)
            
            return suggestions
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء اقتراحات عاطفية: {str(e)}")
            return []
            
    async def _generate_behavioral_suggestions(
        self,
        patterns: List[Dict],
        confidence_score: float
    ) -> List[Dict]:
        """إنشاء اقتراحات سلوكية"""
        try:
            suggestions = []
            
            # اقتراحات بناءً على الأنماط الزمنية
            temporal_suggestions = await self._generate_temporal_suggestions(
                patterns['temporal'],
                confidence_score
            )
            suggestions.extend(temporal_suggestions)
            
            # اقتراحات بناءً على أنماط السلوك
            behavioral_suggestions = await self._generate_behavioral_suggestions(
                patterns['behavioral'],
                confidence_score
            )
            suggestions.extend(behavioral_suggestions)
            
            return suggestions
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء اقتراحات سلوكية: {str(e)}")
            return []
            
    async def _generate_contextual_suggestions(
        self,
        emotion_analysis: Dict,
        patterns: List[Dict],
        confidence_score: float
    ) -> List[Dict]:
        """إنشاء اقتراحات سياقية"""
        try:
            suggestions = []
            
            # اقتراحات بناءً على السياق الزمني
            time_suggestions = await self._generate_time_suggestions(
                emotion_analysis['context_analysis']['time'],
                confidence_score
            )
            suggestions.extend(time_suggestions)
            
            # اقتراحات بناءً على السياق المكاني
            location_suggestions = await self._generate_location_suggestions(
                emotion_analysis['context_analysis']['location'],
                confidence_score
            )
            suggestions.extend(location_suggestions)
            
            return suggestions
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء اقتراحات سياقية: {str(e)}")
            return []
            
    def _create_emotion_visualization(self, emotion_analysis: Dict) -> Dict:
        """إنشاء تصور الحالة العاطفية"""
        try:
            return self.visualization.create_emotion_chart(
                emotion_analysis['current_state'],
                emotion_analysis['trends']
            )
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء تصور الحالة العاطفية: {str(e)}")
            return {}
            
    def _create_pattern_visualization(self, patterns: List[Dict]) -> Dict:
        """إنشاء تصور الأنماط"""
        try:
            return self.visualization.create_pattern_chart(patterns)
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء تصور الأنماط: {str(e)}")
            return {}
            
    def _create_confidence_visualization(self, confidence_score: float) -> Dict:
        """إنشاء تصور الثقة"""
        try:
            return self.visualization.create_confidence_chart(confidence_score)
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء تصور الثقة: {str(e)}")
            return {}
            
    def _create_trend_visualization(self, trends: Dict) -> Dict:
        """إنشاء تصور الاتجاهات"""
        try:
            return self.visualization.create_trend_chart(trends)
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء تصور الاتجاهات: {str(e)}")
            return {}
            
    def _analyze_daily_patterns(
        self,
        emotion_logs: List[Dict],
        time_contexts: List[Dict]
    ) -> List[Dict]:
        """تحليل الأنماط اليومية"""
        try:
            patterns = []
            
            # تجميع البيانات حسب الساعة
            hourly_data = {}
            for log, context in zip(emotion_logs, time_contexts):
                hour = context['hour']
                if hour not in hourly_data:
                    hourly_data[hour] = []
                hourly_data[hour].append(log['emotion_state'])
            
            # تحليل كل ساعة
            for hour, states in hourly_data.items():
                if len(states) < 3:  # نحتاج على الأقل 3 نقاط بيانات
                    continue
                    
                # حساب المتوسط والانحراف المعياري
                avg_state = np.mean(states, axis=0)
                std_state = np.std(states, axis=0)
                
                # تحديد النمط
                pattern = {
                    'type': 'daily',
                    'hour': hour,
                    'average_state': avg_state.tolist(),
                    'std_deviation': std_state.tolist(),
                    'confidence': self._calculate_pattern_confidence(states),
                    'sample_size': len(states)
                }
                
                # إضافة النمط إذا كان ذا دلالة إحصائية
                if pattern['confidence'] > self.confidence_threshold:
                    patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"خطأ في تحليل الأنماط اليومية: {str(e)}")
            return []
            
    def _analyze_weekly_patterns(
        self,
        emotion_logs: List[Dict],
        time_contexts: List[Dict]
    ) -> List[Dict]:
        """تحليل الأنماط الأسبوعية"""
        try:
            patterns = []
            
            # تجميع البيانات حسب اليوم
            daily_data = {}
            for log, context in zip(emotion_logs, time_contexts):
                day = context['day']
                if day not in daily_data:
                    daily_data[day] = []
                daily_data[day].append(log['emotion_state'])
            
            # تحليل كل يوم
            for day, states in daily_data.items():
                if len(states) < 3:  # نحتاج على الأقل 3 نقاط بيانات
                    continue
                    
                # حساب المتوسط والانحراف المعياري
                avg_state = np.mean(states, axis=0)
                std_state = np.std(states, axis=0)
                
                # تحديد النمط
                pattern = {
                    'type': 'weekly',
                    'day': day,
                    'average_state': avg_state.tolist(),
                    'std_deviation': std_state.tolist(),
                    'confidence': self._calculate_pattern_confidence(states),
                    'sample_size': len(states)
                }
                
                # إضافة النمط إذا كان ذا دلالة إحصائية
                if pattern['confidence'] > self.confidence_threshold:
                    patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"خطأ في تحليل الأنماط الأسبوعية: {str(e)}")
            return []
            
    def _analyze_seasonal_patterns(
        self,
        emotion_logs: List[Dict],
        time_contexts: List[Dict]
    ) -> List[Dict]:
        """تحليل الأنماط الموسمية"""
        try:
            patterns = []
            
            # تجميع البيانات حسب الموسم
            seasonal_data = {}
            for log, context in zip(emotion_logs, time_contexts):
                season = context['season']
                if season not in seasonal_data:
                    seasonal_data[season] = []
                seasonal_data[season].append(log['emotion_state'])
            
            # تحليل كل موسم
            for season, states in seasonal_data.items():
                if len(states) < 5:  # نحتاج على الأقل 5 نقاط بيانات للموسم
                    continue
                    
                # حساب المتوسط والانحراف المعياري
                avg_state = np.mean(states, axis=0)
                std_state = np.std(states, axis=0)
                
                # تحليل الاتجاهات الموسمية
                trends = self._analyze_seasonal_trends(states)
                
                # تحديد النمط
                pattern = {
                    'type': 'seasonal',
                    'season': season,
                    'average_state': avg_state.tolist(),
                    'std_deviation': std_state.tolist(),
                    'trends': trends,
                    'confidence': self._calculate_pattern_confidence(states),
                    'sample_size': len(states)
                }
                
                # إضافة النمط إذا كان ذا دلالة إحصائية
                if pattern['confidence'] > self.confidence_threshold:
                    patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"خطأ في تحليل الأنماط الموسمية: {str(e)}")
            return []
            
    def _analyze_seasonal_trends(self, states: List[np.ndarray]) -> Dict:
        """تحليل الاتجاهات الموسمية"""
        try:
            if len(states) < 5:
                return {}
                
            # تحويل البيانات إلى مصفوفة
            data = np.array(states)
            
            # حساب الاتجاه العام
            trend = np.polyfit(range(len(data)), data, 1)[0]
            
            # حساب التغير الموسمي
            seasonal_change = np.mean(np.diff(data, axis=0), axis=0)
            
            # تحديد قوة الموسمية
            seasonal_strength = np.std(seasonal_change) / (np.std(data) + 1e-10)
            
            return {
                'trend': trend.tolist(),
                'seasonal_change': seasonal_change.tolist(),
                'seasonal_strength': float(seasonal_strength)
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل الاتجاهات الموسمية: {str(e)}")
            return {}
            
    def _analyze_interaction_patterns(
        self,
        emotion_logs: List[Dict]
    ) -> List[Dict]:
        """تحليل أنماط التفاعل"""
        try:
            patterns = []
            
            # تجميع البيانات حسب نوع التفاعل
            interaction_data = {}
            for log in emotion_logs:
                if 'interaction_type' not in log:
                    continue
                    
                interaction_type = log['interaction_type']
                if interaction_type not in interaction_data:
                    interaction_data[interaction_type] = []
                interaction_data[interaction_type].append(log['emotion_state'])
            
            # تحليل كل نوع تفاعل
            for interaction_type, states in interaction_data.items():
                if len(states) < 3:  # نحتاج على الأقل 3 نقاط بيانات
                    continue
                    
                # حساب المتوسط والانحراف المعياري
                avg_state = np.mean(states, axis=0)
                std_state = np.std(states, axis=0)
                
                # تحليل تأثير التفاعل
                impact = self._analyze_interaction_impact(states)
                
                # تحديد النمط
                pattern = {
                    'type': 'interaction',
                    'interaction_type': interaction_type,
                    'average_state': avg_state.tolist(),
                    'std_deviation': std_state.tolist(),
                    'impact': impact,
                    'confidence': self._calculate_pattern_confidence(states),
                    'sample_size': len(states)
                }
                
                # إضافة النمط إذا كان ذا دلالة إحصائية
                if pattern['confidence'] > self.confidence_threshold:
                    patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"خطأ في تحليل أنماط التفاعل: {str(e)}")
            return []
            
    def _analyze_interaction_impact(self, states: List[np.ndarray]) -> Dict:
        """تحليل تأثير التفاعل"""
        try:
            if len(states) < 3:
                return {}
                
            # تحويل البيانات إلى مصفوفة
            data = np.array(states)
            
            # حساب التغير في الحالة العاطفية
            state_changes = np.diff(data, axis=0)
            
            # حساب متوسط التغير
            avg_change = np.mean(state_changes, axis=0)
            
            # حساب قوة التأثير
            impact_strength = np.linalg.norm(avg_change)
            
            # تحديد اتجاه التأثير
            impact_direction = np.sign(avg_change)
            
            # حساب استقرار التأثير
            impact_stability = 1 - (np.std(state_changes) / (np.mean(np.abs(state_changes)) + 1e-10))
            
            return {
                'average_change': avg_change.tolist(),
                'impact_strength': float(impact_strength),
                'impact_direction': impact_direction.tolist(),
                'impact_stability': float(impact_stability)
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل تأثير التفاعل: {str(e)}")
            return {}
