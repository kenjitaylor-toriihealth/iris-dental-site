# 計測設計（Measurement plan）

最終目標: **オンライン予約数を増やす**。サイトの役割は「見つけてもらう → 不安を解消する → 予約ボタンを押してもらう」。

## 指標（KPI）

| 段階 | 指標 | データの場所 | 備考 |
|---|---|---|---|
| ゴール | 月間予約数（新患／再来） | IntakeQ | 最重要。毎月手で数えて記録 |
| ゴール | 予約完了率 = 予約数 ÷ book_click | IntakeQ + GA4 | 予約ページで離脱していないか |
| 行動 | `book_click` 件数 | GA4（GTM 経由） | どのボタンか（link_location）も見る |
| 行動 | 予約クリック率 = book_click ÷ セッション | GA4 | サイトの説得力の指標 |
| 行動 | `phone_click`, `book_medical_click` | GA4 | 電話は補助的な指標 |
| 集客 | セッション、ユーザー（新規） | GA4 | チャネル別（Organic Search / Direct / Referral / Social / GBP） |
| 集客 | 表示回数・クリック・CTR・平均掲載順位、主な検索語句 | Google Search Console | 例: "english speaking dentist camp zama" |
| 集客 | プロフィール閲覧、ウェブサイトクリック、ルート検索、通話 | Google ビジネスプロフィール | 地域検索で最も効く |
| 信頼 | 口コミ件数・平均評価 | Google ビジネスプロフィール | |

目標値は最初の1〜2か月をベースラインにして決める。

## イベント（js/site.js が dataLayer に送るもの）

| イベント名 | いつ | パラメータ |
|---|---|---|
| `book_click` | irisdental.intakeq.com/booking へのリンクをクリック | `link_location`（hero, header, footer, mobile-bar, home-cta など）, `link_text`, `page_path` |
| `book_medical_click` | toriihealth.intakeq.com へのリンクをクリック | 同上 |
| `phone_click` | `tel:` リンクをクリック | 同上 |

`link_location` はHTMLの `data-cta` 属性の値。新しい予約ボタンには必ず付ける。

## Google Tag Manager の設定（GTM-TZVKB3WL）

サイト側のタグは設置済み。Tag Manager の管理画面で以下を設定する。

1. **Google タグ**: GA4 の測定ID（G-XXXXXXX）、トリガー = All Pages（Initialization でも可）
2. **データレイヤー変数**: `link_location`, `link_text`, `page_path`（変数名と同じキー）
3. **トリガー**: カスタムイベント `book_click` / `book_medical_click` / `phone_click`（3つ）
4. **タグ**: 「Google アナリティクス: GA4 イベント」を3つ。イベント名は上と同じ。イベントパラメータに `link_location`, `link_text` を追加
5. プレビューモードでボタンを押し、イベントが届くことを確認 → 公開
6. GA4 管理画面:
   - `book_click` と `phone_click` を「キーイベント」に設定
   - カスタム定義で `link_location` をイベントスコープのカスタムディメンションとして登録（レポートで使うため）
   - データ保持期間を 14 か月に変更（前年比較のため）
7. Google Search Console にドメインを登録し、`https://iris-dental-medical.com/sitemap.xml` を送信。GA4 と連携する

## UTM（流入元の付け方）

外部に貼るサイトのリンクには UTM を付ける。すべて小文字・ハイフン区切り。

| 貼る場所 | URL の例 |
|---|---|
| Google ビジネスプロフィールの「ウェブサイト」 | `https://iris-dental-medical.com/?utm_source=google&utm_medium=organic&utm_campaign=gbp` |
| Facebook グループ等への投稿 | `...?utm_source=facebook&utm_medium=social&utm_campaign=2026-12-checkup` |
| Torii Health のサイトからのリンク | `...?utm_source=toriihealth&utm_medium=referral&utm_campaign=partner` |
| チラシ・院内ポスターの QR コード | `...?utm_source=flyer&utm_medium=qr&utm_campaign=camp-zama-2026` |

## 既知の限界

- 予約は IntakeQ（別ドメイン）で完了するため、GA4 では「予約完了」を直接見られない。毎月 IntakeQ の予約数を手で記録し、`book_click` と突き合わせる。
- 将来の改善案: IntakeQ の予約ウィジェットを自サイト内に埋め込めるか、または予約完了時の計測（GTM/GA4）に対応しているかを確認する（docs/backlog.md）。
