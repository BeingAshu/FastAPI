
from fastapi import Depends, FastAPI
from .models import User
from .database import SessionLocal
import frontend.database_models as database_models
from .database import engine
from sqlalchemy.orm import Session


app = FastAPI()


#CORS Configuration
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


database_models.Base.metadata.create_all(bind = engine)


# users = [
#     User(id =1,name="ashutosh",age = "27"),
#     User(id = 2,name = "srujan",age = "19")
# ]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:    
        db.close()

# def init_db():
#     db = SessionLocal()
#     count = db.query(database_models.User).count
#     if count == 0:
#         for user in users:
#             db.add(database_models.User(**user.model_dump()))

#         db.commit()
# init_db()

@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):

    db_users = db.query(database_models.User).all()
    return db_users

@app.get("/user/{id}")
def get_user_by_id(id: int, db: Session =Depends(get_db)):

    db_user = db.query(database_models.User).filter(database_models.User.id == id).first()

    if db_user:
        return db_user
    return "User not found"

@app.post("/user")
def add_user(user: User, db: Session =Depends(get_db)):
    db.add(database_models.User(**user.model_dump(exclude={"id"})))
    db.commit()
    # users.append(user)
    return user

#Update Users
@app.put("/user/{id}")
def update_user(id: int, user: User, db: Session =Depends(get_db)):

    db_user = db.query(database_models.User).filter(database_models.User.id == id).first()
    if db_user:
        db_user.name = user.name
        db_user.age = user.age
        db.commit()
        return "user updated"
    # for i in range(len(users)):
    #     if users[i].id == id:
    #         users[i] = user
    #         return "User added"
    else:
        return "no user found"

@app.delete("/user/{id}")
def delete_user(id: int, db: Session =Depends(get_db)):
    db_user = db.query(database_models.User).filter(database_models.User.id == id).first()
        
    if db_user:
            db.delete(db_user)
            db.commit()
    else:
            return "User not found"