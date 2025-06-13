from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.logger import logger
from app.core.llm import LLMService
from app.models.user import User
from app.models.interaction import Interaction
from app.core.cache import cache

class InversePrompting:
    """نظام Inverse Prompting المتقدم"""
    
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = LLMService()
        self.question_templates = {
            'emotion': [
                "كيف تشعر حيال {topic}؟",
                "ما رأيك في {topic}؟",
                "ما هي مشاعرك تجاه {topic}؟"
            ],
            'trait': [
                "كيف تصف نفسك في {context}؟",
                "ما هي صفاتك في {context}؟",
                "كيف تتصرف في {context}؟"
            ],
            'need': [
                "ما الذي تحتاجه في {situation}؟",
                "ما هي احتياجاتك في {situation}؟",
                "ما الذي تبحث عنه في {situation}؟"
            ],
            'intent': [
                "ما هي أهدافك في {domain}؟",
                "ما الذي تريد تحقيقه في {domain}؟",
                "ما هي خططك في {domain}؟"
            ]
        }
        
    async def generate_prompts(self, user_id: int, context: Dict) -> List[Dict]:
        """إنشاء أسئلة مخصصة"""
        try:
            # جمع معلومات المستخدم
            user = self.db.query(User).filter(User.id == user_id).first()
            interactions = self._get_user_interactions(user_id)
            
            # تحليل السياق
            topics = self._extract_topics(interactions)
            situations = self._extract_situations(interactions)
            domains = self._extract_domains(interactions)
            
            # إنشاء الأسئلة
            prompts = []
            
            # أسئلة المشاعر
            for topic in topics:
                for template in self.question_templates['emotion']:
                    prompt = template.format(topic=topic)
                    prompts.append({
                        'type': 'emotion',
                        'prompt': prompt,
                        'context': {'topic': topic}
                    })
                    
            # أسئلة السمات
            for situation in situations:
                for template in self.question_templates['trait']:
                    prompt = template.format(context=situation)
                    prompts.append({
                        'type': 'trait',
                        'prompt': prompt,
                        'context': {'situation': situation}
                    })
                    
            # أسئلة الاحتياجات
            for situation in situations:
                for template in self.question_templates['need']:
                    prompt = template.format(situation=situation)
                    prompts.append({
                        'type': 'need',
                        'prompt': prompt,
                        'context': {'situation': situation}
                    })
                    
            # أسئلة النوايا
            for domain in domains:
                for template in self.question_templates['intent']:
                    prompt = template.format(domain=domain)
                    prompts.append({
                        'type': 'intent',
                        'prompt': prompt,
                        'context': {'domain': domain}
                    })
                    
            return prompts
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء الأسئلة: {str(e)}")
            return []
            
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
            
    def _extract_topics(self, interactions: List[Dict]) -> List[str]:
        """استخراج المواضيع"""
        try:
            # جمع النصوص
            texts = [i['content'] for i in interactions if i['content']]
            
            # استخدام LLM لاستخراج المواضيع
            topics = set()
            for text in texts:
                prompt = f"""
                استخراج المواضيع الرئيسية من النص:
                {text}
                
                قم بذكر المواضيع الرئيسية فقط.
                """
                
                response = self.llm_service.analyze_context(prompt)
                topics.update(self._parse_topics(response))
                
            return list(topics)
            
        except Exception as e:
            logger.error(f"خطأ في استخراج المواضيع: {str(e)}")
            return []
            
    def _extract_situations(self, interactions: List[Dict]) -> List[str]:
        """استخراج المواقف"""
        try:
            # جمع النصوص
            texts = [i['content'] for i in interactions if i['content']]
            
            # استخدام LLM لاستخراج المواقف
            situations = set()
            for text in texts:
                prompt = f"""
                استخراج المواقف الرئيسية من النص:
                {text}
                
                قم بذكر المواقف الرئيسية فقط.
                """
                
                response = self.llm_service.analyze_context(prompt)
                situations.update(self._parse_situations(response))
                
            return list(situations)
            
        except Exception as e:
            logger.error(f"خطأ في استخراج المواقف: {str(e)}")
            return []
            
    def _extract_domains(self, interactions: List[Dict]) -> List[str]:
        """استخراج المجالات"""
        try:
            # جمع النصوص
            texts = [i['content'] for i in interactions if i['content']]
            
            # استخدام LLM لاستخراج المجالات
            domains = set()
            for text in texts:
                prompt = f"""
                استخراج المجالات الرئيسية من النص:
                {text}
                
                قم بذكر المجالات الرئيسية فقط.
                """
                
                response = self.llm_service.analyze_context(prompt)
                domains.update(self._parse_domains(response))
                
            return list(domains)
            
        except Exception as e:
            logger.error(f"خطأ في استخراج المجالات: {str(e)}")
            return []
            
    async def analyze_response(
        self,
        prompt: Dict,
        response: str
    ) -> Dict:
        """تحليل الرد"""
        try:
            # تحليل الرد
            analysis = {}
            
            if prompt['type'] == 'emotion':
                analysis = await self._analyze_emotion_response(
                    response,
                    prompt['context']
                )
            elif prompt['type'] == 'trait':
                analysis = await self._analyze_trait_response(
                    response,
                    prompt['context']
                )
            elif prompt['type'] == 'need':
                analysis = await self._analyze_need_response(
                    response,
                    prompt['context']
                )
            elif prompt['type'] == 'intent':
                analysis = await self._analyze_intent_response(
                    response,
                    prompt['context']
                )
                
            return {
                'prompt': prompt,
                'response': response,
                'analysis': analysis,
                'timestamp': datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل الرد: {str(e)}")
            return {}
            
    async def _analyze_emotion_response(
        self,
        response: str,
        context: Dict
    ) -> Dict:
        """تحليل رد المشاعر"""
        try:
            prompt = f"""
            تحليل المشاعر في الرد:
            الرد: {response}
            السياق: {context}
            
            قم بتحليل المشاعر الرئيسية وتقديم درجة لكل شعور.
            """
            
            llm_response = await self.llm_service.analyze_context(prompt)
            
            return {
                'emotions': self._parse_emotion_scores(llm_response),
                'context': context
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل رد المشاعر: {str(e)}")
            return {}
            
    async def _analyze_trait_response(
        self,
        response: str,
        context: Dict
    ) -> Dict:
        """تحليل رد السمات"""
        try:
            prompt = f"""
            تحليل السمات في الرد:
            الرد: {response}
            السياق: {context}
            
            قم بتحليل السمات الرئيسية وتقديم درجة لكل سمة.
            """
            
            llm_response = await self.llm_service.analyze_context(prompt)
            
            return {
                'traits': self._parse_trait_scores(llm_response),
                'context': context
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل رد السمات: {str(e)}")
            return {}
            
    async def _analyze_need_response(
        self,
        response: str,
        context: Dict
    ) -> Dict:
        """تحليل رد الاحتياجات"""
        try:
            prompt = f"""
            تحليل الاحتياجات في الرد:
            الرد: {response}
            السياق: {context}
            
            قم بتحليل الاحتياجات الرئيسية وتقديم درجة لكل حاجة.
            """
            
            llm_response = await self.llm_service.analyze_context(prompt)
            
            return {
                'needs': self._parse_need_scores(llm_response),
                'context': context
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل رد الاحتياجات: {str(e)}")
            return {}
            
    async def _analyze_intent_response(
        self,
        response: str,
        context: Dict
    ) -> Dict:
        """تحليل رد النوايا"""
        try:
            prompt = f"""
            تحليل النوايا في الرد:
            الرد: {response}
            السياق: {context}
            
            قم بتحليل النوايا الرئيسية وتقديم درجة لكل نية.
            """
            
            llm_response = await self.llm_service.analyze_context(prompt)
            
            return {
                'intents': self._parse_intent_scores(llm_response),
                'context': context
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل رد النوايا: {str(e)}")
            return {}
            
    def _parse_topics(self, response: str) -> List[str]:
        """تحليل المواضيع"""
        try:
            # TODO: تنفيذ تحليل الاستجابة
            return []
            
        except Exception as e:
            logger.error(f"خطأ في تحليل المواضيع: {str(e)}")
            return []
            
    def _parse_situations(self, response: str) -> List[str]:
        """تحليل المواقف"""
        try:
            # TODO: تنفيذ تحليل الاستجابة
            return []
            
        except Exception as e:
            logger.error(f"خطأ في تحليل المواقف: {str(e)}")
            return []
            
    def _parse_domains(self, response: str) -> List[str]:
        """تحليل المجالات"""
        try:
            # TODO: تنفيذ تحليل الاستجابة
            return []
            
        except Exception as e:
            logger.error(f"خطأ في تحليل المجالات: {str(e)}")
            return []
            
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
