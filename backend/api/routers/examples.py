"""
Examples API router
Handles code generation and common system call patterns
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class CodeExample(BaseModel):
    """Code example model"""
    id: str
    title: str
    description: str
    language: str
    code: str
    system_calls: List[str]
    category: str
    difficulty: str  # "beginner", "intermediate", "advanced"
    tags: List[str]

class GenerationRequest(BaseModel):
    """Code generation request"""
    system_calls: List[str]
    language: str = "c"
    pattern: str = "basic"  # "basic", "error_handling", "performance"
    include_comments: bool = True

# Example code patterns database
EXAMPLES_DB = {
    "file_basic": CodeExample(
        id="file_basic",
        title="Basic File Operations",
        description="Demonstrates basic file open, read, write, and close operations",
        language="c",
        code='''#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>

int main() {
    // Open file for reading
    int fd = open("example.txt", O_RDONLY);
    if (fd == -1) {
        perror("open");
        return 1;
    }
    
    // Read from file
    char buffer[1024];
    ssize_t bytes_read = read(fd, buffer, sizeof(buffer) - 1);
    if (bytes_read == -1) {
        perror("read");
        close(fd);
        return 1;
    }
    
    buffer[bytes_read] = '\\0';
    printf("Read %zd bytes: %s\\n", bytes_read, buffer);
    
    // Close file
    if (close(fd) == -1) {
        perror("close");
        return 1;
    }
    
    return 0;
}''',
        system_calls=["open", "read", "close"],
        category="file_operations",
        difficulty="beginner",
        tags=["file", "basic", "io"]
    ),
    
    "process_fork": CodeExample(
        id="process_fork",
        title="Process Creation with Fork",
        description="Demonstrates process creation using fork() system call",
        language="c",
        code='''#include <unistd.h>
#include <sys/wait.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    pid_t pid = fork();
    
    if (pid == -1) {
        perror("fork");
        return 1;
    } else if (pid == 0) {
        // Child process
        printf("Child process (PID: %d)\\n", getpid());
        printf("Parent PID: %d\\n", getppid());
        exit(0);
    } else {
        // Parent process
        printf("Parent process (PID: %d)\\n", getpid());
        printf("Child PID: %d\\n", pid);
        
        // Wait for child to complete
        int status;
        wait(&status);
        printf("Child process completed\\n");
    }
    
    return 0;
}''',
        system_calls=["fork", "getpid", "getppid", "wait", "exit"],
        category="process_management",
        difficulty="intermediate",
        tags=["process", "fork", "wait"]
    ),
    
    "socket_server": CodeExample(
        id="socket_server",
        title="Simple TCP Server",
        description="Basic TCP server using socket system calls",
        language="c",
        code='''#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main() {
    int server_fd, client_fd;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    char buffer[BUFFER_SIZE] = {0};
    
    // Create socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket");
        return 1;
    }
    
    // Setup address structure
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);
    
    // Bind socket to address
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind");
        close(server_fd);
        return 1;
    }
    
    // Listen for connections
    if (listen(server_fd, 3) < 0) {
        perror("listen");
        close(server_fd);
        return 1;
    }
    
    printf("Server listening on port %d\\n", PORT);
    
    // Accept connection
    if ((client_fd = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
        perror("accept");
        close(server_fd);
        return 1;
    }
    
    // Read from client
    read(client_fd, buffer, BUFFER_SIZE);
    printf("Received: %s\\n", buffer);
    
    // Send response
    char *response = "Hello from server!";
    send(client_fd, response, strlen(response), 0);
    
    // Clean up
    close(client_fd);
    close(server_fd);
    
    return 0;
}''',
        system_calls=["socket", "bind", "listen", "accept", "read", "send", "close"],
        category="network",
        difficulty="advanced",
        tags=["socket", "network", "tcp", "server"]
    ),
    
    "memory_map": CodeExample(
        id="memory_map",
        title="Memory Mapping Example",
        description="Demonstrates memory mapping using mmap system call",
        language="c",
        code='''#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main() {
    const char *filename = "example.txt";
    int fd;
    struct stat sb;
    char *mapped;
    
    // Open file
    fd = open(filename, O_RDONLY);
    if (fd == -1) {
        perror("open");
        return 1;
    }
    
    // Get file size
    if (fstat(fd, &sb) == -1) {
        perror("fstat");
        close(fd);
        return 1;
    }
    
    // Map file into memory
    mapped = mmap(NULL, sb.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (mapped == MAP_FAILED) {
        perror("mmap");
        close(fd);
        return 1;
    }
    
    // File descriptor no longer needed
    close(fd);
    
    // Use mapped memory
    printf("File contents:\\n%.*s\\n", (int)sb.st_size, mapped);
    
    // Unmap memory
    if (munmap(mapped, sb.st_size) == -1) {
        perror("munmap");
        return 1;
    }
    
    return 0;
}''',
        system_calls=["open", "fstat", "mmap", "close", "munmap"],
        category="memory_management",
        difficulty="intermediate",
        tags=["mmap", "memory", "file_mapping"]
    )
}

# Language templates for code generation
LANGUAGE_TEMPLATES = {
    "c": {
        "headers": ["#include <unistd.h>", "#include <fcntl.h>", "#include <stdio.h>", "#include <errno.h>"],
        "main_start": "int main() {",
        "main_end": "    return 0;\n}",
        "error_handling": "if ({call} == -1) {\n        perror(\"{syscall}\");\n        return 1;\n    }"
    },
    "python": {
        "imports": ["import os", "import sys", "import errno"],
        "main_start": "def main():",
        "main_end": "if __name__ == '__main__':\n    main()",
        "error_handling": "try:\n    {call}\nexcept OSError as e:\n    print(f\"Error: {e}\")\n    sys.exit(1)"
    }
}

@router.get("/", response_model=List[CodeExample])
async def list_examples(
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    language: Optional[str] = Query(None, description="Filter by language")
):
    """Get list of code examples with optional filters"""
    examples = list(EXAMPLES_DB.values())
    
    if category:
        examples = [ex for ex in examples if ex.category == category]
    
    if difficulty:
        examples = [ex for ex in examples if ex.difficulty == difficulty]
    
    if language:
        examples = [ex for ex in examples if ex.language == language]
    
    return examples

@router.get("/{example_id}", response_model=CodeExample)
async def get_example(example_id: str):
    """Get a specific code example"""
    if example_id not in EXAMPLES_DB:
        raise HTTPException(status_code=404, detail="Example not found")
    
    return EXAMPLES_DB[example_id]

@router.get("/categories/list")
async def list_categories():
    """Get list of available categories"""
    categories = set(ex.category for ex in EXAMPLES_DB.values())
    return {"categories": list(categories)}

@router.post("/generate")
async def generate_code(request: GenerationRequest):
    """Generate code based on specified system calls and pattern"""
    if request.language not in LANGUAGE_TEMPLATES:
        raise HTTPException(status_code=400, detail=f"Language '{request.language}' not supported")
    
    template = LANGUAGE_TEMPLATES[request.language]
    
    # Generate code based on system calls
    if request.language == "c":
        code = generate_c_code(request, template)
    elif request.language == "python":
        code = generate_python_code(request, template)
    else:
        raise HTTPException(status_code=400, detail="Code generation not implemented for this language")
    
    return {
        "generated_code": code,
        "language": request.language,
        "system_calls": request.system_calls,
        "pattern": request.pattern
    }

def generate_c_code(request: GenerationRequest, template: Dict[str, Any]) -> str:
    """Generate C code for specified system calls"""
    lines = []
    
    # Add headers
    if request.include_comments:
        lines.append("// Generated system call example")
        lines.append("// System calls: " + ", ".join(request.system_calls))
        lines.append("")
    
    lines.extend(template["headers"])
    lines.append("")
    lines.append(template["main_start"])
    
    # Generate system call code
    for syscall in request.system_calls:
        if request.include_comments:
            lines.append(f"    // {syscall} system call")
        
        if syscall == "open":
            lines.append('    int fd = open("example.txt", O_RDONLY);')
            if request.pattern == "error_handling":
                lines.append('    if (fd == -1) {')
                lines.append('        perror("open");')
                lines.append('        return 1;')
                lines.append('    }')
        elif syscall == "read":
            lines.append('    char buffer[1024];')
            lines.append('    ssize_t bytes = read(fd, buffer, sizeof(buffer));')
            if request.pattern == "error_handling":
                lines.append('    if (bytes == -1) {')
                lines.append('        perror("read");')
                lines.append('        return 1;')
                lines.append('    }')
        elif syscall == "write":
            lines.append('    const char *data = "Hello, World!";')
            lines.append('    ssize_t written = write(fd, data, strlen(data));')
            if request.pattern == "error_handling":
                lines.append('    if (written == -1) {')
                lines.append('        perror("write");')
                lines.append('        return 1;')
                lines.append('    }')
        elif syscall == "close":
            lines.append('    close(fd);')
    
    lines.append("")
    lines.append(template["main_end"])
    
    return "\n".join(lines)

def generate_python_code(request: GenerationRequest, template: Dict[str, Any]) -> str:
    """Generate Python code for specified system calls"""
    lines = []
    
    # Add imports
    if request.include_comments:
        lines.append("# Generated system call example")
        lines.append("# System calls: " + ", ".join(request.system_calls))
        lines.append("")
    
    lines.extend(template["imports"])
    lines.append("")
    lines.append(template["main_start"])
    
    # Generate system call code
    for syscall in request.system_calls:
        if request.include_comments:
            lines.append(f"    # {syscall} system call")
        
        if syscall == "open":
            lines.append('    fd = os.open("example.txt", os.O_RDONLY)')
        elif syscall == "read":
            lines.append('    data = os.read(fd, 1024)')
        elif syscall == "write":
            lines.append('    os.write(fd, b"Hello, World!")')
        elif syscall == "close":
            lines.append('    os.close(fd)')
    
    lines.append("")
    lines.append(template["main_end"])
    
    return "\n".join(lines)

@router.get("/search")
async def search_examples(
    query: str = Query(..., description="Search query"),
    language: Optional[str] = Query(None, description="Filter by language")
):
    """Search examples by title, description, or tags"""
    results = []
    
    for example in EXAMPLES_DB.values():
        if language and example.language != language:
            continue
        
        # Search in title, description, and tags
        search_text = f"{example.title} {example.description} {' '.join(example.tags)}".lower()
        if query.lower() in search_text:
            results.append({
                "id": example.id,
                "title": example.title,
                "description": example.description,
                "language": example.language,
                "category": example.category,
                "difficulty": example.difficulty
            })
    
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }