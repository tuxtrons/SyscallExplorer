# SystemCallExplorer - Interactive System Call Learning Platform

An interactive educational tool for exploring Linux system calls with real-time parameter visualization, performance analysis, and code generation capabilities.

## 🚀 Features

- **Interactive Parameter Exploration**: Real-time visualization of system call parameters and their effects
- **Performance Impact Analysis**: Monitor and visualize the performance characteristics of different system calls
- **Code Generation**: Generate code snippets for common system call patterns in multiple languages
- **Strace Integration**: Interactive strace analysis and visualization
- **Educational Content**: Comprehensive guides and examples for learning system calls

## 🏗️ Architecture

```
SystemCallExplorer/
├── frontend/          # React/TypeScript interactive web interface
├── backend/           # Python FastAPI backend for system call analysis
├── tools/             # System call monitoring and analysis tools
├── docs/              # Documentation and learning materials
├── examples/          # Code examples and common patterns
└── scripts/           # Build, deployment, and utility scripts
```

## 🛠️ Tech Stack

- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **Backend**: Python FastAPI + asyncio for real-time capabilities
- **System Integration**: Python + C extensions for low-level system call access
- **Visualization**: D3.js + Chart.js for performance graphs
- **Documentation**: Markdown + interactive examples

## 🚦 Quick Start

1. **Install Dependencies**
   ```bash
   # Backend dependencies
   cd backend && pip install -r requirements.txt
   
   # Frontend dependencies
   cd frontend && npm install
   ```

2. **Run Development Servers**
   ```bash
   # Start backend (terminal 1)
   cd backend && python main.py
   
   # Start frontend (terminal 2)
   cd frontend && npm run dev
   ```

3. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📚 Learning Modules

1. **System Call Basics**: Introduction to system call concepts
2. **File Operations**: open, read, write, close and their variants
3. **Process Management**: fork, exec, wait, signal handling
4. **Memory Management**: mmap, malloc, memory allocation patterns
5. **Network Operations**: socket, bind, listen, accept
6. **Performance Analysis**: Measuring and optimizing system call usage

## 🔧 Development

### Prerequisites
- Python 3.9+
- Node.js 18+
- Linux environment (for system call access)
- root/sudo access (for some advanced features)

### Development Workflow
```bash
# Install development tools
make install-dev

# Run tests
make test

# Format code
make format

# Build for production
make build
```

## 📖 Documentation

- [System Call Reference](docs/syscall-reference.md)
- [API Documentation](docs/api.md)
- [Contributing Guide](docs/contributing.md)
- [Deployment Guide](docs/deployment.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Linux kernel documentation
- strace developers
- Educational resources from various universities and open source projects