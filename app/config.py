#アプリ全体の設定を管理する場所
#APIキーや秘密情報を安全委扱うため
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "devkey")