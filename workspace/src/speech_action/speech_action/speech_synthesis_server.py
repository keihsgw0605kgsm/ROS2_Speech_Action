from __future__ import annotations

import threading

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from .synthesis import SynthesisConfig, synthesize_once


class SpeechSynthesisServer(Node):
    def __init__(self) -> None:
        super().__init__("speech_synthesis_server")

        self.declare_parameter("lang", "en")
        self.declare_parameter("slow", False)
        self.declare_parameter("output_dir", "/tmp/speech_action_tts")
        self.declare_parameter("play", True)
        self.declare_parameter("player_cmd", "ffplay")

        self._busy = False
        self._lock = threading.Lock()

        self._sub = self.create_subscription(String, "/speech", self._on_speech, 10)
        self.get_logger().info("Subscribed to /speech. Publishing text will be spoken.")

    def _config(self) -> SynthesisConfig:
        return SynthesisConfig(
            lang=str(self.get_parameter("lang").value),
            slow=bool(self.get_parameter("slow").value),
            output_dir=str(self.get_parameter("output_dir").value),
            play=bool(self.get_parameter("play").value),
            player_cmd=str(self.get_parameter("player_cmd").value),
        )

    def _on_speech(self, msg: String) -> None:
        text = (msg.data or "").strip()
        if not text:
            return

        with self._lock:
            if self._busy:
                self.get_logger().warn("Busy speaking. Dropping incoming /speech message.")
                return
            self._busy = True

        def worker() -> None:
            try:
                cfg = self._config()
                out_path = synthesize_once(text, cfg)
                self.get_logger().info(f"Spoken: {text!r} (mp3={out_path})")
            except Exception as e:
                self.get_logger().error(f"Synthesis failed: {type(e).__name__}: {e}")
            finally:
                with self._lock:
                    self._busy = False

        threading.Thread(target=worker, daemon=True).start()


def main() -> None:
    rclpy.init()
    node = SpeechSynthesisServer()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

