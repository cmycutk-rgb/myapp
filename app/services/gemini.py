from google import genai
import os
#AIzaSyBjWffPLYdGk_f1mqh5lOFFBgSTAASE1ag

def generate_single_comment(dish_name, month, mood):
    client = genai.Client(api_key="AIzaSyBjWffPLYdGk_f1mqh5lOFFBgSTAASE1ag".strip())
    
    prompt = f"""
    あなたは料理の背景に詳しいコンシェルジュです。「{dish_name}」について詳しく教えてください。
    
    【内容】
    - {month}月の旬の食材（具体的な野菜名など）がどう活かされているか。
    - 「{mood}」という気分の時に、この料理の味や食感がどう癒やしてくれるか。
    - プロが教える、より美味しく食べるための一工夫。
    - 必ず、栄養素面でこの料理がいい理由を一文入れてください。
    
    200文字程度で、温かみのある言葉で語ってください。
    """
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Gemini Error: {e}")
        return f"{dish_name}は、季節にぴったり！甘くておいしいでしょう！楽しんでくださいね！"