# ROS2_Speech_Action

Docker + ROS 2 (Humble) + Python で、音声認識と音声合成を試すプロジェクトです。

## 現時点の実装状況

- Docker 開発基盤
  - `Dockerfile`
  - `docker-compose.yml`
  - `.dockerignore`
  - `requirements.txt`
- ROS2 Python パッケージ雛形
  - `workspace/src/speech_action`
- 音声認識（単体）
  - `speech_recognition_server`
  - `speech_recognition_client`
  - 認識結果を `/speech` (`std_msgs/msg/String`) に publish
- 音声合成（単体）
  - `speech_synthesis_server`
  - `speech_synthesis_client`
  - `/speech` を subscribe して読み上げ

## ディレクトリ構成

```text
.
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
└── workspace/
    └── src/
        └── speech_action/
            ├── package.xml
            ├── setup.py
            ├── setup.cfg
            ├── resource/speech_action
            └── speech_action/
                ├── recognition.py
                ├── synthesis.py
                ├── speech_recognition_server.py
                ├── speech_recognition_client.py
                ├── speech_synthesis_server.py
                ├── speech_synthesis_client.py
                └── speech_client.py  # まだ未実装スタブ
```

## 前提

- Docker Desktop
- `docker compose` が利用可能

## 初期セットアップ

```bash
docker compose up -d --build
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && colcon build --symlink-install"
```

### ビルドで `error: option --editable not recognized` が出る場合

コンテナ内の `pip` が `torch` などと一緒に **setuptools を新しすぎる版へ上げる**と、`colcon build --symlink-install`（editable インストール）が壊れることがあります。

対処:

1. イメージを作り直す（`Dockerfile` で setuptools を Jammy 相当に固定済み）

```bash
docker compose build --no-cache
docker compose up -d
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && colcon build --symlink-install"
```

2. それでもダメなら、**symlink なし**でビルド（開発時の差分反映は `colcon build` の再実行で代替）

```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && colcon build"
```

---

## 音声認識の単体テスト手順

### 1) `/speech` を監視

```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 topic echo /speech"
```

### 2) 音声認識サーバ起動

```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 run speech_action speech_recognition_server"
```

### 3) 音声認識クライアント起動（トリガ）

```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 run speech_action speech_recognition_client"
```

### 成功条件

- クライアント側に `Recognized: ...` が表示される
- `/speech` の `echo` 側に同じ文字列が表示される

---

## 音声合成の単体テスト手順（A案: `/speech` 購読型）

### 1) 音声合成サーバ起動

```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 run speech_action speech_synthesis_server"
```

### 2) 合成クライアントから `/speech` に publish

```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 run speech_action speech_synthesis_client 'hello from ros2 speech synthesis'"
```

### 3) `ros2 topic pub` でも確認可能

```bash
docker compose exec ros2_dev bash -lc "source /opt/ros/humble/setup.bash && cd /root/ros2_ws && source install/setup.bash && ros2 topic pub -1 /speech std_msgs/msg/String \"{data: 'this is topic based synthesis test'}\""
```

### 成功条件

- サーバ側に `Spoken: ...` が表示される
- `mp3=/tmp/speech_action_tts/...` の出力先ログが表示される
- 環境が許せばスピーカから音声が出る

---

## 注意点

- macOS + Docker では、コンテナ内マイク入力とオーディオ出力の取り回しに制約があります。
- 音声が出ない場合でも、まずはログと生成された mp3 ファイルの存在で動作確認してください。
- `speech_client.py`（認識→合成の連携）は別ブランチで実装予定です。
