# EnvLogger (Environment Data Logger)

Raspberry Pi Pico を用いた、乾電池駆動・スタンドアロン型の環境データロガーシステム。
外部電源のない場所でも長期間稼働し、気象データ（温度・湿度・気圧）をmicroSDカードに記録し続けます。

## Features (機能)

* **3要素同時測定:** 温度(℃)・湿度(%)・気圧(hPa) を高精度に記録 (BME280使用)。
* **正確なタイムスタンプ:** 外部RTC (DS3231) により、電源オフ時も時刻を保持。
* **超省電力設計:** 測定時以外は Deep Sleep モードで待機し、単3電池3本で長期稼働を実現。
* **データ管理:** ログデータは月ごとにCSVファイル (`YYYY-MM.csv`) として自動分割・保存。

## Directory Structure (構成)

```text
.
├── src/                # ソースコード一式
│   ├── main.py         # メインプログラム
│   ├── bme280.py       # センサードライバ
│   ├── ds3231.py       # RTCドライバ
│   └── sdcard.py       # SDカードドライバ
├── docs/               # ドキュメント
│   └── specification.md # 詳細仕様書・配線図
└── README.md           # 本ファイル
```

## Quick Start (使い方)

1. **設置:**
   防水ケース等に入れ、直射日光の当たらない場所に設置します。
2. **起動:**
   電池ボックスのスイッチを **ON** にします。
3. **状態確認 (LED):**
   * **1回点滅:** システム起動
   * **3回点滅:** 測定＆SD書き込み成功 → スリープ開始 (正常)
   * **高速点滅:** エラー発生 (SDカード未挿入、配線不良、電池切れ等)
4. **データ回収:**
   任意のタイミングで電源を切り、SDカードをPCで読み込みます。

## Hardware Requirements

詳細な部品表や配線図は [docs/specification.md](docs/specification.md) を参照してください。

* Raspberry Pi Pico
* BME280 (I2C)
* DS3231 RTC (I2C)
* MicroSD Card Module (SPI)
* Power Source: DC 4.5V (AA Batteries x3 recommended)