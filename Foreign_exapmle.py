#encoding=utf8
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String,ForeignKey, or_,func,desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
import time
engine = create_engine('mysql+pymysql://root:weelin@10.10.32.83:3306/sqlalchemytest?charset=utf8', echo=False)#echo=True日志
Base = declarative_base()#生成orm基类


class Author(Base):
    """一个作者多本书"""

    __tablename__ = 'author'
    id = Column(Integer,primary_key=True)
    name = Column(String(32))

    def __repr__(self):
        return "<Author_obj:name=%s, author_id=%s>"%(self.name, self.id)


class Book(Base):
    """一本书一名作者"""

    __tablename__='book'
    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    author_id = Column(Integer,ForeignKey('author.id'))
    author = relationship('Author',backref = backref('books',order_by=id))

    def __repr__(self):
        return "<User_obj:name='%s',author_id=%s>"%(self.name,self.author_id)


# Base.metadata.create_all(engine)
Session_class = sessionmaker(bind=engine)##创建与数据库的会话session class
Session = Session_class()#生成Session_class实例

# ---------------------------------add author

# authors = [Author(name='沉川'),Author(name='怪灾'),Author(name='上燃'),Author(name='故乡月')]
#
# try:
#     for author in authors:
#         Session.add(author)
#     Session.commit()
# except:
#     print('rollback..')
#     Session.rollback()

'''
+----+-----------+
| id | name      |
+----+-----------+
|  1 | 沉川      |
|  2 | 怪灾      |
|  3 | 上燃      |
|  4 | 故乡月    |
+----+-----------+

'''

print(Session.query(Author).all())
#[<Author_obj:name=沉川, author_id=1>, <Author_obj:name=怪灾, author_id=2>, <Author_obj:name=上燃, author_id=3>, <Author_obj:name=故乡月, author_id=4>]

print(Session.query(Author).filter(Author.name == '沉川').all())
#[<Author_obj:name=沉川, author_id=1>]

print(Session.query(Author).filter(Author.name != '沉川').all())
#[<Author_obj:name=怪灾, author_id=2>, <Author_obj:name=上燃, author_id=3>, <Author_obj:name=故乡月, author_id=4>]

print(Session.query(Author).filter(Author.name == '沉川').first())
#<Author_obj:name=沉川, author_id=1>

print(Session.query(Author).filter(Author.name.like('故%')).all())
#[<Author_obj:name=故乡月, author_id=4>]

print(Session.query(Author).filter(Author.name.like('%月')).all())
#[<Author_obj:name=故乡月, author_id=4>]

print(Session.query(Author).filter_by(name = '沉川').all())
#[<Author_obj:name=沉川, author_id=1>]

print(Session.query(Author).filter(Author.name != '沉川',Author.id == 2).all())
#[<Author_obj:name=怪灾, author_id=2>]

print(Session.query(Author).filter(Author.name != '沉川').filter(Author.id == 2).all())
#[<Author_obj:name=怪灾, author_id=2>]

print(Session.query(Author).filter(Author.name != '沉川',Author.id > 2).all())
#[<Author_obj:name=上燃, author_id=3>, <Author_obj:name=故乡月, author_id=4>]


print(Session.query(Author).filter(or_(Author.name == '沉川',Author.id > 3)).all())
#[<Author_obj:name=沉川, author_id=1>, <Author_obj:name=故乡月, author_id=4>]




# ---------------------------------add books

# books = [Book(name='老成的北漂故事', author_id=1),
#          Book(name='明代县令', author_id=1),
#          Book(name='龙梦记', author_id=2),
#          Book(name='孤剑玄刀诀', author_id=3),
#          Book(name='孤剑玄刀诀', author_id=3),
#          Book(name='孤剑玄刀诀', author_id=4),
#          Book(name='女友是个特警', author_id=4)
#          ]
#
# try:
#     for book in books:
#         Session.add(book)
#     Session.commit()
# except:
#     print('rollback..')
#     Session.rollback()

'''
+----+-----------------------+-----------+
| id | name                  | author_id |
+----+-----------------------+-----------+
|  1 | 老成的北漂故事        |         1 |
|  2 | 明代县令              |         1 |
|  3 | 龙梦记                |         2 |
|  4 | 孤剑玄刀诀            |         3 |
|  5 | 武林修罗            |         3 |
|  6 | 超能战士在校园            |         4 |
|  7 | 女友是个特警          |         4 |
+----+-----------------------+-----------+
'''

print(Session.query(Book).first())
# <User_obj:name='老成的北漂故事',author_id=1>

book_obj = Session.query(Book).filter(Book.author_id == 1).first()
author_obj = Session.query(Author).filter(Author.name == '上燃').first()

print(book_obj,book_obj.name,book_obj.author_id,book_obj.author)
# <User_obj:name='老成的北漂故事',author_id=1> 老成的北漂故事 1 <Author_obj:name=沉川, author_id=1>

print(author_obj.name,author_obj.books)
# 上燃 [<User_obj:name='孤剑玄刀诀',author_id=3>, <User_obj:name='武林修罗',author_id=3>]

book_obj = Session.query(Book.name,Book.author_id).filter(Book.author_id == 1).first()
print(book_obj,book_obj[0])
# ('老成的北漂故事', 1) 老成的北漂故事

print(Session.query(Book).order_by(Book.id).all())
# [<User_obj:name='老成的北漂故事',author_id=1>, <User_obj:name='明代县令',author_id=1>, <User_obj:name='龙梦记',author_id=2>, <User_obj:name='孤剑玄刀诀',author_id=3>, <User_obj:name='武林修罗',author_id=3>, <User_obj:name='超能战士在校园',author_id=4>, <User_obj:name='女友是个特警',author_id=4>]

#print(Session.query(Book).order_by(desc(Book.id)).all())

print(Session.query(Book).filter(Book.id.in_([1,2,3])).all())
# [<User_obj:name='老成的北漂故事',author_id=1>, <User_obj:name='明代县令',author_id=1>, <User_obj:name='龙梦记',author_id=2>]

print(Session.query(func.count(Book.author_id),Book.author_id).group_by(Book.author_id).all())
# [(2, 1), (1, 2), (3, 3), (2, 4)]

print(Session.query(func.count(Book.name),Book.name).group_by(Book.name).all())
# [(1, '女友是个特警'), (1, '孤剑玄刀诀'), (1, '明代县令'), (1, '武林修罗'), (1, '老成的北漂故事'), (1, '超能战士在校园'), (1, '龙梦记')]

#创建关联对象

# author_obj.books.append(Book(name='组织豪杰去抗日'))
#
# Session.commit()

Session.query(Book).filter_by(name='组织豪杰去抗日').first().author_id=3
Session.commit()



# obj = User(name='fff',password='fff6')
# Session.add(obj)
# print dir(Session.execute('show databases'))
# sql = "insert into user (name,password) values('fff','fff6')"
# Session.execute(sql)

# print Session.execute('select * from user').fetchall()
#生成需要创建的数据对象
# user_obj = User(name='zhangweijian',password='zhangweijian123')
# print user_obj.id,user_obj.name,user_obj.password

#把要创建的数据对象添加到这个session里， 一会统一创建
# Session.add(user_obj)
# print user_obj.id,user_obj.name,user_obj.password
# Session.add(user_obj)
# print user_obj.id,user_obj.name,user_obj.password
#
# obj = Session.query(User).filter_by(name='zhangweijian').first()
#
# print user_obj.id,user_obj.name,user_obj.password
#现此才统一提交，创建数据
# Session.commit()

#print user_obj.id,user_obj.name,user_obj.password


# print u'#查询'
# my_user = Session.query(User).filter_by(id=2).first()
# print my_user.id,my_user.name,my_user.password
#
# my_user = Session.query(User).filter(User.id==2)[0]
# print my_user.id,my_user.name,my_user.password
# print my_user
#
# print u'#修改'
#
# my_user.name = 'zwj1'
#
# Session.commit()

# print u'#回滚'
# my_user = Session.query(User).filter(User.id==9)[0]
# print my_user
# my_user.name='fuck1'
# print my_user
# Session.rollback()
# print my_user

# new_user = User(name='newname',password='newpwd')
# Session.add(new_user)


# print u'#获得所有数据'
# print Session.query(User).all()
#
# print u'#删除某条数据'


# delete_user = User(name='dele',password='delepwd')
#添加
# Session.add(delete_user)
#检查
# print Session.query(User).filter_by(name='dele').first()

#删除
# Session.delete(Session.query(User).filter_by(name='Tom').first())

#检查
# print Session.query(User).filter_by(name='dele').first()




#
# user_obj = User(name='zhangweijian1',password='zhangweijian1234')
# Session.add(user_obj)
# Session.commit()


#delete
# obj = Session.query(User).filter_by(id=50).first()
# print obj
# Session.delete(obj)

# Session.rollback()
# print 'sleep'
#
# print Session.query(User.password).filter().all()

# print User.query.filter_by(id=50)[0]