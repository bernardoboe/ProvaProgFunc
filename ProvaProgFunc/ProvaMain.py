from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
import datetime

app = FastAPI()

engine = create_engine('mysql://root:root@localhost:3306/provapf')

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = sessionLocal()

Base = declarative_base()

class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(100))

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('job.id', ondelete='CASCADE'))
    name = Column(String(250))
    birth_date = Column(String(50))
    salary = Column(Float)
    department = Column(String(50))

class JobHistory(Base):
    __tablename__ = 'job_history'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id', ondelete='CASCADE'))
    title = Column(String(50))
    start_date = Column(String(50))
    end_date = Column(String(50))
    salary = Column(Float)
    Job = Column(String(50))

Base.metadata.create_all(bind=engine)

@app.get("/job")
def get_jobs():
    jobs = session.query(Job).all()
    Job_list = []
    for job in jobs:
        Job_dict = {'id': job.id, 'name':job.name, 'age': job.description}
        Job_list.append(Job_dict)

    return JSONResponse(content=Job_list)

@app.post("/job")
def create_job(name: str, description: str):
    job = Job(name=name, description=description)
    session.add(job)
    session.commit()
    return JSONResponse(content={'id': job.id, 'name': job.name, 'description': job.description})

@app.get("/job/{id}")
def get_job(id: int):
    job = session.query(Job).filter(Job.id == id).first()
    employees = session.query(Employee).filter(Employee.job_id == id).all()
    list = []
    for employee in employees:
        jobhistory = session.query(JobHistory).filter(JobHistory.employee_id == employee.id).all()
        list2 = []
        for jobh in jobhistory:
            job_dict = {'id': jobh.id, 'employee_id': jobh.employee_id, 'title': jobh.title, 'start_date': jobh.start_date, 'end_date': jobh.end_date, 'salary': jobh.salary, 'Job': jobh.Job}
            list2.append(job_dict)
        employee_dict = {'id': employee.id, 'job_id':employee.job_id, 'name':employee.name, 'birth_date':employee.birth_date, 'salary':employee.salary, 'department':employee.department, 'JobHistory': list2}
        list.append(employee_dict)
    return JSONResponse(content={'id': job.id, 'name': job.name, 'description': job.description, 'Employee': list})

@app.put("/job/{id}")
def update_job(id: int, name: str, description: str):
    job = session.query(Job).filter(Job.id == id).first()
    job.name = name
    job.description = description
    session.commit()
    return JSONResponse(content={'id': job.id, 'name': job.name, 'description': job.description})

@app.delete("/job/{id}")
def delete_job(id: int):
    job = session.query(Job).filter(Job.id == id).first()
    session.delete(job)
    session.commit()
    return JSONResponse(content={'message': 'Job deleted'})

@app.get("/employee")
def get_employees():
    employees = session.query(Employee).all()

    Employee_list = []

    for employee in employees:
        Employee_dict = {'id': employee.id, 'job_id':employee.job_id, 'name':employee.name, 'birth_date':employee.birth_date, 'salary':employee.salary, 'department':employee.department}
        Employee_list.append(Employee_dict)

    return JSONResponse(content=Employee_list)

@app.post("/employee")
def create_employee(job_id: int, name: str, birth_date: str, salary: float, department: str):
    employee = Employee(job_id=job_id, name=name, birth_date=birth_date, salary=salary, department=department)
    session.add(employee)
    session.commit()
    return JSONResponse(content={'id': employee.id, 'job_id': employee.job_id, 'name': employee.name, 'birth_date': employee.birth_date, 'salary': employee.salary, 'department': employee.department})

@app.get("/employee/{id}")
def get_employee(id: int):
    employee = session.query(Employee).filter(Employee.id == id).first()
    jobhistory = session.query(JobHistory).filter(JobHistory.employee_id == id).all()
    list = []
    for job in jobhistory:
        job_dict = {'id': job.id, 'employee_id': job.employee_id, 'title': job.title, 'start_date': job.start_date, 'end_date': job.end_date, 'salary': job.salary, 'Job': job.Job}
        list.append(job_dict)
    return JSONResponse(content={'id': employee.id, 'job_id': employee.job_id, 'name': employee.name, 'birth_date': employee.birth_date, 'salary': employee.salary, 'department': employee.department, 'JobHistory': list})

    return JSONResponse(content=list)
@app.put("/employee/{id}")
def update_employee(id: int, job_id: int, name: str, birth_date: str, salary: float, department: str):
    employee = session.query(Employee).filter(Employee.id == id).first()
    employee.job_id = job_id
    employee.name = name
    employee.birth_date = birth_date
    employee.salary = salary
    employee.department = department
    session.commit()
    return JSONResponse(content={'id': employee.id, 'job_id': employee.job_id, 'name': employee.name, 'birth_date': employee.birth_date, 'salary': employee.salary, 'department': employee.department})

@app.delete("/employee/{id}")
def delete_employee(id: int):
    employee = session.query(Employee).filter(Employee.id == id).first()
    session.delete(employee)
    session.commit()
    return JSONResponse(content={'message': 'Employee deleted'})

@app.get("/job_history")
def get_job_history():
    job_history = session.query(JobHistory).all()

    JobHistory_list = []

    for jobhistory in job_history:
        JobHistory_dict = {'id': jobhistory.id, 'employee_id':jobhistory.employee_id, 'title':jobhistory.title, 'start_date':jobhistory.start_date, 'end_date':jobhistory.end_date, 'salary':jobhistory.salary, 'Job':jobhistory.Job}
        JobHistory_list.append(JobHistory_dict)

    return JSONResponse(content=JobHistory_list)

@app.post("/job_history")
def create_job_history(employee_id: int, title: str, start_date: str, end_date: str, salary: float, Job: str):
    job_history = JobHistory(employee_id=employee_id, title=title, start_date=start_date, end_date=end_date, salary=salary, Job=Job)
    session.add(job_history)
    session.commit()
    return JSONResponse(content={'id': job_history.id, 'employee_id': job_history.employee_id, 'title': job_history.title, 'start_date': job_history.start_date, 'end_date': job_history.end_date, 'salary': job_history.salary, 'Job': job_history.Job})

@app.get("/job_history/{id}")
def get_job_history(id: int):
    job_history = session.query(JobHistory).filter(JobHistory.id == id).first()
    return JSONResponse(content={'id': job_history.id, 'employee_id': job_history.employee_id, 'title': job_history.title, 'start_date': job_history.start_date, 'end_date': job_history.end_date, 'salary': job_history.salary, 'Job': job_history.Job})

@app.put("/job_history/{id}")
def update_job_history(id: int, employee_id: int, title: str, start_date: str, end_date: str, salary: float, Job: str):
    job_history = session.query(JobHistory).filter(JobHistory.id == id).first()
    job_history.employee_id = employee_id
    job_history.title = title
    job_history.start_date = start_date
    job_history.end_date = end_date
    job_history.salary = salary
    job_history.Job = Job
    session.commit()
    return JSONResponse(content={'id': job_history.id, 'employee_id': job_history.employee_id, 'title': job_history.title, 'start_date': job_history.start_date, 'end_date': job_history.end_date, 'salary': job_history.salary, 'Job': job_history.Job})

@app.delete("/job_history/{id}")
def delete_job_history(id: int):
    job_history = session.query(JobHistory).filter(JobHistory.id == id).first()
    session.delete(job_history)
    session.commit()
    return JSONResponse(content={'message': 'Job History deleted'})