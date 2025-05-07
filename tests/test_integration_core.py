#!/usr/bin/env python

"""Tests for `video_processing_toolkit` package."""

from pathlib import Path
import pytest
from unittest.mock import patch

from src.video_processing_toolkit import *

def test_ffmpeg_tools_installed():
    try:
        check_ffmpeg_tools_available()
    except EnvironmentError as e:
        pytest.fail(str(e))


def test_save_all_i_keyframes_not_empty(tmp_path):
    check_ffmpeg_tools_available()

    video_path = "tests/video_test.mp4"
    output_dir = tmp_path

    save_all_i_keyframes(video_path, str(output_dir))

    output_files = list(output_dir.iterdir())
    print(f"Fichiers dans {output_dir}: {[str(p) for p in output_dir.iterdir()]}")

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

    output_files=tmp_path
    
    start_time = "00:00:05"
    end_time = "00:00:15"

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    assert fps > 0
    cap.release()

    save_all_i_keyframes_between_two_timestamps(video_path, str(output_files), start_time , end_time)

    output = list(tmp_path.iterdir())
    assert len(output) > 0
    assert len(output) <= fps * 10

def test_all_i_keyframes_between_two_timestamps_creates_jpg_files(tmp_path):
    video_path = "tests/video_test.mp4"
    start_time = "00:00:00"
    end_time = "00:00:05"

    save_all_i_keyframes_between_two_timestamps(video_path, str(tmp_path), start_time , end_time)

    output_files = list(tmp_path.iterdir())
    assert all(f.suffix.lower() == ".jpg" for f in output_files)