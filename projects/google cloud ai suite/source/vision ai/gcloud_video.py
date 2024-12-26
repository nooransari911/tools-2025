import os, json
from datetime import timedelta
from typing import Optional, Sequence, cast

from google.cloud import videointelligence_v1 as vi

START_TIME=250
STOP_TIME=350


video_uri = "gs://gcloud_image_intelligence/The Lesser Evil - Pick it.mp4"
segment = vi.VideoSegment(
    start_time_offset=timedelta(seconds=START_TIME),
    end_time_offset=timedelta(seconds=STOP_TIME),
)





def detect_text(
    video_uri: str,
    language_hints: Optional[Sequence[str]] = None,
    segments: Optional[Sequence[vi.VideoSegment]] = None,) -> vi.VideoAnnotationResults:

    video_client = vi.VideoIntelligenceServiceClient()
    features = [vi.Feature.TEXT_DETECTION]
    config = vi.TextDetectionConfig(
        language_hints=language_hints,
    )
    context = vi.VideoContext(
        segments=segments,
        text_detection_config=config,
    )
    request = vi.AnnotateVideoRequest(
        input_uri=video_uri,
        features=features,
        video_context=context,
    )

    print(f'Processing video "{video_uri}"...')
    operation = video_client.annotate_video(request)

    # Wait for operation to complete
    response = cast (vi.AnnotateVideoResponse, operation.result())
    # A single video is processed
    results = response.annotation_results[0]


    """results_string = json.dumps (results)


    json_file_path = "/home/ansarimn/Downloads/tools and projects/projects/py_web_dev_2/google cloud intelligence/json"
    output_file_path = os.path.join(json_file_path, os.path.basename("video_intelligence.json"))
    with open(output_file_path, 'w') as file:
        file.write(results_string)"""

    return results




results = detect_text(video_uri, segments=[segment])




def sorted_by_first_segment_end(
        annotations: Sequence[vi.TextAnnotation],) -> Sequence[vi.TextAnnotation]:
    def first_segment_end(annotation: vi.TextAnnotation) -> int:
        return annotation.segments[0].segment.end_time_offset.total_seconds()

    return sorted(annotations, key=first_segment_end)


def segment_seconds(segment: vi.VideoSegment) -> float:
    t1 = segment.start_time_offset.total_seconds()
    t2 = segment.end_time_offset.total_seconds()
    return t2 - t1




def print_video_text(results: vi.VideoAnnotationResults, min_frames: int = 15):
    annotations = sorted_by_first_segment_end(results.text_annotations)

    print(" Detected text ".center(80, "-"))
    for annotation in annotations:
        for text_segment in annotation.segments:
            frames = len(text_segment.frames)
            if frames < min_frames:
                continue
            text = annotation.text
            confidence = text_segment.confidence
            start = text_segment.segment.start_time_offset
            seconds = segment_seconds(text_segment.segment)
            print(f"{text}")
            #print(f"  {confidence:4.0%} | {start} + {seconds:.1f}s | {frames} fr.")






print_video_text(results)
