# utils/exceptions.py
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and isinstance(response.data, dict):
        errors = response.data

        # Pick first error message
        if isinstance(errors, dict):
            # get first message (nested lists happen in serializer errors)
            first_error = None
            for val in errors.values():
                if isinstance(val, list):
                    first_error = val[0]
                else:
                    first_error = val
                break
            response.data = {"detail": str(first_error)}

    return response
