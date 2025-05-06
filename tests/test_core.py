#!/usr/bin/env python

"""Tests for `video_processing_toolkit` package."""

import video_processing_toolkit.core
print(video_processing_toolkit.core.__file__)


from pathlib import Path
import pytest
from unittest.mock import patch

from video_processing_toolkit import *


@patch("subprocess.check_output")
def test_get_frame_types_returns_expected_values(mock_check_output):

    mock_output = b"pict_type=I\npict_type=B\npict_type=P\n"
    mock_check_output.return_value = mock_output

    result = list(get_frame_types("video_test.mp4"))

    expected_result = [(0, 'I'), (1, 'B'), (2, 'P')]
    assert result == expected_result

@patch("subprocess.check_output")
def test_get_frame_types_returns_empty_on_empty_ffprobe_output(mock_check_output):
    mock_check_output.return_value = b""

    result = list(get_frame_types("empty_video.mp4"))
    
    assert result == []

@patch("subprocess.check_output")
def test_get_frame_types_fails_when_invalid_video(mock_check_output):
    mock_check_output.side_effect = subprocess.CalledProcessError(1, "ffprobe")
    
    with pytest.raises(subprocess.CalledProcessError):
        get_frame_types("invalid_video.mp4")


def test_save_all_i_keyframes_not_empty(tmp_path):
    video_path = "tests/video_test.mp4"

    output_dir = tmp_path
    output_dir.mkdir(exist_ok=True)

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