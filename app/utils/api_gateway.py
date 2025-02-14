import time
from functools import wraps
from fastapi import Request, HTTPException, status

class APIGateway:
    """Handles API rate limiting and other gateway functionalities."""

    def __init__(self):
        self.calls = []  # Store timestamps of API requests

    def rate_limited(self, max_calls: int, time_frame: int):
        """
        Rate limit decorator to restrict API requests.
        :param max_calls: Maximum allowed calls in the given time frame.
        :param time_frame: Time frame (in seconds) for rate limiting.
        :return: Decorator function.
        """

        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                now = time.time()
                
                # Keep only recent calls within the time frame
                self.calls = [call for call in self.calls if now - call < time_frame]

                if len(self.calls) >= max_calls:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit exceeded. Please try again later."
                    )

                self.calls.append(now)
                return await func(request, *args, **kwargs)

            return wrapper
        return decorator
