import os
import random
from datetime import date, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.join(os.path.dirname(__file__))
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    location = Column(String(50))

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    hire_date = Column(Date, nullable=False)
    job_title = Column(String(50))

class Salary(Base):
    __tablename__ = 'salaries'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    amount = Column(Float, nullable=False)
    effective_date = Column(Date, nullable=False)

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    budget = Column(Float)
    department_id = Column(Integer, ForeignKey('departments.id'))

class LeaveRequest(Base):
    __tablename__ = 'leave_requests'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(20))

def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    departments = []
    for d_data in DEPARTMENTS:
        d = Department(name=d_data["name"], location=d_data["location"])
        departments.append(d)
    session.add_all(departments)
    session.commit()

    employees = []
    for i in range(10):
        e = Employee(
            name=EMPLOYEE_NAMES[i], 
            department_id=random.choice(departments).id, 
            hire_date=date(2020, 1, 1) + timedelta(days=random.randint(0, 1000)), 
            job_title=random.choice(JOB_TITLES)
        )
        employees.append(e)
    session.add_all(employees)
    session.commit()

    salaries = []
    for i in range(10):
        s = Salary(
            employee_id=employees[i].id, 
            amount=round(random.uniform(50000, 150000), 2), 
            effective_date=date(2023, 1, 1)
        )
        salaries.append(s)
    session.add_all(salaries)

    projects = []
    for name in PROJECT_NAMES:
        p = Project(
            name=name, 
            budget=round(random.uniform(10000, 500000), 2), 
            department_id=random.choice(departments).id
        )
        projects.append(p)
    session.add_all(projects)

    leaves = []
    for i in range(10):
        start = date(2024, 1, 1) + timedelta(days=random.randint(0, 300))
        lr = LeaveRequest(
            employee_id=random.choice(employees).id, 
            start_date=start, 
            end_date=start + timedelta(days=random.randint(1, 14)), 
            status=random.choice(['Approved', 'Pending', 'Rejected'])
        )
        leaves.append(lr)
    session.add_all(leaves)
    
    session.commit()
    print("Database dropped, recreated, and seeded successfully with proper names.")
    session.close()

if __name__ == '__main__':
    init_db()
