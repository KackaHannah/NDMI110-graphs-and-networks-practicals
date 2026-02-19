# NDMI110 - Graphs and Networks

## Credit

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

### IDEs and other interfaces

If you prefer to work inside an editor or an alternative interface:

- **[Visual Studio Code](https://code.visualstudio.com/)** -- open any `.ipynb` file directly; requires the [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) and lets you select the kernel from within the editor.
- **[PyCharm Professional](https://www.jetbrains.com/pycharm/)** -- supports Jupyter notebooks natively; see the [JetBrains documentation](https://www.jetbrains.com/help/pycharm/jupyter-notebook-support.html).
- **Jupyter Notebook (classic)** -- a simpler browser-based alternative to JupyterLab; launch with `jupyter notebook` instead of `jupyter lab`.
