# traceloop_config.py
from traceloop.sdk import Traceloop

def initialize_traceloop():
    Traceloop.init(
        disable_batch=True,
        api_key=<your traceloop api key>
    )
