"""User service: chat history, saved recipes, meal plans, ingredients, shopping lists."""

import json
from app.database.connection import get_db_connection


def save_chat_message(user_id: int, role: str, content: str):
    """Save a chat message to the database."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO chat_history (user_id, role, content) VALUES (%s, %s, %s)",
                (user_id, role, content),
            )
            conn.commit()
    finally:
        conn.close()


def get_chat_history(user_id: int) -> list[dict]:
    """Get all chat history for a user."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, role, content, created_at FROM chat_history WHERE user_id = %s ORDER BY created_at ASC",
                (user_id,),
            )
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def delete_chat_history(user_id: int):
    """Delete all chat history for a user."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM chat_history WHERE user_id = %s", (user_id,)
            )
            conn.commit()
    finally:
        conn.close()


def save_recipe(user_id: int, title: str, ingredients: str, instructions: str) -> dict:
    """Save a recipe for a user."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO saved_recipes (user_id, title, ingredients, instructions) VALUES (%s, %s, %s, %s) RETURNING id, title, created_at",
                (user_id, title, ingredients, instructions),
            )
            recipe = dict(cur.fetchone())
            conn.commit()
            return recipe
    finally:
        conn.close()


def get_saved_recipes(user_id: int) -> list[dict]:
    """Get all saved recipes for a user."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, ingredients, instructions, created_at FROM saved_recipes WHERE user_id = %s ORDER BY created_at DESC",
                (user_id,),
            )
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def save_meal_plan(user_id: int, plan_data: dict) -> dict:
    """Save a meal plan for a user."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO meal_plans (user_id, plan_data) VALUES (%s, %s) RETURNING id, created_at",
                (user_id, json.dumps(plan_data)),
            )
            meal_plan = dict(cur.fetchone())
            conn.commit()
            return meal_plan
    finally:
        conn.close()


def get_user_ingredients(user_id: int) -> list[dict]:
    """Get all ingredients for a user's pantry."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, quantity, unit FROM user_ingredients WHERE user_id = %s ORDER BY name ASC",
                (user_id,),
            )
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def add_ingredient(user_id: int, name: str, quantity: str, unit: str) -> dict:
    """Add or update an ingredient in the user's pantry."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO user_ingredients (user_id, name, quantity, unit)
                   VALUES (%s, %s, %s, %s)
                   ON CONFLICT (user_id, name)
                   DO UPDATE SET quantity = EXCLUDED.quantity, unit = EXCLUDED.unit
                   RETURNING id, name, quantity, unit""",
                (user_id, name.lower(), quantity, unit),
            )
            ingredient = dict(cur.fetchone())
            conn.commit()
            return ingredient
    finally:
        conn.close()


def create_shopping_list(user_id: int, items: list[dict]) -> dict:
    """Create a shopping list for a user."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO shopping_lists (user_id, items) VALUES (%s, %s) RETURNING id, created_at",
                (user_id, json.dumps(items)),
            )
            shopping_list = dict(cur.fetchone())
            conn.commit()
            return shopping_list
    finally:
        conn.close()
