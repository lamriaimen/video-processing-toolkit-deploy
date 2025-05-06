#!/usr/bin/env python

"""Tests for `video_processing_toolkit` package."""

import video_processing_toolkit.core
print(video_processing_toolkit.core.__file__)


from pathlib import Path
import pytest
from unittest.mock import patch

from video_processing_toolkit import *


def test_save_all_i_keyframes_not_empty(tmp_path):
    video_path = "tests/video_test.mp4"

    output_dir = tmp_path
    #output_dir.mkdir(exist_ok=True)

    save_all_i_keyframes(video_path, str(output_dir))
    output_files = list(output_dir.iterdir())

    assert len(output_files) > 0

def test_save_all_i_keyframes_creates_jpg_files(tmp_path):
    video_path = "tests/video_test.mp4"

    output_dir = tmp_path
    output_dir.mkdir(exist_ok=True)

    save_all_i_keyframes(video_path, str(output_dir))
    output_files = list(output_dir.iterdir())

    assert all(f.suffix.lower() == ".jpg" for f in output_files)

def test_save_all_i_keyframes_gets_only_iframes(tmp_path):
    video_path = "tests/video_test.mp4"
    output_dir = tmp_path

    save_all_i_keyframes(video_path, str(output_dir))

    output_files = list(output_dir.iterdir())

    frame_numbers = [
        int(f.name.split("frame_")[1].split(".")[0])
        for f in output_files
    ]

    frame_types = dict(get_frame_types(video_path))

    assert all(frame_types[num] == 'I' for num in frame_numbers)    

def test_save_all_p_keyframes_not_empty(tmp_path):
    video_path = "tests/video_test.mp4"
    output_dir = tmp_path

    save_all_p_keyframes(video_path, str(output_dir))

    output_files = list(output_dir.iterdir())

    assert len(output_files) > 0

def test_save_all_p_keyframes_creates_jpg_files(tmp_path):
    video_path = "tests/video_test.mp4"
    output_dir = tmp_path

    save_all_p_keyframes(video_path, str(output_dir))

    output_files = list(output_dir.iterdir())

    assert all(f.suffix.lower() == ".jpg" for f in output_files)
    
def test_save_all_p_keyframes_gets_only_pframes(tmp_path):
    video_path = "tests/video_test.mp4"
    output_dir = tmp_path

    save_all_p_keyframes(video_path, str(output_dir))

    output_files = list(output_dir.iterdir())

    frame_numbers = [
        int(f.name.split("frame_")[1].split(".")[0])
        for f in output_files
    ]

    frame_types = dict(get_frame_types(video_path))

    assert all(frame_types[num] == 'P' for num in frame_numbers)


    
def test_all_i_keyframes_between_two_timestamps_not_empty(tmp_path):
    video_path = "tests/video_test.mp4"
    
    start_time = "00:00:01"
    end_time = "00:00:03"

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    assert fps > 0
    cap.release()

    save_all_i_keyframes_between_two_timestamps(video_path, tmp_path, start_time , end_time)

    output_files = list(tmp_path.iterdir())
    assert len(output_files) > 0
    assert len(output_files) <= fps * 3

def test_all_i_keyframes_between_two_timestamps_creates_jpg_files(tmp_path):
    video_path = "tests/video_test.mp4"
    start_time = "00:00:01"
    end_time = "00:00:03"

    save_all_i_keyframes_between_two_timestamps(video_path, tmp_path, start_time , end_time)

    output_files = list(tmp_path.iterdir())
    assert all(f.suffix.lower() == ".jpg" for f in output_files)
