from fastapi import FastAPI, HTTPException, status, Response, Depends

from utils.auth import set_jwt_cookie, remove_jwt_cookie, verify_password, create_access_token, hash_password
from models.user import UserProfile
from models.user import LoginData, RegisterData
from dependencies.authentication import get_current_user
from dependencies.authorization import RoleChecker, UserRoles

db = {}

app = FastAPI()

@app.get("/")
async def home():
    return "Server"


@app.post("/login")
async def login(user: LoginData, response: Response):
    user_in_db = db.get(user.email)
    
    if user_in_db is None or not verify_password(user.password, user_in_db['password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data=UserProfile(email=user_in_db['email'], type=UserRoles(user_in_db['type'])))

    set_jwt_cookie(response, access_token)
    return {"msg": "Login successful"}


@app.post("/logout")
async def logout(response: Response):
    remove_jwt_cookie(response)

    return {"msg": "Logout successful"}


@app.get("/protected")
async def protected_route(user: UserProfile = Depends(get_current_user)):
    return {"msg": f"Hello {user.email}:{user.type}, you have access to this route!"}


@app.get("/admin_only")
async def admin_only(user: UserProfile = Depends(RoleChecker(UserRoles.ADMIN))):
    return {"msg": f"Hello {user.email}:{user.type}, you have access to this route!"}


@app.post("/register")
async def register(user: RegisterData):
    if user.email in db:
        raise HTTPException(status_code=400, detail="Email already exists")
    db[user.email] = {"email": user.email, "password": hash_password(user.password), "type": user.type}

    return {"msg": "User registered successfully"}