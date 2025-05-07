#!/usr/bin/env python

"""Tests for `video_processing_toolkit` package."""

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


@patch("video_processing_toolkit.core.ffmpy.FFmpeg.run")
@patch("video_processing_toolkit.core.ffmpy.FFmpeg")
@patch("video_processing_toolkit.core.time.strftime")
def test_convert_video_builds_correct_avi_filename(mock_strftime, mock_ffmpeg_class, mock_run):
    mock_strftime.return_value = "20240506-154500"

    mock_ffmpeg = MagicMock()
    mock_ffmpeg_class.return_value = mock_ffmpeg

    output_filename = convert_video("fake_input.mp4")

    assert output_filename == "20240506-154500.avi"

    mock_ffmpeg_class.assert_called_once_with(
        inputs={"fake_input.mp4": None},
        outputs={"20240506-154500.avi": " -c:a mp3 -c:v mpeg4"}
    )

    mock_ffmpeg.run.assert_called_once()

@patch("video_processing_toolkit.core.ffmpy.FFmpeg.run")
@patch("video_processing_toolkit.core.ffmpy.FFmpeg")
@patch("video_processing_toolkit.core.time.strftime")
def test_convert_video_builds_correct_ffmpeg_command(mock_strftime, mock_ffmpeg_class, mock_run):
    mock_strftime.return_value = "20240506-154500"

    mock_ffmpeg = MagicMock()
    mock_ffmpeg_class.return_value = mock_ffmpeg

    output_filename = convert_video("fake_input.mp4")

    mock_ffmpeg_class.assert_called_once_with(
        inputs={"fake_input.mp4": None},
        outputs={"20240506-154500.avi": " -c:a mp3 -c:v mpeg4"}
    )

@patch("video_processing_toolkit.core.ffmpy.FFmpeg.run")
@patch("video_processing_toolkit.core.ffmpy.FFmpeg")
@patch("video_processing_toolkit.core.time.strftime")
def test_convert_video_executes_ffmpeg_command(mock_strftime, mock_ffmpeg_class, mock_run):
    mock_strftime.return_value = "20240506-154500"

    mock_ffmpeg = MagicMock()
    mock_ffmpeg_class.return_value = mock_ffmpeg

    output_filename = convert_video("fake_input.mp4")

    mock_ffmpeg.run.assert_called_once()

@patch("video_processing_toolkit.core.os.path.isfile", return_value=True)
@patch("video_processing_toolkit.core.os.listdir", return_value=["frame_1.jpg", "frame_2.jpg", "frame_3.jpg"])
@patch("video_processing_toolkit.core.cv2.imread")
@patch("video_processing_toolkit.core.cv2.VideoWriter")
def test_frames_to_video_reads_images(mock_writer, mock_imread, mock_listdir, mock_isfile):
    fake_img = np.ones((480, 640, 3), dtype=np.uint8)
    mock_imread.return_value = fake_img

    frames_to_video("frames/", "output.avi", fps=30)

    assert mock_imread.call_count == 3

@patch("video_processing_toolkit.core.os.path.isfile", return_value=True)
@patch("video_processing_toolkit.core.os.listdir", return_value=["frame_1.jpg", "frame_2.jpg"])
@patch("video_processing_toolkit.core.cv2.imread")
@patch("video_processing_toolkit.core.cv2.VideoWriter")
def test_frames_to_video_writes_all_frames(mock_writer_class, mock_imread, mock_listdir, mock_isfile):
    fake_img = np.ones((480, 640, 3), dtype=np.uint8)
    mock_imread.return_value = fake_img

    writer = MagicMock()
    mock_writer_class.return_value = writer

    frames_to_video("frames/", "output.avi", fps=30)

    assert writer.write.call_count == 2

@patch("video_processing_toolkit.core.os.path.isfile", return_value=True)
@patch("video_processing_toolkit.core.os.listdir", return_value=["frame_1.jpg"])
@patch("video_processing_toolkit.core.cv2.imread")
@patch("video_processing_toolkit.core.cv2.VideoWriter")
def test_frames_to_video_releases_video_writer(mock_writer_class, mock_imread, mock_listdir, mock_isfile):
    fake_img = np.ones((480, 640, 3), dtype=np.uint8)
    mock_imread.return_value = fake_img

    writer = MagicMock()
    mock_writer_class.return_value = writer

    frames_to_video("frames/", "output.avi", fps=30)

    writer.release.assert_called_once()

@patch("video_processing_toolkit.core.os.mkdir")
@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
def test_video_to_all_frames_creates_output_dir(mock_imwrite, mock_VideoCapture, mock_mkdir):
    mock_cap = MagicMock()
    mock_cap.get.return_value = 1
    mock_cap.isOpened.return_value = False
    mock_VideoCapture.return_value = mock_cap

    video_to_all_frames("video.mp4", "output_dir")
    mock_mkdir.assert_called_once_with("output_dir")

@patch("video_processing_toolkit.core.os.mkdir")
@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
def test_video_to_all_frames_reads_frames_correctly(mock_imwrite, mock_VideoCapture, mock_mkdir):
    mock_cap = MagicMock()
    mock_cap.get.return_value = 4
    mock_cap.isOpened.side_effect = [True, True, True, False]
    mock_cap.read.side_effect = [(True, "f1"), (True, "f2"), (True, "f3"), (False, None)]
    mock_VideoCapture.return_value = mock_cap

    video_to_all_frames("video.mp4", "output_dir")

    assert mock_cap.read.call_count == 3

@patch("video_processing_toolkit.core.os.mkdir")
@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
def test_video_to_all_frames_writes_frames(mock_imwrite, mock_VideoCapture, mock_mkdir):
    mock_cap = MagicMock()
    mock_cap.get.return_value = 4
    mock_cap.isOpened.side_effect = [True, True, True, False]
    mock_cap.read.side_effect = [(True, "f1"), (True, "f2"), (True, "f3"), (False, None)]
    mock_VideoCapture.return_value = mock_cap

    video_to_all_frames("video.mp4", "output_dir")

    assert mock_imwrite.call_count == 3

@patch("video_processing_toolkit.core.os.mkdir")
@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
def test_video_to_all_frames_output_file_names(mock_imwrite, mock_VideoCapture, mock_mkdir):
    mock_cap = MagicMock()
    mock_cap.get.return_value = 4
    mock_cap.isOpened.side_effect = [True, True, True, False]
    mock_cap.read.side_effect = [(True, "f1"), (True, "f2"), (True, "f3"), (False, None)]
    mock_VideoCapture.return_value = mock_cap

    video_to_all_frames("video.mp4", "output_dir")

    calls = [call[0][0] for call in mock_imwrite.call_args_list]
    assert calls == [
        "output_dir/%#05d.jpg" % 1,
        "output_dir/%#05d.jpg" % 2,
        "output_dir/%#05d.jpg" % 3,
    ]


@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
def test_extract_images_regular_interval_creates_images(mock_imwrite, mock_VideoCapture):
    mock_cap = MagicMock()
    mock_cap.read.side_effect = [(True, "frame1"), (True, "frame2"), (False, None)]
    mock_VideoCapture.return_value = mock_cap

    extract_images_regular_interval("video.mp4", "output_dir", 5)

    assert mock_imwrite.call_count == 2
    expected_files = [
        "output_dir/%#05d.jpg" % 1,
        "output_dir/%#05d.jpg" % 2
    ]
    actual_files = [call[0][0] for call in mock_imwrite.call_args_list]
    assert actual_files == expected_files

@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
def test_extract_images_regular_interval_sets_correct_position_in_the_video(mock_imwrite, mock_VideoCapture):
    mock_cap = MagicMock()
    mock_cap.read.side_effect = [
        (True, "frame1"),
        (True, "frame2"),
        (True, "frame3"),
        (False, None)
    ]
    mock_VideoCapture.return_value = mock_cap

    extract_images_regular_interval("video.mp4", "output_dir", 5)

    mock_cap.set.assert_any_call(cv2.CAP_PROP_POS_MSEC, 0 * 5000)
    mock_cap.set.assert_any_call(cv2.CAP_PROP_POS_MSEC, 1 * 5000)
    mock_cap.set.assert_any_call(cv2.CAP_PROP_POS_MSEC, 2 * 5000)

@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
def test_extract_images_regular_interval_releases_video(mock_imwrite, mock_VideoCapture):
    mock_cap = MagicMock()
    mock_cap.read.side_effect = [(True, "frame1"), (False, None)]
    mock_VideoCapture.return_value = mock_cap

    extract_images_regular_interval("video.mp4", "output_dir", 5)

    mock_cap.release.assert_called_once()

@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
def test_extract_images_between_two_timestamps_position_cursor_at_start_timestamp(mock_imwrite, mock_VideoCapture):
    mock_cap = MagicMock()
    mock_VideoCapture.return_value = mock_cap

    mock_cap.read.side_effect = [
        (True, "frame1"),  
        (False, None)      
    ]

    extract_images_between_two_timestamps("video.mp4", "output_dir", "00:00:05", "00:00:10")

    mock_cap.set.assert_called_once_with(cv2.CAP_PROP_POS_MSEC, 5000)


@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
def test_extract_frames_between_two_timestamps(mock_imwrite, mock_VideoCapture):
    mock_cap = MagicMock()
    mock_cap.get.return_value = 30  #30 FPS
    mock_cap.read.side_effect = [
        (True, "frame1"),
        (True, "frame2"),
        (False, None)
    ]
    mock_VideoCapture.return_value = mock_cap

    extract_images_between_two_timestamps("video.mp4", "output_dir", "00:00:05", "00:00:10")

    assert mock_imwrite.call_count == 2

    expected_files = [
        "output_dir/%#05d.jpg" % 122,
        "output_dir/%#05d.jpg" % 123
    ]

    actual_files = [call[0][0] for call in mock_imwrite.call_args_list]
    assert actual_files == expected_files

@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
def test_extract_frames_between_two_timestamps_stops_reading_after_last_timestamp(mock_imwrite, mock_VideoCapture):

    mock_cap = MagicMock()
    
    mock_cap.get.return_value = 30  # 30 FPS

    mock_cap.read.side_effect = [(True, f"frame{i}") for i in range(180)] + [(False, None)]
    mock_VideoCapture.return_value = mock_cap

    extract_images_between_two_timestamps("video.mp4", "output_dir", "00:00:05", "00:00:06")

    assert mock_imwrite.call_count == 60

    mock_cap.release.assert_called_once()

@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
@patch("video_processing_toolkit.core.get_frame_types")
def test_save_all_i_keyframes_between_two_timestamps_starts_at_first_timestamp(mock_get_frame_types, mock_imwrite, mock_VideoCapture):
    mock_cap = MagicMock()
    mock_VideoCapture.return_value = mock_cap
    mock_cap.get.return_value = 30  # 30 FPS 

    mock_get_frame_types.return_value = [
        (121, 'I'), 
        (150, 'I'), 
        (180, 'I')
    ]

    mock_cap.read.side_effect = [
        (True, "frame_121"),
        (True, "frame_150"),
        (True, "frame_180"),
        (False, None)  
    ]

    save_all_i_keyframes_between_two_timestamps("video.mp4", "output_dir", "00:00:05", "00:00:06")

    mock_cap.set.assert_any_call(cv2.CAP_PROP_POS_FRAMES, 121)


@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
@patch("video_processing_toolkit.core.get_frame_types")
def test_save_all_i_keyframes_between_two_timestamps_stops_at_last_timestamp(mock_get_frame_types, mock_imwrite, mock_VideoCapture):
    mock_cap = MagicMock()
    mock_VideoCapture.return_value = mock_cap
    mock_cap.get.return_value = 30  # 30 FPS 

    mock_get_frame_types.return_value = [
        (121, 'I'), 
        (150, 'I'), 
        (180, 'I'),
        (181, 'I')  
    ]

    mock_cap.read.side_effect = [
        (True, "frame_121"),
        (True, "frame_150"),
        (True, "frame_180"),
        (True, "frame_181"),
        (False, None)  
    ]

    save_all_i_keyframes_between_two_timestamps("video.mp4", "output_dir", "00:00:05", "00:00:06")

    calls = [call[0][1] for call in mock_cap.set.call_args_list]
    assert 181 not in calls


@patch("video_processing_toolkit.core.cv2.VideoCapture")
@patch("video_processing_toolkit.core.cv2.imwrite")
@patch("video_processing_toolkit.core.get_frame_types")
def test_save_all_i_keyframes_between_two_timestamps_only_saves_iframes(mock_get_frame_types, mock_imwrite, mock_VideoCapture):
    mock_cap = MagicMock()
    mock_VideoCapture.return_value = mock_cap
    mock_cap.get.return_value = 30  # 30 FPS 

    mock_get_frame_types.return_value = [
        (121, 'I'), 
        (125, 'P'), 
        (150, 'I'), 
        (155, 'P'), 
        (180, 'I')
    ]

    mock_cap.read.side_effect = [
        (True, "frame_121"),
        (True, "frame_150"),
        (True, "frame_180"),
        (False, None)  
    ]

    save_all_i_keyframes_between_two_timestamps("video.mp4", "output_dir", "00:00:05", "00:00:06")

    expected_files = [
        "output_dir//0frame_121.jpg",
        "output_dir//1frame_150.jpg",
        "output_dir//2frame_180.jpg"
    ]
    actual_files = [call[0][0] for call in mock_imwrite.call_args_list]
    assert actual_files == expected_files
