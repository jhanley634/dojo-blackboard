#!/usr/bin/env python3
"""
Detects motion in a video to find a list of (start, end) timestamps.
"""

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
    """Return a human-readable string HH:MM:SS.mmm."""
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def detect_motion(
    video_path: Path,
    cfg: MotionConfig,
) -> list[tuple[float, float]]:
    """
    Detect motion in a video file.
    """

    # Open the video and gather basic metadata
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        msg = f"Cannot open video file {video_path}"
        raise OSError(msg)

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = frame_count / fps

    # Background subtractor
    back_sub = cv2.createBackgroundSubtractorMOG2(
        history=cfg.history, varThreshold=cfg.var_threshold, detectShadows=cfg.detect_shadows
    )

    motion_events: list[tuple[float, float]] = []
    motion_start: float | None = None

    frame_idx = 0

    # Loop through frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % cfg.skip_frames != 0:
            frame_idx += 1
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        fg_mask = back_sub.apply(gray)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=2)
        fg_mask = cv2.dilate(fg_mask, kernel, iterations=2)

        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = any(cv2.contourArea(cnt) >= cfg.min_area for cnt in contours)

        current_time = frame_idx / fps

        if motion_detected:
            if motion_start is None:
                motion_start = current_time
                if cfg.verbose:
                    print(f"[DEBUG] Motion starts at {current_time:.2f}s")
        elif motion_start is not None:
            time_since_motion_start = current_time - motion_start
            if time_since_motion_start >= cfg.min_duration:
                motion_events.append((motion_start, current_time))
                if cfg.verbose:
                    print(
                        f"[DEBUG] Motion ends at {current_time:.2f}s"
                        f" (duration {time_since_motion_start:.2f}s)"
                    )
            elif cfg.verbose:
                print(f"[DEBUG] Ignored short motion of {time_since_motion_start:.2f}s")
            motion_start = None

        frame_idx += 1

    # Final cleanup
    if motion_start is not None:
        motion_events.append((motion_start, duration_sec))
        if cfg.verbose:
            print(
                f"[DEBUG] Final motion ends at {duration_sec:.2f}s (duration {(duration_sec -
motion_start):.2f}s)"
            )

    cap.release()
    return motion_events


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
