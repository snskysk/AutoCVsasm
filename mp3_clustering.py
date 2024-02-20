import librosa
import librosa.display
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
import numpy as np
import math
from sklearn import cluster
import pandas as pd
import seaborn as sns
# import IPython.display
import datetime
import os
import sys
import shutil

current_path = os.getcwd() + "/"
test_data_path = current_path + "demo_audio/demo.mp3"
output_dir_path = current_path + "output_audio/"
save_spectrogram_path = current_path + "spectrogram.png"
save_clustering_0_path = current_path + "clustering_0.png"
save_clustering_1_path = current_path + "clustering_1.png"
save_clustering_2_path = current_path + "clustering_2.png"

if os.path.exists(output_dir_path):
    shutil.rmtree(output_dir_path)
os.makedirs(output_dir_path, exist_ok=True)
output_data_path = output_dir_path + "demo"


# mp3の読み込み
# music,fs = librosa.audio.load(test_data_path)
music,fs = librosa.load(test_data_path)

# 後ほど用いる関数
def labels_list_to_df(labels_list):
    labels_01_list = []

    for i in range(len(labels_list)):
        labels_01_list.append(np.bincount([labels_list[i]]))

    return pd.DataFrame(labels_01_list)

def df_to_df_list(df):
    df_list =[]
    for i in range(len(df.columns)):
        df_list.append(df[i])

    return df_list

def pick_colors(df):
    return list(clrs.cnames.values())[:len(df.columns)]

def show_stackplot(index_df, df_list, colors, save_figure_path):
    fig, ax = plt.subplots(1, 1, figsize=(15,5))
    fig.patch.set_facecolor('white')
    ax.stackplot(index_df.index,df_list,colors=colors)
    plt.xticks([i*10 for i in range(int(round(index_df.index.tolist()[-1]))//10 + 1)])
    plt.savefig(save_figure_path)
    plt.close()



# フーリエ変換の初期設定(調整必要)
n_fft = 2048 # データの取得幅
hop_length = n_fft // 4 # 次の取得までの幅

# 短時間フーリエ変換
D =librosa.stft(music,n_fft=n_fft,hop_length=hop_length,win_length=None)

# 結果をスペクトログラムで表示
plt.figure()
librosa.display.specshow(librosa.amplitude_to_db(np.abs(D)**2,ref=np.max),
                         y_axis='log',x_axis='time',hop_length=hop_length)
plt.title('Power spectrogram')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout
plt.savefig(save_spectrogram_path)
plt.close()

print("--- first clustering ---")
# クラスタ分類の数(調整必要)
n_clusters=20

# k_meansのラベルをいくつずつ見ていくか(調整必要)
hop = 50

# クラスタ分類(k_means)
logamp = librosa.amplitude_to_db(np.abs(D)**2,ref=np.max)
k_means = cluster.KMeans(n_clusters=n_clusters)
k_means.fit(logamp.T)

col = k_means.labels_.shape[0]

# グラフ作成
count_list = []

# ラベル付けたデータをhop分持ってきて数を数える。
for i in range(col//hop):
    x = k_means.labels_[i*hop:(i+1)*hop]
    count = np.bincount(x)
    count_list.append(count)

# index内容
index = [(len(music)/fs)/len(count_list)*x for x in range(len(count_list))] # 秒数

df = pd.DataFrame(count_list,index = index).fillna(0)

columns = [chr(i) for i in range(65,65+26)][:10]

df_list = df_to_df_list(df)
colors = pick_colors(df)
df.to_csv(save_clustering_0_path.replace(".png", ".csv"))

show_stackplot(df, df_list, colors, save_clustering_0_path)

print("--- second clustering ---")
# クラス多数（調整必要）
music_cluster_num = 8

k_means_music = cluster.KMeans(n_clusters=music_cluster_num)
k_means_music.fit(df)

df['cluster']  = k_means_music.labels_

df4 = labels_list_to_df(k_means_music.labels_)    
df4_list = df_to_df_list(df4)
colors = pick_colors(df4)
df4.to_csv(save_clustering_1_path.replace(".png", ".csv"))

show_stackplot(df, df4_list, colors, save_clustering_1_path)


print("--- post-processing ---")
# いくつ未満をくっつけるか（調整必要）
min_num = 3

comp_list = []

m=1

for i in range(len(k_means_music.labels_) - 1):
    if k_means_music.labels_[i] == k_means_music.labels_[i+1]:
        m = m + 1
    else:
        comp_list.append([k_means_music.labels_[i],m])
        m=1

# 最後の文字をリストにくっつける。
comp_list.append([k_means_music.labels_[-1],m])

# comp_listの長さが短いものは、前のクラスタと同じIDにする。
for i in range(1,min_num):
    replace_comp_list = []
    replace_comp_list.append(comp_list[0])

    for j in range(1,len(comp_list)):
        if comp_list[j][1] == i:
            replace_comp_list[-1][1] += i
        else:
            replace_comp_list.append(comp_list[j])

    # 同じクラスタが並んでる場合はくっつける
    k = 0
    while k < len(replace_comp_list)-1:
        try:
            while replace_comp_list[k][0] == replace_comp_list[k+1][0]:          
                replace_comp_list[k][1] += replace_comp_list[k+1][1]
                replace_comp_list.pop(k+1)
        except IndexError:
            continue
        else:
            k += 1

    comp_list = replace_comp_list


# 元の形式に戻す
thawing_list = []
for i in range(len(replace_comp_list)):
    for j in range(replace_comp_list[i][1]):
        thawing_list.append(replace_comp_list[i][0])

df5 = labels_list_to_df(thawing_list)
df5_list = df_to_df_list(df5)
colors = pick_colors(df5)
df5.to_csv(save_clustering_2_path.replace(".png", ".csv"))
show_stackplot(df, df5_list, colors, save_clustering_2_path)



