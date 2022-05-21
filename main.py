from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
import uvicorn

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/")
def root():
    return "addresss"

@app.post("/addresses", response_model=schemas.Address, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.AddressDoCreate, session: Session = Depends(get_session)):

    # create an instance of the Address database model
    tododb = models.Address(location = todo.location,country=todo.country,city=todo.city,zip_code=todo.zip_code
                            ,latitude=todo.latitude,longitude=todo.longitude)

    # add it to the session and commit it
    session.add(tododb)
    session.commit()
    session.refresh(tododb)

    # return the address object
    return tododb

@app.get("/addresses/{id}", response_model=schemas.Address)
def read_todo(id: int, session: Session = Depends(get_session)):

    # get the address item with the given id
    todo = session.query(models.Address).get(id)

    # check if address item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"addresses item with id {id} not found")

    return todo

@app.put("/addresses/{id}", response_model=schemas.Address)
def update_todo(id: int, location: str, session: Session = Depends(get_session)):

    # get the address item with the given id
    todo = session.query(models.Address).get(id)

    # update address item with the given task (if an item with the given id was found)
    if todo:
        todo.location = location
        session.commit()

    # check if address item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"addresses item with id {id} not found")

    return todo

@app.delete("/addresses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, session: Session = Depends(get_session)):

    # get the address item with the given id
    todo = session.query(models.Address).get(id)

    # if address item with given id exists, delete it from the database. Otherwise raise 404 error
    if todo:
        session.delete(todo)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"addresses item with id {id} not found")

    return None

@app.get("/addresses", response_model = List[schemas.Address])
def read_todo_list(session: Session = Depends(get_session)):

    # get all address items
    todo_list = session.query(models.Address).all()

    return todo_list


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000)