import os
from notion_client import Client
from pprint import pprint
from dotenv import load_dotenv, dotenv_values
import json
from datetime import datetime, timezone

load_dotenv()

notion_token = os.getenv("NOTION_TOKEN")
notion_page_id = os.getenv("NOTION_PAGE_ID")
notion_database_id = os.getenv("NOTION_DATABASE_ID")

client = Client(auth=notion_token)

def write_dict_to_file_as_json(content, file_name):
  content_as_json_str = json.dumps(content)
  with open(file_name, 'w') as f:
    f.write(content_as_json_str)

def read_text(client, page_id):
  response = client.blocks.children.list(block_id=page_id)
  return response[""]

def write_text(client, page_id, text, type='paragraph'):
    client.blocks.children.append(
        block_id=page_id,
        children=[{
            "object": "block",
            "type": type,
            type: {
                "rich_text": [{ "type": "text", "text": { "content": text } }]
            }
        }]
    )

# get all rows
def get_rows():
  db_rows = client.databases.query(database_id=notion_database_id)
  write_dict_to_file_as_json(db_rows, 'db_rows.json')
  simple_rows = []

  for row in db_rows["results"]:
    id = safe_get(row, "properties.ID.rich_text.0.plain_text")
    english = safe_get(row, "properties.English.title.0.plain_text")
    chinese = safe_get(row, "properties.Chinese.rich_text.0.plain_text")
    content = safe_get(row, "properties.Content.rich_text.0.plain_text")
    post_date = safe_get(row, "properties.Post_Date.date.start")
    
    simple_rows.append({
      'id': id,
      'english': english,
      'chinese': chinese,
      'content': content,
      'post_date': post_date
    })

    write_dict_to_file_as_json(simple_rows, 'simple_rows.json')

def get_page_id(id):
  # Step 1: filter row based on ID
  filtered_row = client.databases.query(
    database_id = notion_database_id,
    filter = {
      "property": "ID",
      "rich_text": {
        "equals": id 
      }
    }
  )
  # Step 2: get page_id
  page_id = filtered_row["results"][0]["id"]
  return page_id

def update_row(page_id):
  current_utc_time = datetime.now(timezone.utc)
  print("UTC Time: ", current_utc_time)
  # 生成 ISO 8601 格式的 UTC 时间
  iso_8601_utc_format = current_utc_time.isoformat()
  print("Current UTC time in ISO 8601:", iso_8601_utc_format)
  # Database/Table 每一個 row 都是一個 page 
  client.pages.update(
    page_id = page_id,
    properties = {
      # 使用 LLM 產生 Content 後填入 column
      "Content": {
        "rich_text": [
          {
            "type": "text",
            "text": {
              "content": "This is content of ID 2"
            }
          }
        ]
      },
      # post 之後補上 post_date
      "Post_Date": {
        "date": {
          "start": iso_8601_utc_format,
          # "end": "2024-04-26"  # 可选：如果你需要一个日期范围
        }
      }
    }
  )

def safe_get(data, dot_chained_keys):
  """
    {'a': {'b': [{'c': 1}]}}
    safe_get(data, 'a.b.0.c') -> 1
  """
  keys = dot_chained_keys.split('.')
  for key in keys:
    try:
      if isinstance(data, list):
        data = data[int(key)]
      else:
        data = data[key]
    except(KeyError, TypeError, IndexError):
      return None
  return data

# def decode_unicode(text):
#   raw_str = text.encode('unicode-escape').decode('ascii')
#   decoded = raw_str.encode().decode('unicode-escape')
#   print(decoded)
#   return decoded




def main():
  page_response = client.pages.retrieve(notion_page_id)


  db_info = client.databases.retrieve(database_id=notion_database_id)
  write_dict_to_file_as_json(db_info, 'db_info.json')


  # update_row (ID = "1")
  page_id = get_page_id("1")
  update_row(page_id)
  # get all rows in db 
  get_rows()


if __name__ == '__main__':
  main()