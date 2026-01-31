import os
import csv
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.recommend import get_recommendations
from app.services.log import save_log 
from app.services.gemini import generate_single_comment

bp = Blueprint('pages', __name__)

@bp.route('/')
def index():
    month = request.args.get('month')
    mood = request.args.get('mood')
    results = [] 
    
    if month and mood:
        # 1. おすすめリストを取得（ここではAIは呼ばない！）
        results = get_recommendations(month, mood, username=session.get('user'))
        # AIコメントを付ける処理をここから削除しました（検索を高速化）
        
    if not month: month = '1'
    if not mood: mood = '和食'
        
    is_searched = (len(results) > 0 or request.args.get('month') is not None)
    return render_template('index.html', results=results, month=month, mood=mood, searched=is_searched)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # デバッグ用：直接判定（CSVが壊れていてもログインできる）
        if username == "admin" and password == "1234":
            session['user'] = username 
            flash(f'ようこそ、{username}さん！')
            return redirect(url_for('pages.index'))
        
        flash('ユーザー名またはパスワードが違います')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('ログアウトしました')
    return redirect(url_for('pages.index'))

@bp.route('/select', methods=['POST'])
def select_dish():
    dish_id = request.form.get('dish_id')
    dish_name = request.form.get('dish_name')
    month = request.form.get('month', '1')
    mood = request.form.get('mood', '和食')
    username = session.get('user')

    if not username:
        return redirect(url_for('pages.login'))

    # 1. ログ保存
    save_log(username, dish_id, dish_name)

    # 2. 決定した1つの料理についてだけAIに聞く
    ai_description = generate_single_comment(dish_name, month, mood)

    # 3. 完了画面に渡す
    return render_template('complete.html', dish_name=dish_name, ai_description=ai_description)

@bp.route('/get_ai_comment')
def get_ai_comment():
    dish_name = request.args.get('dish_name')
    month = request.args.get('month')
    mood = request.args.get('mood')
    
    from app.services.gemini import generate_single_comment
    comment = generate_single_comment(dish_name, month, mood)
    
    return {"comment": comment} # JSONで返却