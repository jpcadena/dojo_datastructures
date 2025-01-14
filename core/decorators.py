"""
This module provides decorators designed to provide additional
 functionality to the functions they are used with.
"""
import functools
import logging
from time import perf_counter
from typing import Any, Callable

logger: logging.Logger = logging.getLogger(__name__)


def with_logging(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator that logs the start and end of a function's execution.
    :param func: The function to be decorated
    :type func: Callable
    :return: The decorated function that logs its call
    :rtype: Callable
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        A wrapper function that adds logging functionality
        :param args: Positional arguments to be passed to the decorated
         function
        :type args: Any
        :param kwargs: Keyword arguments to be passed to the decorated
         function
        :type kwargs: Any
        :return: The result of the decorated function's execution
        :rtype: Any
        """
        logger.info("\nCalling %s", func.__name__)
        value = func(*args, **kwargs)
        logger.info("Finished %s\n", func.__name__)
        return value

    return wrapper


def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    This decorator provides a benchmarking feature by logging the
     execution time of the decorated function
    :param func: The function to be executed
    :type func: Callable
    :return: The decorated function that logs its execution time
    :rtype: Callable
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        A wrapper function that adds benchmarking functionality
        :param args: Positional arguments to be passed to the decorated
         function
        :type args: Any
        :param kwargs: Keyword arguments to be passed to the decorated
         function
        :type kwargs: Any
        :return: The result of the decorated function's execution
        :rtype: Any
        """
        start_time: float = perf_counter()
        value = func(*args, **kwargs)
        end_time: float = perf_counter()
        run_time: float = end_time - start_time
        logger.info("Execution of %s took %s seconds.", func.__name__, run_time)
        return value

    return wrapper
