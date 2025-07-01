import os
import subprocess
from pathlib import Path

def find_project_root():
    """
    Find the project root directory that works both in Bazel and direct execution.
    
    Returns the workspace/project root directory regardless of execution context.
    """
    
    # Method 1: Bazel workspace directory (when running via 'bazel run')
    bazel_workspace = os.environ.get('BUILD_WORKSPACE_DIRECTORY')
    if bazel_workspace and os.path.exists(bazel_workspace):
        return bazel_workspace
    
    # Method 2: Try git command (most reliable when git is available)
    try:
        git_root = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'],
            stderr=subprocess.DEVNULL,
            universal_newlines=True,
            cwd=os.getcwd()  # Use current working directory as starting point
        ).strip()
        if git_root and os.path.exists(git_root):
            return git_root
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        pass
    
    # Method 3: Walk up from current working directory looking for project markers
    current = Path(os.getcwd()).resolve()
    
    while current != current.parent:  # Stop at filesystem root
        # Check for common project root indicators
        project_markers = [
            '.git',
            'WORKSPACE',
            'WORKSPACE.bazel',
            '.bazelrc',
            'pyproject.toml',
            'setup.py',
            'requirements.txt',
            '.project_root'  # Custom marker file you can create
        ]
        
        for marker in project_markers:
            if (current / marker).exists():
                return str(current)
        
        current = current.parent
    
    # Method 4: Check if we're in a Bazel execution environment
    # Look for Bazel-specific environment variables
    if any(var.startswith('BAZEL_') for var in os.environ):
        # Try to find the workspace by looking at the current working directory
        # when Bazel execution started
        test_start_dir = os.environ.get('TEST_SRCDIR', os.getcwd())
        if os.path.exists(test_start_dir):
            test_path = Path(test_start_dir)
            # Navigate up to find workspace markers
            current = test_path
            while current != current.parent:
                if (current / 'WORKSPACE').exists() or (current / 'WORKSPACE.bazel').exists():
                    return str(current)
                current = current.parent
    
    # Fallback: return current working directory
    return os.getcwd()


def find_project_root_with_cache():
    """Cached version to avoid repeated expensive operations"""
    if not hasattr(find_project_root_with_cache, '_cached_root'):
        find_project_root_with_cache._cached_root = find_project_root()
    return find_project_root_with_cache._cached_root
