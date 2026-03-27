from __future__ import annotations

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class SpeechRecognitionClient(Node):
    def __init__(self) -> None:
        super().__init__("speech_recognition_client")
        self._cli = self.create_client(Trigger, "/speech_recognize")

    def run_once(self) -> int:
        self.get_logger().info("Waiting for /speech_recognize service...")
        if not self._cli.wait_for_service(timeout_sec=10.0):
            self.get_logger().error("Service /speech_recognize not available.")
            return 1

        req = Trigger.Request()
        self.get_logger().info("Sending recognition trigger. Speak into the microphone.")
        fut = self._cli.call_async(req)
        rclpy.spin_until_future_complete(self, fut)

        res = fut.result()
        if res is None:
            self.get_logger().error("Service call failed.")
            return 1

        if res.success:
            self.get_logger().info(f"Recognized: {res.message}")
            return 0
        else:
            self.get_logger().error(f"Recognition failed: {res.message}")
            return 2


def main() -> None:
    rclpy.init()
    node = SpeechRecognitionClient()
    try:
        raise SystemExit(node.run_once())
    finally:
        node.destroy_node()
        rclpy.shutdown()

