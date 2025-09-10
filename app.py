from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

class SimpleKWIC:
    """シンプルなKWIC (Key Word In Context) 実装"""
    
    @staticmethod
    def kwic(text, keyword, context_size=50):
        """
        テキスト内でキーワードを検索し、前後の文脈と共に返す
        
        Args:
            text (str): 検索対象のテキスト
            keyword (str): 検索キーワード
            context_size (int): 前後の文脈の文字数
            
        Returns:
            list: マッチした結果のリスト
        """
        results = []
        
        # テキストを行に分割
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # 大文字小文字を無視してキーワードを検索
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            matches = pattern.finditer(line)
            
            for match in matches:
                start_pos = match.start()
                end_pos = match.end()
                
                # 前後の文脈を取得
                left_start = max(0, start_pos - context_size)
                right_end = min(len(line), end_pos + context_size)
                
                left_context = line[left_start:start_pos]
                matched_keyword = line[start_pos:end_pos]
                right_context = line[end_pos:right_end]
                
                # 文脈の前後に省略記号を追加（必要に応じて）
                if left_start > 0:
                    left_context = "..." + left_context
                if right_end < len(line):
                    right_context = right_context + "..."
                
                results.append({
                    'left_context': left_context.strip(),
                    'keyword': matched_keyword,
                    'right_context': right_context.strip(),
                    'line_number': line_num,
                    'full_line': line.strip()
                })
        
        return results

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
        context_size = data.get('context_size', 50)
        
        if not text or not keyword:
            return jsonify({'error': 'テキストとキーワードの両方が必要です'}), 400
        
        if not text.strip():
            return jsonify({'error': 'テキストが空です'}), 400
            
        if not keyword.strip():
            return jsonify({'error': 'キーワードが空です'}), 400
        
        # KWICライブラリを使用してキーワードインコンテキスト分析を実行
        kwic_analyzer = SimpleKWIC()
        kwic_result = kwic_analyzer.kwic(text, keyword, context_size)
        
        # 結果を整形
        results = []
        for item in kwic_result:
            results.append({
                'left_context': item.get('left_context', ''),
                'keyword': item.get('keyword', ''),
                'right_context': item.get('right_context', ''),
                'line_number': item.get('line_number', 0),
                'full_line': item.get('full_line', '')
            })
        
        return jsonify({
            'success': True,
            'results': results,
            'total_matches': len(results),
            'keyword_searched': keyword
        })
        
    except Exception as e:
        return jsonify({'error': f'エラーが発生しました: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """ヘルスチェック用エンドポイント"""
    return jsonify({'status': 'OK', 'message': 'KWIC Web UI is running'})

@app.route('/api/info')
def api_info():
    """API情報を返す"""
    return jsonify({
        'name': 'KWIC Web UI',
        'version': '1.0.0',
        'description': 'Key Word In Context analysis tool',
        'endpoints': {
            '/': 'Web UI',
            '/analyze': 'POST - Analyze text for keywords',
            '/health': 'GET - Health check',
            '/api/info': 'GET - API information'
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
