import os
import sys
import shutil
import glob

import video_splitter
from scenedetect import detect, AdaptiveDetector, split_video_ffmpeg

"""
    ファイル名のルール
        to_split_video/hogehoge_<episode_id(ex:02)>.mp4
"""


divide_video_flag = True
video2scenes_flag = True
n_split = 6
current_path = os.getcwd() + "/"
to_split_video_dir = current_path + "to_split_video/"
devided_video_dir_path = current_path + "devided_video/"
scenes_dir_path = current_path + "devided_scenes/"



# video分割
if divide_video_flag:
    to_split_video_list = sorted(list(glob.glob(to_split_video_dir + "*")))
    episode_list = [f.split("_")[-1].split(".")[0] for f in to_split_video_list]
    ### 分割したvideoの保存先のリセットや作成
    if os.path.exists(devided_video_dir_path):
        shutil.rmtree(devided_video_dir_path)
    os.makedirs(devided_video_dir_path, exist_ok=True)

    ### videoの分割
    for k, episode_n in enumerate(episode_list):
        to_split_f_path = to_split_video_list[k]
        video_splitter.my_split_video(to_split_f_path, devided_video_dir_path, episode_n, n_split)

# video2scenes
if video2scenes_flag:
    to_scenes_video_list = sorted(list(glob.glob(devided_video_dir_path + "*")))
    ### 分割したsceneの保存先のリセットや作成
    if os.path.exists(scenes_dir_path):
        shutil.rmtree(scenes_dir_path)
    os.makedirs(scenes_dir_path, exist_ok=True)
    output_data_path = scenes_dir_path + "video_"

    for v_n, v in enumerate(to_scenes_video_list):
        output_data_path_per_video = output_data_path + "0000"[:-len(str(v_n))] + str(v_n)
        scene_list = detect(v, AdaptiveDetector())
        split_video_ffmpeg(v, scene_list, video_name=output_data_path_per_video)
        if v_n == 2:
            sys.exit()


