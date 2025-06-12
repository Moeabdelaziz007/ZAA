"""
سكربت لإنشاء بيانات تجريبية في قاعدة البيانات
"""
import asyncio
import random
from datetime import datetime, timedelta
from typing import List, Dict

from sqlalchemy.orm import Session
from faker import Faker

from core.database import SessionLocal
from api.models.user import User
from api.models.item import Item
from api.models.interaction import Interaction
from api.models.preference import Preference
from core.security import get_password_hash

fake = Faker('ar_SA')

async def create_test_users(db: Session, count: int = 50) -> List[User]:
    """إنشاء مستخدمين تجريبيين"""
    users = []
    for _ in range(count):
        user = User(
            email=fake.email(),
            hashed_password=get_password_hash("test123"),
            full_name=fake.name(),
            is_active=True,
            is_admin=random.random() < 0.1,  # 10% من المستخدمين هم مدراء
            created_at=fake.date_time_between(start_date="-1y"),
        )
        db.add(user)
        users.append(user)
    
    await db.commit()
    return users

async def create_test_items(db: Session, count: int = 200) -> List[Item]:
    """إنشاء عناصر تجريبية"""
    categories = ["تكنولوجيا", "رياضة", "فن", "تعليم", "ترفيه", "صحة", "سفر"]
    items = []
    
    for _ in range(count):
        item = Item(
            title=fake.sentence(),
            description=fake.paragraph(),
            category=random.choice(categories),
            image_url=fake.image_url(),
            price=random.randint(10, 1000),
            rating=round(random.uniform(1, 5), 1),
            created_at=fake.date_time_between(start_date="-1y"),
        )
        db.add(item)
        items.append(item)
    
    await db.commit()
    return items

async def create_test_interactions(
    db: Session,
    users: List[User],
    items: List[Item],
    count: int = 1000
) -> List[Interaction]:
    """إنشاء تفاعلات تجريبية"""
    interaction_types = ["view", "like", "purchase", "share"]
    interactions = []
    
    for _ in range(count):
        user = random.choice(users)
        item = random.choice(items)
        
        interaction = Interaction(
            user_id=user.id,
            item_id=item.id,
            interaction_type=random.choice(interaction_types),
            created_at=fake.date_time_between(
                start_date=user.created_at,
                end_date=datetime.now()
            ),
        )
        db.add(interaction)
        interactions.append(interaction)
    
    await db.commit()
    return interactions

async def create_test_preferences(
    db: Session,
    users: List[User],
    categories: List[str]
) -> List[Preference]:
    """إنشاء تفضيلات تجريبية"""
    preferences = []
    
    for user in users:
        # كل مستخدم يختار 2-4 فئات مفضلة
        user_categories = random.sample(categories, random.randint(2, 4))
        
        for category in user_categories:
            preference = Preference(
                user_id=user.id,
                category=category,
                weight=random.uniform(0.1, 1.0),
                created_at=fake.date_time_between(start_date=user.created_at),
            )
            db.add(preference)
            preferences.append(preference)
    
    await db.commit()
    return preferences

async def seed_database():
    """الوظيفة الرئيسية لإنشاء البيانات التجريبية"""
    db = SessionLocal()
    try:
        print("بدء إنشاء البيانات التجريبية...")
        
        # إنشاء المستخدمين
        print("إنشاء المستخدمين...")
        users = await create_test_users(db)
        print(f"تم إنشاء {len(users)} مستخدم")
        
        # إنشاء العناصر
        print("إنشاء العناصر...")
        items = await create_test_items(db)
        print(f"تم إنشاء {len(items)} عنصر")
        
        # إنشاء التفاعلات
        print("إنشاء التفاعلات...")
        interactions = await create_test_interactions(db, users, items)
        print(f"تم إنشاء {len(interactions)} تفاعل")
        
        # إنشاء التفضيلات
        print("إنشاء التفضيلات...")
        categories = ["تكنولوجيا", "رياضة", "فن", "تعليم", "ترفيه", "صحة", "سفر"]
        preferences = await create_test_preferences(db, users, categories)
        print(f"تم إنشاء {len(preferences)} تفضيل")
        
        print("تم إنشاء البيانات التجريبية بنجاح!")
        
    except Exception as e:
        print(f"حدث خطأ أثناء إنشاء البيانات التجريبية: {str(e)}")
        await db.rollback()
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(seed_database()) 