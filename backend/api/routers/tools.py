"""
Tools API router
Handles strace integration and system analysis tools
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import subprocess
import asyncio
import tempfile
import os
import json
import uuid
import logging
import signal
import time

logger = logging.getLogger(__name__)

router = APIRouter()

class StraceRequest(BaseModel):
    """Strace execution request"""
    target_type: str  # "command", "pid", "attach"
    target: str       # Command to run or PID to attach to
    options: Optional[Dict[str, Any]] = None
    duration: Optional[int] = None  # Maximum duration in seconds
    output_format: str = "json"  # "json", "text"

class StraceSession(BaseModel):
    """Strace session information"""
    id: str
    status: str  # "running", "completed", "failed", "stopped"
    pid: Optional[int] = None
    start_time: float
    end_time: Optional[float] = None
    target: str
    output_file: Optional[str] = None

class StraceResult(BaseModel):
    """Strace analysis result"""
    session_id: str
    status: str
    raw_output: str
    parsed_data: Dict[str, Any]
    statistics: Dict[str, Any]
    timeline: List[Dict[str, Any]]

class LtraceRequest(BaseModel):
    """Ltrace execution request"""
    target_type: str
    target: str
    options: Optional[Dict[str, Any]] = None
    duration: Optional[int] = None

# Global storage for tool sessions
tool_sessions: Dict[str, StraceSession] = {}
tool_results: Dict[str, StraceResult] = {}

@router.post("/strace/start", response_model=StraceSession)
async def start_strace(request: StraceRequest, background_tasks: BackgroundTasks):
    """Start a new strace session"""
    session_id = str(uuid.uuid4())
    
    session = StraceSession(
        id=session_id,
        status="running",
        start_time=time.time(),
        target=request.target
    )
    
    tool_sessions[session_id] = session
    
    # Start strace in background
    background_tasks.add_task(run_strace, session_id, request)
    
    return session

@router.get("/strace/session/{session_id}", response_model=StraceSession)
async def get_strace_session(session_id: str):
    """Get strace session status"""
    if session_id not in tool_sessions:
        raise HTTPException(status_code=404, detail="Strace session not found")
    
    return tool_sessions[session_id]

@router.get("/strace/session/{session_id}/result", response_model=StraceResult)
async def get_strace_result(session_id: str):
    """Get strace session result"""
    if session_id not in tool_results:
        if session_id in tool_sessions:
            session = tool_sessions[session_id]
            if session.status == "running":
                raise HTTPException(status_code=409, detail="Strace session still running")
            else:
                raise HTTPException(status_code=404, detail="Strace result not available")
        else:
            raise HTTPException(status_code=404, detail="Strace session not found")
    
    return tool_results[session_id]

@router.delete("/strace/session/{session_id}")
async def stop_strace(session_id: str):
    """Stop a running strace session"""
    if session_id not in tool_sessions:
        raise HTTPException(status_code=404, detail="Strace session not found")
    
    session = tool_sessions[session_id]
    
    if session.status == "running" and session.pid:
        try:
            # Send SIGTERM to strace process
            os.kill(session.pid, signal.SIGTERM)
            session.status = "stopped"
            session.end_time = time.time()
            logger.info(f"Stopped strace session {session_id}")
        except ProcessLookupError:
            session.status = "completed"
            logger.info(f"Strace session {session_id} already completed")
        except Exception as e:
            logger.error(f"Error stopping strace session {session_id}: {e}")
            raise HTTPException(status_code=500, detail="Error stopping strace session")
    
    return {"message": f"Strace session {session_id} stopped"}

@router.get("/strace/sessions")
async def list_strace_sessions():
    """List all strace sessions"""
    sessions = []
    
    for session_id, session in tool_sessions.items():
        sessions.append({
            "id": session_id,
            "status": session.status,
            "target": session.target,
            "start_time": session.start_time,
            "end_time": session.end_time
        })
    
    return {"sessions": sessions}

@router.post("/strace/analyze")
async def analyze_strace_output(output: str):
    """Analyze raw strace output and extract insights"""
    try:
        analysis = parse_strace_output(output)
        return {
            "analysis": analysis,
            "insights": generate_strace_insights(analysis)
        }
    except Exception as e:
        logger.error(f"Error analyzing strace output: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing strace output")

@router.get("/system/processes")
async def get_process_list():
    """Get list of running processes for attachment"""
    try:
        result = subprocess.run(
            ["ps", "aux", "--no-headers"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail="Error getting process list")
        
        processes = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split(None, 10)
                if len(parts) >= 11:
                    processes.append({
                        "user": parts[0],
                        "pid": int(parts[1]),
                        "cpu": float(parts[2]),
                        "mem": float(parts[3]),
                        "command": parts[10]
                    })
        
        return {"processes": processes[:100]}  # Limit to first 100 processes
    
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Process list request timed out")
    except Exception as e:
        logger.error(f"Error getting process list: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving process list")

@router.get("/system/syscalls")
async def get_available_syscalls():
    """Get list of available system calls on the system"""
    try:
        # Try to get syscall list from various sources
        syscalls = []
        
        # Method 1: Check if we have syscall numbers
        try:
            result = subprocess.run(
                ["grep", "-r", "^#define.*__NR_", "/usr/include/"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            for line in result.stdout.split('\n'):
                if '__NR_' in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        syscall_name = parts[1].replace('__NR_', '')
                        try:
                            syscall_num = int(parts[2])
                            syscalls.append({"name": syscall_name, "number": syscall_num})
                        except ValueError:
                            continue
        except:
            pass
        
        # Method 2: Use ausyscall if available
        if not syscalls:
            try:
                result = subprocess.run(
                    ["ausyscall", "--dump"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                for line in result.stdout.split('\n')[1:]:  # Skip header
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            syscalls.append({
                                "name": parts[1],
                                "number": int(parts[0])
                            })
            except:
                pass
        
        # Fallback: Common syscalls
        if not syscalls:
            syscalls = [
                {"name": "read", "number": 0},
                {"name": "write", "number": 1},
                {"name": "open", "number": 2},
                {"name": "close", "number": 3},
                {"name": "stat", "number": 4},
                {"name": "fstat", "number": 5},
                {"name": "lstat", "number": 6},
                {"name": "poll", "number": 7},
                {"name": "lseek", "number": 8},
                {"name": "mmap", "number": 9},
                {"name": "mprotect", "number": 10}
            ]
        
        return {"syscalls": syscalls[:200]}  # Limit results
    
    except Exception as e:
        logger.error(f"Error getting syscall list: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving syscall list")

async def run_strace(session_id: str, request: StraceRequest):
    """Background task to run strace"""
    session = tool_sessions[session_id]
    
    try:
        # Create temporary output file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.strace') as f:
            output_file = f.name
        
        session.output_file = output_file
        
        # Build strace command
        cmd = ["strace", "-o", output_file]
        
        # Add options
        if request.options:
            if request.options.get("follow_forks"):
                cmd.append("-f")
            if request.options.get("trace_syscalls"):
                syscalls = request.options["trace_syscalls"]
                if isinstance(syscalls, list):
                    cmd.extend(["-e", "trace=" + ",".join(syscalls)])
            if request.options.get("timestamps"):
                cmd.append("-t")
            if request.options.get("relative_timestamps"):
                cmd.append("-r")
        
        # Add target
        if request.target_type == "command":
            cmd.extend(request.target.split())
        elif request.target_type == "pid":
            cmd.extend(["-p", request.target])
        
        # Run strace
        process = subprocess.Popen(cmd)
        session.pid = process.pid
        
        # Wait for completion or timeout
        try:
            if request.duration:
                process.wait(timeout=request.duration)
            else:
                process.wait()
        except subprocess.TimeoutExpired:
            process.kill()
            session.status = "timeout"
        
        session.end_time = time.time()
        
        # Read and parse output
        try:
            with open(output_file, 'r') as f:
                raw_output = f.read()
            
            parsed_data = parse_strace_output(raw_output)
            statistics = generate_strace_statistics(parsed_data)
            
            result = StraceResult(
                session_id=session_id,
                status="completed",
                raw_output=raw_output,
                parsed_data=parsed_data,
                statistics=statistics,
                timeline=[]  # Generate timeline in real implementation
            )
            
            tool_results[session_id] = result
            session.status = "completed"
            
        except Exception as e:
            logger.error(f"Error parsing strace output: {e}")
            session.status = "failed"
        
        # Clean up temporary file
        try:
            os.unlink(output_file)
        except:
            pass
        
    except Exception as e:
        logger.error(f"Error running strace: {e}")
        session.status = "failed"
        session.end_time = time.time()

def parse_strace_output(output: str) -> Dict[str, Any]:
    """Parse strace output and extract system call information"""
    syscalls = []
    errors = []
    
    for line in output.split('\n'):
        line = line.strip()
        if not line or line.startswith('+++') or line.startswith('---'):
            continue
        
        try:
            # Simple parsing - in production, use more robust parsing
            if '(' in line and ')' in line:
                syscall_name = line.split('(')[0].strip()
                if '=' in line:
                    result_part = line.split('=')[-1].strip()
                    if result_part.startswith('-1'):
                        errors.append(line)
                
                syscalls.append({
                    "name": syscall_name,
                    "raw": line
                })
        except:
            continue
    
    return {
        "syscalls": syscalls,
        "errors": errors,
        "total_calls": len(syscalls),
        "error_count": len(errors)
    }

def generate_strace_statistics(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate statistics from parsed strace data"""
    syscalls = parsed_data["syscalls"]
    
    # Count syscall frequency
    syscall_counts = {}
    for call in syscalls:
        name = call["name"]
        syscall_counts[name] = syscall_counts.get(name, 0) + 1
    
    # Sort by frequency
    most_frequent = sorted(syscall_counts.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "total_syscalls": len(syscalls),
        "unique_syscalls": len(syscall_counts),
        "error_rate": parsed_data["error_count"] / len(syscalls) if syscalls else 0,
        "most_frequent": [{"name": name, "count": count} for name, count in most_frequent[:10]],
        "syscall_distribution": syscall_counts
    }

def generate_strace_insights(analysis: Dict[str, Any]) -> List[str]:
    """Generate insights from strace analysis"""
    insights = []
    
    stats = analysis["statistics"]
    
    if stats["error_rate"] > 0.1:
        insights.append("High error rate detected - check for failed system calls")
    
    if stats["total_syscalls"] > 10000:
        insights.append("High number of system calls - consider optimizing I/O operations")
    
    most_frequent = stats["most_frequent"]
    if most_frequent and most_frequent[0]["name"] in ["read", "write"]:
        insights.append("I/O intensive application - monitor buffer sizes and batch operations")
    
    if len(stats["unique_syscalls"]) > 50:
        insights.append("Application uses many different system calls - complex functionality detected")
    
    return insights