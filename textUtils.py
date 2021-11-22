def index_before(text: str, search: str, start_index=None, require_found=True) -> int:
  index = text.find(search, start_index)
  if require_found and index < 0:
    raise Exception('Failed to find search string %s.' % search)
  return index

def index_after(text: str, search: str, start_index=None, require_found=True) -> int:
  return index_before(text, search, start_index, require_found) + len(search)

def insert_before(text: str, search: str, new_text: str) -> str:
  index = index_before(text, search)
  return text[:index] + new_text + text[index:]

def insert_after(text: str, search: str, new_text: str) -> str:
  index = index_after(text, search)
  return text[:index] + new_text + text[index:]

def text_between(text: str, before: str, after: str):
  before_index = index_after(text, before)
  return text[before_index:index_before(text, after, before_index)]
