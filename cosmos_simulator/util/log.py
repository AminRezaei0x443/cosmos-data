def log(artifact_type, artifact_name, event, time, message):
    # print(
    #     f"[{artifact_type}] [{artifact_name}::{event}] [{format_time(time)}] {message}"
    # )
    print(
        f"[{artifact_type} | {artifact_name}::{event} | {format_time(time)}] {message}"
    )


def format_time(s):
    h = s // 3600
    m = (s - h * 3600) // 60
    s = s - h * 3600 - m * 60
    return f"{h:02d}:{m:02d}:{s:02d}"
