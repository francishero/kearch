# keach

## 初期化
1. python3 setup_database.py でデータベースを作成する
2. python3 average_document.py seed_url_list で平均文書を作成する
3. python3 crawler.py seed_url_list でクローラを走らせる
4. python3 flask_main.py で http://localhost:5000/ にアプリケーションが開く

## 目標
- クローリング速度0.1second/page
- 保存ページ数1000万ページ
- 10日ぐらいでindexの中のすべてのページを更新
- twitterや2chなどの価値の少ない情報、時代によって価値の変わりやすい情報を保持しない
- LDA topicモデルでページをフィルタリングする
- pagerankでページに順位をつける

## Todo
- LDA topic model + SGD classifier を用いたクラスタ分類
  https://www.slideshare.net/tsubosaka/tokyotextmining
- Mecab?を使った日本語対応
- tfidf以外の優先度の導入。単語の共起確率を用いてまともだと考えられる文書と比べる。
- Pagerankの導入
- html以外のコンテンツを弾く
- アクセスログを取る
- クローラの優先度をアクセスログにしたがって変える
- pdfファイルに対応する
- クローラの高速化。不要なファイルをダウンロードしないとか。
- linkをInt型に変換してデータベースに保存する
- insert処理が遅すぎる
  indexを外してinsertしたうえでindex構築する必要がある

## Done
- Computer Science に関する記事を100本、それ以外の記事を100本記録する
- readbilityを使った本文取得の高速化
- とりあえずpdfは弾いた
- プロセス並列化によるクローラの高速化
- tfidfテーブルの圧縮（登録する単語を一ページあたり上位100語に限定)
- png,jpg,PDF,jsonを弾いた
- crawlerテーブルはurl indexedのものとlast_date indexedのものの2つを作り検索の高速化をする
- 同一ドメインへの連続アクセスを避ける  
  last_dateに乱数を足して対応  
- クロールするドメインにできるだけ多様性をもたせる  
  last_dateに乱数を足して対応  
- ページのダウンロードに時間制限を設ける
  register処理にも時間制限を設けた
- 複数INSERTをまとめる
  やったけどあんまり効果なし
- 結果からJaveScriptの部分を除く
- 言語判定を行う
  http://lab.astamuse.co.jp/entry/try-polyglot
- JaveScriptをscriptタグを検出して除く
- 外部サイトへのリンクを重要視する

## クローラの速度
今のところ1second/1pageぐらい
