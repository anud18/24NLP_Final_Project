import os
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import numpy as np

load_dotenv()  # take environment variables from .env.

def extract_methods(abstract: str) -> str:
    prompt = (
        "Extract the sentences that describe the methods used in the research from the following abstract. "
        "Only provide the sentences related to the methods, nothing else.\n\n"
        f"Abstract:\n{abstract}"
    )
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    output_text = response.choices[0].message.content.strip()
    return output_text

def str_to_upper(s: str) -> str:
    return s.upper()

df = pd.read_csv('./arxiv_dataset.csv')

# 對每個摘要應用 extract_methods 函數並更新 Methods 列
# df['Methods'] = df['Abstract'].apply(extract_methods)
try:
    df['Methods'] = df['Abstract'].apply(extract_methods)
except Exception as e:
    print(f"An error occurred: {e}")
    print("Saving DataFrame to CSV...")
    df.to_csv('./error_handling_arxiv_dataset.csv', index=False)
else:
    # 檢查結果
    print(df[['Abstract', 'Methods']].head())

    # 將更新後的 DataFrame 保存回 CSV 文件
    df.to_csv('./updated_arxiv_dataset.csv', index=False)

# 檢查結果
# print(df[['Abstract', 'Methods']].head())

# 將更新後的 DataFrame 保存回 CSV 文件
df.to_csv('./updated_arxiv_dataset.csv', index=False)
