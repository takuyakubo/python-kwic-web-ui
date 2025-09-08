from flask import Flask, render_template, request, jsonify
import kwic

app = Flask(__name__)

@app.route('/')
def index():
    """メインページを表示"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    """テキストのKWIC分析を実行"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        keyword = data.get('keyword', '')
        
        if not text or not keyword:
            return jsonify({'error': 'テキストとキーワードの両方が必要です'}), 400
        
        # KWICライブラリを使用してキーワードインコンテキスト分析を実行
        kwic_result = kwic.kwic(text, keyword)
        
        # 結果を整形
        results = []
        for item in kwic_result:
            results.append({
                'left_context': item.get('left', ''),
                'keyword': item.get('keyword', ''),
                'right_context': item.get('right', ''),
                'line_number': item.get('line_number', 0)
            })
        
        return jsonify({
            'success': True,
            'results': results,
            'total_matches': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': f'エラーが発生しました: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """ヘルスチェック用エンドポイント"""
    return jsonify({'status': 'OK', 'message': 'KWIC Web UI is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
