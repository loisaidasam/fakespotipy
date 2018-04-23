
import logging


logger = logging.getLogger(__name__)


class FakeSpotify(object):
    # <dict{
    #   <str> function name: <list(<object>|<function>, ...)> responses for this function
    # }>
    responses = None

    def __init__(self, *args, **kwargs):
        """TODO: Do we need to persist any args/kwargs?
        """
        self.responses = {}

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
