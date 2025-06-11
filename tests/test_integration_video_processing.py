#!/usr/bin/env python

"""Tests for `video_processing_toolkit` package."""

from pathlib import Path
import pytest
from unittest.mock import patch
import shutil
import math
from src.video_processing_toolkit import *
import cv2

def test_save_all_i_keyframes_not_empty(tmp_path):
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

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    frame_types = dict(get_frame_types(video_path))

    i_frame_timestamps = set(
        math.floor(frame_no / fps)
        for frame_no, frame_type in frame_types.items()
        if frame_type == 'I'
    )

    for f in output_files:
        ts = f.stem.split("frame_")[1]
        hh = int(ts[0:2])
        mm = int(ts[2:4])
        ss = int(ts[4:6])
        total_seconds = hh * 3600 + mm * 60 + ss

        assert total_seconds in i_frame_timestamps, f"{f.name} is not from an I-frame"

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

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    frame_types = dict(get_frame_types(video_path))

    p_frame_timestamps = set(
        math.floor(frame_no / fps)
        for frame_no, frame_type in frame_types.items()
        if frame_type == 'P'
    )

    for f in output_files:
        ts = f.stem.split("frame_")[1]
        hh = int(ts[0:2])
        mm = int(ts[2:4])
        ss = int(ts[4:6])
        total_seconds = hh * 3600 + mm * 60 + ss

        assert total_seconds in p_frame_timestamps, f"{f.name} is not from a P-frame"


def test_all_i_keyframes_between_two_timestamps_not_empty_and_correct(tmp_path):
    video_path = "tests/video_test.mp4"
    output_dir = tmp_path
    
    start_time = "00:00:05"
    end_time = "00:00:15"
    
    cap = cv2.VideoCapture(video_path)
        
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    
    assert fps > 0, "Le FPS de la vidéo doit être supérieur à 0"
    
    save_all_i_keyframes_between_two_timestamps(video_path, str(output_dir), start_time, end_time)
    
    output_files = list(output_dir.iterdir())
    
    assert len(output_files) > 0, "Aucun I-frame n'a été extrait"
 
    max_expected_frames = int(fps * 10)
    assert len(output_files) <= max_expected_frames
    
    for img_file in output_files:
        assert img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']
        img = cv2.imread(str(img_file))
        assert img is not None
        assert img.shape[0] > 0 and img.shape[1] > 0, f"Image vide ou corrompue: {img_file}"
    
    for img_file in output_files:
        assert "frame_" in img_file.name

    start_sec = 5
    end_sec = 15

    for img_file in output_files:
        ts = img_file.stem.split("frame_")[1]
        hh = int(ts[0:2])
        mm = int(ts[2:4])
        ss = int(ts[4:6])
        total_seconds = hh * 3600 + mm * 60 + ss

        assert start_sec <= total_seconds <= end_sec

def test_all_p_keyframes_between_two_timestamps_not_empty_and_correct(tmp_path):
    video_path = "tests/video_test.mp4"
    output_dir = tmp_path

    start_time = "00:00:05"
    end_time = "00:00:15"

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    assert fps > 0, "Le FPS de la vidéo doit être supérieur à 0"

    save_all_p_keyframes_between_two_timestamps(video_path, str(output_dir), start_time, end_time)

    output_files = list(output_dir.iterdir())

    assert len(output_files) > 0, "Aucun P-frame n'a été extrait"

    max_expected_frames = int(fps * 10)
    assert len(output_files) <= max_expected_frames

    for img_file in output_files:
        assert img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']
        img = cv2.imread(str(img_file))
        assert img is not None
        assert img.shape[0] > 0 and img.shape[1] > 0, f"Image vide ou corrompue: {img_file}"

    for img_file in output_files:
        assert "frame_" in img_file.name

    start_sec = 4
    end_sec = 15

    for img_file in output_files:
        ts = img_file.stem.split("frame_")[1]
        hh = int(ts[0:2])
        mm = int(ts[2:4])
        ss = int(ts[4:6])
        total_seconds = hh * 3600 + mm * 60 + ss

        assert start_sec <= total_seconds <= end_sec


def test_convert_video(tmp_path):
    original = Path("tests/video_test.mp4")
    target = tmp_path / "video_test.mp4"
    shutil.copy(original, target)
    
    original_dir = os.getcwd()
    os.chdir(tmp_path)

    output_name = convert_video(str(target))
    output_path = tmp_path / output_name
    
    assert Path(output_name).exists()
    assert output_path.suffix == ".avi"
    
    assert output_path.stat().st_size > 0

    os.chdir(original_dir)

def test_compute_frame_per_sec_rate():
    video_path = "tests/video_test.mp4"

    fps = compute_frame_per_sec_rate(video_path)
    
    assert isinstance(fps, (int, float)), "FPS doit être un nombre"
    assert fps == 30, "FPS doit être strictement positif"

def test_video_to_all_frames(tmp_path):
    video_path = "tests/video_test.mp4"
    output_dir = tmp_path / "frames_output"

    video_to_all_frames(video_path, str(output_dir))

    output_files = sorted(output_dir.glob("*.jpg"))
    
    assert len(output_files) > 0, "Aucun frame extrait"

    for file in output_files:
        img = cv2.imread(str(file))
        assert img is not None, f"Image non lisible : {file}"
        assert img.shape[0] > 0 and img.shape[1] > 0, f"Image vide ou corrompue : {file}"

    cap = cv2.VideoCapture(video_path)
    expected_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    assert abs(len(output_files) - expected_frame_count) <= 1

def test_frames_to_video(tmp_path):
    frames_dir = tmp_path / "frames"
    frames_dir.mkdir()

    for i in range(5):
        img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        img_path = frames_dir / f"frame_{i}.jpg"
        cv2.imwrite(str(img_path), img)

    output_video = tmp_path / "output.avi"

    frames_to_video(str(frames_dir) + os.sep, str(output_video), fps=10)

    assert output_video.exists()
    assert output_video.suffix == ".avi"

    cap = cv2.VideoCapture(str(output_video))
    success, _ = cap.read()
    cap.release()
    assert success

def test_extract_images_regular_interval(tmp_path):
    original = Path("tests/video_test.mp4")
    target_video = tmp_path / "video_test.mp4"
    shutil.copy(original, target_video)

    output_dir = tmp_path / "frames"
    output_dir.mkdir()

    extract_images_regular_interval(str(target_video), str(output_dir), time_interval_in_sec=1)

    extracted_files = list(output_dir.glob("*.jpg"))
    assert len(extracted_files) > 0

    for img_path in extracted_files:
        img = cv2.imread(str(img_path))
        assert img is not None

def test_extract_images_at_particular_timestamp(tmp_path):
    original_video = Path("tests/video_test.mp4")
    target_video = tmp_path / "video_test.mp4"
    shutil.copy(original_video, target_video)

    output_dir = tmp_path / "output_images"
    output_dir.mkdir()

    extract_images_at_particular_timestamp(
        str(target_video),
        str(output_dir),
        "00:00:01"
    )

    images = list(output_dir.glob("*.jpg"))
    assert len(images) >= 1

    img = cv2.imread(str(images[0]))
    assert img is not None


def test_extract_images_between_two_timestamps(tmp_path):
    original_video = Path("tests/video_test.mp4")
    target_video = tmp_path / "video_test.mp4"
    shutil.copy(original_video, target_video)

    output_dir = tmp_path / "timestamp_frames"
    output_dir.mkdir()

    extract_images_between_two_timestamps(
        str(target_video),
        str(output_dir),
        hh_mm_ss_start="00:00:00",
        hh_mm_ss_end="00:00:02"
    )

    images = list(output_dir.glob("*.jpg"))
    assert len(images) >= 1

    for img_path in images:
        img = cv2.imread(str(img_path))
        assert img is not None


def test_extract_regular_interval_images_between_two_timestamps(tmp_path):
    original_video = Path("tests/video_test.mp4")
    target_video = tmp_path / "video_test.mp4"
    shutil.copy(original_video, target_video)

    output_dir = tmp_path / "interval_between_timestamps"
    output_dir.mkdir()

    extract_regular_interval_images_between_two_timestamps(
        str(target_video),
        str(output_dir),
        hh_mm_ss_start="00:00:00",
        hh_mm_ss_end="00:00:03",
        time_interval_in_sec=1
    )

    images = list(output_dir.glob("*.jpg"))
    assert len(images) >= 2

    for img_path in images:
        img = cv2.imread(str(img_path))
        assert img is not None