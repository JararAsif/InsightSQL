import os
from datetime import date
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
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    if session.query(Department).count() == 0:
        d1 = Department(name='Engineering', location='New York')
        d2 = Department(name='Sales', location='Chicago')
        d3 = Department(name='HR', location='New York')
        session.add_all([d1, d2, d3])
        session.commit()
        
        e1 = Employee(name='Alice Smith', department_id=d1.id, hire_date=date(2021, 5, 12), job_title='Senior Engineer')
        e2 = Employee(name='Bob Jones', department_id=d2.id, hire_date=date(2022, 10, 1), job_title='Sales Lead')
        e3 = Employee(name='Charlie Brown', department_id=d1.id, hire_date=date(2023, 1, 15), job_title='Software Engineer')
        e4 = Employee(name='Diana Prince', department_id=d3.id, hire_date=date(2020, 3, 10), job_title='HR Manager')
        e5 = Employee(name='Evan Davis', department_id=d2.id, hire_date=date(2024, 2, 20), job_title='Sales Rep')
        session.add_all([e1, e2, e3, e4, e5])
        session.commit()
        
        session.add_all([
            Salary(employee_id=e1.id, amount=120000, effective_date=date(2021, 5, 12)),
            Salary(employee_id=e2.id, amount=95000, effective_date=date(2022, 10, 1)),
            Salary(employee_id=e3.id, amount=85000, effective_date=date(2023, 1, 15)),
            Salary(employee_id=e4.id, amount=105000, effective_date=date(2020, 3, 10)),
            Salary(employee_id=e5.id, amount=65000, effective_date=date(2024, 2, 20)),
        ])
        session.add_all([
            Project(name='AI Migration', budget=500000, department_id=d1.id),
            Project(name='Q3 Expansion', budget=150000, department_id=d2.id),
            Project(name='Employee Wellness', budget=50000, department_id=d3.id),
        ])

        session.add_all([
            LeaveRequest(employee_id=e1.id, start_date=date(2023, 12, 20), end_date=date(2023, 12, 31), status='Approved'),
            LeaveRequest(employee_id=e3.id, start_date=date(2024, 6, 1), end_date=date(2024, 6, 10), status='Pending'),
        ])
        
        session.commit()
        print("Database initialized with sample data successfully.")
    else:
        print("Database already contains data. Skipping initialization.")
        
    session.close()

if __name__ == '__main__':
    init_db()
