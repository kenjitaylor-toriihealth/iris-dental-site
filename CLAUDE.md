# CLAUDE.md — Iris Dental Medical website

このファイルは、Claude がこのサイトを編集・分析するときの前提とルールです。作業の前に必ず読んでください。
公開URL: https://iris-dental-medical.com/

## ゴール

**最終目標は「オンライン予約数を増やすこと」。** すべての変更はこの目標に照らして判断する。

- North Star 指標: IntakeQ での月間予約数（新患／再来）
- 先行指標: `book_click`（予約ボタンのクリック）、予約クリック率 = book_click ÷ セッション
- 計測設計の詳細: `docs/analytics/measurement-plan.md`
- 毎月の振り返り: `docs/reports/monthly/`（手順は下の「月次レポート」）

## 対象患者と方針

- 対象は **アメリカの歯科保険を持つ患者のみ**（Camp Zama の SOFA 関係者・米軍家族・駐在者など）。日本の健康保険は扱わない。
- そのため **日本語ページは作らない**。サイトは英語（米国式の綴り: color, center など）。
- **予約はオンライン（IntakeQ）のみ。** 「電話で予約」を促す文言やボタンは作らない。電話番号は連絡先として掲載するだけ。迷ったら FAQ に誘導する。
- 料金の具体的な数字・保険の適用範囲は、クリニックの確認なしに掲載しない（詳細は IntakeQ の予約ページにある）。

## クリニック情報（正しい情報はここ。変わったらここも更新）

| 項目 | 内容 |
|---|---|
| 正式名 | Iris Dental Medical（アイリス歯科相武台前）。旧名 Iris Dental Care（2019年開業） |
| 住所 | Ishikawa Building 1F, 1-26-6 Sobudai, Minami-ku, Sagamihara, Kanagawa 252-0324（〒252-0324 神奈川県相模原市南区相武台1-26-6 石川ビル1F） |
| アクセス | Sōbudai-mae 駅から徒歩5分。Camp Zama Gate 4 の近く。向かいに有料駐車場（駐車券の割引なし） |
| 診療時間 | 火〜土 9:00–17:00／日・月 休診 |
| 祝日 | **時と場合による。「予約サイトで確認してください」と書く**（例: "Open on some Japanese national holidays — check the booking site."） |
| 予約URL | https://irisdental.intakeq.com/booking （旧 reserve.ne.jp は使わない） |
| 電話 | 046-244-5818（リンクは `tel:+81462445818`） |
| メール | irisdentalcaregate4@gmail.com |
| 対応する米国保険 | TRICARE, United Concordia, Cigna, Blue Cross Blue Shield, MetLife, Delta Dental, Aetna, Aetna International, GEHA。それ以外は要相談（基本的に不可） |
| 日本の保険 | 不可 |
| 強み | Invisalign 相談は無料（3Dスキャン付き）／CT・デジタルX線を院内に完備／完全個室の診療室が3室／すべて英語で対応 |
| 院長 | Azusa Kaneshima, DDS — Lead Dentist & Practice Director（DDS/DMD 表記は院長に最終確認） |
| 医科連携 | Torii Health（米国で研修を受けた医師。https://www.toriihealth.org ／予約 https://toriihealth.intakeq.com/booking） |

## ファイル構成

```
index.html  treatments.html  about.html  access.html  faq.html  blog.html  privacy.html  404.html
posts/                記事。新しい記事は posts/post-template.html をコピー
css/site.css          全ページ共通のスタイル（色・フォント・部品）
js/site.js            スマホメニュー、予約/電話クリックの計測（dataLayer）
images/               画像。og-image.jpg は SNS シェア用（1200×630）
sitemap.xml robots.txt _redirects    SEO と公開設定（_redirects は Netlify 用）
docs/                 社内用ドキュメント（公開しない）
tools/check_site.py   公開前チェック
```

- ビルド工程はない。**HTML ファイルそのものが正**。編集したらそのままアップロード。
- `docs/`, `tools/`, `CLAUDE.md`, `README.txt` は `_redirects` で公開サイトから 404 にしている。
- `Claude outputs/` フォルダは Claude アプリが自動で作るもの。サイトの一部ではない（.gitignore 済み）。

## 編集ルール

1. **全ページ共通のブロック**は、1ページを直したら全ページ同じように直す:
   - `<head>` 内の Google Tag Manager（GTM-TZVKB3WL）と `<body>` 直後の noscript
   - ヘッダー（`<header class="site-header">`）、フッター（`<footer class="site-footer">`）、スマホ下部バー（`.mobile-cta`）
   - `posts/` 内のページはパスが `../` 始まり、`404.html` は `/` 始まり
2. **予約リンク**には必ず `data-cta="場所の名前"` を付ける（例: `hero`, `header`, `footer`, `mobile-bar`, `home-cta`, `faq`）。月次レポートでどのボタンが効いているかを見るため。
3. **新しいページを作るとき**:
   - 一意の `<title>`（60字以内）と `<meta name="description">`（155字以内）
   - `<link rel="canonical">` と `og:url` / `og:image`
   - `sitemap.xml` に追加
   - ナビやフッターから辿れるようにする
   - 最後に CTA（予約ボタン）を置く
4. 診療時間・電話・保険リストなどの情報を変えるときは、`grep` で全ファイルを検索して全箇所を直す（index.html の構造化データ `openingHoursSpecification` も）。
5. 作業後は必ず `python3 tools/check_site.py` を実行し、エラー 0 にする。PC（1440px）とスマホ（390px）の表示も確認する。
6. サイトを変えたら `docs/changelog.md` に日付と内容を1行で記録する（数値の変化と結び付けるため）。
7. git の commit / push は、依頼されたときだけ行う。

## デザインシステム（Style A “Feels like home”）

- フォント: 見出し Lora（500/600、強調は italic）、本文 Poppins（400/500/600）
- 色: navy `#1F3D5C`（文字・メインボタン）、blue `#2A5A82`（アクセント）、本文 `#3E5468`、背景 cream `#F8F6F2`、sky `#EEF5F9` / `#D6E8F0`、pink `#F6E3E9`、カード枠 `#E6E1DA`
- 形: ボタンは pill（`border-radius: 999px`）、カード 24px、大きいパネル 32px、アイコンはアーチ型（`.icon-arch`）
- 装飾: 放射状の円（`.arc`）、ハイビスカス（`#iris-flower` を `<use>`）、ピンクの波（`.wave`）
- 部品のクラス: `.btn-primary` `.btn-light` `.btn-pink`／`.t-card`（治療カード）`.a-card`（治療詳細）`.fact`（強み）`.chip`／`.faq-item`（アコーディオン）／`.cta-panel`（最後の予約パネル）
- 新しい色やフォントは増やさない。`css/site.css` の `:root` の変数を使う。

## コンテンツのルール

- 文章は短く、具体的に。患者の不安（保険・言葉・費用・場所）に先に答える。
- 医療に関する記述は一般的で正確な内容にとどめ、**公開前に院長の確認を取る**。効果を保証する表現はしない。
- 口コミ・患者の声は本物だけ（本人の同意を得たもの、または Google の口コミ）。作らない。
- ストック写真を「当院の写真」として見せない。院内・スタッフ・外観は実際の写真を使う（`docs/photo-shot-list.md`）。
- 他社のロゴ（保険会社など）は使わず、名前をテキストで書く。

## 月次レポート（毎月）

1. 毎月1〜5日に、前月分のデータを `docs/analytics/exports/YYYY-MM/` に置く（取り出し方: `docs/analytics/exports/README.md`）。
2. Claude に「YYYY-MM の月次レポートを作って」と依頼する。Claude は:
   - `docs/reports/monthly/_template.md` をもとに `docs/reports/monthly/YYYY-MM.md` を作る
   - 前月・前年同月と比べ、`docs/changelog.md` の変更と結び付けて考察する
   - 次の1か月でやる改善を1〜3個提案する（`docs/backlog.md` から優先度順）
   - 同じ内容を claude.ai の Project「Website - Iris Dental Medical」にも保存する
3. 実行した改善は `docs/changelog.md` に記録する。

## 保留中（クリニックの確認待ち）

- 保険・支払いページ（保険会社名はFAQとHomeに掲載済み。詳細ページは保留）
- ブログの新規記事（現在は posts/cleanings-every-6-months.html の1本のみ）
- 写真の追加（`docs/photo-shot-list.md`）
- その他の改善候補: `docs/backlog.md`

## デプロイ

- README.txt 参照（Netlify にフォルダをアップロード、または GitHub 連携）。
- 公開後の確認: トップ・FAQ・予約ボタン、Google Tag Manager のプレビューでイベントが届くか、Search Console に sitemap.xml を送信。
