import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from lightfm import LightFM
from lightfm.data import Dataset
from typing import List, Dict, Any, Tuple
import pandas as pd
from datetime import datetime, timedelta

class HybridRecommender:
    def __init__(self):
        self.content_model = None
        self.collaborative_model = None
        self.dataset = Dataset()
        self.item_features = None
        self.user_features = None
        
    def prepare_data(self, interactions: List[Dict], items: List[Dict], users: List[Dict]):
        """تحضير البيانات للتدريب"""
        # تحويل التفاعلات إلى مصفوفة
        interactions_df = pd.DataFrame(interactions)
        
        # تحضير ميزات العناصر
        item_features = []
        for item in items:
            features = {
                'title': item['title'],
                'description': item['description'],
                'category': item['category']
            }
            features.update(item.get('features', {}))
            item_features.append(features)
            
        # تحضير ميزات المستخدمين
        user_features = []
        for user in users:
            features = {
                'preferences': user.get('preferences', {}),
                'behavior': user.get('behavior_data', {})
            }
            user_features.append(features)
            
        # تحضير البيانات للـ LightFM
        self.dataset.fit(
            users=[str(u['id']) for u in users],
            items=[str(i['id']) for i in items],
            item_features=[list(f.values()) for f in item_features],
            user_features=[list(f.values()) for f in user_features]
        )
        
        # تحويل التفاعلات إلى تنسيق LightFM
        interactions_matrix, weights = self.dataset.build_interactions(
            ((str(i['user_id']), str(i['item_id']), i['interaction_value'])
             for i in interactions)
        )
        
        return interactions_matrix, weights, item_features, user_features
    
    def train_models(self, interactions_matrix, weights, item_features, user_features):
        """تدريب نماذج التوصيات"""
        # تدريب نموذج التعاوني
        self.collaborative_model = LightFM(loss='warp')
        self.collaborative_model.fit(
            interactions_matrix,
            item_features=self.dataset.build_item_features(item_features),
            user_features=self.dataset.build_user_features(user_features),
            sample_weight=weights,
            epochs=30
        )
        
        # تدريب نموذج المحتوى
        item_texts = [' '.join(str(v) for v in f.values()) for f in item_features]
        self.content_model = TfidfVectorizer()
        self.item_features = self.content_model.fit_transform(item_texts)
    
    def get_recommendations(self, user_id: int, n_recommendations: int = 10) -> List[Dict]:
        """الحصول على توصيات للمستخدم"""
        # الحصول على التوصيات من النموذج التعاوني
        collab_scores = self.collaborative_model.predict(
            user_ids=[str(user_id)],
            item_ids=[str(i) for i in range(len(self.item_features))],
            item_features=self.item_features,
            user_features=self.user_features
        )[0]
        
        # الحصول على التوصيات من نموذج المحتوى
        user_interactions = self.get_user_interactions(user_id)
        if user_interactions:
            content_scores = self.get_content_based_scores(user_interactions)
        else:
            content_scores = np.zeros(len(self.item_features))
        
        # دمج التوصيات
        final_scores = 0.7 * collab_scores + 0.3 * content_scores
        
        # ترتيب التوصيات
        top_items = np.argsort(-final_scores)[:n_recommendations]
        
        recommendations = []
        for item_id in top_items:
            recommendations.append({
                'item_id': int(item_id),
                'score': float(final_scores[item_id]),
                'algorithm': 'hybrid'
            })
        
        return recommendations
    
    def get_content_based_scores(self, user_interactions: List[Dict]) -> np.ndarray:
        """الحصول على توصيات قائمة على المحتوى"""
        # تحويل تفاعلات المستخدم إلى نصوص
        user_texts = [' '.join(str(v) for v in i.values()) for i in user_interactions]
        user_features = self.content_model.transform(user_texts)
        
        # حساب التشابه
        similarities = cosine_similarity(user_features, self.item_features)
        return np.mean(similarities, axis=0)
    
    def get_user_interactions(self, user_id: int) -> List[Dict]:
        """الحصول على تفاعلات المستخدم الأخيرة"""
        # هنا يجب تنفيذ استعلام قاعدة البيانات للحصول على تفاعلات المستخدم
        # هذا مثال بسيط
        return []
    
    def update_recommendations(self, new_interaction: Dict):
        """تحديث التوصيات بناءً على تفاعل جديد"""
        # تحديث البيانات
        # إعادة تدريب النماذج إذا لزم الأمر
        pass 