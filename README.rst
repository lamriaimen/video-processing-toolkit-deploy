========================
Video Processing Toolkit
========================

.. image:: https://img.shields.io/pypi/v/video_processing_toolkit.svg
        :target: https://pypi.python.org/pypi/video_processing_toolkit

.. image:: https://img.shields.io/travis/alyssia-fourali/video_processing_toolkit.svg
        :target: https://travis-ci.com/alyssia-fourali/video_processing_toolkit

.. image:: https://readthedocs.org/projects/video-processing-toolkit/badge/?version=latest
        :target: https://video-processing-toolkit.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/alyssia-fourali/video_processing_toolkit/shield.svg
     :target: https://pyup.io/repos/github/alyssia-fourali/video_processing_toolkit/
     :alt: Updates
.. image:: https://github.com/<your-user>/<your-repo>/actions/workflows/ci.yml/badge.svg
   :alt: CI

.. image:: https://github.com/<your-user>/<your-repo>/actions/workflows/release.yml/badge.svg
   :alt: Release

.. image:: https://codecov.io/gh/<your-user>/<your-repo>/branch/main/graph/badge.svg
   :alt: Coverage

A Python toolkit for slicing, annotating, and processing video files for data analysis and machine learning.

* Free software: MIT license
* Documentation: https://loicsc1.github.io/video-processing-toolkit.

Features
--------

* Extract and slice video into frames or clips
* Add annotations or labels to specific frames
* Convert between video formats
* Resize and preprocess video for ML models
* Batch processing of multiple videos
* CLI and Python API support

Prerequisites
-------------

Before installing, make sure the following dependencies are installed on your system:

* `ffmpeg` and `ffprobe` – required for video decoding and analysis

You can install them via your package manager:

.. code-block:: bash

    sudo apt install ffmpeg    # for Debian/Ubuntu
    brew install ffmpeg        # for macOS

Installation
------------
 install the latest version directly from GitHub:

.. code-block:: bash

    pip install git+https://github.com/LoicSc1/video-processing-toolkit.git

Or clone and install in editable mode:

.. code-block:: bash

    git clone https://github.com/LoicSc1/video-processing-toolkit.git
    cd video_processing_toolkit
    pip install -e .

Usage
-----

Basic example:

.. code-block:: python

    # Extract all I-frames from a video and save them to the specified directory
    from video_processing_toolkit import save_all_i_keyframes
    save_all_i_keyframes ("video.mp4", "/output_frames")

See the full documentation for detailed usage and advanced options.

Contributing
------------

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-xyz`)
3. Make your changes
4. Submit a pull request

Before submitting, please make sure to run tests and follow the project's coding standards.

License
-------

This project is licensed under the MIT License - see the `LICENSE` file for details.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
