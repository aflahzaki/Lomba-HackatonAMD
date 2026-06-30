"""In-memory metrics collector for monitoring."""

import time
from collections import defaultdict
from typing import Any, Dict, List


class MetricsCollector:
    """Collects and reports application metrics in memory."""

    def __init__(self):
        self.start_time: float = time.time()
        self.total_requests: int = 0
        self.total_predictions: int = 0
        self.total_explanations: int = 0
        self.total_batch_requests: int = 0
        self.total_what_if: int = 0
        self.total_response_time_ms: float = 0.0
        self.endpoint_stats: Dict[str, int] = defaultdict(int)
        self.program_requests: Dict[str, int] = defaultdict(int)
        self.model_version: str = "1.0.0"

    def record_request(self, path: str, response_time_ms: float) -> None:
        """Record a request for metrics tracking."""
        self.total_requests += 1
        self.total_response_time_ms += response_time_ms
        self.endpoint_stats[path] += 1

    def record_prediction(self, program_name: str) -> None:
        """Record a prediction request for a specific program."""
        self.total_predictions += 1
        if program_name:
            self.program_requests[program_name] += 1

    def record_explain(self) -> None:
        """Record an explain request."""
        self.total_explanations += 1

    def record_batch(self, count: int) -> None:
        """Record a batch prediction request."""
        self.total_batch_requests += 1

    def record_what_if(self) -> None:
        """Record a what-if analysis request."""
        self.total_what_if += 1

    @property
    def avg_response_time_ms(self) -> float:
        """Calculate average response time in milliseconds."""
        if self.total_requests == 0:
            return 0.0
        return round(self.total_response_time_ms / self.total_requests, 2)

    @property
    def uptime_seconds(self) -> float:
        """Calculate uptime in seconds since startup."""
        return round(time.time() - self.start_time, 2)

    @property
    def popular_programs(self) -> List[Dict[str, Any]]:
        """Get top 5 most requested programs."""
        sorted_programs = sorted(
            self.program_requests.items(), key=lambda x: x[1], reverse=True
        )
        return [
            {"program": name, "count": count}
            for name, count in sorted_programs[:5]
        ]

    def get_metrics(self) -> Dict[str, Any]:
        """Return all collected metrics as a dictionary."""
        return {
            "total_predictions": self.total_predictions,
            "total_requests": self.total_requests,
            "total_explanations": self.total_explanations,
            "total_batch_requests": self.total_batch_requests,
            "total_what_if": self.total_what_if,
            "avg_response_time_ms": self.avg_response_time_ms,
            "model_version": self.model_version,
            "uptime_seconds": self.uptime_seconds,
            "popular_programs": self.popular_programs,
            "endpoint_stats": dict(self.endpoint_stats),
        }


# Global metrics collector instance
metrics = MetricsCollector()
