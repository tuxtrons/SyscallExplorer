"""
System calls API router
Handles system call exploration and parameter visualization
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
import os
import subprocess
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class SystemCallInfo(BaseModel):
    """System call information model"""
    name: str
    number: int
    description: str
    parameters: List[Dict[str, Any]]
    return_type: str
    examples: List[str]
    man_page: Optional[str] = None

class SystemCallRequest(BaseModel):
    """System call execution request"""
    name: str
    parameters: Dict[str, Any]
    trace: bool = False

class SystemCallResult(BaseModel):
    """System call execution result"""
    success: bool
    return_value: Any
    errno: Optional[int] = None
    error_message: Optional[str] = None
    trace_data: Optional[Dict[str, Any]] = None
    performance_metrics: Optional[Dict[str, Any]] = None

# Common system calls database
SYSTEM_CALLS_DB = {
    "open": {
        "name": "open",
        "number": 2,
        "description": "Open file and return file descriptor",
        "parameters": [
            {"name": "pathname", "type": "const char *", "description": "Path to file"},
            {"name": "flags", "type": "int", "description": "File access mode and flags"},
            {"name": "mode", "type": "mode_t", "description": "File permission mode (optional)"}
        ],
        "return_type": "int",
        "examples": [
            'open("/tmp/test.txt", O_RDONLY)',
            'open("/tmp/test.txt", O_WRONLY | O_CREAT, 0644)'
        ]
    },
    "read": {
        "name": "read",
        "number": 0,
        "description": "Read bytes from file descriptor",
        "parameters": [
            {"name": "fd", "type": "int", "description": "File descriptor"},
            {"name": "buf", "type": "void *", "description": "Buffer to read into"},
            {"name": "count", "type": "size_t", "description": "Number of bytes to read"}
        ],
        "return_type": "ssize_t",
        "examples": [
            'read(fd, buffer, 1024)',
            'read(STDIN_FILENO, buffer, sizeof(buffer))'
        ]
    },
    "write": {
        "name": "write",
        "number": 1,
        "description": "Write bytes to file descriptor",
        "parameters": [
            {"name": "fd", "type": "int", "description": "File descriptor"},
            {"name": "buf", "type": "const void *", "description": "Buffer to write from"},
            {"name": "count", "type": "size_t", "description": "Number of bytes to write"}
        ],
        "return_type": "ssize_t",
        "examples": [
            'write(fd, "Hello", 5)',
            'write(STDOUT_FILENO, message, strlen(message))'
        ]
    },
    "close": {
        "name": "close",
        "number": 3,
        "description": "Close file descriptor",
        "parameters": [
            {"name": "fd", "type": "int", "description": "File descriptor to close"}
        ],
        "return_type": "int",
        "examples": [
            'close(fd)',
            'close(STDIN_FILENO)'
        ]
    },
    "fork": {
        "name": "fork",
        "number": 57,
        "description": "Create a child process",
        "parameters": [],
        "return_type": "pid_t",
        "examples": [
            'pid_t pid = fork();'
        ]
    },
    "exec": {
        "name": "execve",
        "number": 59,
        "description": "Execute a program",
        "parameters": [
            {"name": "filename", "type": "const char *", "description": "Path to executable"},
            {"name": "argv", "type": "char *const argv[]", "description": "Argument vector"},
            {"name": "envp", "type": "char *const envp[]", "description": "Environment variables"}
        ],
        "return_type": "int",
        "examples": [
            'execve("/bin/ls", argv, envp)',
            'execve("/usr/bin/python3", argv, envp)'
        ]
    }
}

@router.get("/", response_model=List[str])
async def list_system_calls():
    """Get list of available system calls"""
    return list(SYSTEM_CALLS_DB.keys())

@router.get("/{syscall_name}", response_model=SystemCallInfo)
async def get_system_call_info(syscall_name: str):
    """Get detailed information about a specific system call"""
    if syscall_name not in SYSTEM_CALLS_DB:
        raise HTTPException(status_code=404, detail=f"System call '{syscall_name}' not found")
    
    call_info = SYSTEM_CALLS_DB[syscall_name]
    return SystemCallInfo(**call_info)

@router.get("/category/{category}")
async def get_system_calls_by_category(category: str):
    """Get system calls by category (file, process, network, etc.)"""
    categories = {
        "file": ["open", "read", "write", "close"],
        "process": ["fork", "exec"],
        "network": [],  # To be implemented
        "memory": [],   # To be implemented
    }
    
    if category not in categories:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found")
    
    return {
        "category": category,
        "system_calls": categories[category],
        "details": [SYSTEM_CALLS_DB[name] for name in categories[category] if name in SYSTEM_CALLS_DB]
    }

@router.post("/simulate", response_model=SystemCallResult)
async def simulate_system_call(request: SystemCallRequest):
    """Simulate a system call execution (educational purposes)"""
    if request.name not in SYSTEM_CALLS_DB:
        raise HTTPException(status_code=404, detail=f"System call '{request.name}' not found")
    
    # This is a simulation for educational purposes
    # In a real implementation, you would carefully control actual system call execution
    
    try:
        # Simulate different system call behaviors
        if request.name == "open":
            # Simulate file opening
            return SystemCallResult(
                success=True,
                return_value=3,  # Simulated file descriptor
                performance_metrics={"execution_time_us": 125}
            )
        elif request.name == "read":
            # Simulate reading
            return SystemCallResult(
                success=True,
                return_value=request.parameters.get("count", 0),
                performance_metrics={"execution_time_us": 45}
            )
        elif request.name == "write":
            # Simulate writing
            return SystemCallResult(
                success=True,
                return_value=request.parameters.get("count", 0),
                performance_metrics={"execution_time_us": 78}
            )
        else:
            return SystemCallResult(
                success=True,
                return_value=0,
                performance_metrics={"execution_time_us": 50}
            )
    
    except Exception as e:
        logger.error(f"Error simulating system call {request.name}: {e}")
        return SystemCallResult(
            success=False,
            return_value=-1,
            errno=1,
            error_message=str(e)
        )

@router.get("/man/{syscall_name}")
async def get_man_page(syscall_name: str):
    """Get manual page information for a system call"""
    try:
        # Get man page content
        result = subprocess.run(
            ["man", "2", syscall_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return {
                "syscall": syscall_name,
                "man_page": result.stdout,
                "available": True
            }
        else:
            return {
                "syscall": syscall_name,
                "man_page": None,
                "available": False,
                "error": "Manual page not found"
            }
    
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Manual page request timed out")
    except Exception as e:
        logger.error(f"Error getting man page for {syscall_name}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving manual page")

@router.get("/search")
async def search_system_calls(
    query: str = Query(..., description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """Search system calls by name or description"""
    results = []
    
    for name, info in SYSTEM_CALLS_DB.items():
        if (query.lower() in name.lower() or 
            query.lower() in info["description"].lower()):
            results.append({
                "name": name,
                "description": info["description"],
                "number": info["number"]
            })
    
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }