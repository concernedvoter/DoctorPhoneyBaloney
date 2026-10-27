#!/usr/bin/env python3
"""
Local video/audio transcription for Apple Silicon Macs.

Downloads a clip (YouTube, X, Instagram) or reads a local file, transcribes it
with Whisper (MLX), optionally labels speakers, and writes a timestamped
transcript you can cite by time code.

Usage:
  python3 transcribe.py URL_OR_FILE [URL_OR_FILE ...] [--diarize] [--lang en]
                        [--cookies-browser chrome] [--out transcripts]

Notes:
  --diarize needs a free Hugging Face token in the HF_TOKEN environment
  variable, and you must accept the terms for pyannote/speaker-diarization-3.1
  on huggingface.co first.
  --cookies-browser lets yt-dlp use your logged-in browser session, which X
  and Instagram often require.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

MODEL = "mlx-community/whisper-large-v3-turbo"


def fmt(t):
    t = int(t)
    return f"{t // 3600:02d}:{(t % 3600) // 60:02d}:{t % 60:02d}"


def fetch(src, workdir, cookies_browser):
    """Return a local audio path for a URL or an existing file."""
    if os.path.exists(src):
        return Path(src)
    workdir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "yt-dlp", "-x", "--audio-format", "wav",
        "--restrict-filenames",
        "-o", str(workdir / "%(id)s.%(ext)s"),
        "--print", "after_move:filepath",
        "--no-simulate",
    ]
    if cookies_browser:
        cmd += ["--cookies-from-browser", cookies_browser]
    cmd.append(src)
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"Download failed for {src}:\n{res.stderr.strip()}")
    path = res.stdout.strip().splitlines()[-1]
    return Path(path)


def transcribe(audio, lang):
    import mlx_whisper
    return mlx_whisper.transcribe(
        str(audio),
        path_or_hf_repo=MODEL,
        language=lang,
        verbose=False,
        # Reduces repeated or invented text over silence and music.
        condition_on_previous_text=False,
        no_speech_threshold=0.6,
    )


def diarize(audio):
    import torch
    from pyannote.audio import Pipeline
    token = os.environ.get("HF_TOKEN")
    if not token:
        sys.exit("Set HF_TOKEN to use --diarize.")
    try:
        pipe = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1", token=token)
    except TypeError:
        pipe = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1", use_auth_token=token)
    if torch.backends.mps.is_available():
        pipe.to(torch.device("mps"))
    result = pipe(str(audio))
    annotation = getattr(result, "speaker_diarization", result)
    return [(turn.start, turn.end, spk)
            for turn, _, spk in annotation.itertracks(yield_label=True)]


def speaker_for(seg, turns):
    best, best_overlap = None, 0.0
    for start, end, spk in turns:
        overlap = min(seg["end"], end) - max(seg["start"], start)
        if overlap > best_overlap:
            best, best_overlap = spk, overlap
    return best or "UNKNOWN"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sources", nargs="+")
    ap.add_argument("--diarize", action="store_true")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--cookies-browser", default=None)
    ap.add_argument("--out", default="transcripts")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    for src in args.sources:
        audio = fetch(src, out / "audio", args.cookies_browser)
        print(f"Transcribing {audio.name} ...")
        result = transcribe(audio, args.lang)
        segs = result["segments"]

        if args.diarize:
            print("Labeling speakers ...")
            turns = diarize(audio)
            for s in segs:
                s["speaker"] = speaker_for(s, turns)

        stem = audio.stem
        with open(out / f"{stem}.txt", "w", encoding="utf-8") as f:
            f.write(f"Source: {src}\n\n")
            for s in segs:
                who = f"{s['speaker']}: " if "speaker" in s else ""
                f.write(f"[{fmt(s['start'])}] {who}{s['text'].strip()}\n")
        with open(out / f"{stem}.json", "w", encoding="utf-8") as f:
            json.dump({"source": src, "segments": segs}, f, indent=2)
        print(f"Wrote {out / (stem + '.txt')}")


if __name__ == "__main__":
    main()
