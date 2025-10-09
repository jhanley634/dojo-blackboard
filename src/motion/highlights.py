#!/usr/bin/env python3
"""
Create a condensed highlights reel from a set of motion intervals.

Uses ffmpeg to catenate video segments.
"""

from __future__ import annotations

import shlex
import shutil
import subprocess  # nosec
import tempfile
from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING

import typer

from motion.find_motion import MotionConfig, detect_motion

if TYPE_CHECKING:
    from collections.abc import Iterable


def _run_ffmpeg(cmd: list[str]) -> None:
    cmd = list(map(shlex.quote, cmd))
    subprocess.check_call(cmd, stderr=subprocess.STDOUT)


def create_highlights_reel(
    video_path: Path,
    events: Iterable[tuple[float, float]],
    output_path: Path,
    context_sec: float = 1.0,
    *,
    verbose: bool = False,
) -> Path:
    """
    Builds a highlights reel that contains every motion segment,
    along with a short context window on either side.
    """
    probe_cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(video_path),
    ]
    try:
        raw_duration = subprocess.check_output(
            probe_cmd, stderr=subprocess.STDOUT, text=True  # nosec
        ).strip()
        total_duration = float(raw_duration)
    except Exception as exc:
        msg = f"Could not determine video duration for {video_path!s}"
        raise RuntimeError(msg) from exc

    tmp_dir = Path(tempfile.mkdtemp(prefix="motion_highlights_"))
    try:
        fragment_paths = []

        for idx, (s, e) in enumerate(events, start=1):
            # Expand by context, clamp to bounds
            clip_start = max(0.0, s - context_sec)
            clip_end = min(total_duration, e + context_sec)
            clip_duration = clip_end - clip_start
            if clip_duration <= 0:
                continue  # nothing to extract

            fragment_path = tmp_dir / f"frag_{idx:04d}.mp4"
            ffmpeg_cmd = [
                "ffmpeg",
                "-y",  # overwrite if exists
                "-loglevel",
                "error",
                "-ss",
                f"{clip_start:.6f}",
                "-i",
                f"{video_path}",
                "-t",
                f"{clip_duration:.6f}",
                "-c",
                "copy",
                f"{fragment_path}",
            ]
            if verbose:
                print("Running:", " ".join(ffmpeg_cmd))
            _run_ffmpeg(ffmpeg_cmd)

            fragment_paths.append(fragment_path)

        if not fragment_paths:
            msg = "No valid motion intervals to process."
            raise RuntimeError(msg)

        concat_file = tmp_dir / "concat.txt"
        with concat_file.open("w", encoding="utf-8") as f:
            for frag in fragment_paths:
                # ffmpeg concat needs paths quoted
                f.write(f"file '{frag.resolve()}'\n")

        final_cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            f"{concat_file}",
            "-c",
            "copy",
            f"{output_path}",
        ]
        if verbose:
            print("Running:", " ".join(final_cmd))
        _run_ffmpeg(final_cmd)

        if verbose:
            print(f"Highlights reel written to {output_path}")

        return output_path

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def main(
    video_path: Path,
    output_path: Path = Path("highlights.mp4"),
    context_sec: float = 1.0,
    *,
    verbose: bool = False,
) -> None:
    events = detect_motion(video_path, MotionConfig())
    create_highlights_reel(
        video_path,
        events,
        output_path,
        context_sec=context_sec,
        verbose=verbose,
    )


if __name__ == "__main__":
    typer.run(main)
