"""List Of NoBBomb Monitored Services Objects for ANTI BURST control."""

from config.monitored_services import MonitoredService

# NOTE: All SKU are from US-CENTRAL1
# ascii using: https://patorjk.com/software/taag/

MONITORED_SERVICES: list[MonitoredService] = [
    # - - - - - - - - - - - - - - - - - - - - - - - -
    #  ___ _            _
    # | __(_)_ _ ___ __| |_ ___ _ _ ___
    # | _|| | '_/ -_|_-<  _/ _ \ '_/ -_)
    # |_| |_|_| \___/__/\__\___/_| \___|
    #
    # - - - - - - - - - - - - - - - - - - - - - - - -
    # Read Operations
    MonitoredService(
        service_name="Firestore - Read Operations",
        service_id="EE2C-7FAC-5E08",
        sku_name="read_ops",
        sku_id="6A94-8525-876F",
        metric_name="firestore.googleapis.com/document/read_ops_count",
    ),
    # - - - - - - - - - - - - - - - - - - - - - - -
    # Write Operations
    MonitoredService(
        service_name="Firestore - Write Operations",
        service_id="EE2C-7FAC-5E08",
        sku_name="write_ops",
        sku_id="BFCC-1D11-14E1",
        metric_name="firestore.googleapis.com/document/write_ops_count",
    ),
    # - - - - - - - - - - - - - - - - - - - - - - -
    # Delete Operations
    MonitoredService(
        service_name="Firestore - Delete Operations",
        service_id="EE2C-7FAC-5E08",
        sku_name="delete_ops",
        sku_id="B813-E6E7-37F4",
        metric_name="firestore.googleapis.com/document/delete_ops_count",
    ),
    # - - - - - - - - - - - - - - - - - - - - - - -
    # TTL Delete Operations
    MonitoredService(
        service_name="Firestore - TTL Delete Operations",
        service_id="EE2C-7FAC-5E08",
        sku_name="ttl_delete_ops",
        sku_id="6088-280E-4225",
        metric_name="firestore.googleapis.com/document/ttl_deletion_count",
    ),
    # - - - - - - - - - - - - - - - - - - - - - - - -
    #  ___ _       ___
    # | _ |_)__ _ / _ \ _  _ ___ _ _ _  _
    # | _ \ / _` | (_) | || / -_) '_| || |
    # |___/_\__, |\__\_\\_,_\___|_|  \_, |
    #       |___/                    |__/
    # - - - - - - - - - - - - - - - - - - - - - - - -
    # BigQuery - Scanned Bytes
    MonitoredService(
        service_name="BigQuery - Scanned Bytes",
        service_id="24E6-581D-38E5",
        sku_name="Analysis",
        sku_id="3362-E469-6BEF",
        price_tier=1,
        metric_name="bigquery.googleapis.com/query/statement_scanned_bytes_billed",
    ),
    # - - - - - - - - - - - - - - - - - - - - - - - -
    # ____   ____             __                     _____  .___
    # \   \ /   /____________/  |_  ____ ___  ___   /  _  \ |   |
    #  \   Y   // __ \_  __ \   __\/ __ \\  \/  /  /  /_\  \|   |
    #   \     /\  ___/|  | \/|  | \  ___/ >    <  /    |    \   |
    #    \___/  \___  >__|   |__|  \___  >__/\_ \ \____|__  /___|
    #
    # - - - - - - - - - - - - - - - - - - - - - - - -
    # Using : Gemini xxx Text Input - Predictions
    # - - - - - - - - - - - - - - - - - - - - - - -
    # GEMINI 3.0 PRO - TOKENS COUNT (INPUT & OUTPUT)
    MonitoredService(
        service_name="Vertex AI - Gemini 3.0 Pro",
        service_id="C7E2-9256-1C43",
        sku_name="input_token",
        sku_id="EAC4-305F-1249",
        metric_name="aiplatform.googleapis.com/publisher/online_serving/token_count",
        metric_filter='resource.type = "aiplatform.googleapis.com/PublisherModel" AND resource.label.model_user_id = "gemini-3.0-pro" AND metric.label.type = "input"',
    ),
    MonitoredService(
        service_name="Vertex AI - Gemini 3.0 Pro",
        service_id="C7E2-9256-1C43",
        sku_name="output_token",
        sku_id="2737-2D33-D986",
        metric_name="aiplatform.googleapis.com/publisher/online_serving/token_count",
        metric_filter='resource.type = "aiplatform.googleapis.com/PublisherModel" AND resource.label.model_user_id = "gemini-3.0-pro" AND metric.label.type = "output"',
    ),
    # GEMINI 3.0 FLASH - TOKENS COUNT (INPUT & OUTPUT)
    MonitoredService(
        service_name="Vertex AI - Gemini 3.0 Flash",
        service_id="C7E2-9256-1C43",
        sku_name="input_token",
        sku_id="7EBE-3B46-F75C",
        metric_name="aiplatform.googleapis.com/publisher/online_serving/token_count",
        metric_filter='resource.type = "aiplatform.googleapis.com/PublisherModel" AND resource.label.model_user_id = "gemini-3.0-flash" AND metric.label.type = "input"',
    ),
    MonitoredService(
        service_name="Vertex AI - Gemini 3.0 Flash",
        service_id="C7E2-9256-1C43",
        sku_name="output_token",
        sku_id="0127-F0B7-365E",
        metric_name="aiplatform.googleapis.com/publisher/online_serving/token_count",
        metric_filter='resource.type = "aiplatform.googleapis.com/PublisherModel" AND resource.label.model_user_id = "gemini-3.0-flash" AND metric.label.type = "output"',
    ),
    # - - - - - - - - - - - - - - - - - - - - - - -
    # GEMINI 2.5 PRO - TOKENS COUNT (INPUT & OUTPUT)
    MonitoredService(
        service_name="Vertex AI - Gemini 2.5 Pro",
        service_id="C7E2-9256-1C43",
        sku_name="input_token",
        sku_id="A121-E2B5-1418",
        metric_name="aiplatform.googleapis.com/publisher/online_serving/token_count",
        metric_filter='resource.type = "aiplatform.googleapis.com/PublisherModel" AND resource.label.model_user_id = "gemini-2.5-pro" AND metric.label.type = "input"',
    ),
    MonitoredService(
        service_name="Vertex AI - Gemini 2.5 Pro",
        service_id="C7E2-9256-1C43",
        sku_name="output_token",
        sku_id="5DA2-3F77-1CA5",
        metric_name="aiplatform.googleapis.com/publisher/online_serving/token_count",
        metric_filter='resource.type = "aiplatform.googleapis.com/PublisherModel" AND resource.label.model_user_id = "gemini-2.5-pro" AND metric.label.type = "output"',
    ),
    # - - - - - - - - - - - - - - - - - - - - - - -
    # GEMINI 2.5 FLASH - TOKENS COUNT (INPUT & OUTPUT)
    MonitoredService(
        service_name="Vertex AI - Gemini 2.5 Flash",
        service_id="C7E2-9256-1C43",
        sku_name="input_token",
        sku_id="FDAB-647C-5A22",
        metric_name="aiplatform.googleapis.com/publisher/online_serving/token_count",
        metric_filter='resource.type = "aiplatform.googleapis.com/PublisherModel" AND resource.label.model_user_id = "gemini-2.5-flash" AND metric.label.type = "input"',
    ),
    MonitoredService(
        service_name="Vertex AI - Gemini 2.5 Flash",
        service_id="C7E2-9256-1C43",
        sku_name="output_token",
        sku_id="AF56-1BF9-492A",
        metric_name="aiplatform.googleapis.com/publisher/online_serving/token_count",
        metric_filter='resource.type = "aiplatform.googleapis.com/PublisherModel" AND resource.label.model_user_id = "gemini-2.5-flash" AND metric.label.type = "output"',
    ),
    # - - - - - - - - - - - - - - - - - - - - - - -
    # GEMINI 2.5 FLASH LITE - TOKENS COUNT (INPUT & OUTPUT)
    MonitoredService(
        service_name="Vertex AI - Gemini 2.5 Flash Lite",
        service_id="C7E2-9256-1C43",
        sku_name="input_token",
        sku_id="F91E-007E-3BA1",
        metric_name="aiplatform.googleapis.com/publisher/online_serving/token_count",
        metric_filter='resource.type = "aiplatform.googleapis.com/PublisherModel" AND resource.label.model_user_id = "gemini-2.5-flash-lite" AND metric.label.type = "input"',
    ),
    MonitoredService(
        service_name="Vertex AI - Gemini 2.5 Flash Lite",
        service_id="C7E2-9256-1C43",
        sku_name="output_token",
        sku_id="2D6E-6AC5-B1FD",
        metric_name="aiplatform.googleapis.com/publisher/online_serving/token_count",
        metric_filter='resource.type = "aiplatform.googleapis.com/PublisherModel" AND resource.label.model_user_id = "gemini-2.5-flash-lite" AND metric.label.type = "output"',
    ),
    # - - - - - - - - - - - - - - - - - - - - - - -
    # GEMINI 2.0 FLASH - TOKENS COUNT (INPUT & OUTPUT)
    MonitoredService(
        service_name="Vertex AI - Gemini 2.0 Flash",
        service_id="C7E2-9256-1C43",
        sku_name="input_token",
        sku_id="1127-99B9-1860",
        metric_name="aiplatform.googleapis.com/publisher/online_serving/token_count",
        metric_filter='resource.type = "aiplatform.googleapis.com/PublisherModel" AND resource.label.model_user_id = "gemini-2.0-flash" AND metric.label.type = "input"',
    ),
    MonitoredService(
        service_name="Vertex AI - Gemini 2.0 Flash",
        service_id="C7E2-9256-1C43",
        sku_name="output_token",
        sku_id="DFB0-8442-43A8",
        metric_name="aiplatform.googleapis.com/publisher/online_serving/token_count",
        metric_filter='resource.type = "aiplatform.googleapis.com/PublisherModel" AND resource.label.model_user_id = "gemini-2.0-flash" AND metric.label.type = "output"',
    ),
    # - - - - - - - - - - - - - - - - - - - - - - -
    # GEMINI 2.0 FLASH LITE - TOKENS COUNT (INPUT & OUTPUT)
    MonitoredService(
        service_name="Vertex AI - Gemini 2.0 Flash Lite",
        service_id="C7E2-9256-1C43",
        sku_name="input_token",
        sku_id="CF72-F84C-8E3B",
        metric_name="aiplatform.googleapis.com/publisher/online_serving/token_count",
        metric_filter='resource.type = "aiplatform.googleapis.com/PublisherModel" AND resource.label.model_user_id = "gemini-2.0-flash-lite" AND metric.label.type = "input"',
    ),
    MonitoredService(
        service_name="Vertex AI - Gemini 2.0 Flash Lite",
        service_id="C7E2-9256-1C43",
        sku_name="output_token",
        sku_id="4D69-506A-5D33",
        metric_name="aiplatform.googleapis.com/publisher/online_serving/token_count",
        metric_filter='resource.type = "aiplatform.googleapis.com/PublisherModel" AND resource.label.model_user_id = "gemini-2.0-flash-lite" AND metric.label.type = "output"',
    ),
]
