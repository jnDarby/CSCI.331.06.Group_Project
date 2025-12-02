"""
Graphviz Diagnostic and Manual Rendering Script (Generated using CLAUDE AI)
Use this to diagnose why PNG files aren't being created
"""

import os
import sys
import subprocess

print("="*80)
print("GRAPHVIZ DIAGNOSTIC TOOL")
print("="*80 + "\n")

# Step 1: Check if DOT files exist
print("Step 1: Checking for DOT files...")
dot_files = [f for f in os.listdir('.') if f.endswith('.dot') or f.endswith('')]

# Look for our specific files
expected_files = ['full_network', 'ids_route_rochester_to_nyc', 'ids_route_rochester_to_nyc_full']
found_dot_files = []

for file in expected_files:
    if os.path.exists(file):
        found_dot_files.append(file)
        print(f"  ✓ Found: {file}")

if not found_dot_files:
    print("  ✗ No DOT files found!")
    print("  Run main_route_planner_graphviz.py first")
    sys.exit(1)

print()

# Step 2: Check if dot command is available
print("Step 2: Checking Graphviz 'dot' command...")
try:
    result = subprocess.run(['dot', '-V'], 
                          capture_output=True, 
                          text=True, 
                          timeout=5)
    
    if result.returncode == 0:
        version = result.stderr.strip() if result.stderr else result.stdout.strip()
        print(f"  ✓ Graphviz is installed: {version}")
        dot_available = True
    else:
        print("  ✗ 'dot' command failed")
        dot_available = False
        
except FileNotFoundError:
    print("  ✗ 'dot' command not found")
    print()
    print("  PROBLEM: Graphviz is not installed or not in PATH")
    print()
    print("  Solutions:")
    print("  1. Windows: Download and install from https://graphviz.org/download/")
    print("     - During installation, CHECK 'Add Graphviz to system PATH'")
    print("     - Restart your terminal after installation")
    print()
    print("  2. Mac: brew install graphviz")
    print()
    print("  3. Linux: sudo apt-get install graphviz")
    print()
    dot_available = False
    
except subprocess.TimeoutExpired:
    print("  ✗ 'dot' command timed out")
    dot_available = False

print()

# Step 3: Check Python graphviz package
print("Step 3: Checking Python graphviz package...")
try:
    import graphviz
    print(f"  ✓ Python graphviz package is installed")
except ImportError:
    print("  ✗ Python graphviz package not installed")
    print("  Run: python -m pip install graphviz")

print()

# Step 4: Try to manually render the DOT files
if dot_available and found_dot_files:
    print("Step 4: Manually rendering DOT files to PNG...")
    print()
    
    for dot_file in found_dot_files:
        output_file = f"{dot_file}.png"
        
        try:
            print(f"  Rendering {dot_file} -> {output_file}...")
            
            # Read the DOT file
            with open(dot_file, 'r') as f:
                dot_content = f.read()
            
            # Use subprocess to call dot directly
            result = subprocess.run(
                ['dot', '-Tpng', '-o', output_file],
                input=dot_content,
                text=True,
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0 and os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"    ✓ Created {output_file} ({file_size} bytes)")
            else:
                print(f"    ✗ Failed to create {output_file}")
                if result.stderr:
                    print(f"    Error: {result.stderr}")
                    
        except subprocess.TimeoutExpired:
            print(f"    ✗ Timeout rendering {dot_file}")
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    print()
    print("="*80)
    print("RENDERING COMPLETE")
    print("="*80)
    print()
    print("Check your directory for PNG files:")
    png_files = [f for f in os.listdir('.') if f.endswith('.png')]
    if png_files:
        print("  PNG files created:")
        for png in png_files:
            size = os.path.getsize(png)
            print(f"    - {png} ({size:,} bytes)")
    else:
        print("  ✗ No PNG files were created")
    
elif not dot_available:
    print("Step 4: SKIPPED - 'dot' command not available")
    print()
    print("="*80)
    print("ACTION REQUIRED")
    print("="*80)
    print()
    print("You need to install Graphviz system software:")
    print()
    print("Windows:")
    print("  1. Download from: https://graphviz.org/download/")
    print("  2. Run installer (graphviz-X.X.X-win64.exe)")
    print("  3. CHECK 'Add Graphviz to system PATH' during install")
    print("  4. Restart terminal/PowerShell")
    print("  5. Run this script again")
    print()
    print("Mac:")
    print("  1. brew install graphviz")
    print("  2. Run this script again")
    print()
    print("Linux:")
    print("  1. sudo apt-get install graphviz")
    print("  2. Run this script again")

else:
    print("Step 4: No DOT files to render")

print()
print("="*80)