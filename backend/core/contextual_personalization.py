from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.logger import logger
from app.core.cache import cache
from app.models.user import User
from app.models.item import Item
from app.models.interaction import Interaction
from app.models.context import Context
from app.core.llm import LLMService
from app.core.weather import WeatherService
from app.core.news import NewsService
import lightgbm as lgb
from sklearn.preprocessing import LabelEncoder
import torch
import torch.nn as nn

class ContextualBandit:
    """نموذج Contextual Bandit"""
    
    def __init__(self, n_arms: int, context_dim: int):
        self.n_arms = n_arms
        self.context_dim = context_dim
        self.model = lgb.LGBMClassifier(
            n_estimators=100,
            learning_rate=0.1,
            num_leaves=31
        )
        self.label_encoder = LabelEncoder()
        
    def fit(self, contexts: np.ndarray, actions: np.ndarray, rewards: np.ndarray):
        """تدريب النموذج"""
        try:
            # تحويل الإجراءات
            encoded_actions = self.label_encoder.fit_transform(actions)
            
            # تدريب النموذج
            self.model.fit(contexts, encoded_actions, sample_weight=rewards)
            
        except Exception as e:
            logger.error(f"خطأ في تدريب Contextual Bandit: {str(e)}")
            
    def predict(self, context: np.ndarray) -> int:
        """التنبؤ بالإجراء الأمثل"""
        try:
            # التنبؤ
            encoded_action = self.model.predict(context.reshape(1, -1))[0]
            
            # تحويل الإجراء
            return self.label_encoder.inverse_transform([encoded_action])[0]
            
        except Exception as e:
            logger.error(f"خطأ في تنبؤ Contextual Bandit: {str(e)}")
            return 0

class SequenceModel(nn.Module):
    """نموذج التسلسل (LSTM)"""
    
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=2,
            batch_first=True
        )
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """تمرير البيانات"""
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])

class ContextualPersonalization:
    """نظام التخصيص السياقي"""
    
    def __init__(self, db: Session):
        self.db = db
        self.bandit = ContextualBandit(n_arms=100, context_dim=50)
        self.sequence_model = SequenceModel(
            input_dim=50,
            hidden_dim=128,
            output_dim=100
        )
        self.context_cache = {}
        self.llm_service = LLMService()
        self.weather_service = WeatherService()
        self.news_service = NewsService()
        self.update_interval = timedelta(hours=1)  # تحديث كل ساعة
        
    def _extract_context(self, user: User, current_time: datetime) -> np.ndarray:
        """استخراج السياق"""
        try:
            # جمع معلومات السياق
            context = {
                'time_of_day': current_time.hour / 24,
                'day_of_week': current_time.weekday() / 7,
                'month': current_time.month / 12,
                'user_age': user.age / 100 if user.age else 0.5,
                'user_gender': 1 if user.gender == 'male' else 0,
                'last_interaction': self._get_last_interaction_time(user.id),
                'interaction_frequency': self._get_interaction_frequency(user.id),
                'preferred_categories': self._get_preferred_categories(user.id),
                'device_type': self._get_device_type(user.id),
                'location': self._get_user_location(user.id)
            }
            
            # تحويل السياق إلى مصفوفة
            return np.array(list(context.values()))
            
        except Exception as e:
            logger.error(f"خطأ في استخراج السياق: {str(e)}")
            return np.zeros(50)
            
    def _get_last_interaction_time(self, user_id: int) -> float:
        """الحصول على وقت آخر تفاعل"""
        try:
            last_interaction = self.db.query(Interaction)\
                .filter(Interaction.user_id == user_id)\
                .order_by(Interaction.timestamp.desc())\
                .first()
                
            if last_interaction:
                time_diff = datetime.utcnow() - last_interaction.timestamp
                return min(time_diff.total_seconds() / (24 * 3600), 1.0)
            return 1.0
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على وقت آخر تفاعل: {str(e)}")
            return 1.0
            
    def _get_interaction_frequency(self, user_id: int) -> float:
        """الحصول على تكرار التفاعل"""
        try:
            interactions = self.db.query(Interaction)\
                .filter(Interaction.user_id == user_id)\
                .all()
                
            if interactions:
                return min(len(interactions) / 100, 1.0)
            return 0.0
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على تكرار التفاعل: {str(e)}")
            return 0.0
            
    def _get_preferred_categories(self, user_id: int) -> List[float]:
        """الحصول على الفئات المفضلة"""
        try:
            # TODO: تنفيذ تحليل الفئات المفضلة
            return [0.0] * 10
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على الفئات المفضلة: {str(e)}")
            return [0.0] * 10
            
    def _get_device_type(self, user_id: int) -> float:
        """الحصول على نوع الجهاز"""
        try:
            # TODO: تنفيذ تحليل نوع الجهاز
            return 0.5
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على نوع الجهاز: {str(e)}")
            return 0.5
            
    def _get_user_location(self, user_id: int) -> float:
        """الحصول على موقع المستخدم"""
        try:
            # TODO: تنفيذ تحليل الموقع
            return 0.5
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على موقع المستخدم: {str(e)}")
            return 0.5
            
    async def get_personalized_recommendations(
        self,
        user: User,
        n_recommendations: int = 10
    ) -> List[Item]:
        """الحصول على توصيات مخصصة"""
        try:
            # استخراج السياق
            context = self._extract_context(user, datetime.utcnow())
            
            # الحصول على تنبؤات النموذجين
            bandit_prediction = self.bandit.predict(context)
            sequence_prediction = self._get_sequence_prediction(context)
            
            # دمج التنبؤات
            final_prediction = self._combine_predictions(
                bandit_prediction,
                sequence_prediction
            )
            
            # الحصول على التوصيات
            recommendations = self._get_recommendations(
                user.id,
                final_prediction,
                n_recommendations
            )
            
            return recommendations
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على توصيات مخصصة: {str(e)}")
            return []
            
    def _get_sequence_prediction(self, context: np.ndarray) -> int:
        """الحصول على تنبؤ نموذج التسلسل"""
        try:
            # تحويل السياق إلى تنسيق PyTorch
            context_tensor = torch.FloatTensor(context).unsqueeze(0)
            
            # التنبؤ
            with torch.no_grad():
                prediction = self.sequence_model(context_tensor)
                
            return torch.argmax(prediction).item()
            
        except Exception as e:
            logger.error(f"خطأ في تنبؤ نموذج التسلسل: {str(e)}")
            return 0
            
    def _combine_predictions(
        self,
        bandit_prediction: int,
        sequence_prediction: int
    ) -> int:
        """دمج تنبؤات النموذجين"""
        try:
            # حساب الأوزان
            bandit_weight = 0.6
            sequence_weight = 0.4
            
            # دمج التنبؤات
            return int(
                bandit_prediction * bandit_weight +
                sequence_prediction * sequence_weight
            )
            
        except Exception as e:
            logger.error(f"خطأ في دمج التنبؤات: {str(e)}")
            return bandit_prediction
            
    def _get_recommendations(
        self,
        user_id: int,
        prediction: int,
        n_recommendations: int
    ) -> List[Item]:
        """الحصول على التوصيات"""
        try:
            # الحصول على العناصر الموصى بها
            recommendations = self.db.query(Item)\
                .filter(Item.category_id == prediction)\
                .order_by(Item.popularity_score.desc())\
                .limit(n_recommendations)\
                .all()
                
            return recommendations
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على التوصيات: {str(e)}")
            return []
            
    def update_models(self, user_id: int, item_id: int, reward: float):
        """تحديث النماذج"""
        try:
            # جمع البيانات
            user = self.db.query(User).filter(User.id == user_id).first()
            context = self._extract_context(user, datetime.utcnow())
            
            # تحديث Contextual Bandit
            self.bandit.fit(
                contexts=np.array([context]),
                actions=np.array([item_id]),
                rewards=np.array([reward])
            )
            
            # تحديث نموذج التسلسل
            self._update_sequence_model(context, item_id, reward)
            
        except Exception as e:
            logger.error(f"خطأ في تحديث النماذج: {str(e)}")
            
    def _update_sequence_model(
        self,
        context: np.ndarray,
        item_id: int,
        reward: float
    ):
        """تحديث نموذج التسلسل"""
        try:
            # تحويل البيانات
            context_tensor = torch.FloatTensor(context).unsqueeze(0)
            target = torch.LongTensor([item_id])
            
            # حساب الخسارة
            criterion = nn.CrossEntropyLoss()
            output = self.sequence_model(context_tensor)
            loss = criterion(output, target)
            
            # تحديث النموذج
            optimizer = torch.optim.Adam(self.sequence_model.parameters())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
        except Exception as e:
            logger.error(f"خطأ في تحديث نموذج التسلسل: {str(e)}")

    async def get_contextual_preferences(self, user_id: int) -> Dict:
        """الحصول على التفضيلات السياقية"""
        try:
            # جمع السياق
            context = await self._gather_context(user_id)
            
            # تحليل السياق
            context_analysis = await self._analyze_context(context)
            
            # تحديث التفضيلات
            preferences = await self._update_preferences(user_id, context_analysis)
            
            return preferences
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على التفضيلات السياقية: {str(e)}")
            return {}
            
    async def _gather_context(self, user_id: int) -> Dict:
        """جمع السياق"""
        try:
            # جمع معلومات المستخدم
            user = self.db.query(User).filter(User.id == user_id).first()
            
            # جمع التفاعلات الأخيرة
            interactions = self._get_recent_interactions(user_id)
            
            # جمع معلومات الطقس
            weather = await self.weather_service.get_weather(user.location)
            
            # جمع الأخبار
            news = await self.news_service.get_relevant_news(user.interests)
            
            # جمع السياق الزمني
            time_context = self._get_time_context()
            
            return {
                'user': user,
                'interactions': interactions,
                'weather': weather,
                'news': news,
                'time': time_context
            }
            
        except Exception as e:
            logger.error(f"خطأ في جمع السياق: {str(e)}")
            return {}
            
    async def _analyze_context(self, context: Dict) -> Dict:
        """تحليل السياق"""
        try:
            # تحليل المشاعر
            emotions = await self._analyze_emotions(context)
            
            # تحليل السلوك
            behavior = await self._analyze_behavior(context)
            
            # تحليل التفضيلات
            preferences = await self._analyze_preferences(context)
            
            # تحليل النوايا
            intents = await self._analyze_intents(context)
            
            return {
                'emotions': emotions,
                'behavior': behavior,
                'preferences': preferences,
                'intents': intents,
                'timestamp': datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل السياق: {str(e)}")
            return {}
            
    async def _update_preferences(
        self,
        user_id: int,
        context_analysis: Dict
    ) -> Dict:
        """تحديث التفضيلات"""
        try:
            # الحصول على التفضيلات الحالية
            current_preferences = self._get_current_preferences(user_id)
            
            # تحديث التفضيلات
            updated_preferences = self._adjust_preferences(
                current_preferences,
                context_analysis
            )
            
            # حفظ التفضيلات
            await self._save_preferences(user_id, updated_preferences)
            
            return updated_preferences
            
        except Exception as e:
            logger.error(f"خطأ في تحديث التفضيلات: {str(e)}")
            return {}
            
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
            logger.error(f"خطأ في الحصول على التفاعلات: {str(e)}")
            return []
            
    def _get_time_context(self) -> Dict:
        """الحصول على السياق الزمني"""
        try:
            now = datetime.utcnow()
            
            return {
                'hour': now.hour,
                'day': now.day,
                'month': now.month,
                'season': self._get_season(now),
                'is_weekend': now.weekday() >= 5,
                'is_holiday': self._is_holiday(now)
            }
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على السياق الزمني: {str(e)}")
            return {}
            
    def _get_season(self, date: datetime) -> str:
        """الحصول على الموسم"""
        try:
            month = date.month
            
            if month in [12, 1, 2]:
                return 'winter'
            elif month in [3, 4, 5]:
                return 'spring'
            elif month in [6, 7, 8]:
                return 'summer'
            else:
                return 'autumn'
                
        except Exception as e:
            logger.error(f"خطأ في الحصول على الموسم: {str(e)}")
            return 'unknown'
            
    def _is_holiday(self, date: datetime) -> bool:
        """التحقق من العطلة"""
        try:
            # TODO: تنفيذ التحقق من العطل
            return False
            
        except Exception as e:
            logger.error(f"خطأ في التحقق من العطلة: {str(e)}")
            return False
            
    async def _analyze_emotions(self, context: Dict) -> Dict:
        """تحليل المشاعر"""
        try:
            # تحليل مشاعر التفاعلات
            interaction_emotions = await self._analyze_interaction_emotions(
                context['interactions']
            )
            
            # تحليل مشاعر الأخبار
            news_emotions = await self._analyze_news_emotions(
                context['news']
            )
            
            # تحليل مشاعر الطقس
            weather_emotions = await self._analyze_weather_emotions(
                context['weather']
            )
            
            return {
                'interactions': interaction_emotions,
                'news': news_emotions,
                'weather': weather_emotions
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل المشاعر: {str(e)}")
            return {}
            
    async def _analyze_behavior(self, context: Dict) -> Dict:
        """تحليل السلوك"""
        try:
            # تحليل أنماط التفاعل
            interaction_patterns = self._analyze_interaction_patterns(
                context['interactions']
            )
            
            # تحليل التفضيلات الزمنية
            time_preferences = self._analyze_time_preferences(
                context['interactions']
            )
            
            # تحليل التفضيلات الموسمية
            seasonal_preferences = self._analyze_seasonal_preferences(
                context['interactions']
            )
            
            return {
                'patterns': interaction_patterns,
                'time': time_preferences,
                'seasonal': seasonal_preferences
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل السلوك: {str(e)}")
            return {}
            
    async def _analyze_preferences(self, context: Dict) -> Dict:
        """تحليل التفضيلات"""
        try:
            # تحليل التفضيلات العامة
            general_preferences = self._analyze_general_preferences(
                context['interactions']
            )
            
            # تحليل التفضيلات السياقية
            contextual_preferences = self._analyze_contextual_preferences(
                context
            )
            
            # تحليل التفضيلات الديناميكية
            dynamic_preferences = self._analyze_dynamic_preferences(
                context
            )
            
            return {
                'general': general_preferences,
                'contextual': contextual_preferences,
                'dynamic': dynamic_preferences
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل التفضيلات: {str(e)}")
            return {}
            
    async def _analyze_intents(self, context: Dict) -> Dict:
        """تحليل النوايا"""
        try:
            # تحليل نوايا التفاعل
            interaction_intents = await self._analyze_interaction_intents(
                context['interactions']
            )
            
            # تحليل نوايا البحث
            search_intents = await self._analyze_search_intents(
                context['interactions']
            )
            
            # تحليل نوايا الشراء
            purchase_intents = await self._analyze_purchase_intents(
                context['interactions']
            )
            
            return {
                'interaction': interaction_intents,
                'search': search_intents,
                'purchase': purchase_intents
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل النوايا: {str(e)}")
            return {}
            
    def _get_current_preferences(self, user_id: int) -> Dict:
        """الحصول على التفضيلات الحالية"""
        try:
            # TODO: تنفيذ الحصول على التفضيلات
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على التفضيلات: {str(e)}")
            return {}
            
    def _adjust_preferences(
        self,
        current_preferences: Dict,
        context_analysis: Dict
    ) -> Dict:
        """تعديل التفضيلات"""
        try:
            # TODO: تنفيذ تعديل التفضيلات
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تعديل التفضيلات: {str(e)}")
            return {}
            
    async def _save_preferences(self, user_id: int, preferences: Dict):
        """حفظ التفضيلات"""
        try:
            # TODO: تنفيذ حفظ التفضيلات
            pass
            
        except Exception as e:
            logger.error(f"خطأ في حفظ التفضيلات: {str(e)}")
            
    async def _analyze_interaction_emotions(self, interactions: List[Dict]) -> Dict:
        """تحليل مشاعر التفاعلات"""
        try:
            # TODO: تنفيذ تحليل المشاعر
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل مشاعر التفاعلات: {str(e)}")
            return {}
            
    async def _analyze_news_emotions(self, news: List[Dict]) -> Dict:
        """تحليل مشاعر الأخبار"""
        try:
            # TODO: تنفيذ تحليل المشاعر
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل مشاعر الأخبار: {str(e)}")
            return {}
            
    async def _analyze_weather_emotions(self, weather: Dict) -> Dict:
        """تحليل مشاعر الطقس"""
        try:
            # TODO: تنفيذ تحليل المشاعر
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل مشاعر الطقس: {str(e)}")
            return {}
            
    def _analyze_interaction_patterns(self, interactions: List[Dict]) -> Dict:
        """تحليل أنماط التفاعل"""
        try:
            # TODO: تنفيذ تحليل الأنماط
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل أنماط التفاعل: {str(e)}")
            return {}
            
    def _analyze_time_preferences(self, interactions: List[Dict]) -> Dict:
        """تحليل التفضيلات الزمنية"""
        try:
            # TODO: تنفيذ تحليل التفضيلات
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل التفضيلات الزمنية: {str(e)}")
            return {}
            
    def _analyze_seasonal_preferences(self, interactions: List[Dict]) -> Dict:
        """تحليل التفضيلات الموسمية"""
        try:
            # TODO: تنفيذ تحليل التفضيلات
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل التفضيلات الموسمية: {str(e)}")
            return {}
            
    def _analyze_general_preferences(self, interactions: List[Dict]) -> Dict:
        """تحليل التفضيلات العامة"""
        try:
            # TODO: تنفيذ تحليل التفضيلات
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل التفضيلات العامة: {str(e)}")
            return {}
            
    def _analyze_contextual_preferences(self, context: Dict) -> Dict:
        """تحليل التفضيلات السياقية"""
        try:
            # TODO: تنفيذ تحليل التفضيلات
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل التفضيلات السياقية: {str(e)}")
            return {}
            
    def _analyze_dynamic_preferences(self, context: Dict) -> Dict:
        """تحليل التفضيلات الديناميكية"""
        try:
            # TODO: تنفيذ تحليل التفضيلات
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل التفضيلات الديناميكية: {str(e)}")
            return {}
            
    async def _analyze_interaction_intents(self, interactions: List[Dict]) -> Dict:
        """تحليل نوايا التفاعل"""
        try:
            # TODO: تنفيذ تحليل النوايا
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل نوايا التفاعل: {str(e)}")
            return {}
            
    async def _analyze_search_intents(self, interactions: List[Dict]) -> Dict:
        """تحليل نوايا البحث"""
        try:
            # TODO: تنفيذ تحليل النوايا
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل نوايا البحث: {str(e)}")
            return {}
            
    async def _analyze_purchase_intents(self, interactions: List[Dict]) -> Dict:
        """تحليل نوايا الشراء"""
        try:
            # TODO: تنفيذ تحليل النوايا
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل نوايا الشراء: {str(e)}")
            return {}
