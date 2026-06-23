"""Chat service using LangChain + Ollama with Chef Zoya persona."""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import settings

# Chef Zoya system prompt
CHEF_SYSTEM_PROMPT = """You are Chef Zoya, a friendly and professional chef assistant. 
You have deep knowledge of world cuisines, cooking techniques, ingredient substitutions, 
and meal planning. You are warm, encouraging, and passionate about food.

Guidelines:
- Always respond in a helpful, enthusiastic chef persona
- Give clear, step-by-step cooking instructions
- Suggest ingredient substitutions when relevant
- Ask clarifying questions when needed about dietary restrictions or preferences
- Keep responses concise but thorough
- When asked for recipes, provide complete recipes with ingredients list and instructions"""

# Initialize the Ollama LLM
llm = ChatOllama(
    base_url=settings.OLLAMA_BASE_URL,
    model=settings.OLLAMA_MODEL,
    temperature=0.7,
)


def get_chat_response(user_message: str, chat_history: list[dict] = None) -> str:
    """Get a response from Chef Zoya via LangChain + Ollama."""
    messages = [SystemMessage(content=CHEF_SYSTEM_PROMPT)]

    # Add chat history if provided
    if chat_history:
        for msg in chat_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                messages.append(HumanMessage(content=content))
            else:
                messages.append(SystemMessage(content=content))

    # Add the current user message
    messages.append(HumanMessage(content=user_message))

    # Get response from LLM
    response = llm.invoke(messages)
    return response.content


def get_recipe_response(
    dish_name: str, dietary_restrictions: str = "", cuisine: str = ""
) -> str:
    """Get a detailed recipe for a specific dish from Chef Zoya."""
    prompt_parts = [f"Please provide a detailed recipe for {dish_name}."]
    if dietary_restrictions:
        prompt_parts.append(
            f"Dietary restrictions: {dietary_restrictions}"
        )
    if cuisine:
        prompt_parts.append(f"Cuisine style: {cuisine}")
    prompt_parts.append(
        "Include: ingredients list with measurements, step-by-step instructions, "
        "cooking time, serving size, and any helpful tips."
    )

    return get_chat_response(" ".join(prompt_parts))
