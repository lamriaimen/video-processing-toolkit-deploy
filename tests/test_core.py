#!/usr/bin/env python

"""Tests for `video_processing_toolkit` package."""

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

