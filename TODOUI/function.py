from database import DBUser,DBTask,DBTaskHistory,session
from sqlalchemy import update


class Function():

    def user_id(self,user_id):
        fetch_data=session.query(DBUser).filter(DBUser.id==user_id).first()
        return fetch_data
    
#___________________insert data into logininfo table through registration____________
    
    def registration(self,Name,Email,Password):
        insert_data=DBUser(Name=Name,Email=Email,Password=Password)
        session.add(insert_data)
        session.commit()         
        return insert_data
       
#_________________fetching data for login______________________

    def verify_register(self,Name,Email,Password):
        verified_data=session.query(DBUser).filter(DBUser.Password==Password).first()
        # print(verified_data)
        return verified_data
        
    
#___________________ verification for registeration _________________

    def user_login(self,Email,Password):
        fetch_data=session.query(DBUser).filter(DBUser.Email==Email,DBUser.Password==Password).first()
        return fetch_data
    


#________________insert task in todo table_______________
    
    def addtask(self,TaskName,StartDate,StartTime,DueDate):
        insert_task=DBTask(TaskName=TaskName,StartDate=StartDate,StartTime=StartTime,DueDate=DueDate)
        session.add(insert_task)
        session.commit()
        return "task added successfully!!"
    
#_______________fetching task_____________________
    
    def fetchtask(self,ID):
        fetch_data=session.query(DBTask).filter(DBTask.ID==ID)
        if fetch_data:
            task_info=""
            for f in fetch_data:
                ID=f.ID
                TaskName=f.TaskName
                StartDate=f.StartDate
                StartTime=f.StartTime
                DueDate=f.DueDate
                task_info=ID,TaskName,StartDate,StartTime,DueDate
            return task_info
        else:
            return "There is not any data on this ID "
        
#______________ fetch list of all task_______________________
        
    def taskilist(self):
        fetchtask=session.query(DBTask).all()
        task_append=[]
        for f in fetchtask:
            ID=f.ID
            TaskName=f.TaskName
            StartDate=f.StartDate
            StartTime=f.StartTime
            DueDate=f.DueDate
            data=ID,TaskName,StartDate,StartTime,DueDate
            task_append.append(data)
        return task_append
        
        
            
#___________________deleting task___________________________
    
    def DeleteTask(self,ID):
        delete_data=session.query(DBTask).filter(DBTask.ID==ID).first()
        session.delete(delete_data)
        session.commit()
        return "data deleted"
    
    
        
#___________________fetching one task to update___________________________

        
    def fetchonetask(self,ID):
        fetch_data=session.query(DBTask).filter(DBTask.ID==ID)
        
        for f in fetch_data:
        
            ID=f.ID
            TaskName=f.TaskName
            StartDate=f.StartDate
            StartTime=f.StartTime
            DueDate=f.DueDate
            data=ID,TaskName,StartDate,StartTime,DueDate
        return data
    
##___________________updating task___________________________


    def update_task(self, ID, TaskName, StartDate, StartTime, DueDate):
        update_data = update(DBTask).where(DBTask.ID == ID).values(
            ID=ID,
            TaskName=TaskName,
            StartDate=StartDate,
            StartTime=StartTime,
            DueDate=DueDate
        )

        result = session.execute(update_data)
        session.commit()

        return result

#____________making histories of task_____________________
    
    def makehistory(self,ID):
        existing_history = session.query(DBTaskHistory).filter(DBTaskHistory.task_id == ID).first()
        if existing_history:
            
            return "Data Already Exists!"
        
        else:
            fetchone = session.query(DBTask).filter(DBTask.ID == ID).first()
            if fetchone:
                new_task_history = DBTaskHistory(
                    task_id=fetchone.ID,
                    taskname=fetchone.TaskName,
                    startdate=fetchone.StartDate,
                    duedate=fetchone.DueDate
                )
                session.add(new_task_history)
                session.commit()
                return "Data entered"
    
#________________getting task history___________________
    
    def gettaskhistory(self,date):
        exist_date=session.query(DBTaskHistory).filter(DBTaskHistory.startdate==date)
        if exist_date:
            data=""
            for f in exist_date:
                ID=f.task_id
                TaskName=f.taskname
                StartDate=f.startdate
                DueDate=f.duedate
                history_id=f.history_id
                data=ID,TaskName,StartDate,DueDate,history_id
            return data
        else:
            return "On there is not any task assigned"