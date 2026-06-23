"""Chat router: general chat and recipe endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.services.chat_service import get_chat_response, get_recipe_response
from app.services.auth_service import get_current_user
from app.services.user_service import save_chat_message, get_chat_history

router = APIRouter(tags=["chat"])


security = HTTPBearer()

def require_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to require a valid JWT token."""
    token = credentials.credentials
    user = get_current_user(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user


class ChatRequest(BaseModel):
    message: str


class RecipeRequest(BaseModel):
    dish_name: str
    dietary_restrictions: str = ""
    cuisine: str = ""


@router.post("/chat")
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(require_auth),
):
    """Send a message to Chef Zoya and get a response."""
    user_id = current_user["user_id"]

    # Get recent chat history for context
    history = get_chat_history(user_id)
    # Use last 10 messages as context
    context = history[-10:] if len(history) > 10 else history

    # Get response from Chef Zoya
    response = get_chat_response(request.message, context)

    # Save both messages to history
    save_chat_message(user_id, "user", request.message)
    save_chat_message(user_id, "assistant", response)

    return {"response": response}


@router.post("/chat/recipe")
async def get_recipe(
    request: RecipeRequest,
    current_user: dict = Depends(require_auth),
):
    """Get a detailed recipe from Chef Zoya and optionally save it."""
    user_id = current_user["user_id"]

    response = get_recipe_response(
        request.dish_name,
        request.dietary_restrictions,
        request.cuisine,
    )

    # Save to chat history
    save_chat_message(
        user_id,
        "user",
        f"Give me a recipe for {request.dish_name}",
    )
    save_chat_message(user_id, "assistant", response)

    return {
        "dish": request.dish_name,
        "recipe": response,
    }
