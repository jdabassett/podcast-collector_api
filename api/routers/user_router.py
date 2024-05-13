from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import List

from .. import database, database_operations, hashing, models, oauth2, schemas

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/create/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(potential_user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
      database_operations.does_user_exist(potential_user, db)
    except:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Either name or email is already in use")
    
    try:
      hashed_password = hashing.Hash.bcrypt(potential_user.password)
      hashed_user = models.User(name=potential_user.name, email=potential_user.email, password=hashed_password)
    except:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create hashed password or new user record")
                                
    try:
      new_user = database_operations.add_item(hashed_user, db)
    except:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not save record")

    return schemas.User(name=new_user.name, email=new_user.email, id=new_user.id, podcasts=new_user.podcasts)

@router.get("/read/", status_code= status.HTTP_200_OK, response_model=schemas.User)
def read_user(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  try:
    user = database_operations.find_item("id", current_user, models.User, db)
    return schemas.User(name=user.name, email=user.email, id=user.id, podcasts=user.podcasts)
  except Exception:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found") 


@router.put("/update/", status_code= status.HTTP_201_CREATED, response_model=schemas.Response)
def update_user(request: schemas.UserUpdate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

  try:
    database_operations.is_name_email_available(request, current_user, db)
  except:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Either name or email is already in use")

  keys = ["name", "email","password", "id", "playlist"]
  if len([key for key in request.dict().keys() if key in keys])==0:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update must contain at least one attribute to update.")

  try:
    current = database_operations.update_item(request, current_user, db)
  except:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update record.")
  
  return schemas.Response(detail=f"User record {current.id} successfully updated.")


@router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  try:
    database_operations.delete_item(current_user, db)
  except:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Couldn't delete record from database")
  
  return schemas.Response(detail=f"User record successfully deleted.")
