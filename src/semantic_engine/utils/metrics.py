# m2-semantic-engine
# -----------------------------------------
# License : Dual License
#           - Apache 2.0 for open-source / personal use
#           - Commercial license required for closed-source use
# Author  : Md Mahbubur Rahman
# URL     : https://m-a-h-b-u-b.github.io
# GitHub  : https://github.com/m-a-h-b-u-b/m2-semantic-engine

from prometheus_client import Counter, Histogram

queries_total = Counter("m2_queries_total", "Total number of queries served")
query_latency_seconds = Histogram("m2_query_latency_seconds", "Query latency in seconds")
