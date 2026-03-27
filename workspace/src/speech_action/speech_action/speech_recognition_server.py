from __future__ import annotations

import traceback

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger

from .recognition import RecognitionConfig, recognize_once


class SpeechRecognitionServer(Node):
    def __init__(self) -> None:
        super().__init__("speech_recognition_server")

        self.declare_parameter("timeout_sec", 10.0)
        self.declare_parameter("phrase_time_limit_sec", 8.0)
        self.declare_parameter("model", "base")
        self.declare_parameter("language", "ja")
        self.declare_parameter("energy_threshold", rclpy.Parameter.Type.INTEGER)
        self.declare_parameter("dynamic_energy_threshold", True)

        self._pub = self.create_publisher(String, "/speech", 10)
        self._srv = self.create_service(Trigger, "/speech_recognize", self._on_trigger)

        self.get_logger().info("Ready. Call /speech_recognize to start recognition.")

    def _on_trigger(self, request: Trigger.Request, response: Trigger.Response) -> Trigger.Response:
        _ = request
        try:
            cfg = RecognitionConfig(
                timeout_sec=float(self.get_parameter("timeout_sec").value),
                phrase_time_limit_sec=float(self.get_parameter("phrase_time_limit_sec").value),
                model=str(self.get_parameter("model").value),
                language=str(self.get_parameter("language").value) or None,
                energy_threshold=(
                    int(self.get_parameter("energy_threshold").value)
                    if self.get_parameter("energy_threshold").type_
                    != rclpy.Parameter.Type.NOT_SET
                    else None
                ),
                dynamic_energy_threshold=bool(self.get_parameter("dynamic_energy_threshold").value),
            )
            text = recognize_once(cfg)

            msg = String()
            msg.data = text
            self._pub.publish(msg)

            response.success = True
            response.message = text
            self.get_logger().info(f"Recognized: {text!r}")
            return response
        except Exception as e:
            response.success = False
            response.message = f"{type(e).__name__}: {e}"
            self.get_logger().error(response.message)
            self.get_logger().debug(traceback.format_exc())
            return response


def main() -> None:
    rclpy.init()
    node = SpeechRecognitionServer()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

