import logging
import time

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestTimingMiddleware(MiddlewareMixin):
    """
    Middleware that measures request processing time.
    Demonstrates process_request and process_response methods.
    """

    def process_request(self, request):
        """Called before the view is executed."""
        request.start_time = time.time()
        logger.info(f"Request started: {request.method} {request.path}")
        return None  # Continue processing

    def process_response(self, request, response):
        """Called after the view returns a response."""
        if hasattr(request, "start_time"):
            duration = time.time() - request.start_time
            logger.info(
                f"Request completed: {request.method} {request.path} - {duration:.3f}s"
            )
            # Add timing header to response
            response["X-Process-Time"] = f"{duration:.3f}"
        return response


class RateLimitingMiddleware(MiddlewareMixin):
    """
    Simple rate limiting middleware.
    Demonstrates process_request method with early return.
    """

    def process_request(self, request):
        """Check rate limit before processing the request."""
        # Skip rate limiting for admin and static files
        if request.path.startswith("/admin/") or request.path.startswith("/static/"):
            return None

        # Get client IP
        ip_address = self.get_client_ip(request)
        cache_key = f"rate_limit_{ip_address}"

        # Get current request count
        request_count = cache.get(cache_key, 0)

        # Set limit (e.g., 100 requests per minute)
        if request_count >= 100:
            logger.warning(f"Rate limit exceeded for IP: {ip_address}")
            return JsonResponse(
                {"error": "Rate limit exceeded. Please try again later."}, status=429
            )

        # Increment counter
        cache.set(cache_key, request_count + 1, 60)  # 60 seconds TTL
        return None  # Continue processing

    def get_client_ip(self, request):
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class APIErrorHandlingMiddleware(MiddlewareMixin):
    """
    Middleware for handling API errors gracefully.
    Demonstrates process_exception method.
    """

    def process_exception(self, request, exception):
        """Handle exceptions that occur during request processing."""
        # Only handle API requests
        if request.path.startswith("/api/"):
            logger.error(f"API Error: {str(exception)}", exc_info=True)

            # Return JSON error response for API requests
            return JsonResponse(
                {
                    "error": "An internal server error occurred.",
                    "detail": str(exception) if settings.DEBUG else None,
                },
                status=500,
            )

        # Return None to let Django handle it normally for non-API requests
        return None


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware for detailed request logging.
    Demonstrates process_view method.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Called just before Django calls the view."""
        # Log view information
        view_name = (
            view_func.__name__ if hasattr(view_func, "__name__") else str(view_func)
        )
        logger.info(
            f"View called: {view_name} with args={view_args}, kwargs={view_kwargs}"
        )

        # Add view info to request for use in response
        request.view_name = view_name
        return None  # Continue processing

    def process_response(self, request, response):
        """Add view information to response headers."""
        if hasattr(request, "view_name"):
            response["X-View-Name"] = request.view_name
        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware to add security headers to responses.
    Demonstrates process_response method.
    """

    def process_response(self, request, response):
        """Add security headers to all responses."""
        # Add security headers
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"

        # Add CORS headers for API requests (if not already handled by django-cors-headers)
        if request.path.startswith("/api/"):
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        return response
