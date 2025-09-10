# Python KWIC Web UI

シンプルで使いやすいKWIC (Key Word In Context) 分析のためのWeb UIです。

## 概要

このプロジェクトは、テキスト内のキーワードを文脈と共に検索・表示するWebアプリケーションです。独自のKWIC実装を使用しており、外部ライブラリへの依存を最小限に抑えています。

## 機能

- **テキスト分析**: テキストエリアにテキストを入力してキーワードを検索
- **文脈表示**: キーワードの前後の文脈と共に結果を表示
- **文脈サイズ調整**: キーワード前後の文字数を調整可能
- **大文字小文字無視**: 大文字小文字を区別しない検索
- **行番号表示**: マッチした行の番号を表示
- **レスポンシブデザイン**: モバイル対応のWebインターフェース
- **REST API**: プログラムからも利用可能なAPIエンドポイント

## 必要要件

- Python 3.7+
- Flask
- requests（demo.py用）

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

### Webアプリケーション

1. アプリケーションを起動:
```bash
python app.py
```

2. ブラウザで `http://localhost:5000` にアクセス

3. テキストエリアに分析したいテキストを入力

4. 検索したいキーワードを入力

5. 文脈サイズを調整（オプション）

6. 「分析実行」ボタンをクリック

7. 結果が表示されます

### コマンドラインからのAPIテスト

```bash
python demo.py
```

## API エンドポイント

### POST /analyze
テキストのKWIC分析を実行します。

**リクエスト:**
```json
{
  "text": "分析対象のテキスト",
  "keyword": "検索キーワード",
  "context_size": 50
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
      "line_number": 1,
      "full_line": "完全な行のテキスト"
    }
  ],
  "total_matches": 1,
  "keyword_searched": "検索したキーワード"
}
```

### GET /health
ヘルスチェック用エンドポイント

### GET /api/info
API情報を取得

## 使用例

### 入力例:
- **テキスト:** "This is a sample text. The text contains many words. Text analysis is useful."
- **キーワード:** "text"
- **文脈サイズ:** 50

### 出力例:
```
1. This is a sample [text]. The [text] contains many words. [Text] analysis is useful.
   (行 1) マッチ 1

2. This is a sample [text]. The [text] contains many words. [Text] analysis is useful.
   (行 1) マッチ 2

3. This is a sample [text]. The [text] contains many words. [Text] analysis is useful.
   (行 1) マッチ 3
```

## 特徴

- **自立性**: 外部のKWICライブラリに依存せず、独自の実装を使用
- **柔軟性**: 文脈サイズを自由に調整可能
- **使いやすさ**: 直感的なWebインターフェース
- **プログラマブル**: REST APIで自動化可能
- **軽量**: 最小限の依存関係

## 開発

開発モードで起動する場合:
```bash
export FLASK_ENV=development
python app.py
```

または

```bash
FLASK_ENV=development python app.py
```

## プロジェクト構造

```
python-kwic-web-ui/
├── app.py                 # メインのFlaskアプリケーション
├── requirements.txt       # 依存関係
├── templates/
│   └── index.html        # Web UIのHTMLテンプレート
├── demo.py               # APIデモスクリプト
├── .gitignore           # Git除外設定
└── README.md            # このファイル
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 参考

- [Original KWIC concept by mattbriggs](https://github.com/mattbriggs/KWIC)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 貢献

プルリクエストやイシューの報告を歓迎します。以下のような改善を考えています：

- [ ] ファイルアップロード機能
- [ ] 複数キーワードの同時検索
- [ ] 結果のエクスポート機能（CSV, JSON）
- [ ] 正規表現サポート
- [ ] ハイライト色のカスタマイズ
