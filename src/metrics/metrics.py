from prometheus_client import Counter, Histogram

WORK_TIME = Histogram("lead_time", "The time for which the filter is applied")

FILTERS_USED = Counter("filters_used", "Filters used for photo processing", labelnames=["filter"])

