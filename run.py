#アプリを起動するための入口ファイル
#Flaskサーバーを立ち上げる役割
from app import create_app

app = create_app()
app.secret_key = 'your-very-secret-key-12345'

if __name__ == "__main__":
    # サーバーを起動
    app.run(debug=True)

