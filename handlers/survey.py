from aiogram import Router, F, types
from config import database
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

survey_router = Router()


class BookSurvey(StatesGroup):
    name = State()
    age = State()
    occupation = State()
    salary_or_grade = State()
    comment = State()

@survey_router.message(Command("survey"))
async def start_survey(message: types.Message, state: FSMContext):
    await state.set_state(BookSurvey.name)
    await message.answer("Как вас зовут?")


@survey_router.message(BookSurvey.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(BookSurvey.age)
    await message.answer("Ваш возраст")

@survey_router.message(BookSurvey.age)
async def process_age(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        age = int(message.text)
        if 60 >= age >= 7:
            await state.update_data(age=age)
            await state.set_state(BookSurvey.occupation)
            await message.answer("Введите род занятий")
              # Завершаем опрос
        else:
            await message.answer("спасбо за прохождение нажмите /stop")
    else:
        await message.answer("Пожалуйста, введите число")

@survey_router.message(BookSurvey.occupation)
async def process_occupation(message: types.Message, state: FSMContext):
    occupation = message.text
    data = await state.get_data()  # Получение данных из состояния
    age = data.get('age')
    if age >= 18:
        await state.update_data(occupation=occupation)
        await state.set_state(BookSurvey.salary_or_grade)
        await message.answer("Введите заработную плату")
    else:
        await state.update_data(occupation=occupation)
        await state.set_state(BookSurvey.salary_or_grade)
        await message.answer("Введите среднею оценку")
@survey_router.message(BookSurvey.salary_or_grade)
async def process_salary_or_grade(message: types.Message, state: FSMContext):
    salary_or_grade = message.text.isdigit()
    await state.update_data(salary_or_grade=salary_or_grade)
    await state.set_state(BookSurvey.comment)
    await message.answer("спасбо за прохождение нажмите /stop")




@survey_router.message(F.text.lower() == "стоп")
async def stop(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    await state.clear()
    await database.execute(
        "INSERT INTO surveys (name, age, occupation, occupation) VALUES (?, ?, ?, ?)",
        (data["name"], data["age"], data["occupation"], data["occupation"]),
    )
    await message.answer("Спасибо за прохождение опроса!")
