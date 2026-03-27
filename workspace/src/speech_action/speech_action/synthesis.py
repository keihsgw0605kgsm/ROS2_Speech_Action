from __future__ import annotations

import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SynthesisConfig:
    lang: str = "en"
    slow: bool = False
    output_dir: str = "/tmp/speech_action_tts"
    play: bool = True
    player_cmd: str = "ffplay"


def synthesize_to_mp3(text: str, cfg: SynthesisConfig) -> Path:
    from gtts import gTTS

    out_dir = Path(cfg.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(prefix="tts_", suffix=".mp3", dir=out_dir, delete=False) as f:
        out_path = Path(f.name)

    tts = gTTS(text=text, lang=cfg.lang, slow=cfg.slow)
    tts.save(str(out_path))
    return out_path


def play_audio(path: Path, cfg: SynthesisConfig) -> None:
    if not cfg.play:
        return

    # ffplay is included in ffmpeg package. In Docker, audio routing may depend on host setup.
    env = os.environ.copy()
    subprocess.run(
        [cfg.player_cmd, "-nodisp", "-autoexit", "-loglevel", "error", str(path)],
        check=False,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def synthesize_once(text: str, cfg: SynthesisConfig) -> Path:
    path = synthesize_to_mp3(text, cfg)
    play_audio(path, cfg)
    return path

