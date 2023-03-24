from api import create_chat_completion_clean
from subprocess import run
from tempfile import NamedTemporaryFile

def read_csv(csv):
  python_program = generate_read_csv(csv)

  result = run([
    'python',
    '-c',
    python_program
  ], capture_output=True, input=csv, text=True)

  if result.returncode != 0:
    print('ERROR: Python program failed to run')
    print(result.stderr)
  else:
    print(result.stdout)

def generate_read_csv(csv):
  return create_chat_completion_clean([
    {
      "role": "system",
      "content": "Given the first few lines in a csv file, write a program to read a csv from standard input and print the contents of the into a pandas dataframe then prints the dataframe."
    },
    {
      "role": "user",
      "content": """Name,Age,Country
John,32,USA
Jane,28,Canada
Jim,45,UK"""
    },
    {
      "role": "assistant",
      "content": """import sys
import pandas as pd
from io import StringIO
raw_data = '\\n'.join([ line.strip('\\n') for line in sys.stdin ])
df = pd.read_csv(StringIO(raw_data))
print(df)"""
    },
    {
      "role": "user",
      "content": """Product,Price,Stock
Apple,0.99,100
Banana,0.5,200
Cherry,2.99,50"""
    },
    {
      "role": "assistant",
      "content": """import sys
import pandas as pd
from io import StringIO
raw_data = '\\n'.join([ line.strip('\\n') for line in sys.stdin ])
df = pd.read_csv(StringIO(raw_data))
print(df)"""
    },
    {
      "role": "user",
      "content": csv
    }
  ])

if __name__ == '__main__':
  csv = """Employee ID,Name,Department,Salary
1,John Doe,Marketing,50000
2,Jane Smith,Sales,60000
3,Jim Brown,IT,65000"""

  read_csv(csv)