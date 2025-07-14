# Getting Started with SystemCallExplorer

Welcome to SystemCallExplorer! This guide will help you get up and running with the interactive system call learning platform.

## Prerequisites

- **Linux Environment**: SystemCallExplorer is designed for Linux systems
- **Python 3.9+**: For the backend API
- **Node.js 18+**: For the frontend interface
- **strace**: System call tracer (usually pre-installed)
- **GCC**: For compiling C examples (optional)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SystemCallExplorer
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

### Development Mode

Start both the backend and frontend in development mode:

```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Or use the Makefile:

```bash
make dev
```

### Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Quick Tour

### 1. System Call Explorer

Navigate to the "System Calls" section to:
- Browse available system calls
- View detailed parameter information
- See usage examples
- Access manual pages

### 2. Interactive Analysis

Use the "Analysis" section to:
- Start real-time system call monitoring
- Analyze process behavior
- View performance metrics
- Get optimization recommendations

### 3. Code Examples

In the "Examples" section you can:
- Browse pre-built code examples
- Generate custom code snippets
- Learn common patterns
- Export examples in different languages

### 4. Analysis Tools

The "Tools" section provides:
- Integrated strace functionality
- Process monitoring
- Custom analysis scripts
- Export capabilities

## Your First Analysis

Let's trace a simple command:

1. Go to **Tools** → **Strace**
2. Select "Run Command"
3. Enter: `ls -la`
4. Click "Start Trace"
5. View the results in real-time

You'll see all system calls made by the `ls` command, including:
- `openat()` calls to open directories
- `getdents64()` calls to read directory entries
- `fstat()` calls to get file information
- `write()` calls to output results

## Understanding System Calls

### File Operations
- `open()`, `openat()`: Open files
- `read()`, `write()`: I/O operations
- `close()`: Close file descriptors
- `lseek()`: Change file position

### Process Management
- `fork()`: Create new processes
- `execve()`: Execute programs
- `wait()`, `waitpid()`: Wait for child processes
- `exit()`: Terminate processes

### Memory Management
- `mmap()`: Map memory
- `munmap()`: Unmap memory
- `brk()`, `sbrk()`: Adjust heap size
- `mprotect()`: Change memory protection

## Tips for Learning

1. **Start Simple**: Begin with basic file operations
2. **Use Examples**: Study the provided code examples
3. **Compare Patterns**: See how different approaches affect system call usage
4. **Monitor Real Programs**: Use strace on actual applications
5. **Read Documentation**: Check manual pages for detailed information

## Common Workflows

### Analyzing Program Performance

1. Start analysis session for your program
2. Run the program normally
3. Review system call frequency and timing
4. Identify bottlenecks (excessive calls, slow operations)
5. Apply optimizations

### Learning New System Calls

1. Search for the system call in the explorer
2. Read the description and parameters
3. View code examples
4. Try the examples in the interactive editor
5. Experiment with different parameters

### Code Generation

1. Select the system calls you want to use
2. Choose your programming language
3. Select error handling level
4. Generate and download the code
5. Compile and test

## Next Steps

- Explore the [System Call Reference](syscall-reference.md)
- Read the [API Documentation](api.md)
- Check out [Advanced Examples](advanced-examples.md)
- Join our community discussions

## Troubleshooting

### Backend Won't Start
- Check Python version: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check port availability: `netstat -ln | grep 8000`

### Frontend Won't Start
- Check Node.js version: `node --version`
- Clear cache: `npm cache clean --force`
- Reinstall: `rm -rf node_modules && npm install`

### strace Permission Errors
- Some strace operations require elevated privileges
- Use `sudo` when necessary
- Check system security policies

## Support

- **Documentation**: Check the `/docs` directory
- **Examples**: Browse the `/examples` directory
- **API Reference**: Visit http://localhost:8000/docs when running
- **Issues**: Report bugs and feature requests on our repository

Happy exploring! 🚀