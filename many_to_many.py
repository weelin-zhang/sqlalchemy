    # encoding=utf8
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
import time

engine = create_engine('mysql+pymysql://root:weelin@10.10.32.83:3306/sqlalchemytest?charset=utf8',
                       echo=False)  # echo=True日志
Session_class = sessionmaker(bind=engine)  ##创建与数据库的会话session class
Session = Session_class()  # 生成Session_class实例
Base = declarative_base()  # 生成orm基类

student_m_to_m_teacher = Table('student_m_to_m_teacher', Base.metadata,
                               Column('student_id', Integer, ForeignKey('student.id')),
                               Column('teacher_id', Integer, ForeignKey('teacher.id'))
                               )


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    teachers = relationship('Teacher', secondary=student_m_to_m_teacher, backref='students')

    def __repr__(self):
        return "<Student_obj:name='%s'>" % (self.name)


class Teacher(Base):
    __tablename__ = 'teacher'  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(20))

    def __repr__(self):
        return "<Teacher_obj:name='%s'>" % (self.name)


Base.metadata.create_all(engine)  # 创建表结构

Session_class = sessionmaker(bind=engine)

Session = Session_class()

# t1, t2, t3 = [Teacher(name='teach1'), Teacher(name='teach2'), Teacher(name='teach3')]
#
# s1, s2, s3 = [Student(name='stud1'), Student(name='stud2'), Student(name='stud3')]
#
# s1.teachers = [t1, t2]
# s2.teachers = [t1, t2, t3]
# s3.teachers = [t2, t3]
# Session.add_all([t1, t2, t3, s1, s2, s3])
# Session.commit()

print('--------通过书表查关联的作者---------')

teacher_obj = Session.query(Teacher).filter_by(name="teach1").first()
print(teacher_obj.name, teacher_obj.students)

print('--------通过作者表查关联的书---------')
student_obj =Session.query(Student).filter_by(name="stud2").first()
print(student_obj.name , student_obj.teachers)
Session.commit()


print('通过书删除作者')

student_obj = Session.query(Student).filter_by(name="stud2").first()

teacher_obj = Session.query(Teacher).filter_by(name="teach2").first()

# student_obj.teachers.remove(teacher_obj)
# Session.commit()


# print('直接删除作者-删除作者时，会把这个作者跟所有书的关联关系数据也自动删除')
# Session.delete(student_obj)
# Session.commit()


# student_obj = Session.query(Student).filter_by(id=2).first()
# teacher_obj = Session.query(Teacher).filter_by(id=1).first()
#
# student_obj.teachers.append(teacher_obj)
# Session.commit()


student = Student(name='studtest')

# Session.add(student)

teacher = Teacher(name='techtest')

# Session.add(teacher)
s = Session.query(Student).filter_by(name='studtest').first()
t = Session.query(Teacher).filter_by(name='techtest').first()
s.teachers.append(t)

Session.commit()





