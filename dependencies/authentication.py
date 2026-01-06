from fastapi import HTTPException, status, Depends, Request
from utils.auth import verify_token, cookie_scheme, COOKIE_NAME

async def get_current_user(request: Request, token: str = Depends(cookie_scheme)):
    access_token = request.cookies.get(COOKIE_NAME)

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="No token sent"
        )

    validated_token = verify_token(access_token)
    if not validated_token.valid or not validated_token.user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or expired token"
        )
    
    return validated_token.user