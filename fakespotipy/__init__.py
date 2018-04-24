
import logging


logger = logging.getLogger(__name__)


class FakeSpotify(object):
    # <dict{
    #   <str> function name: <list(<object>|<function>, ...)> responses for this function
    # }>
    responses = None

    # <list(<str>, ...)> list of calls made to client, for testing call history
    call_history = None

    def __init__(self, *args, **kwargs):
        """TODO: Should we persist any constructor args/kwargs?
        """
        self.responses = {}
        self.call_history = []

    def add_response(self, function_name, response):
        """
        Params:
            function_name <str>
            response <object>|<function>
        """
        if function_name not in self.responses:
            self.responses[function_name] = []
        self.responses[function_name].append(response)

    def __getattr__(self, function_name):
        logger.info("Called `FakeSpotify.%s`", function_name)
        self.call_history.append(function_name)

        def method(*args, **kwargs):
            if function_name not in self.responses:
                raise NotImplementedError
            responses = self.responses[function_name]
            if not responses:
                raise NotImplementedError
            response = responses.pop(0)
            if callable(response):
                return response(*args, **kwargs)
            return response
        return method
