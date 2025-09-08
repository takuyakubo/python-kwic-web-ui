# Python KWIC Web UI

Python KWIC (Key Word In Context) ライブラリのシンプルなWeb UIです。

## 概要

このプロジェクトは、[mattbriggs/KWIC](https://github.com/mattbriggs/KWIC) ライブラリを使用してテキスト内のキーワードを文脈と共に検索・表示するWebアプリケーションです。

## 機能

- テキストエリアにテキストを入力
- キーワードを指定してKWIC分析を実行
- キーワードの前後の文脈と共に結果を表示
- レスポンシブなWebデザイン
- リアルタイムでの結果表示

## 必要要件

- Python 3.7+
- Flask
- KWIC ライブラリ

## インストール

1. リポジトリをクローン:
```bash
git clone https://github.com/takuyakubo/python-kwic-web-ui.git
cd python-kwic-web-ui
```

2. 必要なパッケージをインストール:
```bash
pip install -r requirements.txt
```

## 使用方法

1. アプリケーションを起動:
```bash
python app.py
```

2. ブラウザで `http://localhost:5000` にアクセス

3. テキストエリアに分析したいテキストを入力

4. 検索したいキーワードを入力

5. 「分析実行」ボタンをクリック

6. 結果が表示されます

## API エンドポイント

### POST /analyze
テキストのKWIC分析を実行します。

**リクエスト:**
```json
{
  "text": "分析対象のテキスト",
  "keyword": "検索キーワード"
}
```

**レスポンス:**
```json
{
  "success": true,
  "results": [
    {
      "left_context": "キーワード前の文脈",
      "keyword": "キーワード",
      "right_context": "キーワード後の文脈",
      "line_number": 1
    }
  ],
  "total_matches": 1
}
```

### GET /health
ヘルスチェック用エンドポイント

## 使用例

### 入力例:
- **テキスト:** "This is a sample text. The text contains many words. Text analysis is useful."
- **キーワード:** "text"

### 出力例:
```
This is a sample [text]. The [text] contains many words. [Text] analysis is useful.
```

## 開発

開発モードで起動する場合:
```bash
export FLASK_ENV=development
python app.py
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 参考

- [Original KWIC Library by mattbriggs](https://github.com/mattbriggs/KWIC)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 貢献

プルリクエストやイシューの報告を歓迎します。
