from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.llms import openai


app = FastAPI()

# Клас для вхідного запиту з текстом


class TextRequest(BaseModel):
    text: str


# Ключ API OpenAI
openai_api_key = 'your_openai_api_key_here'

# Обробка POST-запиту /summarize для підсумовування тексту


@app.post("/summarize")
async def summarize_text(request: TextRequest):
    try:
        # Логування вхідного тексту для перевірки
        print(f"Received text: {request.text}")

        # Перевірка вхідного тексту
        if not isinstance(request.text, str) or len(request.text) < 20:
            raise HTTPException(
                status_code=400, detail="Invalid text input. Minimum length required: 20 characters.")

        # Створення екземпляру OpenAI з параметрами
        llm = openai(temperature=0, openai_api_key=openai_api_key)

        # Використання моделі OpenAI для підсумовування тексту
        summary = llm(request.text)
        return {"summary": summary}

    except HTTPException as http_error:
        raise http_error

    except Exception as e:
        # Додаткові логи для виведення інформації про помилку
        print(f"An error occurred: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
