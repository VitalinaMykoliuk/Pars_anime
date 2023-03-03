import asyncio
import requests
from bs4 import BeautifulSoup
from aiogram import types, executor, Dispatcher, Bot
from dotenv import dotenv_values
import key_board
TIME_SLEEP = 1.5


config = dotenv_values('.env')
bot = Bot(config['tokens'])
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.message):
    await message.answer(f'''Привет {message.from_user.full_name} я бот для поиска лучших аниме
      <b><a href='https://yummyanime.tv/'>Anime</a></b>:)''',
        parse_mode='html', disable_web_page_preview=True, reply_markup=key_board.main_meny)


@dp.message_handler(commands=['Топ-100'])
async def top100(message: types.message):
    top25_lst = ['1-25', '26-50', '51-75', '76-100']
    kb = types.InlineKeyboardMarkup(row_width=2).add(*[types.InlineKeyboardButton(text=top25_lst[i],
                                    callback_data=f"films_{top25_lst[i]}") for i in range(0, 4)])
    await message.answer('Please make your choose', reply_markup=kb)


@dp.callback_query_handler(lambda k: k.data.startswith('films_'))
async def process_top100(call: types.CallbackQuery):
    films = call.data.split('_')[-1]
    await bot.answer_callback_query(call.id)
    await call.message.answer(f'page{films}', reply_markup=types.ReplyKeyboardRemove())

    url = f'https://yummyanime.tv/1top-100/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    movies = soup.find_all('div', class_='movie-item')
    movies_start, movies_end = int(films.split('-')[0]), int(films.split('-')[1])
    movie = [movies[i] for i in range(movies_start, movies_end + 1)]


    for top in movie:
        main_link = 'https://yummyanime.tv'
        name = top.select('.movie-item__title')[0].text
        rating = top.select('.movie-item__rating')[0].text.strip()
        year = top.select('.movie-item__meta')[0].text.replace('(', '').replace(')', '').strip()
        link = main_link + top.select('.movie-item__link')[0]['href']
        img = main_link + top.select('.movie-item__img > img')[0]['src']
        await asyncio.sleep(2)
        await bot.send_photo(call.from_user.id, img, caption="<b>" + name + "</b>\n<i>" +
                rating + "</i>\n<i>" + year + f"</i>\n<a href='{link}'>Ссылка на фильм</a>", parse_mode='html')

    await top100(call.message)


@dp.message_handler(commands=['Фильмы'])
async def movies(message: types.message):
    url = 'https://yummyanime.tv/movies/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    page_count = int(soup.find('div', class_='pagination__inner').find_all('a')[-1].text.strip())

    kb = types.InlineKeyboardMarkup(row_width=3).add(*[types.InlineKeyboardButton(text=str(i),
                                    callback_data=f"page_{i}") for i in range(1, page_count + 1)])
    await message.answer('Please choose a page', reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data.startswith('page_'))
async def process_movies(call: types.CallbackQuery):
    page = int(call.data.split('_')[-1])
    await bot.answer_callback_query(call.id)
    await call.message.answer(f'page {page}', reply_markup=types.ReplyKeyboardRemove())

    url = f'https://yummyanime.tv/movies/page/{page}/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_movies = soup.select('.section > .section__content > .movie-item > .movie-item__inner')

    for movie in all_movies:
        main_link = 'https://yummyanime.tv'
        name = movie.select('.movie-item__title')[0].text
        rating = movie.select('.movie-item__rating')[0].text.strip()
        year = movie.select('.movie-item__meta')[0].text.replace('(', '').replace(')', '').strip()
        link = main_link + movie.select('.movie-item__link')[0]['href']
        img = main_link + movie.select('.movie-item__img > img')[0]['src']
        await asyncio.sleep(TIME_SLEEP)
        await bot.send_photo(call.from_user.id, img, caption="<b>" + name + "</b>\n<i>" +
                rating + "</i>\n<i>" + year + f"</i>\n<a href='{link}'>Ссылка на фильм</a>", parse_mode='html')

    await movies(call.message)

if __name__ == '__main__':
    executor.start_polling(dp)



