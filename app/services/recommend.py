import csv
import os
import re
from app.services.log import get_dish_scores, get_recent_dish_ids

def get_recommendations(month, mood, username=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, '..', '..', 'recipes.csv')
    
    all_recipes = []
    
    # ユーザーごとのログデータを取得
    scores = get_dish_scores(username) if username else {}
    # IDをすべて文字列にしてリスト化（比較ミスを防ぐ）
    recent_dishes = [str(did).strip() for did in get_recent_dish_ids(username, days=3)] if username else []

    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dish_id = str(row.get('id', '')).strip()
                name = row.get('name', '').strip()
                
                # --- 月の判定ロジック (1/2/3/4 などに対応) ---
                season_raw = str(row.get('season', '')).strip()
                # スラッシュ、カンマ、空白で分割してリスト化
                seasons = [s.strip() for s in re.split(r'[/,]', season_raw) if s.strip()]
                
                match_score = 0
                # 選択した月が含まれているか、またはseasonが空なら加点
                if str(month) in seasons or not season_raw:
                    match_score += 10
                
                # --- 気分の判定ロジック (和食/あっさり などに対応) ---
                tags_raw = str(row.get('tags', '')).strip()
                # 同じく分割してリスト化
                tags = [t.strip() for t in re.split(r'[/,]', tags_raw) if t.strip()]
                
                # 選択した気分が含まれているか、またはタグに含まれているか（部分一致も考慮）
                if mood in tags or any(mood in t for t in tags):
                    match_score += 5

                # --- 最終スコアの計算 ---
                match_score > 0
                    # 過去の選択回数による加点
                past_count = scores.get(dish_id, 0)
                final_score = match_score + past_count
                    
                    # 【重要】最近食べたIDがあれば大幅減点して下位へ飛ばす
                if dish_id in recent_dishes:
                        final_score -= 1000
                    
                all_recipes.append({
                        'id': dish_id,
                        'name': name,
                        'final_score': final_score,
                        'ai_comment': "" 
                    })

    except Exception as e:
        print(f"Error in recommend.py: {e}")

    # スコアが高い順に並び替え
    sorted_results = sorted(all_recipes, key=lambda x: x['final_score'], reverse=True)
    
    # 上位5件を返す
    return sorted_results[:10]