"""
Tests for disk monitoring functionality (CVE-2025-6297 mitigation)
"""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from app.disk_monitor import DiskMonitor


def test_disk_monitor_initialization():
    """Test that DiskMonitor initializes correctly with default parameters."""
    monitor = DiskMonitor()
    assert monitor.warning_threshold == 80.0
    assert monitor.critical_threshold == 90.0
    assert '/tmp' in monitor.temp_dirs
    assert '/var/tmp' in monitor.temp_dirs


def test_disk_monitor_custom_thresholds():
    """Test DiskMonitor with custom thresholds."""
    monitor = DiskMonitor(warning_threshold=70.0, critical_threshold=85.0)
    assert monitor.warning_threshold == 70.0
    assert monitor.critical_threshold == 85.0


def test_get_disk_usage_healthy():
    """Test disk usage reporting for healthy system."""
    monitor = DiskMonitor()
    
    # Mock shutil.disk_usage to return healthy usage
    with patch('app.disk_monitor.shutil.disk_usage') as mock_usage:
        mock_usage.return_value = MagicMock(
            total=1000000000,  # 1GB
            used=500000000,    # 500MB (50%)
            free=500000000     # 500MB
        )
        
        usage = monitor.get_disk_usage('/')
        
        assert usage['path'] == '/'
        assert usage['used_percent'] == 50.0
        assert usage['free_percent'] == 50.0
        assert 'timestamp' in usage


def test_get_health_status_healthy():
    """Test overall health status for healthy system."""
    monitor = DiskMonitor()
    
    with patch('app.disk_monitor.shutil.disk_usage') as mock_usage, \
         patch.object(monitor, 'check_temp_directories') as mock_temp:
        
        mock_usage.return_value = MagicMock(
            total=1000000000,
            used=500000000,    # 50% usage - healthy
            free=500000000
        )
        
        mock_temp.return_value = [
            {
                'path': '/tmp',
                'file_count': 10,
                'dpkg_related_files': 0
            }
        ]
        
        health = monitor.get_health_status()
        
        assert health['status'] == 'healthy'
        assert len(health['alerts']) == 0
        assert health['cve_mitigation'] == 'CVE-2025-6297'


def test_get_health_status_warning():
    """Test health status when disk usage is at warning level."""
    monitor = DiskMonitor(warning_threshold=75.0)
    
    with patch('app.disk_monitor.shutil.disk_usage') as mock_usage, \
         patch.object(monitor, 'check_temp_directories') as mock_temp:
        
        mock_usage.return_value = MagicMock(
            total=1000000000,
            used=800000000,    # 80% usage - warning
            free=200000000
        )
        
        mock_temp.return_value = []
        
        health = monitor.get_health_status()
        
        assert health['status'] == 'warning'
        assert len(health['alerts']) > 0
        assert 'Disk usage at 80.0%' in health['alerts'][0]


def test_get_health_status_critical():
    """Test health status when disk usage is critical."""
    monitor = DiskMonitor(critical_threshold=85.0)
    
    with patch('app.disk_monitor.shutil.disk_usage') as mock_usage, \
         patch.object(monitor, 'check_temp_directories') as mock_temp:
        
        mock_usage.return_value = MagicMock(
            total=1000000000,
            used=900000000,    # 90% usage - critical
            free=100000000
        )
        
        mock_temp.return_value = []
        
        health = monitor.get_health_status()
        
        assert health['status'] == 'critical'
        assert len(health['alerts']) > 0
        assert 'Critical: Disk usage at 90.0%' in health['alerts'][0]


def test_check_temp_directories_with_dpkg_files():
    """Test detection of suspicious dpkg files in temp directories."""
    monitor = DiskMonitor()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some test files including dpkg-related ones
        os.makedirs(os.path.join(temp_dir, 'subdir'), exist_ok=True)
        
        test_files = [
            'normal_file.txt',
            'dpkg-tmp-123',
            'tmp.dpkg.456',
            'another_file.log'
        ]
        
        for filename in test_files:
            filepath = os.path.join(temp_dir, filename)
            with open(filepath, 'w') as f:
                f.write('test content')
        
        # Override temp_dirs to use our test directory
        monitor.temp_dirs = [temp_dir]
        
        temp_stats = monitor.check_temp_directories()
        
        assert len(temp_stats) == 1
        stats = temp_stats[0]
        assert stats['path'] == temp_dir
        assert stats['file_count'] == len(test_files)
        assert stats['dpkg_related_files'] == 2  # dpkg-tmp-123 and tmp.dpkg.456


def test_cleanup_temp_files_dry_run():
    """Test temp file cleanup in dry-run mode."""
    monitor = DiskMonitor()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create an old temporary file
        old_file = os.path.join(temp_dir, 'tmp.old_file')
        with open(old_file, 'w') as f:
            f.write('old content')
        
        # Modify file time to make it appear old
        import time
        old_time = time.time() - (25 * 3600)  # 25 hours ago
        os.utime(old_file, (old_time, old_time))
        
        monitor.temp_dirs = [temp_dir]
        
        # Run dry cleanup
        result = monitor.cleanup_temp_files(max_age_hours=24, dry_run=True)
        
        assert result['dry_run'] == True
        assert result['files_deleted'] >= 1
        assert os.path.exists(old_file)  # File should still exist in dry-run


def test_error_handling_nonexistent_path():
    """Test error handling for nonexistent paths."""
    monitor = DiskMonitor()
    
    usage = monitor.get_disk_usage('/nonexistent/path')
    
    assert 'error' in usage
    assert usage['path'] == '/nonexistent/path'


def test_global_monitor_instance():
    """Test that the global disk_monitor instance is available."""
    from app.disk_monitor import disk_monitor
    
    assert isinstance(disk_monitor, DiskMonitor)
    assert disk_monitor.warning_threshold == 80.0