# Lattice Paths Genetic Algorithm

A sophisticated genetic algorithm implementation for finding maximum sets of k-distinct lattice paths. This project addresses optimization problems in graph theory, circuit design, scheduling, routing, and network data transmission by efficiently identifying optimal path configurations in lattice structures.

[Read paper](https://arielfayol.com/view_pdf/lattice_paths)

## 🎯 Project Overview

This research project employs advanced genetic algorithms to solve the k-distinct lattice paths problem, building upon previous work by Gillman et al. The algorithm overcomes computational limitations of traditional brute-force techniques, providing an efficient approach to finding maximum sets of paths that share at most (k-1) edges.

### Key Features

- **Genetic Algorithm Optimization**: Advanced evolutionary computation with fitness scaling and divergence-based selection
- **Parallel Processing**: Multi-core execution for improved search efficiency
- **Visualization**: Turtle graphics for path visualization and lattice representation
- **Flexible Configuration**: Customizable parameters for different problem instances
- **Data Collection**: Excel-based data storage and analysis capabilities

## 📋 Installation & Setup

### Step 1: Install Python Dependencies

```bash
# Install required packages
pip install pebble openpyxl numpy

# Verify installation
python -c "import pebble, openpyxl, numpy; print('All packages installed successfully!')"
```

### Step 2: Clone or Download the Project

```bash
# If using git
git clone https://github.com/arielfayol37/Lattice_paths
cd Lattice_paths

# Or simply download and extract the files to a folder
```

### Step 3: Test Basic Functionality

```python
# Test if everything works
python -c "
from run import search
print('Testing basic search...')
result = search(size=100, target=3, m=2, n=2, k=2, visualize=False)
print('Test completed successfully!')
"
```

## 🚀 Quick Start Guide

### Your First Run

1. **Open a Python terminal or create a script file**

2. **Try this simple example:**
```python
from run import search

# Find 3 paths in a 2x2 lattice with k=2
result = search(
    size=200,       # Small population for quick testing
    target=3,       # Number of paths to find
    m=2,           # 2 rows
    n=2,           # 2 columns
    k=2,           # Paths can share at most 1 edge
    visualize=True # Show the result graphically
)
```

3. **What you should see:**
   - A turtle graphics window showing the lattice and paths
   - Console output with fitness information
   - The algorithm will find 3 paths that share at most 1 edge

### Understanding the Parameters

- **`size`**: Population size (larger = better results but slower)
- **`target`**: Number of k-distinct paths you want to find
- **`m, n`**: Lattice dimensions (m rows, n columns)
- **`k`**: Maximum shared edges + 1 (k=2 means paths share ≤1 edge)
- **`visualize`**: Show graphical result (True/False)

## 🏗️ Project Structure

```
Lattice_paths/
├── run.py              # 🚀 Start here - Main interface
├── Population.py       # 🧬 Genetic algorithm engine
├── Genome.py          # 🧬 Individual representation
├── Sequence.py        # 🛤️ Path representation
├── lp_utils.py        # 🔧 Utility functions
├── drawing_paths.py   # 🎨 Visualization module
└── README.md          # 📖 This file
```

## 📖 Understanding the Problem

### What is a Lattice Path?

Imagine a grid (lattice) with m rows and n columns:
```
(0,0) → → → (0,n)
  ↓         ↓
  ↓         ↓
(m,0) → → → (m,n)
```

A **path** starts at (0,0) and ends at (m,n), moving only:
- **East (→)**: Right
- **North (↑)**: Up

### What are k-Distinct Paths?

Two paths are **k-distinct** if they share at most (k-1) edges.

**Important**: k-distinctness is hierarchical:
- If paths are k-distinct, they are also (k+1)-distinct, (k+2)-distinct, etc.
- The challenge is finding the **maximum** number of paths that are k-distinct

**Example with k=2:**
- Path A: →→↑↑ (shares 1 edge with Path B)
- Path B: →↑→↑ (shares 1 edge with Path A)
- These are 2-distinct (share ≤1 edge)
- They are also 3-distinct, 4-distinct, etc.

**Example with k=3:**
- Path A: →→↑↑ (shares 2 edges with Path C)
- Path C: →→↑↑ (shares 2 edges with Path A)
- These are 3-distinct (share ≤2 edges)
- They are also 4-distinct, 5-distinct, etc.

**The Problem**: Find the maximum number of paths that are k-distinct from each other.

## 🧬 How the Genetic Algorithm Works

### The Big Picture

The algorithm tries to find the **maximum number** of paths that can coexist while being k-distinct from each other.

1. **Create Population**: Generate random sets of paths
2. **Evaluate Fitness**: Count how many pairs are k-distinct
3. **Select Parents**: Choose better individuals to reproduce
4. **Create Children**: Combine and mutate parent paths
5. **Repeat**: Until finding a perfect solution or time runs out

### What Makes This Hard?

- **Combinatorial Explosion**: The number of possible paths grows exponentially
- **Constraint Satisfaction**: Every pair must be k-distinct
- **Optimization**: We want the maximum possible number of paths
- **Trade-offs**: More paths = harder to satisfy k-distinctness

### Key Concepts

#### Fitness Function
- Perfect solution = all path pairs are k-distinct
- Fitness = 9999 for perfect solutions
- Otherwise, fitness = 1/(number of k-equivalent pairs)

#### Selection Strategy
- **Fitness-based**: Better individuals have higher chance to reproduce
- **Diversity-based**: Prevents getting stuck in local optima
- **Scaling**: Adjusts fitness values to maintain population diversity

## 📊 Practical Examples

### Example 1: Small Problem (Quick Test)
```python
from run import search

# 2x2 lattice, find 3 paths, k=2 (paths share at most 1 edge)
result = search(size=200, target=3, m=2, n=2, k=2, visualize=True)
print(f"Best fitness: {result.fitnesses[result.bfi]}")
```

### Example 2: Medium Problem (Realistic)
```python
from run import search

# 4x3 lattice, find 7 paths, k=3 (paths share at most 2 edges)
result = search(size=1000, target=7, m=4, n=3, k=3, visualize=True)
if result.fitnesses[result.bfi] == 9999:
    print("Perfect solution found!")
else:
    print("No perfect solution found")
```

### Example 3: Parallel Search (Best Results)
```python
from run import parallel_search

# Use multiple cores for better results
success, config = parallel_search(target=7, m=4, n=3, k=3)
if success:
    print(f"Solution found with configuration {config}")
else:
    print("No solution found - try increasing target")
```

### Example 4: Data Collection
```python
from run import collect_data_genetic

# Generate comprehensive results table
collect_data_genetic(m=4, n=3)
# This creates Excel files with results
```

## ⚙️ Configuration Guide

### Population Settings

| Problem Size | Population | Temperature | Generations |
|-------------|------------|-------------|-------------|
| Small (≤5×5) | 500-1000   | 3-5         | m×n×k×500   |
| Medium (≤10×10) | 1000-5000 | 4-7         | m×n×k×700   |
| Large (>10×10) | 5000-10000 | 5-10        | m×n×k×1000  |

### Parameter Explanations

- **`size`**: More individuals = better exploration but slower
- **`temperature`**: Higher = more exploration, Lower = more exploitation
- **`crossover_freq`**: How often parents exchange genes (default: 0.7)
- **`kill_mode`**: How to reduce population size (default: "non_bias_random")

## 🔧 Advanced Usage

### Custom Problem Setup
```python
from run import search

# Custom parameters for your specific problem
result = search(
    size=2000,           # Large population
    target=10,           # Find 10 paths
    m=5,                # 5 rows
    n=4,                # 4 columns
    k=3,                # Share ≤2 edges
    kill_mode="non_bias_random",
    mode="roulette",
    norm=True,
    scale=True,
    visualize=True,
    temp=5.0
)
```

### Save and Load Results
```python
from run import save_object, read_object

# Save a successful population
save_object(result, "my_solution")

# Load it later
loaded_result = read_object("my_solution", showBestIndividual=True)
```

### Custom Visualization
```python
from drawing_paths import draw_lattice, draw_path

# Draw empty lattice
draw_lattice(m=4, n=3)

# Draw specific paths
for i, path in enumerate(best_paths):
    draw_path(path, m=4, n=3, o=0, index=i)
``

## 📈 Understanding Results

### Fitness Values
- **9999**: Perfect solution found
- **0.1-1.0**: Good solution (few k-equivalent pairs)
- **0.01-0.1**: Poor solution (many k-equivalent pairs)

### Population Statistics
```python
# Check population health
print(f"Best fitness: {result.fitnesses[result.bfi]}")
print(f"Average fitness: {sum(result.fitnesses)/len(result.fitnesses)}")
print(f"Population size: {len(result.individuals)}")
```

### Visual Interpretation
- **Green paths**: Good solutions
- **Red paths**: K-equivalent pairs
- **Lattice grid**: Problem boundaries

## 🧪 Testing Your Understanding

### Test 1: Basic Functionality
```python
# Should find 3 paths easily
result = search(size=100, target=3, m=2, n=2, k=2, visualize=True)
assert result.fitnesses[result.bfi] == 9999, "Should find perfect solution"
```

### Test 2: Impossible Problem
```python
# Should NOT find 10 paths in 2x2 lattice with k=2 (impossible due to limited paths)
result = search(size=500, target=10, m=2, n=2, k=2, visualize=False)
assert result.fitnesses[result.bfi] < 9999, "Should not find impossible solution"
```

### Test 3: Parallel Processing
```python
# Test parallel search
success, config = parallel_search(target=5, m=3, n=3, k=2)
print(f"Parallel search {'succeeded' if success else 'failed'}")
```

