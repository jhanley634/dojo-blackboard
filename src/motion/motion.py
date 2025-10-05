#!/usr/bin/env python3
"""
Detects motion in a video to find a list of (start, end) timestamps.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from pprint import pp

import cv2


@dataclass
class MotionConfig:
    min_area: int = 500
    min_duration: float = 7.0
    skip_frames: int = 1
    history: int = 500
    var_threshold: int = 16
    detect_shadows: bool = True
    verbose: bool = False


def _format_time(sec: float) -> str:
    """Return a human-readable time as HH:MM:SS.mmm."""
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def _create_bg_subtractor(cfg: MotionConfig) -> cv2.BackgroundSubtractorMOG2:
    """Create and return a background subtractor."""
    return cv2.createBackgroundSubtractorMOG2(
        history=cfg.history,
        varThreshold=cfg.var_threshold,
        detectShadows=cfg.detect_shadows,
    )


def _preprocess_frame(frame: cv2.Mat) -> cv2.Mat:
    """Convert to gray and blur the frame."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(gray, (5, 5), 0)


def _apply_mask(mask: cv2.Mat) -> cv2.Mat:
    """Clean up the foreground mask with morphological operations."""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    return cv2.dilate(mask, kernel, iterations=2)


def _contour_detects_motion(contours: list[cv2.Mat], cfg: MotionConfig) -> bool:
    """Return True if any contour is large enough."""
    return any(cv2.contourArea(cnt) >= cfg.min_area for cnt in contours)


def _update_motion_state(
    current_time: float,
    motion_start: float | None,
    events: list[tuple[float, float]],
    cfg: MotionConfig,
    *,
    motion_detected: bool,
) -> float | None:
    """
    Update the motion state machine.

    Returns the new `motion_start` value (or None if motion ended).
    """
    if motion_detected:
        if motion_start is None:
            motion_start = current_time
            if cfg.verbose:
                print(f"[DEBUG] Motion starts at {current_time:.2f}s")
    elif motion_start is not None:
        duration = current_time - motion_start
        if duration >= cfg.min_duration:
            events.append((motion_start, current_time))
            if cfg.verbose:
                print(f"[DEBUG] Motion ends at {current_time:.2f}s (duration {duration:.2f}s)")
        elif cfg.verbose:
            print(f"[DEBUG] Ignored short motion of {duration:.2f}s")
        motion_start = None
    return motion_start


def _finalise_motion(
    motion_start: float | None,
    duration_sec: float,
    events: list[tuple[float, float]],
    cfg: MotionConfig,
) -> None:
    """Append the last motion event if the video ends while motion is ongoing."""
    if motion_start is not None:
        events.append((motion_start, duration_sec))
        if cfg.verbose:
            print(
                f"[DEBUG] Final motion ends at {duration_sec:.2f}s "
                f"(duration {(duration_sec - motion_start):.2f}s)"
            )


def detect_motion(video_path: Path, cfg: MotionConfig) -> list[tuple[float, float]]:
    """
    Detects motion in a video file.
    """
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        msg = f"Cannot open video file {video_path}"
        raise OSError(msg)

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = frame_count / fps

    back_sub = _create_bg_subtractor(cfg)

    events: list[tuple[float, float]] = []
    motion_start: float | None = None
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Skip frames if required
        if frame_idx % cfg.skip_frames != 0:
            frame_idx += 1
            continue

        gray = _preprocess_frame(frame)
        fg_mask = back_sub.apply(gray)
        fg_mask = _apply_mask(fg_mask)

        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = _contour_detects_motion(contours, cfg)
        current_time = frame_idx / fps

        motion_start = _update_motion_state(
            current_time, motion_start, events, cfg, motion_detected=motion_detected
        )

        frame_idx += 1

    _finalise_motion(motion_start, duration_sec, events, cfg)

    cap.release()
    return events


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python motion.py <video_path>")
        sys.exit(1)

    video_file = Path(sys.argv[1])
    events = detect_motion(video_file, MotionConfig())

    print("\n=== Motion events ===")
    for i, (s, e) in enumerate(events, start=1):
        print(f"{i:02d}. { _format_time(s) } --> { _format_time(e) } ({e - s:6.2f}s)")

    pp(events)
