# import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, or_, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session,sessionmaker

engine = create_engine('mysql+pymysql://root:weelin@10.10.33.229:3306/test?charset=utf8', echo=False) #创建一个连接,echo=True表示打印日志
Base = declarative_base()#生成orm基类


class Info(Base):
    __tablename__='info'
    id = Column(Integer,primary_key=True)
    name = Column(String(30))

    def __repr__(self):
        return "<User_obj:name='%s'>"%(self.name)


#Base.metadata.create_all(engine)  #根据上名定义的Info类创建表info
Session_class = sessionmaker(bind=engine) #创建与数据库的会话session class
Session = Session_class() #生成Session_class实例,用于操作数据库

# 增
#
# info1 = Info(name='newff')
# info2 = Info(name="ffnewff")
# info3 = Info(name="new")
# info4 = Info(name='ffnew')
# #
# Session.add(info1)
# Session.add(info2)
# Session.add(info3)
# Session.commit()

#delete
# objs = Session.query(Info).all()
# for obj in objs:
#     print (obj)
# obj = Session.query(Info).filter_by(id=2).first()
# Session.delete(obj)
# Session.commit()
# objs = Session.query(Info).all()
# for obj in objs:
#     print (obj)

# 改
# obj = Session.query(Info).filter_by(id=3).first()
# obj.name='newname3'
# Session.commit()
# objs = Session.query(Info).all()
# for obj in objs:
#     print (obj)

# 查
obj = Session.query(Info).filter_by(id=3).first()
# obj = Session.query(Info).filter_by(name="newname3").first()
print(obj.id,obj.name,obj)
objs = Session.query(Info).all()
print (len(objs))

for obj in Session.query(Info).all():
    print (obj.name)


print('a')
print(Session.query(Info.name,Info.id).filter(Info.id.in_([1,2,3])).all())


