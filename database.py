[database.py.txt](https://github.com/user-attachments/files/27851010/database.py.txt)
from sqlalchemy import create_all_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Bazani yaratish (SQLite — eng osoni, fayl ko'rinishida saqlanadi)
engine = create_engine('sqlite:///finflow.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Foydalanuvchilar jadvali
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    balance = Column(Float, default=0.0)

@dp.message()
async def handle_text(message: types.Message):
    parts = message.text.split()
    if len(parts) == 2 and parts[1].isdigit():
        category, amount = parts[0], float(parts[1])
        
        # 1. Foydalanuvchini bazadan topamiz yoki yaratamiz
        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        if not user:
            user = User(telegram_id=message.from_user.id, username=message.from_user.username)
            session.add(user)
            session.commit()

        # 2. Xarajatni bazaga qo'shamiz
        new_expense = Expense(user_id=user.id, amount=amount, category=category)
        session.add(new_expense)
        
        # 3. Balansni kamaytiramiz
        user.balance -= amount
        session.commit()

        await message.answer(f"✅ Saqlandi!\nKategoriya: {category}\nSumma: {amount} so'm\nYangi balans: {user.balance}")
    else:
        await message.answer("Xarajatni mana bu formatda yozing: <i>ovqat 25000</i>", parse_mode="HTML")

# Jadvallarni yaratish buyrug'i
Base.metadata.create_all(engine)
