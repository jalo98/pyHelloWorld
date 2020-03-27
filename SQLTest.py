import panda as pd
from sqlalchemy import create_engine

engine = create_engine(*args, **kwargs)

sql = """
SELECT *
FROM table_1
"""
df = pd.read_sql_query(sql, engine)
df.head()