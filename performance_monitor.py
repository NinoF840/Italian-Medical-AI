#!/usr/bin/env python3
"""
Performance Monitor for New Medical Italian
Tracks memory usage, cache performance, and response times
"""

import psutil
import time
import gc
from functools import wraps
from typing import Dict, Any
from datetime import datetime

class PerformanceMonitor:
    """Monitor application performance metrics"""
    
    def __init__(self):
        self.metrics = {
            'cache_hits': 0,
            'cache_misses': 0,
            'total_requests': 0,
            'avg_response_time': 0,
            'memory_usage': [],
            'gc_collections': 0
        }
        self.start_time = time.time()
    
    def track_memory(self):
        """Track current memory usage"""
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        self.metrics['memory_usage'].append({
            'timestamp': datetime.now().isoformat(),
            'memory_mb': round(memory_mb, 2)
        })
        return memory_mb
    
    def track_cache_performance(self, hit: bool):
        """Track cache hit/miss ratio"""
        if hit:
            self.metrics['cache_hits'] += 1
        else:
            self.metrics['cache_misses'] += 1
    
    def get_cache_hit_ratio(self) -> float:
        """Calculate cache hit ratio"""
        total = self.metrics['cache_hits'] + self.metrics['cache_misses']
        if total == 0:
            return 0.0
        return self.metrics['cache_hits'] / total
    
    def performance_decorator(self, func):
        """Decorator to track function performance"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            self.metrics['total_requests'] += 1
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                response_time = end_time - start_time
                
                # Update average response time
                current_avg = self.metrics['avg_response_time']
                total_requests = self.metrics['total_requests']
                self.metrics['avg_response_time'] = (
                    (current_avg * (total_requests - 1) + response_time) / total_requests
                )
                
                # Track memory usage periodically
                if self.metrics['total_requests'] % 10 == 0:
                    self.track_memory()
        
        return wrapper
    
    def force_garbage_collection(self):
        """Force garbage collection and track it"""
        collected = gc.collect()
        self.metrics['gc_collections'] += 1
        return collected
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        uptime = time.time() - self.start_time
        current_memory = self.track_memory()
        
        report = {
            'uptime_seconds': round(uptime, 2),
            'total_requests': self.metrics['total_requests'],
            'avg_response_time': round(self.metrics['avg_response_time'], 3),
            'cache_hit_ratio': round(self.get_cache_hit_ratio(), 3),
            'current_memory_mb': current_memory,
            'gc_collections': self.metrics['gc_collections'],
            'requests_per_second': round(self.metrics['total_requests'] / uptime, 2) if uptime > 0 else 0
        }
        
        # Memory trend (last 10 measurements)
        if len(self.metrics['memory_usage']) > 1:
            recent_memory = self.metrics['memory_usage'][-10:]
            memory_values = [m['memory_mb'] for m in recent_memory]
            report['memory_trend'] = {
                'min': min(memory_values),
                'max': max(memory_values),
                'avg': round(sum(memory_values) / len(memory_values), 2)
            }
        
        return report
    
    def print_performance_summary(self):
        """Print a formatted performance summary"""
        report = self.get_performance_report()
        
        print("\n" + "="*50)
        print("🚀 PERFORMANCE OPTIMIZATION SUMMARY")
        print("="*50)
        print(f"⏱️  Uptime: {report['uptime_seconds']}s")
        print(f"📊 Total Requests: {report['total_requests']}")
        print(f"⚡ Avg Response Time: {report['avg_response_time']}s")
        print(f"💾 Cache Hit Ratio: {report['cache_hit_ratio']:.1%}")
        print(f"🧠 Current Memory: {report['current_memory_mb']:.1f} MB")
        print(f"🗑️  GC Collections: {report['gc_collections']}")
        print(f"📈 Requests/Second: {report['requests_per_second']}")
        
        if 'memory_trend' in report:
            trend = report['memory_trend']
            print(f"📉 Memory Trend: {trend['min']:.1f}-{trend['max']:.1f} MB (avg: {trend['avg']:.1f})")
        
        print("="*50)

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

# Usage examples:
# @performance_monitor.performance_decorator
# def my_function():
#     pass
#
# performance_monitor.track_cache_performance(hit=True)
# performance_monitor.print_performance_summary()

