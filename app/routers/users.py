"""User data router: history, saved recipes, meal plans, ingredients, shopping lists."""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from app.services.auth_service import get_current_user
from app.services.user_service import (
    get_chat_history,
    delete_chat_history,
    get_saved_recipes,
    save_recipe,
    save_meal_plan,
    get_user_ingredients,
    add_ingredient,
    create_shopping_list,
)

router = APIRouter(prefix="/users", tags=["users"])


def require_auth(authorization: str = Header(...)):
    """Dependency to require a valid JWT token."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ", 1)[1]
    user = get_current_user(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user


class MealPlanRequest(BaseModel):
    plan_data: dict


class ShoppingListRequest(BaseModel):
    items: list[dict]


@router.get("/{user_id}/history")
async def get_history(
    user_id: int,
    current_user: dict = Depends(require_auth),
):
    """Get chat history for a user."""
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    history = get_chat_history(user_id)
    return {"history": history}


@router.delete("/{user_id}/history")
async def delete_history(
    user_id: int,
    current_user: dict = Depends(require_auth),
):
    """Delete chat history for a user."""
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    delete_chat_history(user_id)
    return {"message": "Chat history deleted successfully"}


@router.get("/{user_id}/saved-recipes")
async def get_recipes(
    user_id: int,
    current_user: dict = Depends(require_auth),
):
    """Get all saved recipes for a user."""
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    recipes = get_saved_recipes(user_id)
    return {"recipes": recipes}


@router.post("/{user_id}/meal-plan")
async def create_meal_plan(
    user_id: int,
    request: MealPlanRequest,
    current_user: dict = Depends(require_auth),
):
    """Save a meal plan for a user."""
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    meal_plan = save_meal_plan(user_id, request.plan_data)
    return {"message": "Meal plan saved", "meal_plan_id": meal_plan["id"]}


@router.get("/{user_id}/ingredients")
async def get_ingredients(
    user_id: int,
    current_user: dict = Depends(require_auth),
):
    """Get all ingredients in a user's pantry."""
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    ingredients = get_user_ingredients(user_id)
    return {"ingredients": ingredients}


@router.post("/{user_id}/shopping-list")
async def create_shopping_list_endpoint(
    user_id: int,
    request: ShoppingListRequest,
    current_user: dict = Depends(require_auth),
):
    """Create a shopping list for a user."""
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    shopping_list = create_shopping_list(user_id, request.items)
    return {"message": "Shopping list created", "shopping_list_id": shopping_list["id"]}
