# game-idea-researcher

実際のプレイヤー需要・コミュニティトレンド・実績あるインディーゲームのビジネスモデルに基づいて、ニッチなインディーゲームアイデアをリサーチする Claude Code スキルです。

## できること

スキルを呼び出すと、以下の処理を実行します。

1. 対象年とゲームコンセプトを（日本語で）質問する
2. Reddit のゲームコミュニティから不満・要望投稿を取得する
3. Hacker News からエンゲージメントの高いゲームリリース情報を取得する
4. Indie Hackers から収益ベンチマークと収益化戦略を検索する
5. 調査結果を統合し、3〜5 件のニッチなゲームアイデア案を提示する
6. 構造化レポートを `reports/{year}/{YYYYMMDD}/{HHMMSS}.md` に保存する

各提案には、収益化プラン・マーケティング方針・5 軸スコアカードが含まれます：
実現可能性 / 開発期間 / 収益性 / 競合優位性 / 小規模チーム適性

## ディレクトリ構成

```
.
├── SKILL.md                          # スキル定義: ワークフロー手順のみ
├── scripts/
│   ├── fetch_reddit.py               # 16 個のゲーム系サブレディットから投稿を取得
│   ├── fetch_hn.py                   # HN Algolia API 経由でゲーム投稿を取得
│   ├── fetch_indiehackers.py         # プレースホルダー（IH 調査は WebSearch を使用）
│   └── analyze_data.py               # Reddit + HN の出力をまとめてサマリーを生成
├── references/
│   ├── reddit-research.md            # Reddit データの読み方
│   ├── hn-research.md                # HN データの読み方
│   ├── indiehackers-research.md      # Indie Hackers 向け WebSearch クエリ
│   ├── synthesis-criteria.md         # 提案に値するギャップの判断基準
│   ├── monetization-strategies.md    # プラットフォーム・対象読者別の収益化オプション
│   ├── marketing-strategies.md       # フェーズ別マーケティングチャネル
│   └── evaluation-rubric.md          # 5 軸スコアリング基準（各軸 1〜5 点）
└── reports/                          # 生成レポート（git 管理外）
    └── {year}/{YYYYMMDD}/{HHMMSS}.md
```

## スクリプト

すべてのスクリプトは Python 標準ライブラリのみを使用しており、追加インストールは不要です。

| スクリプト | 目的 | 主なオプション |
|-----------|------|--------------|
| `fetch_reddit.py` | 16 個のゲーム系サブレディットからトップ投稿を取得 | `--year`, `--keywords`, `--limit` |
| `fetch_hn.py` | Algolia API 経由で HN のゲーム投稿を取得 | `--year`, `--keywords`, `--min-points` |
| `fetch_indiehackers.py` | Firebase REST API 経由で Indie Hackers の投稿を取得 | `--year`, `--rolling`, `--limit`, `--min-replies` |
| `analyze_data.py` | Reddit + HN + IH の JSON をマージしてマークダウンサマリーを生成 | `--reddit`, `--hn`, `--ih`, `--game-overview` |

### クイックテスト

```bash
python scripts/fetch_reddit.py --year 2025 --output /tmp/reddit.json
python scripts/fetch_hn.py --year 2025 --output /tmp/hn.json
python scripts/fetch_indiehackers.py --year 2025 --output /tmp/ih.json
python scripts/analyze_data.py --reddit /tmp/reddit.json --hn /tmp/hn.json --ih /tmp/ih.json --output /tmp/summary.md
```

## データソース

| ソース | アクセス方法 | 提供される情報 |
|--------|------------|--------------|
| Reddit | 公開 JSON API（認証不要） | プレイヤーの不満・機能要望・課金への不満 |
| Hacker News | Algolia Search API（認証不要） | インディーゲームのリリース情報・収益議論・技術的アプローチ |
| Indie Hackers | WebSearch（`site:indiehackers.com`） | 収益ベンチマーク・収益化戦略・個人開発者の成功事例 |

## 出力レポート構成

```
reports/{year}/{YYYYMMDD}/{HHMMSS}.md
├── 元のプロンプト
├── ゲーム概要
├── リサーチサマリー（Reddit / HN / Indie Hackers）
├── プレイヤーの主要な不満点
├── ゲームアイデア提案（3〜5 案）
│   ├── コンセプト + コアループ + 独自の切り口
│   ├── 根拠（シグナル強度ラベル付き）
│   ├── 収益化プラン
│   ├── マーケティングプラン
│   └── 5 軸スコアカード
├── 収益化戦略概要
├── マーケティング戦略概要
├── 競合状況
└── 推奨する次のステップ
```
