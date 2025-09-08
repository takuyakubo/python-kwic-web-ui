#!/usr/bin/env python3
"""
KWIC Web UI Demo Script
簡単なデモンストレーション用スクリプト
"""

import requests
import json

def demo_kwic_api():
    """KWIC Web UI APIのデモンストレーション"""
    
    # デモ用のテキストとキーワード
    sample_text = """
    Python is a high-level programming language. 
    Python is easy to learn and use. 
    Many developers love Python because of its simplicity.
    Python has a rich ecosystem of libraries.
    The Python community is very supportive.
    """
    
    keyword = "Python"
    
    # APIエンドポイント
    url = "http://localhost:5000/analyze"
    
    # リクエストデータ
    data = {
        "text": sample_text,
        "keyword": keyword
    }
    
    try:
        print("KWIC Web UI API Demo")
        print("=" * 50)
        print(f"分析テキスト: {sample_text[:100]}...")
        print(f"検索キーワード: {keyword}")
        print("\nAPIリクエスト送信中...")
        
        # APIリクエスト送信
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            
            if result['success']:
                print(f"\n✅ 分析完了! {result['total_matches']} 件の一致が見つかりました")
                print("\n結果:")
                print("-" * 80)
                
                for i, match in enumerate(result['results'], 1):
                    left = match['left_context']
                    keyword_found = match['keyword']
                    right = match['right_context']
                    
                    print(f"{i:2d}. {left}[{keyword_found}]{right}")
                    if match.get('line_number'):
                        print(f"    (行 {match['line_number']})")
                    print()
            else:
                print(f"❌ エラー: {result.get('error', '不明なエラー')}")
        else:
            print(f"❌ HTTPエラー: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 接続エラー: アプリケーションが起動していることを確認してください")
        print("   python app.py を実行してからもう一度お試しください")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    demo_kwic_api()
