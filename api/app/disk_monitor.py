"""
Disk Space Monitoring Module for CVE-2025-6297 Mitigation

This module provides disk space monitoring functionality to detect potential
disk exhaustion attacks that could be exploited through the dpkg vulnerability.
"""

import os
import shutil
import logging
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class DiskMonitor:
    """Monitor disk space and detect potential exhaustion attacks."""
    
    def __init__(self, 
                 warning_threshold: float = 80.0,
                 critical_threshold: float = 90.0,
                 temp_dirs: Optional[List[str]] = None):
        """
        Initialize disk monitor.
        
        Args:
            warning_threshold: Percentage at which to issue warnings
            critical_threshold: Percentage at which to issue critical alerts
            temp_dirs: List of temporary directories to monitor
        """
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.temp_dirs = temp_dirs or ['/tmp', '/var/tmp']
        
    def get_disk_usage(self, path: str = '/') -> Dict[str, float]:
        """
        Get disk usage statistics for a given path.
        
        Args:
            path: Path to check (default: root filesystem)
            
        Returns:
            Dictionary with usage statistics
        """
        try:
            usage = shutil.disk_usage(path)
            total = usage.total
            used = usage.used
            free = usage.free
            
            used_percent = (used / total) * 100 if total > 0 else 0
            free_percent = (free / total) * 100 if total > 0 else 0
            
            return {
                'path': path,
                'total_bytes': total,
                'used_bytes': used,
                'free_bytes': free,
                'used_percent': round(used_percent, 2),
                'free_percent': round(free_percent, 2),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        except OSError as e:
            logger.error(f"Failed to get disk usage for {path}: {e}")
            return {
                'path': path,
                'error': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
    
    def check_temp_directories(self) -> List[Dict]:
        """
        Check temporary directories for unusual file accumulation.
        
        Returns:
            List of temp directory statistics
        """
        temp_stats = []
        
        for temp_dir in self.temp_dirs:
            if not os.path.exists(temp_dir):
                continue
                
            try:
                # Count files and calculate total size
                file_count = 0
                total_size = 0
                dpkg_files = 0
                
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            stat = os.stat(file_path)
                            file_count += 1
                            total_size += stat.st_size
                            
                            # Check for dpkg-related temporary files
                            if 'dpkg' in file.lower() or file.startswith('tmp.'):
                                dpkg_files += 1
                        except (OSError, FileNotFoundError):
                            # File may have been deleted during scan
                            continue
                
                temp_stats.append({
                    'path': temp_dir,
                    'file_count': file_count,
                    'total_size_bytes': total_size,
                    'dpkg_related_files': dpkg_files,
                    'timestamp': datetime.now(timezone.utc).isoformat()
                })
                
            except OSError as e:
                logger.error(f"Failed to scan temp directory {temp_dir}: {e}")
                temp_stats.append({
                    'path': temp_dir,
                    'error': str(e),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                })
        
        return temp_stats
    
    def get_health_status(self) -> Dict:
        """
        Get overall disk health status for health checks.
        
        Returns:
            Health status dictionary
        """
        root_usage = self.get_disk_usage('/')
        temp_stats = self.check_temp_directories()
        
        # Determine overall status
        status = 'healthy'
        alerts = []
        
        if 'used_percent' in root_usage:
            if root_usage['used_percent'] >= self.critical_threshold:
                status = 'critical'
                alerts.append(f"Critical: Disk usage at {root_usage['used_percent']}%")
            elif root_usage['used_percent'] >= self.warning_threshold:
                status = 'warning'
                alerts.append(f"Warning: Disk usage at {root_usage['used_percent']}%")
        
        # Check for excessive temp files
        for temp_stat in temp_stats:
            if 'dpkg_related_files' in temp_stat and temp_stat['dpkg_related_files'] > 100:
                status = 'warning'
                alerts.append(f"Many dpkg temp files found in {temp_stat['path']}: {temp_stat['dpkg_related_files']}")
        
        return {
            'status': status,
            'disk_usage': root_usage,
            'temp_directories': temp_stats,
            'alerts': alerts,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'cve_mitigation': 'CVE-2025-6297'
        }
    
    def cleanup_temp_files(self, max_age_hours: int = 24, dry_run: bool = True) -> Dict:
        """
        Clean up old temporary files to prevent accumulation.
        
        Args:
            max_age_hours: Maximum age of files to keep (hours)
            dry_run: If True, only report what would be deleted
            
        Returns:
            Cleanup report
        """
        import time
        
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        cleanup_report = {
            'dry_run': dry_run,
            'max_age_hours': max_age_hours,
            'files_processed': 0,
            'files_deleted': 0,
            'bytes_freed': 0,
            'errors': [],
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        for temp_dir in self.temp_dirs:
            if not os.path.exists(temp_dir):
                continue
                
            try:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            stat = os.stat(file_path)
                            cleanup_report['files_processed'] += 1
                            
                            # Check if file is old enough and looks like a temp file
                            if (current_time - stat.st_mtime > max_age_seconds and 
                                (file.startswith('tmp.') or 'dpkg' in file.lower())):
                                
                                if not dry_run:
                                    os.remove(file_path)
                                    logger.info(f"Cleaned up temp file: {file_path}")
                                
                                cleanup_report['files_deleted'] += 1
                                cleanup_report['bytes_freed'] += stat.st_size
                                
                        except (OSError, FileNotFoundError) as e:
                            cleanup_report['errors'].append(f"Error processing {file_path}: {str(e)}")
                            
            except OSError as e:
                cleanup_report['errors'].append(f"Error scanning {temp_dir}: {str(e)}")
        
        return cleanup_report


# Global disk monitor instance
disk_monitor = DiskMonitor()