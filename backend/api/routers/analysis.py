"""
Analysis API router
Handles performance analysis and real-time monitoring
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import asyncio
import time
import subprocess
import json
import uuid
import logging
import psutil

logger = logging.getLogger(__name__)

router = APIRouter()

class AnalysisRequest(BaseModel):
    """Analysis request model"""
    target_type: str  # "process", "command", "pid"
    target: str       # Process name, command, or PID
    duration: int = 10  # Analysis duration in seconds
    metrics: List[str] = ["syscalls", "performance", "io"]
    filters: Optional[Dict[str, Any]] = None

class AnalysisSession(BaseModel):
    """Analysis session information"""
    id: str
    status: str  # "running", "completed", "failed"
    start_time: float
    end_time: Optional[float] = None
    target: str
    metrics: List[str]
    progress: int = 0

class AnalysisResult(BaseModel):
    """Analysis result model"""
    session_id: str
    status: str
    syscall_summary: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    io_analysis: Dict[str, Any]
    timeline: List[Dict[str, Any]]
    recommendations: List[str]

# Global storage for analysis sessions (in production, use a proper database)
active_sessions: Dict[str, AnalysisSession] = {}
completed_results: Dict[str, AnalysisResult] = {}

@router.post("/start", response_model=AnalysisSession)
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Start a new analysis session"""
    session_id = str(uuid.uuid4())
    
    session = AnalysisSession(
        id=session_id,
        status="running",
        start_time=time.time(),
        target=request.target,
        metrics=request.metrics
    )
    
    active_sessions[session_id] = session
    
    # Start analysis in background
    background_tasks.add_task(run_analysis, session_id, request)
    
    return session

@router.get("/session/{session_id}", response_model=AnalysisSession)
async def get_session_status(session_id: str):
    """Get analysis session status"""
    if session_id in active_sessions:
        return active_sessions[session_id]
    elif session_id in completed_results:
        # Return completed session info
        result = completed_results[session_id]
        return AnalysisSession(
            id=session_id,
            status=result.status,
            start_time=0,  # Set from stored data in real implementation
            target="",     # Set from stored data in real implementation
            metrics=[],    # Set from stored data in real implementation
            progress=100
        )
    else:
        raise HTTPException(status_code=404, detail="Analysis session not found")

@router.get("/session/{session_id}/result", response_model=AnalysisResult)
async def get_analysis_result(session_id: str):
    """Get completed analysis result"""
    if session_id not in completed_results:
        if session_id in active_sessions:
            raise HTTPException(status_code=409, detail="Analysis still in progress")
        else:
            raise HTTPException(status_code=404, detail="Analysis result not found")
    
    return completed_results[session_id]

@router.delete("/session/{session_id}")
async def stop_analysis(session_id: str):
    """Stop an active analysis session"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Analysis session not found")
    
    session = active_sessions[session_id]
    session.status = "stopped"
    session.end_time = time.time()
    
    return {"message": f"Analysis session {session_id} stopped"}

@router.get("/sessions")
async def list_analysis_sessions():
    """List all analysis sessions"""
    all_sessions = {}
    
    # Add active sessions
    for session_id, session in active_sessions.items():
        all_sessions[session_id] = {
            "id": session_id,
            "status": session.status,
            "target": session.target,
            "progress": session.progress
        }
    
    # Add completed sessions
    for session_id, result in completed_results.items():
        all_sessions[session_id] = {
            "id": session_id,
            "status": result.status,
            "target": "",  # Get from result in real implementation
            "progress": 100
        }
    
    return {"sessions": list(all_sessions.values())}

@router.get("/system/info")
async def get_system_info():
    """Get current system information"""
    try:
        return {
            "cpu": {
                "count": psutil.cpu_count(),
                "usage": psutil.cpu_percent(interval=1),
                "load_avg": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "usage": psutil.disk_usage('/').percent,
                "io": psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else None
            },
            "network": psutil.net_io_counters()._asdict() if psutil.net_io_counters() else None,
            "processes": len(psutil.pids())
        }
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving system information")

@router.get("/processes")
async def list_processes():
    """List running processes with basic information"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                proc_info = proc.info
                processes.append({
                    "pid": proc_info['pid'],
                    "name": proc_info['name'],
                    "cpu_percent": proc_info['cpu_percent'],
                    "memory_percent": proc_info['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return {"processes": processes[:50]}  # Limit to first 50 processes
    
    except Exception as e:
        logger.error(f"Error listing processes: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving process list")

async def run_analysis(session_id: str, request: AnalysisRequest):
    """Background task to run analysis"""
    try:
        session = active_sessions[session_id]
        
        # Simulate analysis progress
        for i in range(0, 101, 10):
            session.progress = i
            await asyncio.sleep(request.duration / 10)
            
            if session.status == "stopped":
                return
        
        # Create mock analysis result
        result = AnalysisResult(
            session_id=session_id,
            status="completed",
            syscall_summary={
                "total_calls": 1250,
                "unique_calls": 23,
                "most_frequent": [
                    {"name": "read", "count": 342},
                    {"name": "write", "count": 298},
                    {"name": "open", "count": 156},
                    {"name": "close", "count": 154},
                    {"name": "mmap", "count": 89}
                ],
                "error_rate": 0.02
            },
            performance_metrics={
                "avg_execution_time": 0.000123,
                "total_cpu_time": 0.152,
                "context_switches": 45,
                "page_faults": 12
            },
            io_analysis={
                "bytes_read": 1048576,
                "bytes_written": 524288,
                "files_accessed": 15,
                "network_connections": 3
            },
            timeline=[
                {"timestamp": time.time() - 10, "event": "Analysis started"},
                {"timestamp": time.time() - 5, "event": "Peak system call activity"},
                {"timestamp": time.time(), "event": "Analysis completed"}
            ],
            recommendations=[
                "Consider batching write operations to reduce system call overhead",
                "Monitor file descriptor usage to prevent leaks",
                "Optimize buffer sizes for better I/O performance"
            ]
        )
        
        # Move session to completed results
        completed_results[session_id] = result
        session.status = "completed"
        session.end_time = time.time()
        
        # Remove from active sessions
        del active_sessions[session_id]
        
        logger.info(f"Analysis {session_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Error in analysis {session_id}: {e}")
        session = active_sessions.get(session_id)
        if session:
            session.status = "failed"
            session.end_time = time.time()