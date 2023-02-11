# Northrop Grumman -- Data Engineer Candidate Assignment

-------------
#### **<font color=red>CAVEAT</font>**: The structure I've described in this Markdown file might be different what the grader will receive due to the .gzip compression process. Please be advised that all contents(outputs, core codebase, etc) should still be present, and feel free to reach out to me for any questions. Thank you
-------------

### **Candidate**: Jayden Lee

This repository contains my work for Data Engineer Candidate Assignment for Northrop Grumman. The written answer for Questionnaire.$4$ is written at the bottom of this Markdown file.

**<font color=orange>How to execute the script</font>**:

1. Install the dependent Python libraries using 
```bash
pip3 install -r requirements.txt
```

2. Once venv is activated and required libraries are intstalled in it, execute the Python file(`parse.py`) with filepaths(`fp1`, `fp2`) to the sample datasets and filepath(`fp3`) to the destination using
```bash
python3 parse.py fp1 fp2 fp3
```
    
- <font color=red>**Caveat**</font>: `parse.py` contains several `assert` statements to ensure proper execution of the functions. To ignore them, run:
```bash
python3 -O parse.py fp1 fp2 fp3
```

3. Arguments I used:
    - `fp1`: `data/sample_input_1.csv`
    - `fp2`: `data/sample_input_2.csv`
    - `fp3`: `output/output.csv'`


**<font color=orange>Directory Structure</font>**

- `data`: Two sample datasets are stored under this directory
- `output`: Output dataset is stored under this directory
- `Northrop assessment.ipynb`: Jupyter Notebook for demonstration of my code
- `src/CSV_parser.py`: CSV_Parser object is defined here
- `src/concatenrate_two_data.py`: Concatenation function for concatenating two processed datasets
- `requirements.txt`: List of Python libraries required for dependencies along with their versions
- `main.py`: Main script to run

## **<font color=orange>Questionnaire.4 solution</font>**
> The datasets are made up of mix of String, Integer, and Decimal values, `dec`, `rd`, `dt`, and `val` being String, `id` and `spd` being Integer, and `len` being Decimal. Though in `sample_input_2.csv` dataset, `spd` is inferred as Decimal, but that's because there are no null values in `sample_input_1.csv` while there are in `sample_input_2.csv`. 
 
> Without any context provided behind these datasets, it is hard to tell what the measurement in each column represents, but the mean and standard deviation between the `spd` and `len` measures are approximately similar to each other. `spd` values in `sample_input_1.csv` show average of $124.16800$ with standard deviation of $74.23461$ and `spd` values in `sample_input_2.csv` show average of $123.979798$ with standard deviation of $72.789973$. For `len`, values in `sample_input_1.csv` show average of $8.240040$ varying at $1.549111$ while values in `sample_input_2.csv` show average of $8.298193$ varying at $1.526986$.

> Distribution of `val` values were similar between the two as well. For `sample_input_1.csv`, approximately $56\%$ of them were `F` labeled and for `sample_input_2.csv`, $52\%$ of them were labeled `F`.

> Records in both `sample_input_1.csv` and `sample_input_1.csv` are recorded in $2025$ or $2026$.

> Both datasets had missing values in `len` column and while missing values are observed in `val` in `sample_input_1.csv` data, missing values are observed in `spd` in `sample_input_2.csv`.