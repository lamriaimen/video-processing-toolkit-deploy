#!/usr/bin/env python

"""Tests for `video_processing_toolkit` package."""

import video_processing_toolkit.core
print(video_processing_toolkit.core.__file__)


from pathlib import Path
import pytest
from unittest.mock import MagicMock, patch

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


@patch("video_processing_toolkit.core.get_frame_types")
@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
def test_save_all_i_keyframes_creates_correct_number_of_images(mock_imwrite, mock_VideoCapture, mock_get_frame_types, tmp_path):
    mock_get_frame_types.return_value = [(0, 'I'), (1, 'B'), (5, 'I'), (10, 'I'), (12, 'P')]

    mock_cap = MagicMock()
    mock_cap.read.return_value = (True, "fake_frame")
    mock_VideoCapture.return_value = mock_cap

    save_all_i_keyframes("fake_video.mp4", str(tmp_path))

    assert mock_imwrite.call_count == 3

@patch("video_processing_toolkit.core.get_frame_types")
@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
def test_save_all_i_keyframes_with_no_iframes(mock_imwrite, mock_VideoCapture, mock_get_frame_types, tmp_path):
    mock_get_frame_types.return_value = [(0, 'P'), (1, 'B'), (2, 'P')]

    mock_cap = MagicMock()
    mock_cap.read.return_value = (True, "fake_frame")
    mock_VideoCapture.return_value = mock_cap

    save_all_i_keyframes("fake_video.mp4", str(tmp_path))

    mock_imwrite.assert_not_called()

@patch("video_processing_toolkit.core.get_frame_types")
@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
def test_save_all_i_keyframes_creates_correct_number_of_images(mock_imwrite, mock_VideoCapture, mock_get_frame_types, tmp_path):
    mock_get_frame_types.return_value = [(0, 'P'), (1, 'P'), (5, 'I'), (10, 'P'), (12, 'B')]

    mock_cap = MagicMock()
    mock_cap.read.return_value = (True, "fake_frame")
    mock_VideoCapture.return_value = mock_cap

    save_all_p_keyframes("fake_video.mp4", str(tmp_path))

    assert mock_imwrite.call_count == 3

@patch("video_processing_toolkit.core.get_frame_types")
@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
def test_save_all_p_keyframes_with_no_iframes(mock_imwrite, mock_VideoCapture, mock_get_frame_types, tmp_path):
    mock_get_frame_types.return_value = [(0, 'I'), (1, 'B'), (2, 'I')]

    mock_cap = MagicMock()
    mock_cap.read.return_value = (True, "fake_frame")
    mock_VideoCapture.return_value = mock_cap

    save_all_p_keyframes("fake_video.mp4", str(tmp_path))

    mock_imwrite.assert_not_called()
