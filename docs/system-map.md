<!-- SPDX-License-Identifier: MPL-2.0 -->
# System Map

```mermaid
graph TD
  api[REST API] -->|Publishes metrics| prometheus[(Prometheus)]
  api -->|Streams events| kafka[(Event Bus)]
  ingestion[Ingestion Workers] --> storage[(Object Storage)]
  storage --> analytics[Analytics Jobs]
  analytics --> dashboard[Clinician Dashboard]
```
