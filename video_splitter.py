import os
import sys
import shutil
from moviepy.editor import VideoFileClip, concatenate_videoclips

# TODO:動画の類似度を導入したら、マージンを含めて分割するようにする。



def my_split_video(test_data_path, output_dir_path, episode_n, n_split):
    clip = VideoFileClip(test_data_path)
    print("frames: {}".format(clip.reader.nframes))
    print("fps: {}".format(clip.fps))
    print("duration: {}".format(clip.duration))


    all_duration = clip.duration
    one_step = all_duration // n_split
    acm_v = 0
    for k in range(n_split):
        print("--- {}番目のカット ---".format(k))
        if k+1 == n_split:
            one_clip = VideoFileClip(test_data_path).subclip(acm_v, all_duration)
        else:
            one_clip = VideoFileClip(test_data_path).subclip(acm_v, acm_v + one_step)
        one_clip.write_videofile(output_dir_path + "ep{}_cut{}.mp4".format("0000"[:-len(str(episode_n))] + str(episode_n), "0000"[:-len(str(k))] + str(k)))
        acm_v += one_step
    return


if __name__ == "__main__": 
    episode_n = 3
    n_split = 6
    current_path = os.getcwd() + "/"
    test_data_path = current_path + "to_split_video/demo.mp4"
    output_dir_path = current_path + "devided_video/"
    if os.path.exists(output_dir_path):
        shutil.rmtree(output_dir_path)
    os.makedirs(output_dir_path, exist_ok=True)

    my_split_video(test_data_path, output_dir_path, episode_n, n_split)