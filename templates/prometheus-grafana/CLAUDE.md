# [PROJECT NAME] - [ONE LINE DESCRIPTION]

## Tech Stack

- Prometheus v2.50+ for metrics collection and alerting
- Grafana v10+ for dashboards and visualization
- Alertmanager for alert routing, grouping, and silencing
- Thanos Sidecar for long-term storage and global querying
- Node Exporter, kube-state-metrics, and cAdvisor for infrastructure metrics
- Prometheus Operator (kube-prometheus-stack) for CRD-based configuration
- Loki for log aggregation alongside metrics

## Project Structure

```
.
├── prometheus/
│   ├── rules/
│   │   ├── infrastructure/
│   │   │   ├── node-alerts.yaml
│   │   │   ├── kube-alerts.yaml
│   │   │   └── recording-rules.yaml
│   │   ├── application/
│   │   │   ├── slo-alerts.yaml
│   │   │   ├── latency-alerts.yaml
│   │   │   └── error-rate-alerts.yaml
│   │   └── business/
│   │       └── kpi-alerts.yaml
│   ├── servicemonitors/
│   ├── podmonitors/
│   └── prometheus-config.yaml
├── alertmanager/
│   ├── alertmanager-config.yaml
│   ├── templates/
│   │   ├── slack.tmpl
│   │   └── pagerduty.tmpl
│   └── routes/
├── grafana/
│   ├── dashboards/
│   │   ├── infrastructure/
│   │   ├── application/
│   │   └── business/
│   ├── provisioning/
│   │   ├── dashboards/
│   │   └── datasources/
│   └── grafana.ini
├── thanos/
│   ├── query.yaml
│   ├── store.yaml
│   └── compactor.yaml
└── exporters/
    ├── blackbox/
    └── custom/
```

## Architecture Rules

- All alerting rules must follow the multi-window multi-burn-rate approach for SLO-based alerts
- Recording rules must pre-aggregate high-cardinality metrics; store as namespace:metric_name:aggregation
- ServiceMonitors must have a namespaceSelector and label selector that matches exactly one service
- Retention policy: Prometheus local storage 15d, Thanos object storage 90d for 5m resolution, 1y for 1h resolution
- Every PrometheusRule must define a runbook_url annotation linking to the runbook in the ops wiki
- Dashboard UIDs must be deterministic (derived from dashboard title) to enable version-controlled provisioning
- Alertmanager routing tree: critical goes to PagerDuty, warning goes to Slack, info goes to email digest

## Coding Conventions

- Alert names use PascalCase: HighErrorRate, PodCrashLooping, NodeMemoryPressure
- Recording rule names follow the convention: level:metric_name:operations (e.g., job:http_requests_total:rate5m)
- Dashboard JSON files must be generated from Grafonnet or grafana-foundation-sdk, never hand-edited
- PromQL queries must use rate() over a window of at least 4x the scrape interval
- All histogram queries must use histogram_quantile() with le label; never compute percentiles from summaries in new code
- Labels: severity (critical/warning/info), team (owning team slug), service (service name from service catalog)

## Library Preferences

- Use Grafonnet (Jsonnet library) for all dashboard definitions; JSON exports only for one-off exploration
- Use Prometheus Operator CRDs (PrometheusRule, ServiceMonitor, PodMonitor) instead of file-based config
- Use Thanos for multi-cluster federation instead of Prometheus federation
- Use promtool for rule validation and unit testing
- Use Mimir for scenarios requiring multi-tenancy at scale

## File Naming

- Alert rule files: {domain}-alerts.yaml (e.g., payment-alerts.yaml)
- Recording rule files: {domain}-recording-rules.yaml
- Grafana dashboards: {service}-{aspect}.json (e.g., api-gateway-latency.json)
- ServiceMonitors: {service-name}-servicemonitor.yaml
- Alertmanager templates: {channel}.tmpl

## NEVER DO THIS

1. Never use count() without a by() clause on alerts; unbounded cardinality will cause OOM on Prometheus
2. Never set a scrape interval below 15s for production workloads; 30s is the recommended default
3. Never create alerts that fire on instantaneous values; always use for: duration of at least 5m for warnings and 2m for critical
4. Never use regex matchers (=~) in PromQL when an exact match (=) works; regex matching is 10x slower
5. Never store Grafana dashboard state in the Grafana database; all dashboards must be provisioned from version control
6. Never create alerts without severity, team, and runbook_url labels/annotations

## Testing

- Run `promtool check rules` on all rule files in CI before merge
- Write promtool unit tests for every alerting rule covering both firing and resolved scenarios
- Validate ServiceMonitor selectors match existing services with a CI script that runs kubectl dry-run
- Grafana dashboards must pass `grafana-cli dashboard validate` with no undefined variables
- Load-test recording rules against production-scale cardinality using Prometheus benchmarking dataset
- Test Alertmanager routing with amtool config routes test using representative label sets
- Run thanos-tools bucket verify on object storage configuration in staging before production rollout
