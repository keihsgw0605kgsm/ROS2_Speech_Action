from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RecognitionConfig:
    timeout_sec: Optional[float] = 10.0
    phrase_time_limit_sec: Optional[float] = 8.0
    model: str = "base"
    language: Optional[str] = "ja"
    energy_threshold: Optional[int] = None
    dynamic_energy_threshold: bool = True


def recognize_once(cfg: RecognitionConfig) -> str:
    """
    Record from default microphone and transcribe using SpeechRecognition's Whisper backend.

    Requires `SpeechRecognition` + `openai-whisper` to be installed inside the container.
    """
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = cfg.dynamic_energy_threshold
    if cfg.energy_threshold is not None:
        recognizer.energy_threshold = int(cfg.energy_threshold)

    with sr.Microphone() as source:
        audio = recognizer.listen(
            source,
            timeout=cfg.timeout_sec,
            phrase_time_limit=cfg.phrase_time_limit_sec,
        )

    text = recognizer.recognize_whisper(
        audio_data=audio,
        model=cfg.model,
        language=cfg.language,
    )
    return text.strip()

