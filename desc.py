from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from urllib.parse import quote
import json 

playlist_id = "PLuwe7eTRW5-7KyF6O0SfxHKqtF3iT6JWl"

# INFO about client and user which generated
# by script "access.py" into files 
# client_secret.json and user_token.json

client_id = "read_from_client_secret.json_below"
client_secret = "read_from_client_secret.json_below"
refresh_token = "read_from_user_token,json_below"

file_client_secret = "client_secret.json"
with open(file_client_secret, "r", encoding="utf-8") as fp:
    cs_dt = json.load(fp)

client_id = cs_dt["installed"]["client_id"]
client_secret = cs_dt["installed"]["client_secret"]

file_user_token = "user_token.json"
with open(file_user_token, "r", encoding="utf-8") as fp:
    ut_dt = json.load(fp)

refresh_token = ut_dt["refresh_token"]    

###

# Создайте объект Credentials из данных клиента и токена обновления
credentials = Credentials(
    None,
    client_id=client_id,
    client_secret=client_secret,
    refresh_token=refresh_token,
    token_uri="https://oauth2.googleapis.com/token",
)

def update_video_access(playlist_id):
    youtube = build('youtube', 'v3', credentials=credentials)

    try:
        playlist_items_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50
        ).execute()

        for item in playlist_items_response['items']:
            video_id = item['snippet']['resourceId']['videoId']

            # Update video access control
            youtube.videos().update(
                part='status',
                body={
                    'id': video_id,
                    'status': {
                        #unlisted
                        'privacyStatus': 'public'
                    }
                }
            ).execute()

        print("Video access updated successfully!")

    except HttpError as e:
        print("An error occurred while updating video access:")
        print(e)


def update_video_descriptions(playlist_id, text_to_write):
    youtube = build('youtube', 'v3', credentials=credentials)

    try:
        playlist_items_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50
        ).execute()
        i = 0
        for item in playlist_items_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            
            video_response = youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()

            #video_title = video_response['items'][0]['snippet']['title']
            if i == 0:
                video_title = f"Предисловие. Аудиокнига «Ферментное питание», Эдвард Хоуэлл"
            if i == 1:
                video_title = f"Введение. Аудиокнига «Ферментное питание», Эдвард Хоуэлл"
            if i == 11:
                video_title = f"Залючение. Аудиокнига «Ферментное питание», Эдвард Хоуэлл"
                       
            else:
                video_title = f"{i - 1} глава. Аудиокнига «Ферментное питание», Эдвард Хоуэлл"
            i += 1
            # Удаление текущего описания и запись нового описания
            updated_description = text_to_write

            # Обновление категории видео
            category_id = '27'  # Замените на фактический идентификатор категории
            youtube.videos().update(
                part='snippet',
                body={
                    'id': video_id,
                    'snippet': {
                        'title': video_title,
                        'description': updated_description,
                        'categoryId': category_id
                    }
                }
            ).execute()

        print("Описания видео в плейлисте успешно обновлены!")

    except HttpError as e:
        print("Произошла ошибка при обновлении описаний видео:")
        print(e)


def get_video_categories():
    youtube = build('youtube', 'v3', credentials=credentials)

    try:
        categories_response = youtube.videoCategories().list(
            part='snippet',
            regionCode='RU'  # Укажите код своего региона, если требуется
        ).execute()

        categories = categories_response['items']
        for category in categories:
            category_id = category['id']
            category_title = category['snippet']['title']
            print(f"Category ID: {category_id}, Title: {category_title}")

    except HttpError as e:
        print("Произошла ошибка при получении категорий видео:")
        print(e)


if __name__ == "__main__":

    desc_to_playlist_videos = """Перевод и озвучку можно скачать по ссылке https://alex-renat.site/audiobooks.php

    «Продолжительность жизни обратно пропорциональна скорости истощения ферментного
    потенциала организма. Повышенное потребление пищевых ферментов вызывает снижение
    скорости истощения ферментного потенциала.»

    Аксиома ферментного питания,
    Доктор Эдвард Хоуэлл.
    """
    
    update_video_descriptions(playlist_id, desc_to_playlist_videos)
    #update_video_access(playlist_id)

