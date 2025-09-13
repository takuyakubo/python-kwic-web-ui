
import csv
import json
import os
import re
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

# 対訳コーパスCSVを2カラム（日本語・英語）で返すAPI
@app.route('/corpus', methods=['GET'])
def get_corpus():
    """
    対訳コーパスCSVを2カラム（日本語・英語）で返すAPI
    """
    filename = request.args.get('filename', 'sample_corpus.csv')
    keyword = request.args.get('keyword', '').strip()
    samples_dir = os.path.join(os.path.dirname(__file__), 'samples')
    fpath = os.path.join(samples_dir, filename)
    wordmap_path = os.path.join(samples_dir, 'wordmap.json')
    if not os.path.exists(fpath):
        return jsonify({'error': 'ファイルが存在しません'}), 404
    # enWords取得
    enWords = []
    if keyword and os.path.exists(wordmap_path):
        with open(wordmap_path, encoding='utf-8') as wf:
            wordmap = json.load(wf)
            enWords = wordmap.get(keyword, [])
    context_size = 50  # 適度な文脈サイズ
    corpus = []
    with open(fpath, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                jp = row[0]
                en = row[1]
                if not keyword:
                    # キーワード未指定なら全件返す
                    corpus.append({
                        'jp': jp,
                        'en': en,
                        'jp_kwic': [],
                        'en_kwic': []
                    })
                else:
                    # KWICで日本語・英語両方を判定
                    jp_kwic = SimpleKWIC.kwic(jp, keyword, context_size)
                    en_kwic_results = []
                    for enWord in enWords:
                        en_kwic_results.extend(SimpleKWIC.kwic(en, enWord, context_size))
                    # どちらかのkwic結果が空でなければ返す
                    if (jp_kwic and len(jp_kwic) > 0) or (en_kwic_results and len(en_kwic_results) > 0):
                        corpus.append({
                            'jp': jp,
                            'en': en,
                            'jp_kwic': jp_kwic,
                            'en_kwic': en_kwic_results
                        })
    return jsonify({'corpus': corpus, 'filename': filename})

# 静的ファイル（samples/wordmap.json等）を提供するルート
@app.route('/samples/<path:filename>')
def serve_sample_file(filename):
    samples_dir = os.path.join(os.path.dirname(__file__), 'samples')
    return send_from_directory(samples_dir, filename)

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
        lines = text.split('\n')
        for line_num, line in enumerate(lines, 1):
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            matches = pattern.finditer(line)
            for match in matches:
                start_pos = match.start()
                end_pos = match.end()
                left_start = max(0, start_pos - context_size)
                right_end = min(len(line), end_pos + context_size)
                left_context = line[left_start:start_pos]
                matched_keyword = line[start_pos:end_pos]
                right_context = line[end_pos:right_end]
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

@app.route('/samples', methods=['GET'])
def get_samples():
    """サンプルテキストファイル一覧と内容を返すAPI"""
    samples_dir = os.path.join(os.path.dirname(__file__), 'samples')
    sample_files = [f for f in os.listdir(samples_dir) if f.endswith('.txt') or f.endswith('.csv')]
    samples = []
    for fname in sample_files:
        fpath = os.path.join(samples_dir, fname)
        with open(fpath, encoding='utf-8') as f:
            content = f.read()
        samples.append({
            'filename': fname,
            'label': fname.replace('.txt', ''),
            'content': content
        })
    return jsonify({'samples': samples})

@app.route('/')
def index():
    """
    メインページを表示
    """
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    """
    テキストのKWIC分析を実行
    """
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
    """
    ヘルスチェック用エンドポイント
    """
    return jsonify({'status': 'OK', 'message': 'KWIC Web UI is running'})

@app.route('/api/info')
def api_info():
    """
    API情報を返す
    """
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
    app.run(debug=True, host='0.0.0.0', port=5050)
