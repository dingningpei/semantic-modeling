# Experiment Reproduction Guide

This repository contains experiments for evaluating different LLMs on structured data tasks.  
You can reproduce the experiments using the provided Jupyter notebooks and data.

## Directory Structure

- `data/` — Contains all datasets required for the experiments (no download needed).
- `src/` — Source code for data loading, prompt generation, and evaluation.
- `run_deep_seek.ipynb`, `run_gpt_4_turbo.ipynb`, `run_claude_3_5_sonnet.ipynb` — Main experiment notebooks.
- `check_accuracy.ipynb` — Notebook to evaluate and compare experiment results.

## Setup

1. **Clone this repository** and navigate to its root directory.

2. **Install dependencies**  
   You can use the following command to install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   - Jupyter Notebook is also required. Install with:
     ```bash
     pip install notebook
     ```

## Running the Experiments

1. **Run the experiment notebooks**  
   Open and execute each of the following notebooks in order:
   - `run_deep_seek.ipynb`
   - `run_gpt_4_turbo.ipynb`
   - `run_claude_3_5_sonnet.ipynb`

   > **Note:** You may need to adjust file paths and parameters in each notebook to match your data or experiment settings.

2. **Evaluate results**  
   After running the above notebooks, open and execute `check_accuracy.ipynb` to compute and view the results.

## Notes

- All required data is already provided in the `data/` folder.
- If you encounter issues with file paths, please update them in the notebooks to match your local setup.
- For any issues with API keys (e.g., OpenAI, Anthropic), ensure you have set the appropriate environment variables or updated the notebook cells accordingly. 