#!/bin/bash
#MISE alias=["destroy","purge"]
#MISE description="Destroy major components of NoBBomb. Use with caution, this is irreversible."

source .mise-tasks/utils/base_import.sh

source .mise-tasks/destroy/cloud_scheduler.sh

source .mise-tasks/destroy/pub_sub.sh

source .mise-tasks/destroy/event_arc.sh

source .mise-tasks/destroy/cloud_run.sh

source .mise-tasks/destroy/budget_alert.sh