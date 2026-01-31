import csv
import os
from datetime import datetime, timedelta

# ログファイルの保存場所（myappの直下）
LOG_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'user_logs.csv')

def save_log(username, dish_id, dish_name):
    """料理を決定した時にCSVに保存する"""
    file_exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, mode='a', encoding='utf-8', newline='') as f:
        fieldnames = ['timestamp', 'user', 'dish_id', 'dish_name']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'user': username,
            'dish_id': dish_id,
            'dish_name': dish_name
        })

def get_dish_scores(username):
    """そのユーザーが過去に何回その料理を選んだか集計する"""
    scores = {}
    if not os.path.exists(LOG_PATH):
        return scores
    with open(LOG_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['user'] == username:
                d_id = row['dish_id']
                scores[d_id] = scores.get(d_id, 0) + 1
    return scores

def get_recent_dish_ids(username, days=3):
    """最近3日以内に選んだ料理のIDリストを返す"""
    recent_ids = []
    if not os.path.exists(LOG_PATH):
        return recent_ids
    
    threshold = datetime.now() - timedelta(days=days)
    with open(LOG_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['user'] == username:
                try:
                    log_date = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M')
                    if log_date > threshold:
                        recent_ids.append(row['dish_id'])
                except:
                    continue
    return recent_ids