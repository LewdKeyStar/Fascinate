from dataclasses import dataclass

from src.utils.ffprobe_utils import get_resolution, get_fps, get_duration

@dataclass(init = False)
class VideoInfo:

    fps: int
    resolution: str
    duration: int

    def __init__(self, video_path):
        self.fps = get_fps(video_path)
        self.resolution = get_resolution(video_path)
        self.duration = get_duration(video_path)
