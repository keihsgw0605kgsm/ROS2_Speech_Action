from setuptools import setup

package_name = "speech_action"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="hasegawakei",
    maintainer_email="you@example.com",
    description="Speech recognition and synthesis actions for ROS 2",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "speech_recognition_server = speech_action.speech_recognition_server:main",
            "speech_recognition_client = speech_action.speech_recognition_client:main",
            "speech_synthesis_server = speech_action.speech_synthesis_server:main",
            "speech_synthesis_client = speech_action.speech_synthesis_client:main",
            "speech_client = speech_action.speech_client:main",
        ],
    },
)
