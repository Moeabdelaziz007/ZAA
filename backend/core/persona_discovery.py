from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.logger import logger
from app.core.llm import LLMService
from app.models.user import User
from app.models.interaction import Interaction
from app.core.cache import cache

class PersonaDiscovery:
    """نظام اكتشاف الشخصية المتقدم"""
    
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = LLMService()
        self.emotion_weights = {
            'joy': 0.2,
            'sadness': 0.15,
            'anger': 0.1,
            'fear': 0.1,
            'surprise': 0.1,
            'disgust': 0.05,
            'trust': 0.15,
            'anticipation': 0.15
        }
        
    async def discover_persona(self, user_id: int) -> Dict:
        """اكتشاف شخصية المستخدم"""
        try:
            # جمع البيانات الأساسية
            user = self.db.query(User).filter(User.id == user_id).first()
            interactions = self._get_user_interactions(user_id)
            
            # تحليل المشاعر
            emotions = await self._analyze_emotions(interactions)
            
            # تحليل السمات
            traits = await self._analyze_traits(interactions)
            
            # تحليل الاحتياجات
            needs = await self._analyze_needs(interactions)
            
            # تحليل النوايا
            intent = await self._analyze_intent(interactions)
            
            # إنشاء الشخصية
            persona = self._create_persona(
                user,
                emotions,
                traits,
                needs,
                intent
            )
            
            # تحديث الشخصية
            self._update_persona(user_id, persona)
            
            return persona
            
        except Exception as e:
            logger.error(f"خطأ في اكتشاف الشخصية: {str(e)}")
            return {}
            
    def _get_user_interactions(self, user_id: int) -> List[Dict]:
        """الحصول على تفاعلات المستخدم"""
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
            logger.error(f"خطأ في الحصول على تفاعلات المستخدم: {str(e)}")
            return []
            
    async def _analyze_emotions(self, interactions: List[Dict]) -> Dict:
        """تحليل المشاعر"""
        try:
            # جمع النصوص
            texts = [i['content'] for i in interactions if i['content']]
            
            # تحليل المشاعر
            emotions = {}
            for text in texts:
                # استخدام LLM لتحليل المشاعر
                prompt = f"""
                تحليل المشاعر في النص:
                {text}
                
                قم بتحليل المشاعر الرئيسية وتقديم درجة لكل شعور.
                """
                
                response = await self.llm_service.analyze_context(prompt)
                
                # تحليل الاستجابة
                emotion_scores = self._parse_emotion_scores(response)
                
                # تحديث المشاعر
                for emotion, score in emotion_scores.items():
                    emotions[emotion] = emotions.get(emotion, 0) + score
                    
            # حساب المتوسط
            for emotion in emotions:
                emotions[emotion] /= len(texts)
                
            return emotions
            
        except Exception as e:
            logger.error(f"خطأ في تحليل المشاعر: {str(e)}")
            return {}
            
    async def _analyze_traits(self, interactions: List[Dict]) -> Dict:
        """تحليل السمات الشخصية"""
        try:
            # جمع النصوص
            texts = [i['content'] for i in interactions if i['content']]
            
            # تحليل السمات
            traits = {}
            for text in texts:
                # استخدام LLM لتحليل السمات
                prompt = f"""
                تحليل السمات الشخصية في النص:
                {text}
                
                قم بتحليل السمات الشخصية الرئيسية وتقديم درجة لكل سمة.
                """
                
                response = await self.llm_service.analyze_context(prompt)
                
                # تحليل الاستجابة
                trait_scores = self._parse_trait_scores(response)
                
                # تحديث السمات
                for trait, score in trait_scores.items():
                    traits[trait] = traits.get(trait, 0) + score
                    
            # حساب المتوسط
            for trait in traits:
                traits[trait] /= len(texts)
                
            return traits
            
        except Exception as e:
            logger.error(f"خطأ في تحليل السمات: {str(e)}")
            return {}
            
    async def _analyze_needs(self, interactions: List[Dict]) -> Dict:
        """تحليل الاحتياجات"""
        try:
            # جمع النصوص
            texts = [i['content'] for i in interactions if i['content']]
            
            # تحليل الاحتياجات
            needs = {}
            for text in texts:
                # استخدام LLM لتحليل الاحتياجات
                prompt = f"""
                تحليل الاحتياجات في النص:
                {text}
                
                قم بتحليل الاحتياجات الرئيسية وتقديم درجة لكل حاجة.
                """
                
                response = await self.llm_service.analyze_context(prompt)
                
                # تحليل الاستجابة
                need_scores = self._parse_need_scores(response)
                
                # تحديث الاحتياجات
                for need, score in need_scores.items():
                    needs[need] = needs.get(need, 0) + score
                    
            # حساب المتوسط
            for need in needs:
                needs[need] /= len(texts)
                
            return needs
            
        except Exception as e:
            logger.error(f"خطأ في تحليل الاحتياجات: {str(e)}")
            return {}
            
    async def _analyze_intent(self, interactions: List[Dict]) -> Dict:
        """تحليل النوايا"""
        try:
            # جمع النصوص
            texts = [i['content'] for i in interactions if i['content']]
            
            # تحليل النوايا
            intents = {}
            for text in texts:
                # استخدام LLM لتحليل النوايا
                prompt = f"""
                تحليل النوايا في النص:
                {text}
                
                قم بتحليل النوايا الرئيسية وتقديم درجة لكل نية.
                """
                
                response = await self.llm_service.analyze_context(prompt)
                
                # تحليل الاستجابة
                intent_scores = self._parse_intent_scores(response)
                
                # تحديث النوايا
                for intent, score in intent_scores.items():
                    intents[intent] = intents.get(intent, 0) + score
                    
            # حساب المتوسط
            for intent in intents:
                intents[intent] /= len(texts)
                
            return intents
            
        except Exception as e:
            logger.error(f"خطأ في تحليل النوايا: {str(e)}")
            return {}
            
    def _create_persona(
        self,
        user: User,
        emotions: Dict,
        traits: Dict,
        needs: Dict,
        intent: Dict
    ) -> Dict:
        """إنشاء شخصية المستخدم"""
        try:
            # حساب الدرجة الإجمالية
            emotion_score = sum(
                emotions.get(emotion, 0) * weight
                for emotion, weight in self.emotion_weights.items()
            )
            
            trait_score = sum(traits.values()) / len(traits) if traits else 0
            need_score = sum(needs.values()) / len(needs) if needs else 0
            intent_score = sum(intent.values()) / len(intent) if intent else 0
            
            # إنشاء الشخصية
            return {
                'user_id': user.id,
                'emotions': emotions,
                'traits': traits,
                'needs': needs,
                'intent': intent,
                'scores': {
                    'emotion': emotion_score,
                    'trait': trait_score,
                    'need': need_score,
                    'intent': intent_score
                },
                'timestamp': datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء الشخصية: {str(e)}")
            return {}
            
    def _update_persona(self, user_id: int, persona: Dict):
        """تحديث شخصية المستخدم"""
        try:
            # حفظ في الكاش
            cache.set(f'user_persona_{user_id}', persona)
            
            # TODO: حفظ في قاعدة البيانات
            
        except Exception as e:
            logger.error(f"خطأ في تحديث الشخصية: {str(e)}")
            
    def _parse_emotion_scores(self, response: str) -> Dict:
        """تحليل درجات المشاعر"""
        try:
            # TODO: تنفيذ تحليل الاستجابة
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل درجات المشاعر: {str(e)}")
            return {}
            
    def _parse_trait_scores(self, response: str) -> Dict:
        """تحليل درجات السمات"""
        try:
            # TODO: تنفيذ تحليل الاستجابة
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل درجات السمات: {str(e)}")
            return {}
            
    def _parse_need_scores(self, response: str) -> Dict:
        """تحليل درجات الاحتياجات"""
        try:
            # TODO: تنفيذ تحليل الاستجابة
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل درجات الاحتياجات: {str(e)}")
            return {}
            
    def _parse_intent_scores(self, response: str) -> Dict:
        """تحليل درجات النوايا"""
        try:
            # TODO: تنفيذ تحليل الاستجابة
            return {}
            
        except Exception as e:
            logger.error(f"خطأ في تحليل درجات النوايا: {str(e)}")
            return {}
