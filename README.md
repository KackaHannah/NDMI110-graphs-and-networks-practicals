# NDMI110 - Graphs and Networks

Tutorials are in turns practical and theoretical. During practical tutorials we
will work with specific graphs and real-world networks. On theoretical tutorials
we will deepen our understanding of theoretical knowledge gained from lectures.

There is a mirror of this repository at [MFF Gitlab](https://gitlab.mff.cuni.cz/kubekd/ndmi110-graphs-and-networks#)

## Gaining tutorial credit

Throughout the semester there will be 3 short tests oriented on understanding
the material from lectures, each exam for 10 points. This makes overall 30
points which can be obtained from tests.

By being active during practical tutorials you gain 5 points per practical
tutorial.

The condition for gaining the tutorial credit is having *30 points*.

### Missing

If you are unable to attend the practical tutorial from any reason (or if you
fail to be active enough), you can send your solution anytime before the next
tutorial, by which you can gain 5 points. 

## Schedule

### 1. Tutorial Schedule 2026

| week | Date | Character | Event | Topic |
|:---|:---|:---|:---|:---|
| 1 | 16.2.2026 | — | — | *Skipped (Week 1)* |
| 2 | 23.2.2026 | practical tutorial | **1P** | introduction, working with graphs |
| 3 | 2.3.2026 | theoretical tutorial | | small-world character |
| 4 | 9.3.2026 | practical tutorial | **2P** | centrality measures on real networks|
| 5 | 16.3.2026 | **Test** + theoretical | **1T** | centrality measures |
| 6 | 23.3.2026 | practical tutorial | **3P** | random networks vs. real networks |
| 7 | 30.3.2026 | theoretical tutorial | |  |
| 8 | 6.4.2026 | **Cancelled** | — | **Easter Monday** |
| 9 | 13.4.2026 | practical tutorial | **4P** |  |
| 10 | 20.4.2026 | **Test** + theoretical | **2T** |  |
| 11 | 27.4.2026 | theoretical tutorial | |  |
| 12 | 4.5.2026 | practical tutorial | **5P** |  |
| 13 | 11.5.2026 | theoretical tutorial | |  |
| 14 | 18.5.2026 | **Test** + practical | **3T + 6P** | |

## Environment Setup

This section will help you set up the Python environment for the 
[Graphs and Networks](https://iuuk.mff.cuni.cz/~hartman/teach/graphs-and-networks/)
course.

Python libraries are installed into isolated **virtual environments** to avoid
conflicts between projects. You need to create one, install the required
packages into it, and then tell Jupyter to use it.

The recommended approach is to use the `uv` project manager, which handles both
the virtual environment and dependencies automatically. If `uv` cannot be
installed, you can use the standard `venv` + `pip` approach instead -- both are
described below.

### Option A: Using `uv` (recommended)

`uv` is a fast, modern Python project manager. It reads the project dependencies
from `pyproject.toml` and sets everything up for you.

1. **Install `uv`**: Follow the instructions for your OS on the [uv installation page](https://docs.astral.sh/uv/getting-started/installation/).

2. **Install dependencies**: Open a terminal in the project root directory (the folder containing `pyproject.toml`) and run:
   ```bash
   uv sync
   ```
   This creates a virtual environment in `.venv/` and installs all required packages.


### Option B: Using `pip` and `venv`

If you can't use `uv`, you can set up the environment manually using Python's
built-in tools.

1. **Create a virtual environment** in the project directory:
   ```bash
   python -m venv .venv
   ```

2. **Activate the environment** -- the command differs by OS:

   - **Windows (Command Prompt / PowerShell)**:
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS / Linux**:
     ```bash
     source .venv/bin/activate
     ```

   Your terminal prompt should change to indicate the environment is active (e.g. `(.venv)`).

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

### Registering the Jupyter Kernel

Jupyter needs to be told about your virtual environment so you can select it as
a kernel when running notebooks. After setting up and activating your
environment (via either method above), run:

```bash
# If using uv:
uv run python -m ipykernel install --user --name=gn-course --display-name "Python (GN Course)"

# If using venv + pip (with the environment activated):
python -m ipykernel install --user --name=gn-course --display-name "Python (GN Course)"
```

Then, when opening a notebook in Jupyter or VS Code, select **"Python (GN
Course)"** as the kernel. You can verify everything works by running the demo
notebook in `00/`.

---

## Running Notebooks

There are several ways to work with the notebooks.

### JupyterLab (recommended)

JupyterLab is the standard browser-based interface for working with Jupyter
notebooks.

```bash
# If using uv:
uv run jupyter lab
```

```bash
# If using venv + pip (with the environment activated):
jupyter lab
```

This will open JupyterLab in your browser. From there, navigate to the notebook
file (`.ipynb`) you want to open.
