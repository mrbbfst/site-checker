from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, \
     ForeignKey, event, BigInteger, Boolean, Text, Table
from sqlalchemy.orm import relationship
Base = declarative_base()


bot_site_association = Table(
    'model_site_bot',
    Base.metadata,
    Column('bot_id', Integer, ForeignKey('model_bot.id')),
    Column('site_id', Integer, ForeignKey('model_site.id'))
)

bot_contact_association = Table(
    'model_bot_contacts',
    Base.metadata,
    Column('bot_id', Integer, ForeignKey('model_bot.id')),
    Column('contact_id', Integer, ForeignKey('model_contact.id'))
)

class Bot(Base):
    __tablename__ = 'model_bot'

    id = Column(Integer, primary_key=True)
    label = Column(String(100), nullable=False)
    token = Column(String(255), nullable=False)
    # chat_id = Column(String(255), nullable=False)
    message_pattern = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    contacts = relationship('Contact', secondary=bot_contact_association, lazy=False)


class Site(Base):
    __tablename__ = 'model_site'

    id = Column(Integer, primary_key=True)
    label = Column(String(100), nullable=False)
    url = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    expected_response_code = Column(String(255), nullable=False)
    expected_response_body_pattern = Column(String(255), nullable=False)
    checking_active = Column(Boolean, default=False)
    inverse_conditions = Column(Boolean, default=False)
    # bot_id = Column(Integer, ForeignKey('model_bot.id'))
    cron_schedule = Column(String(255), nullable=False)
    bots = relationship('Bot', secondary=bot_site_association, lazy=False)


class Contact(Base):
    __tablename__ = 'model_contact'

    id = Column(Integer, primary_key=True)
    label = Column(String(100), nullable=False)
    contact_string = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)