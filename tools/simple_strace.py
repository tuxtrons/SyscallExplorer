#!/usr/bin/env python3
"""
Simple strace wrapper for SystemCallExplorer
Demonstrates basic strace integration
"""

import subprocess
import argparse
import json
import re
import sys
from typing import Dict, List, Any

def parse_strace_line(line: str) -> Dict[str, Any]:
    """Parse a single strace output line"""
    # Simple regex to extract syscall name and result
    pattern = r'^(\w+)\((.*?)\)\s*=\s*(.+)$'
    match = re.match(pattern, line.strip())
    
    if match:
        syscall_name = match.group(1)
        params = match.group(2)
        result = match.group(3)
        
        return {
            'syscall': syscall_name,
            'parameters': params,
            'result': result,
            'raw_line': line.strip()
        }
    
    return {'raw_line': line.strip()}

def run_strace(command: List[str], output_format: str = 'json') -> Dict[str, Any]:
    """Run strace on a command and parse output"""
    strace_cmd = ['strace', '-o', '/dev/stderr'] + command
    
    try:
        result = subprocess.run(
            strace_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Parse strace output (from stderr)
        syscalls = []
        for line in result.stderr.split('\n'):
            if line.strip() and not line.startswith('+++') and not line.startswith('---'):
                parsed = parse_strace_line(line)
                if 'syscall' in parsed:
                    syscalls.append(parsed)
        
        return {
            'command': ' '.join(command),
            'exit_code': result.returncode,
            'stdout': result.stdout,
            'syscalls': syscalls,
            'total_syscalls': len(syscalls)
        }
    
    except subprocess.TimeoutExpired:
        return {
            'error': 'Command timed out',
            'command': ' '.join(command)
        }
    except FileNotFoundError:
        return {
            'error': 'strace not found - please install strace',
            'command': ' '.join(command)
        }
    except Exception as e:
        return {
            'error': str(e),
            'command': ' '.join(command)
        }

def main():
    parser = argparse.ArgumentParser(description='Simple strace wrapper')
    parser.add_argument('command', nargs='+', help='Command to trace')
    parser.add_argument('--format', choices=['json', 'text'], default='json',
                      help='Output format')
    parser.add_argument('--summary', action='store_true',
                      help='Show syscall summary')
    
    args = parser.parse_args()
    
    result = run_strace(args.command, args.format)
    
    if args.format == 'json':
        print(json.dumps(result, indent=2))
    else:
        if 'error' in result:
            print(f"Error: {result['error']}")
            sys.exit(1)
        
        print(f"Command: {result['command']}")
        print(f"Exit code: {result['exit_code']}")
        print(f"Total system calls: {result['total_syscalls']}")
        
        if args.summary:
            # Count syscall frequency
            syscall_counts = {}
            for syscall in result['syscalls']:
                name = syscall['syscall']
                syscall_counts[name] = syscall_counts.get(name, 0) + 1
            
            print("\nSyscall Summary:")
            for name, count in sorted(syscall_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  {name}: {count}")
        else:
            print("\nSystem calls:")
            for syscall in result['syscalls']:
                print(f"  {syscall['syscall']}({syscall['parameters']}) = {syscall['result']}")

if __name__ == '__main__':
    main()