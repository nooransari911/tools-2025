from genai_gemini_parallel import *

events_blueprint = Blueprint('events', __name__)


@events_blueprint.route('/events')
def sse_stream_process():
    def event_stream_process():
        while True:
            data = sse_json_processes()
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(5)  # Adjust interval as needed

    return Response(stream_with_context(event_stream_process()), content_type='text/event-stream')