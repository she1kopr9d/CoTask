import ai.bot
import ai.models.qwen_model
import ai.history


#TOKEN_API = """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"""
# TOKEN_API = """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"""

# data = [
#     {
#         "role": "user",
#         "content": """Отвечай кратко и со смыслом, сначало спрашивай (по одному вопросу за раз, сообщения должны быть максимум из 2 предложений), уточняй, после уже выписывай что человеку нужно сделать! ЭТО ГЛАВНЫЙ АЛГОРИТМ""",
#     },
#     {
#         "role": "user",
#         "content": """_Используй этот шаблон, чтобы я мог дать наиболее точный и полезный ответ. Объясни свою задачу так, чтобы я понял:_

# 1. **Что ты хочешь сделать?**  
#    (Например: "Написать статью", "Создать план проекта", "Решить проблему", "Объяснить процесс" и т.д.)

# 2. **Для чего это нужно?**  
#    (Цель: "Образовательный материал", "Деловая презентация", "Техническая задача", "Креативный проект" и т.д.)

# 3. **Какие у тебя есть ограничения или требования?**  
#    (Формат ответа: "Список", "Разговорный стиль", "Техническое описание", "Максимум 500 слов" и т.д.)

# 4. **Есть ли дополнительные детали или контекст?**  
#    (Пример: "Нужно использовать Python", "Аудитория — студенты", "Учти, что мы говорили ранее об этом [тема]").

# ---

# ### **Пример заполнения:**
# > _Пользователь:_  
# > "Помоги уточнить задачу: Сделать проект по машинному обучению."  
# >  
# > _Я:_  
# > "Что ты хочешь сделать в проекте по машинному обучению? Например, создать модель прогноза, провести анализ данных или обучить нейросеть? Какой тип данных ты будешь использовать? Нужно ли включить визуализацию, пояснения к коду или готовый прототип? Есть ли у тебя опыт или нужно всё пошагово?" """
#     }
# ]

# bot = ai.bot.Bot(
#     token=TOKEN_API,
#     model=ai.models.qwen_model.QwenModel(),
#     history=ai.history.History(data),
# )

# while True:
#     message = input("Your message: ")
#     if message == "exit":
#         break
#     print(bot.send(message))

import json
import requests

TOKEN_API = "sk-f96ad8dae9dd4b6bba2cbc5dd913b0e7"
response = requests.post(
    url="https://api.deepseek.com/chat/completions",
    headers={
        "Authorization": f"Bearer {TOKEN_API}",
        "Content-Type": "application/json",
    },
    data=json.dumps({
        #"model": "qwen/qwen3-14b:free",
        "model": "deepseek-chat",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Hello!"}
        ],
        "stream": False,
    })
)

print(response.text)