from fastapi import HTTPException, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from . import models, schemas

def add_item(item, session:Session):
  try:
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
  except:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not save a record")
  

def delete_item(item, session: Session) -> None:
  try:
    session.delete(item)
    session.commit()
  except:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Couldn't delete record from database")


def does_user_exist(potential_user: schemas.UserCreate, session: Session) -> None:

  queried_user = session.query(models.User).filter(or_(models.User.name==potential_user.name, models.User.email==potential_user.email)).first()

  if queried_user:
    message = ""
    if queried_user.name == potential_user.name:
        message += "Username already in use."
    if queried_user.email == potential_user.email:
        message += "Email already in use." if len(message)==0 else " Email already in use."
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message)
  
def find_item(attribute:str, current_user: schemas.User, database_model , session: Session):
  value = getattr(current_user, attribute)
  db_item = session.query(database_model).filter(getattr(database_model,attribute)==value).first()
  if not db_item:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
  return db_item
  
def is_name_email_available(updated_user:schemas.UserUpdate, current_user: schemas.User, session:Session) -> None:
  queried = session.query(models.User).filter(and_(models.User.name==updated_user.name, models.User.id!=current_user.id)).first()
  if queried:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User name already in use")
  
  queried = session.query(models.User).filter(and_(models.User.email==updated_user.email, models.User.id!=current_user.id)).first()
  if queried:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use") 


def update_item(new_item, past_item, session: Session):
  try:
    for attr,value in new_item.__dict__.items():
      if attr != 'id':
        setattr(past_item, attr,value)
        print(attr,value)
    print("commit")
    session.commit()
    print("refresh")
    session.refresh(past_item)
    return past_item
  except Exception as e:
    print("update error: ",e)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update record.")
  

    
  