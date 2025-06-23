<!-- ============================================================
  Project Image
 ============================================================ -->
<div align=center>
  <img
    src='docs/image/demo.gif'
    alt='Project Image.'
    width=500
  />
</div>

<!-- ============================================================
  Overview
 ============================================================ -->
# :book:Overview

<!-- [![English](https://img.shields.io/badge/English-018EF5.svg?labelColor=d3d3d3&logo=readme)](./README.md) -->
<!-- [![Japanese](https://img.shields.io/badge/Japanese-018EF5.svg?labelColor=d3d3d3&logo=readme)](./README_JA.md) -->
[![Japanese](https://img.shields.io/badge/Japanese-018EF5.svg?labelColor=d3d3d3&logo=readme)](./README.md)
[![license](https://img.shields.io/github/license/r-dev95/pyside-thread-demo)](./LICENSE)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

[![Python](https://img.shields.io/badge/Python-3776AB.svg?labelColor=d3d3d3&logo=python)](https://github.com/python)
[![Sphinx](https://img.shields.io/badge/Sphinx-000000.svg?labelColor=d3d3d3&logo=sphinx&logoColor=000000)](https://github.com/sphinx-doc/sphinx)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?labelColor=d3d3d3&logo=pytest)](https://github.com/pytest-dev/pytest)
[![Pydantic](https://img.shields.io/badge/Pydantic-ff0055.svg?labelColor=d3d3d3&logo=pydantic&logoColor=ff0055)](https://github.com/pydantic/pydantic)
[![Pyside](https://img.shields.io/badge/Pyside-neogreen.svg?labelColor=d3d3d3&logo=qt)](https://www.qt.io/qt-for-python)

本リポジトリでは、pysideの`QThread`を用いたGUIアプリのデモを示します。

下記のことを意識して実装しています。

- UI処理とロジック処理の分離
- 実装を最小限にスレッドを増やせる
- 循環参照しないようにする

<!-- ============================================================
  Features
 ============================================================ -->
## :desktop_computer:Features

<div align=center>
  <img
    src='docs/image/app.png'
    alt='App Home Page.'
    width=500
  />
</div>

|項目                          |機能                              |
| ---                          | ---                              |
|スタートボタン                |スレッド処理を開始。              |
|ストップボタン                |スレッド処理を停止。              |
|自動スクロールチェックボックス|ログ領域の自動スクロールのON/OFF。|
|ログ表示領域                  |ログの表示。                      |

<!-- ============================================================
  Usage
 ============================================================ -->
## :keyboard:Usage

### Install

```bash
git clone https://github.com/r-dev95/pyside-thread-demo.git
```

### Build virtual environment

`uv`がインストールされていることが前提です。

pythonの開発環境がまだ整っていない方は、[こちら](https://github.com/r-dev95/env-python)。

```bash
cd pyside-thread-demo/
uv sync
```

### Run

```bash
cd src
uv run python app.py
```

<!-- ============================================================
  Structure
 ============================================================ -->
## :bookmark_tabs:Structure

<div align=center>
  <img
    src='docs/image/classes.png'
    alt='classes.'
  />
</div>

### MessageMixin

下記、機能を定義するためのメソッドを持つだけのクラスです。

実際の処理は子クラスに実装します。

- `Router`クラスを介して、別スレッドへメッセージを送信する機能 (`send_msg`)
- `Router`クラスを介して、別スレッドからメッセージを受信する機能 (`receive_msg`)

### Worker (QThread, MessageMixin)

- `QThread`を用いたスレッドの基本機能 (ex. `run`)

    `QThread`を用いたスレッド実装方法が分からない方は[こちら](#qthreadを用いたスレッドの実装方法)

### Router (Worker)

- スレッド間のメッセージ通信を行うスレッドの登録機能 (`register_thread`)
- 各スレッド間のメッセージ通信を制御する機能 (`route_msg`)

### 実装方法

#### スレッドクラス

- `Worker`クラスを継承したクラスを実装
- `thread_id`クラス変数にスレッドIDを定義
- `task`メソッドにスレッドの処理を実装
- `receive_msg`メソッドにメッセージ受信時の処理を実装

#### メインスレッドクラス (MainWindow)

- `send_msg`メソッドにメッセージ送信時の処理を実装
- `receive_msg`メソッドにメッセージ受信時の処理を実装
- `Router`クラスにメインスレッドを含む各スレッドを登録する処理を実装 (`setup`を参照)
- メインスレッドを含む各スレッドの`sig_send`シグナルと`Router`クラスの`route_msg`スロットを接続 (`setup`を参照)
- `Router`及びメインスレッドを除くスレッドを開始(停止)する機能を実装

### 基本知識

#### `QThread`を用いたスレッドの実装方法

```python
import sys
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QApplication, QWidget

class Thread(QThread):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.is_running = True

    def run(selff):
        while self.is_running:
            # スレッドの処理を記述

class MainWindow(QWidget):
    def __init__(self):
        self.thread = Thread(parent=self)

        # スレッドの開始 -> runメソッドが呼ばれる
        self.thread.start()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
```

`QThread`を用いたスレッドは上記のように実装する。

- メインスレッドのクラス内でスレッドクラスをインスタンス化し、インスタンス変数に代入する。
- `.start`でスレッドを開始され、スレッドクラスの`run`メソッドが呼ばれる。

<!-- ============================================================
  License
 ============================================================ -->
## :key:License

本リポジトリは、[MIT License](LICENSE)に基づいてライセンスされています。
