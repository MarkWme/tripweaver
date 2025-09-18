#!/bin/bash
# CVE-2025-6297 Mitigation Script
set -euo pipefail

check_disk_usage() {
    local path="${1:-/}"
    local usage
    usage=$(df "$path" | awk 'NR==2 {print $(NF-1)}' | sed 's/%//')
    echo "Disk usage: ${usage}%"
    
    if [[ $usage -ge 90 ]]; then
        echo "CRITICAL: Disk usage at ${usage}%"
        return 2
    elif [[ $usage -ge 80 ]]; then
        echo "WARNING: Disk usage at ${usage}%"
        return 1
    else
        echo "OK: Disk usage at ${usage}%"
        return 0
    fi
}

echo "=== CVE-2025-6297 Disk Monitoring Report ===" 
echo "Timestamp: $(date)"
echo
check_disk_usage
