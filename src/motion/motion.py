#!/usr/bin/env python3
#  motion.py
#
#  Detect motion in a video and return a list of (start, end) timestamps.
#
#  Requirements:  opencv-python  (pip install opencv-python inside .venv/)
#
#  Usage:
#      python motion.py one-hour.mp4
#  or
#      >>> from motion import detect_motion
#      >>> events = detect_motion("one-hour.mp4")
#      >>> for s, e in events:
#      ...     print(f"Motion from {s:.2f}s to {e:.2f}s")
#

import sys

import cv2


def _format_time(sec: float) -> str:
    """Return a human-readable string HH:MM:SS.mmm."""
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def detect_motion(
    video_path: str,
    *,
    min_area: int = 500,  # Minimum contour area to be considered motion
    min_duration: float = 5.0,  # Minimum duration (in seconds) to call a *continuous* event
    skip_frames: int = 1,  # Process every Nth frame (helps for very long videos)
    history: int = 500,  # Number of frames for background model history
    var_threshold: int = 16,  # Threshold on the squared Mahalanobis distance to decide
    detect_shadows: bool = True,  # Optionally detect shadows (color mask will contain 0)
    verbose: bool = False,
) -> list[tuple[float, float]]:
    """
    Detect motion in a video file.
    """
    # ------------------------------------------------------------------
    # 1. Open the video and gather basic metadata
    # ------------------------------------------------------------------
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        msg = f"Cannot open video file {video_path}"
        raise OSError(msg)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:  # Fallback if FPS is unknown
        fps = 30.0

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = frame_count / fps

    print(f"[INFO] Video opened: {video_path}")
    print(f"  FPS         : {fps:.2f}")
    print(f"  Frame count : {frame_count}")
    print(f"  Duration    : {duration_sec:.2f}s")

    # ------------------------------------------------------------------
    # 2. Background subtractor
    # ------------------------------------------------------------------
    back_sub = cv2.createBackgroundSubtractorMOG2(
        history=history, varThreshold=var_threshold, detectShadows=detect_shadows
    )

    # ------------------------------------------------------------------
    # 3. State variables for motion detection
    # ------------------------------------------------------------------
    motion_events: list[tuple[float, float]] = []
    motion_start: float | None = None

    frame_idx = 0

    # ------------------------------------------------------------------
    # 4. Loop through frames
    # ------------------------------------------------------------------
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        # Process only every Nth frame
        if frame_idx % skip_frames != 0:
            frame_idx += 1
            continue

        # 4a. Pre-processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # 4b. Apply background subtractor
        fg_mask = back_sub.apply(gray)

        # 4c. Clean up the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=2)
        fg_mask = cv2.dilate(fg_mask, kernel, iterations=2)

        # 4d. Find contours
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area >= min_area:
                motion_detected = True
                break  # One significant contour is enough

        # ------------------------------------------------------------------
        # 5. Update motion event logic
        # ------------------------------------------------------------------
        current_time = frame_idx / fps

        if motion_detected:
            # If we were already in motion, just update the last frame
            if motion_start is None:
                motion_start = current_time
                print(f"[DEBUG] Motion starts at {current_time:.2f}s")
        # No motion this frame
        elif motion_start is not None:
            # Check if we have had a sustained motion for min_duration
            time_since_motion_start = current_time - motion_start
            if time_since_motion_start >= min_duration:
                # End the motion event
                motion_end = current_time
                motion_events.append((motion_start, motion_end))
                print(
                    f"[DEBUG] Motion ends at {motion_end:.2f}s"
                    f" (duration {time_since_motion_start:.2f}s)"
                )
            # Motion was too short; discard
            elif verbose:
                print(f"[DEBUG] Ignored short motion of {time_since_motion_start:.2f}s")
            motion_start = None

        frame_idx += 1

    # ------------------------------------------------------------------
    # 6. Final cleanup (in case video ends while motion is still detected)
    # ------------------------------------------------------------------
    if motion_start is not None:
        # End at the very last frame
        motion_end = duration_sec
        motion_events.append((motion_start, motion_end))
        print(
            f"[DEBUG] Final motion ends at {motion_end:.2f}s (duration {(motion_end -
motion_start):.2f}s)"
        )

    cap.release()
    return motion_events


# ----------------------------------------------------------------------
# 7. Demo / CLI
# ----------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python motion.py <video_path>")
        sys.exit(1)

    video_file = sys.argv[1]
    events = detect_motion(video_file, min_area=800, min_duration=2.0, skip_frames=2)

    print("\n=== Motion events ===")
    for i, (s, e) in enumerate(events, start=1):
        print(f"{i:02d}. { _format_time(s) } --> { _format_time(e) } ({e - s:6.2f}s)")
