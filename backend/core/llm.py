from typing import List, Dict, Optional
import openai
from google.cloud import language_v1
from app.core.config import settings
from app.core.logger import logger

class LLMService:
    """خدمة التكامل مع نماذج اللغة"""
    
    def __init__(self):
        self.openai_client = openai.Client(api_key=settings.OPENAI_API_KEY)
        self.gemini_client = language_v1.LanguageServiceClient()
        
    async def analyze_sentiment(self, texts: List[str]) -> str:
        """تحليل المشاعر من النصوص"""
        try:
            # استخدام GPT-4 لتحليل المشاعر
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت محلل مشاعر متخصص. قم بتحليل النصوص وتحديد المشاعر السائدة."},
                    {"role": "user", "content": f"قم بتحليل المشاعر في النصوص التالية: {texts}"}
                ]
            )
            
            sentiment = response.choices[0].message.content
            return sentiment
            
        except Exception as e:
            logger.error(f"خطأ في تحليل المشاعر: {str(e)}")
            return "neutral"
            
    async def analyze_context(self, text: str) -> Dict:
        """تحليل السياق من النص"""
        try:
            # استخدام Gemini لتحليل السياق
            document = language_v1.Document(
                content=text,
                type_=language_v1.Document.Type.PLAIN_TEXT
            )
            
            response = self.gemini_client.analyze_entities(
                document=document,
                encoding_type=language_v1.EncodingType.UTF8
            )
            
            # استخراج الكيانات والسياق
            context = {
                'entities': [entity.name for entity in response.entities],
                'categories': [entity.type_ for entity in response.entities],
                'sentiment': response.document_sentiment.score
            }
            
            return context
            
        except Exception as e:
            logger.error(f"خطأ في تحليل السياق: {str(e)}")
            return {}
            
    async def generate_conversational_recommendation(
        self,
        user_id: int,
        conversation_history: List[Dict],
        user_preferences: Dict
    ) -> Dict:
        """توليد توصية مستندة للمحادثة"""
        try:
            # تحليل تاريخ المحادثة
            context = await self.analyze_context(
                " ".join([msg['content'] for msg in conversation_history])
            )
            
            # توليد التوصية باستخدام GPT-4
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت مساعد توصيات ذكي. قم بتحليل المحادثة وتفضيلات المستخدم لتقديم توصية مناسبة."},
                    {"role": "user", "content": f"""
                    تاريخ المحادثة: {conversation_history}
                    تفضيلات المستخدم: {user_preferences}
                    السياق: {context}
                    
                    قم بتقديم توصية مناسبة بناءً على هذه المعلومات.
                    """}
                ]
            )
            
            recommendation = {
                'content': response.choices[0].message.content,
                'context': context,
                'confidence': response.choices[0].finish_reason == 'stop'
            }
            
            return recommendation
            
        except Exception as e:
            logger.error(f"خطأ في توليد التوصية المحادثة: {str(e)}")
            return {
                'content': "عذراً، حدث خطأ في توليد التوصية.",
                'context': {},
                'confidence': False
            }
            
    async def analyze_user_feedback(self, feedback: str) -> Dict:
        """تحليل ملاحظات المستخدم"""
        try:
            # تحليل الملاحظات باستخدام GPT-4
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت محلل ملاحظات متخصص. قم بتحليل ملاحظات المستخدم واستخراج النقاط الرئيسية."},
                    {"role": "user", "content": f"قم بتحليل الملاحظات التالية: {feedback}"}
                ]
            )
            
            analysis = {
                'summary': response.choices[0].message.content,
                'sentiment': await self.analyze_sentiment([feedback]),
                'key_points': response.choices[0].message.content.split('\n')
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"خطأ في تحليل ملاحظات المستخدم: {str(e)}")
            return {
                'summary': "عذراً، حدث خطأ في تحليل الملاحظات.",
                'sentiment': "neutral",
                'key_points': []
            } 