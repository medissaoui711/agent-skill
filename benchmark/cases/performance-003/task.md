# Performance Review Task — Spring report export

## Contract
The endpoint accepts authenticated export requests. The service may receive bursts of concurrent requests. Each export performs blocking database and file operations. The application must apply bounded concurrency and reject or queue excess work according to the documented executor policy. Do not infer deployment-specific traffic numbers.

## Review scope
Inspect the supplied service. Identify concrete resource, throughput, or reliability defects and explain their operational impact without inventing load-test results.
