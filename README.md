
# Automatic creation of video with sound-aware scene merging

個人開発RPAプロジェクト。ベースディレクトリ名は、タイトルを略してAutoCVsasm。

## 環境構築

LinuxやWSL2環境を想定。`python3.8.10`。

```
### 仮想環境作成・起動
python -m venv <venv_name>
cd ./<venv_name>
source ./<venv_name>/bin/activate

### 各種パッケージインストール
cd ./AutoCVsasm

# pip install -r requirements.txtでもよいが
# 以下のコアパッケージを各個インストールすることを推奨
# for video split
pip install moviepy

# for scene segmentation
pip install --upgrade scenedetect[opencv]
pip install ffmpeg
sudo apt update
sudo apt upgrade
sudo apt install ffmpeg

# mp3 analysis
pip install librosa
pip install matplotlib
pip install pandas

```



## USAGE

### video split & scene segmentation

- 1.`scene segmentation`のための前処理として、ビデオを複数に分割する。様々な手法を試したが、長いビデオではプロセスがクラッシュしやすい。4分ほどに分割することが望ましい。
  - `AutoCVsasm/to_split_video/`以下に、動画ファイル(mp4)を配置。複数ある場合は、`xx_01.mp4`、`xx_02.mp4`のように命名する。
- 2.上記の処理により`AutoCVsasm/devided_video/`以下に、分割されたビデオが保存される。各ビデオに対して`scene segmentation`が実行される。`AutoCVsasm/devided_scenes/`以下にシーンごとの動画が保存される。

```
# パラメータを決定後、argparse実装予定。現状は必要に応じてコードを直接編集。
python main.py
```

### mp3 analysis(楽曲構成クラスタリング)

- `AutoCVsasm/demo_audio/`以下に、音声ファイル(mp3)を配置。
- パラメータはこれから色々試していく。成功すると、結果を示すcsvやpngが作成される。

```
python mp3_clustering.py
```



