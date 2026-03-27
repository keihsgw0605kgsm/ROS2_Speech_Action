from __future__ import annotations

import argparse

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SpeechSynthesisClient(Node):
    def __init__(self) -> None:
        super().__init__("speech_synthesis_client")
        self._pub = self.create_publisher(String, "/speech", 10)

    def publish_once(self, text: str) -> None:
        msg = String()
        msg.data = text
        self._pub.publish(msg)
        self.get_logger().info(f"Published to /speech: {text!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("text", nargs="+", help="Text to publish to /speech")
    args = parser.parse_args()

    text = " ".join(args.text).strip()
    if not text:
        raise SystemExit(2)

    rclpy.init()
    node = SpeechSynthesisClient()
    try:
        node.publish_once(text)
        # give DDS a moment to send
        rclpy.spin_once(node, timeout_sec=0.2)
    finally:
        node.destroy_node()
        rclpy.shutdown()

