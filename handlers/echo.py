from aiogram import Router, types


echo_router = Router()

def reverse_words(message: str) -> str:
    words = message.split()
    reversed_message = ' '.join(words[::-1])
    return reversed_message

# Хэндлер для обработки текстовых сообщений
@echo_router.message()
async def echo(message: types.Message):
    reversed_message = reverse_words(message.text)
    await message.reply(reversed_message)