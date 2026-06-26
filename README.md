<div align="center">

# 🧑‍🍳 Chef Zoya — AI Chef Assistant API

**Your intelligent kitchen companion powered by FastAPI, LangChain, and Ollama**

[![Python](https://img.shields.io/badge/python-3.14+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.138+-00a393?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1.3+-1C3C3C?logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Ollama](https://img.shields.io/badge/Ollama-llama3.1:latest-000?logo=ollama&logoColor=white)](https://ollama.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-316192?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![uv](https://img.shields.io/badge/uv-package%20manager-4F46E5?logo=python&logoColor=white)](https://docs.astral.sh/uv/)

</div>

---

## 🌟 Overview

**Chef Zoya** is a friendly and professional AI chef assistant that lives in your API. Built with **FastAPI** and powered by **LangChain + Ollama (llama3.1:latest)**, she helps users with:

- 🍳 **Recipes** — Detailed, step-by-step recipes for any dish
- 📋 **Meal Plans** — Custom weekly meal plans tailored to preferences
- 🛒 **Shopping Lists** — Auto-generated shopping lists from meals and pantry
- 🧺 **Pantry Management** — Track what ingredients you have on hand
- 💬 **Chat History** — Persistent, per-user conversation history stored in PostgreSQL

Every user gets a secure **JWT-authenticated** session with their own private chat history, saved recipes, meal plans, and ingredient pantry.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (fast Python package manager)
- PostgreSQL 16+
- [Ollama](https://ollama.com/) with `llama3.1:latest` pulled

### 1. Clone & Install

```bash
git clone <repository-url>
cd chef-chatbot
uv sync
```

> `uv sync` reads `pyproject.toml` and installs all dependencies into a virtual environment.

### 2. Configure Environment

Create a `.env` file in the project root:

```env
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:latest

# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=chef_chatbot
DB_USER=postgres
DB_PASSWORD=yourpassword

# JWT
JWT_SECRET=your-super-secret-key-change-me
```

> ⚠️ Change `JWT_SECRET` to a strong, random value before deploying to production.

### 3. Start Ollama

```bash
ollama pull llama3.1:latest
ollama serve
```

### 4. Run the API

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at **http://localhost:8000**. Interactive docs at **http://localhost:8000/docs**.

---

## 📡 API Reference

### 🔐 Authentication

All endpoints except `/health`, `/auth/register`, and `/auth/login` require a **Bearer JWT token** in the `Authorization` header:

```
Authorization: Bearer <your-jwt-token>
```

---

#### `POST /auth/register` — Register a new user

| Parameter | Type     | Description           |
|-----------|----------|-----------------------|
| `username` | `string` | Unique username       |
| `email`   | `string` | Valid email address   |
| `password` | `string` | Account password      |

<details>
<summary><b>📥 Example Request</b></summary>

```json
{
  "username": "homecook",
  "email": "homecook@example.com",
  "password": "securePassword123"
}
```
</details>

<details>
<summary><b>📤 Example Response (201 Created)</b></summary>

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "homecook",
    "email": "homecook@example.com",
    "created_at": "2026-06-26T12:00:00+00:00"
  }
}
```
</details>

---

#### `POST /auth/login` — Login and receive a JWT token

| Parameter | Type     | Description      |
|-----------|----------|------------------|
| `username` | `string` | Your username    |
| `password` | `string` | Your password    |

<details>
<summary><b>📥 Example Request</b></summary>

```json
{
  "username": "homecook",
  "password": "securePassword123"
}
```
</details>

<details>
<summary><b>📤 Example Response (200 OK)</b></summary>

```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "homecook",
    "email": "homecook@example.com"
  }
}
```
</details>

> Save the `token` — you'll need it for all subsequent requests.

---

### 💬 Chat Endpoints

All chat endpoints require **JWT authentication**.

---

#### `POST /chat` — Chat with Chef Zoya

Send a message and get an AI chef response. The last 10 messages of conversation history are included for context.

| Parameter | Type     | Description                         |
|-----------|----------|-------------------------------------|
| `message` | `string` | Your question or cooking request    |

<details>
<summary><b>📥 Example Request</b></summary>

```json
{
  "message": "What's a good substitute for buttermilk in pancakes?"
}
```
</details>

<details>
<summary><b>📤 Example Response (200 OK)</b></summary>

```json
{
  "response": "Great question! For a quick buttermilk substitute in pancakes, mix 1 cup of regular milk with 1 tablespoon of lemon juice or white vinegar. Let it sit for 5 minutes — it will curdle slightly and give you that same tangy, tender result! You can also use plain yogurt thinned with a little milk. Happy cooking! 🥞"
}
```
</details>

---

#### `POST /chat/recipe` — Get a detailed recipe

Request a complete recipe with ingredients, instructions, and tips.

| Parameter             | Type     | Description                              |
|-----------------------|----------|------------------------------------------|
| `dish_name`           | `string` | Name of the dish                         |
| `dietary_restrictions`| `string` | *(optional)* Dietary restrictions         |
| `cuisine`             | `string` | *(optional)* Preferred cuisine style      |

<details>
<summary><b>📥 Example Request</b></summary>

```json
{
  "dish_name": "Pad Thai",
  "dietary_restrictions": "vegetarian, gluten-free",
  "cuisine": "Thai"
}
```
</details>

<details>
<summary><b>📤 Example Response (200 OK)</b></summary>

```json
{
  "dish": "Pad Thai",
  "recipe": "Chef Zoya's Vegetarian & Gluten-Free Pad Thai\n\n**Ingredients:**\n- 200g rice noodles (gluten-free)\n- 2 tbsp tamari (gluten-free soy sauce)\n- 3 tbsp tamarind paste\n- 2 tbsp maple syrup\n- Juice of 1 lime\n- 2 tbsp oil\n- 2 cloves garlic, minced\n- 1 block firm tofu, cubed\n- 2 eggs (omit for vegan)\n- 1 cup bean sprouts\n- 3 green onions, sliced\n- ¼ cup crushed peanuts (omit for nut-free)\n- Fresh cilantro\n\n**Instructions:**\n1. Soak noodles in warm water for 30 min, then drain\n2. Mix tamari, tamarind paste, maple syrup, and lime juice\n3. Heat oil in wok, fry garlic and tofu until golden\n4. Push to side, scramble eggs\n5. Add noodles and sauce, toss for 2 min\n6. Add bean sprouts and green onions\n7. Serve with peanuts and cilantro\n\n⏱️ Prep: 10 min | Cook: 15 min | Serves: 2"
}
```
</details>

---

### 📜 History Endpoints

---

#### `GET /users/{user_id}/history` — Get chat history

Retrieve all past conversations for the authenticated user.

<details>
<summary><b>📤 Example Response (200 OK)</b></summary>

```json
{
  "history": [
    {
      "id": 1,
      "role": "user",
      "content": "What's a good substitute for buttermilk in pancakes?",
      "created_at": "2026-06-26T12:00:00+00:00"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "Great question! For a quick buttermilk substitute...",
      "created_at": "2026-06-26T12:00:01+00:00"
    }
  ]
}
```
</details>

---

#### `DELETE /users/{user_id}/history` — Delete chat history

Permanently removes all chat history for the authenticated user.

<details>
<summary><b>📤 Example Response (200 OK)</b></summary>

```json
{
  "message": "Chat history deleted successfully"
}
```
</details>

---

### 🧠 Smart Endpoints

---

#### `GET /users/{user_id}/saved-recipes` — Get saved recipes

Returns all recipes the user has saved.

<details>
<summary><b>📤 Example Response (200 OK)</b></summary>

```json
{
  "recipes": [
    {
      "id": 1,
      "title": "Vegetarian Pad Thai",
      "ingredients": "200g rice noodles, 2 tbsp tamari, 3 tbsp tamarind paste...",
      "instructions": "1. Soak noodles... 2. Mix sauce...",
      "created_at": "2026-06-26T12:00:00+00:00"
    }
  ]
}
```
</details>

---

#### `POST /users/{user_id}/meal-plan` — Save a meal plan

Save a custom weekly meal plan.

| Parameter    | Type     | Description                     |
|--------------|----------|----------------------------------|
| `plan_data`  | `object` | JSON object with meal plan data  |

<details>
<summary><b>📥 Example Request</b></summary>

```json
{
  "plan_data": {
    "week": "2026-06-29",
    "days": {
      "monday": { "breakfast": "Oatmeal", "lunch": "Caesar Salad", "dinner": "Grilled Salmon" },
      "tuesday": { "breakfast": "Smoothie Bowl", "lunch": "Quinoa Bowl", "dinner": "Pad Thai" },
      "wednesday": { "breakfast": "Avocado Toast", "lunch": "Tomato Soup", "dinner": "Chicken Stir Fry" },
      "thursday": { "breakfast": "Greek Yogurt", "lunch": "Wrap", "dinner": "Pasta Primavera" },
      "friday": { "breakfast": "Pancakes", "lunch": "Salad", "dinner": "Homemade Pizza" }
    }
  }
}
```
</details>

<details>
<summary><b>📤 Example Response (201 Created)</b></summary>

```json
{
  "message": "Meal plan saved",
  "meal_plan_id": 1
}
```
</details>

---

#### `GET /users/{user_id}/ingredients` — Get pantry ingredients

Retrieve all ingredients in the user's pantry.

<details>
<summary><b>📤 Example Response (200 OK)</b></summary>

```json
{
  "ingredients": [
    { "id": 1, "name": "chicken breast", "quantity": "2", "unit": "lbs" },
    { "id": 2, "name": "olive oil", "quantity": "1", "unit": "bottle" },
    { "id": 3, "name": "garlic", "quantity": "1", "unit": "head" }
  ]
}
```
</details>

---

#### `POST /users/{user_id}/shopping-list` — Create a shopping list

Generate and save a shopping list with items.

| Parameter | Type    | Description                        |
|-----------|---------|------------------------------------|
| `items`   | `array` | List of items with name, quantity, unit |

<details>
<summary><b>📥 Example Request</b></summary>

```json
{
  "items": [
    { "name": "Salmon fillet", "quantity": 2, "unit": "lbs" },
    { "name": "Lemon", "quantity": 3, "unit": "whole" },
    { "name": "Fresh dill", "quantity": 1, "unit": "bunch" },
    { "name": "Asparagus", "quantity": 1, "unit": "bunch" }
  ]
}
```
</details>

<details>
<summary><b>📤 Example Response (201 Created)</b></summary>

```json
{
  "message": "Shopping list created",
  "shopping_list_id": 1
}
```
</details>

---

### ❤️ Health Endpoint

---

#### `GET /health` — Check API health

Public endpoint — no authentication required.

<details>
<summary><b>📤 Example Response (200 OK)</b></summary>

```json
{
  "status": "healthy",
  "chef": "Chef Zoya is ready to cook! 🧑‍🍳"
}
```
</details>

---

## 🗄️ Database Schema

The API uses **PostgreSQL** with **psycopg2**. Tables are automatically created on startup.

```mermaid
erDiagram
    users ||--o{ chat_history : has
    users ||--o{ saved_recipes : saves
    users ||--o{ meal_plans : plans
    users ||--o{ user_ingredients : stores
    users ||--o{ shopping_lists : owns

    users {
        int id PK
        varchar(50) username UK
        varchar(255) email UK
        varchar(255) password_hash
        timestamptz created_at
    }

    chat_history {
        int id PK
        int user_id FK
        varchar(20) role
        text content
        timestamptz created_at
    }

    saved_recipes {
        int id PK
        int user_id FK
        varchar(255) title
        text ingredients
        text instructions
        timestamptz created_at
    }

    meal_plans {
        int id PK
        int user_id FK
        jsonb plan_data
        timestamptz created_at
    }

    user_ingredients {
        int id PK
        int user_id FK
        varchar(255) name
        varchar(100) quantity
        varchar(50) unit
        timestamptz created_at
        unique(user_id, name)
    }

    shopping_lists {
        int id PK
        int user_id FK
        jsonb items
        timestamptz created_at
    }
```

---

## 🔧 Environment Variables

| Variable            | Required | Default                               | Description                                |
|---------------------|----------|---------------------------------------|--------------------------------------------|
| `OLLAMA_BASE_URL`   | ✅       | `http://154.57.212.236:11434`         | Ollama server base URL                     |
| `OLLAMA_MODEL`      | ✅       | `llama3.1:latest`                     | Ollama model name                          |
| `DB_HOST`           | ✅       | `localhost`                           | PostgreSQL host                            |
| `DB_PORT`           | ✅       | `5432`                                | PostgreSQL port                            |
| `DB_NAME`           | ✅       | `chef_chatbot`                        | PostgreSQL database name                   |
| `DB_USER`           | ✅       | `postgres`                            | PostgreSQL username                        |
| `DB_PASSWORD`       | ✅       | `postgres`                            | PostgreSQL password                        |
| `JWT_SECRET`        | ✅       | `super-secret-key-change-in-production`| JWT signing secret — **change in production** |

The API also uses these **fixed** settings (not configurable via env):

| Setting                 | Value    |
|-------------------------|----------|
| `JWT_ALGORITHM`         | `HS256`  |
| `JWT_EXPIRATION_HOURS`  | `24`     |

---

## 🏗️ Project Structure

```
chef-chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app entry point
│   ├── config.py              # Settings & env vars
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py      # PostgreSQL connection management
│   │   └── models.py          # Table creation SQL
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py            # Register & login endpoints
│   │   ├── chat.py            # Chat & recipe endpoints
│   │   ├── health.py          # Health check endpoint
│   │   └── users.py           # User data endpoints
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py    # JWT, password hashing, auth logic
│       ├── chat_service.py    # LangChain + Ollama integration
│       └── user_service.py    # CRUD for user data
├── .env                      # Environment variables (gitignored)
├── .gitignore
├── .python-version
├── pyproject.toml            # Project metadata & dependencies
├── uv.lock                   # Locked dependency versions
└── README.md                 # ← You are here
```

---

## 🛠️ Tech Stack

| Technology     | Role                                     |
|----------------|------------------------------------------|
| **FastAPI**    | Async Python web framework               |
| **LangChain**  | LLM orchestration & prompt management    |
| **Ollama**     | Local LLM server (`llama3.1:latest`)     |
| **PostgreSQL** | Relational database                      |
| **psycopg2**   | PostgreSQL adapter for Python            |
| **JWT**        | Stateless authentication                 |
| **bcrypt**     | Password hashing                         |
| **uv**         | Python package manager                   |
| **pydantic**   | Request/response validation              |

---

## 📘 Usage Examples

### Python (using `requests`)

```python
import requests

BASE = "http://localhost:8000"

# 1. Register
requests.post(f"{BASE}/auth/register", json={
    "username": "homecook",
    "email": "homecook@example.com",
    "password": "securePassword123"
})

# 2. Login
res = requests.post(f"{BASE}/auth/login", json={
    "username": "homecook",
    "password": "securePassword123"
})
token = res.json()["token"]
headers = {"Authorization": f"Bearer {token}"}

# 3. Ask Chef Zoya
res = requests.post(f"{BASE}/chat", json={
    "message": "How do I make creamy mushroom risotto?"
}, headers=headers)
print(res.json()["response"])
```

### cURL

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "homecook", "email": "homecook@example.com", "password": "securePassword123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "homecook", "password": "securePassword123"}'

# Chat with Chef Zoya
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{"message": "What can I make with leftover chicken and rice?"}'
```

---

## ⚠️ Disclaimer

> **Chef Zoya is an AI assistant** powered by a large language model (llama3.1 via Ollama). While she strives to provide accurate, safe, and helpful cooking advice, please note:
>
> - 🥜 **Allergies & Dietary Restrictions** — Always double-check ingredients and recipes against your specific dietary needs and allergies. Chef Zoya's suggestions should not replace professional dietary advice.
> - 🍖 **Food Safety** — Follow proper food handling, cooking temperatures, and storage guidelines. Chef Zoya is not a certified food safety professional.
> - 🧪 **Nutritional Information** — Any nutritional data provided is approximate. Consult a qualified nutritionist for precise dietary planning.
> - 🔥 **Cooking Temperatures** — Always use a food thermometer to ensure meats and other foods are cooked to safe internal temperatures.
> - ⚙️ **API in Development** — This API is under active development. Endpoints, authentication, and data models may change. Use the provided versioning and migration strategies when upgrading.
>
> Cook with joy, but cook safely! 🧑‍🍳❤️

---

<div align="center">

**Made with ❤️ and a pinch of 🧂**

</div>
