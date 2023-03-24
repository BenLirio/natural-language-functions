import openai
import hashlib
import os
import pickle

CACHE_DIRECTORY = "cache"

openai.api_key_path = "api_key.txt"

def create_chat_completion_from_cache(key):
  cache_file = f'{CACHE_DIRECTORY}/{key}.pkl'
  os.makedirs(os.path.dirname(cache_file), exist_ok=True)
  if os.path.exists(cache_file):
    return pickle.load(open(cache_file, "rb"))
  return None

def create_chat_completion(messages):
  key = hashlib.md5(str(messages).encode()).hexdigest()
  completion = create_chat_completion_from_cache(key)
  if completion is not None:
    return completion
  print('WARNING: Cache miss, calling OpenAI API')
  completion = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=messages
  )
  pickle.dump(completion, open(f'{CACHE_DIRECTORY}/{key}.pkl', 'wb'))
  return completion

