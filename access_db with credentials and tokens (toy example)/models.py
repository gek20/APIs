from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()  # factory function that constructs a base class for declarative class


class User(Base):  # define the table structure
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))

    def hash_password(self, password):
        '''
        :param password: password we want to encript
        '''
        self.password_hash = pwd_context.encrypt(password)  # we are saving the hash, not the password

    def verify_password(self, password):
        '''
        :param password: password
        :return: we want to verify the password using the hash
        '''
        return pwd_context.verify(password, self.password_hash)


class Object(Base):
    __tablename__ = 'object'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    quantity = Column(String)
    price = Column(String)

    @property
    def serialize(self):
        '''
        :return: object data in serializeable format
        '''
        return {
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'price': self.price
        }


engine = create_engine('sqlite:///database_2.db?check_same_thread=False')

Base.metadata.create_all(engine)
