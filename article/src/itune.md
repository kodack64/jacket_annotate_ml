# iTune Search API

---

consumer keyなどがなく無料枠で使えることから、iTune Search APIはサービスとして飛びぬけています。しかし、あまりにドキュメントが情報不足などころか誤っている箇所すらあるため、全容が分かっていません。ネットにある情報も断片的だったり、本ドキュメントの単なる翻訳だったりします。使用感を纏めておきます。

APIの公式ページは https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/ にあります。

### 使い方

URLを叩くとjsonが帰ってきます。https://itunes.apple.com/search?term=君の知らない&media=music&country=JP で検索すれば正しい情報が返ってきます。日本語のクエリをしっかり受け付けるというのも地味ながら非常に優れた特徴です。以下が公式に乗っているパラメータリストです。スペースで区切るとand検索になります。詳細は隠しパラメータにて。

- term:検索したいワード
- country:JP一択
- lang:言語 ja_jp一択
- media:返答がほしいメディアの分類　今は全部music
- entity:mediaの詳細な分類　今はalbum
- limit:返ってくる結果の最大値　最大200
- attribute:検索ワードが検索する対象

### 取得できるメタ情報

アルバム名やアーティスト名に加え、ジャンル、値段、トラック数、発売日、発売国などのメタ情報が取得できます。発売国から意図しない検索結果を弾けたりするのはいいです。値段も他ではなかなか取得できない情報です。


### 巨大な画像の取得

リクエストを送って帰ってきたjsonにはいろいろな情報が含まれていますが、ジャケット画像のurlはartworkUrl100に入っています。名前の通り、100x100のジャケット画像なのですが、機械学習ではもう少し大きい画像を用いたいです。URLのアドレスは http://is4.mzstatic.com/image/thumb/Music/v4/hogehogehoge/source/100x100bb.jpg となっていますが、最後のあたりを変えてやれば170,225,600あたりは取得できます。従って http://is4.mzstatic.com/image/thumb/Music/v4/02/68/2a/02682ac8-9717-3550-2d39-9b653436d473/source/600x600bb.jpg を取ってくることで大きな画像が取得できます。

自身が使用した範囲では、画像ファイルに欠損のある楽曲はありませんでした。このあたりは流石にAppleという感じがあります。

### Rate limit

iTune Search APIはrate limitが明記されておらず、大量にアクセスするとレスポンスが遅くなって次第に403が変えるようになるという仕様になっています。非常に雑ですが自身が使用した範囲では以下のような感じです。

- 1時間に300アクセスぐらいしたあたりからレスが10秒～10分ぐらいになります。最初の数百アクセスは非常に高速です。
- 一度遅くなると少なくとも数時間はそのままです。
- 少なくとも数日待ったら戻ってました


### 隠し要素

iTune Search APIの最強にヤバイところは、ドキュメントに書かれていない隠し要素が大量にあります。精一杯オブラートに包んだ表現をすると、ファミコン初期のようなゲーム性が楽しめます。

##### 隠しattribute


attributeは検索する対象を指定するパラメータで、使えるattributeは指定したmediaに依存しています。mediaをmusicにした場合に使えるattributeはドキュメントで7個が紹介されていますが、実際には[http://jmblog.jp/archives/798](http://jmblog.jp/archives/798) のサイト様の調査により
- "albumTerm","mixTerm", "genreTerm", "completeTitle", "allTitle", "composerTerm", "genreIndex", "flavor", "tier", "musicTrackTerm", "artistAndComposer", "allArtistNames", "songTerm", "releaseDate", "ratingIndex", "artistTerm", "completePlaylistTitle", "ringtone", "iMixTerm", "matchName"

の20個の隠しパラメータが指定でき、少なくともエラー無く帰ってきます。しかし、attributeが何に対応しているのか全く謎なので、使えるのはごく一部です。特になんちゃらindex系は何を指定すれば良いのか本当に謎です。

##### 最大検索件数を超える検索

limitの最大件数が200件なので、200件目より先のアイテムは取得できません。これはoffsetという隠しパラメータで回避できます。offsetを指定することでoffset番目からlimit個返るようになります。これを利用することで、rate limitの範囲内であれば全検索結果を取得できます。

https://itunes.apple.com/search?term=君の知らない&media=music&country=JP&offset=1

とoffsetを追加すると、offsetがない場合に比べ最初のアイテムがなくなっているのが分かると思います。

##### ジャンル

attributeの中にはもともとgenreIndexなるものがあります。itune genreとかで検索するとhttps://affiliate.itunes.apple.com/resources/documentation/genre-mapping/ のページが出てくるので、数字や文字で検索できるのかと思いきや、出来ません。

上記のジャンルIDで検索したい場合は、genreIdをattributeではなくパラメータとして使用します。

例として、Animeを指定すれば https://itunes.apple.com/search?term=hope&media=music&entity=album&country=JP&limit=10&lang=ja_jp&genreId=29 返ってくるのはLiSA Rising Hope - EPであり、J-Popを指定すれば https://itunes.apple.com/search?term=hope&media=music&entity=album&country=JP&limit=10&lang=ja_jp&genreId=27 で返ってくるのは山下達郎 Ray Of Hopeになります。ただし、優先度が変化されるだけで記載されているジャンルだけがフィルターされて返ってくるわけではないです。特定ジャンルをフィルターしたい場合はレスポンスのgenreTermを見て指定のジャンルだけを抜き出しましょう。

### たぶん出来ないこと

- ソートの変更(sortパラメータの指定はできるが、結果に変化はない)
- 検索ワードを指定しない、指定ジャンルでの全列挙(誰か出来たら教えてください)
- or検索
- 複数のattributeのand検索
- 発表年での検索
