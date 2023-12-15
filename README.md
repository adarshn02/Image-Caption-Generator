# Image Caption Generator

## Overview

This project is an Image Caption Generator implemented in Python, utilizing OpenCV, Tensorflow, and Natural Language Toolkit (NLTK). The goal is to generate descriptive captions for images, providing a richer understanding of the visual content.

## Features

- Incorporates pre-trained Tensorflow models for image segmentation and object detection within images.
- Integrates NLTK and OpenCV to create a Text-to-Speech (TTS) model for image description.
- Encourages users to input images, generating descriptive captions for better accessibility.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/image-caption-generator.git
    cd image-caption-generator
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the main script:

    ```bash
    python image_caption_generator.py
    ```

2. Follow the instructions to input images for caption generation.

## Dependencies

- OpenCV
- Tensorflow
- NLTK

Install dependencies using:

```bash
pip install opencv-python tensorflow nltk
```

## Pre-trained Models

The project utilizes pre-trained Tensorflow models for image segmentation and object detection. Make sure to check the official Tensorflow model zoo for the latest models:

[Tensorflow Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md)
