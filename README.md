# Automated Flux Analysis

## Synopsis

Developed for 13C metabolic flux analysis (MFA), this tool processes mass isotopomer distribution (MID) data from mass
spectrometry to accurately fit MID data and deduce metabolic activities. It includes functionality for MFA, sensitivity
analysis, experimental data analysis, and visualization of results for publication.

## Requirements

The tool is built for Python 3.8 and requires the following packages:

| Packages           | Version has been tested |
|--------------------|-------------------------|
| `numpy`            | 1.22                    |
| `scipy`            | 1.7                     |
| `matplotlib`       | 3.6                     |
| `tqdm`             | 4.64                    |
| `pandas`           | 1.5.2                   |
| `sklearn`          | 3.0                     |
| `xlsxwriter`       | 3.0                     |
| `numba` (optional) | 0.56                    |

[//]: # (For convenience, an out-of-the-box Docker image is provided to run this code. This docker image is tested on `docker-ce` in Ubuntu with Docker version `19.03.1`. &#40;See Usages part for details.&#41;)

## Model

Models utilized in this software are in [`scripts/model`](scripts/model) folder.

The basic model (
[`base_model`](
scripts/model/base_model/base_model.py)) contains the base model utilized in algorithm development, analysis to data availability
and experimental data analysis for cultured cells.

The basic model with GLC and CIT buffers (
[`base_model_with_glc_tca_buffer`](scripts/model/base_model/base_model_with_glc_tca_buffer.py)
) 
contains the model for analysis of in vivo infusion data from patients, 
which is slightly different from base model in several reactions.

## Data

All <sup>13</sup>C-isotope labeling data are in `scripts/data` folder.

Infusion data from patients with renal, brain and lung cancer are from [Faubert *et
al*, 2017](https://doi.org/10.1016/j.cell.2017.09.019) ([`renal_carcinoma/data.xlsx`](scripts/data/renal_carcinoma/data.xlsx)) 
and [Courtney *et al*, 2018](https://doi.org/10.1016/j.cmet.2018.07.020) ([`lung_tumor/data.xlsx`](scripts/data/lung_tumor/data.xlsx)).

Labeling data from cultured cell line HCT-116 are from [Reid *et
al*, 2018](https://doi.org/10.1038/s41467-018-07868-6) ([`hct116_cultured_cell_line/13C-Glucose_tracing_Mike.xlsx`](
scripts/data/hct116_cultured_cell_line/13C-Glucose_tracing_Mike.xlsx)).

Data for the eight colon cancer cell lines are generated in this study (
[`colon_cancer_cell_line/data.xlsx`](scripts/data/colon_cancer_cell_line/data.xlsx)).

These raw data are loaded and converted to standard form for MFA.

## Algorithm and Solver

Algorithm and solver utilized in this study are located in the [`scripts/src/core`](scripts/src/core) folder.

The `model` and `data` folder include some class definition and corresponding processing functions. Specifically, EMU
algorithm is encoded in [`model/emu_analyzer_functions.py`](scripts/src/core/model/emu_analyzer_functions.py).

Most optimizations are based on `slsqp_solver` and `slsqp_numba_solver`. As their names indicate,
the `slsqp_numba_solver` is implemented based on `numba` package for faster execution (roughly 50% time reduction).
However, the numba version has the memory leak problem in parallelized executions in Linux system. If running for long
time (longer than 50 hours), the normal version is recommended.


<!---
The Docker version will be available in the future


### Docker (recommended)
First install an appropriate Docker version ([see here for details](https://docs.docker.com/install/)). Then a model could be executed by the following script:

```shell script
MODEL=model1_m5
TARGET_PATH=/your/path/to/output
cd $TARGET_PATH
docker run -it --rm --name python_$MODEL -v `pwd`:/Lactate_MFA/new_models \
  locasalelab/lactate_mfa:latest $MODEL --test_mode
```

In this script, you could modify the value of `MODEL` to the name of your target model, and modify the value of `TARGET_PATH` to the path that you want to output results. Available model name is listed in following section. BE CAREFUL that the target path would be visited as root account in container! The flag `--test_mode` or `-t` makes the code run quickly in a test mode, and could be removed to run a formal mode. The formal running takes tens of hours.

-->

## Getting started

This script could also be executed as a raw Python project. Make sure Python 3.8 and all required packages are correctly
installed. First switch to a target directory and download the source code:

```shell script
git clone https://github.com/LocasaleLab/Automated-MFA-2023
```

Switch to the source direct, add PYTHONPATH environment and run the `main.py`:

```shell script
cd Automated-MFA-2023
export PYTHONPATH=$PYTHONPATH:`pwd`
python main.py
```

You could try multiple different arguments according to help information. For example:

```shell script
python main.py computation experiments flux_analysis hct116_cultured_cell_line -t
```

This instruction means running a `computation`, which is a `flux_analysis` process of data in `experiments`
named `hct116_cultured_cell_line` in test mode (`-t`).
Detailed argument list will be explained below.

## Arguments

There are two different options under the main manu:

- `figure`: Option to generate figures in paper. This option must be executed after that analysis results are generated
  by the `computation` option.
- `computation`: Option to run most computations.

### Computations

There are four different options under the `computation` manu:

- `standard_name`: Option to output standard name of metabolites and reactions
- `simulation`: Option to generate simulated MID data
- `sensitivity`: Option to analyze protocol, model, data and config sensitivity of MFA
- `experiments`: Option to run MFA for several experimental data analyses

#### Standard name

This option will output the standard name of all metabolites and reactions to `common_data/raw_data/standard_name.xlsx`.

#### Simulation

This option will generate simulated MID data utilized in algorithm development and robustness analysis. Simulated data
Excel and pickle file will be output to the folder `common_data/raw_data/simulated_data`
and `scripts/data/simulated_data` respectively. This option has following optional parameters:

`-b, --batch_num n`:

This parameter is used to generated batched (determined by `n`) known fluxes and corresponding simulated MID data.
It is used in verifying the performance of algorithm in multiple simulated data.

`-f, --new_flux`:

If this optional parameter appear, new known flux optimized from PHDGH mass spectrometry data will be generated.
Otherwise, the stored flux vector will be loaded.

`-n, --with_noise`:

If this optional parameter appear, all-available and experimentally-available MID data will be generated with randomized
noise. Otherwise, the precise MID data will be generated.

`-i, --index p`:

This parameter will add an extra number suffix `p` to generated simulated data file. It is usually used to distinguish
the newly generated simulated data.

#### Common Arguments of Sensitivity and Experiments

Usage: `python main.py computation {sensitivity, experiments} running_mode job_name`

**Positional arguments**

`running_mode`: Running mode of the script.

- `flux_analysis`: Option to start a new flux analysis process to the target job.
- `result_process`: Option to process analysis results of the target job.
- `solver_output`: Option to output detailed model, data and configurations of the target job.
- `raw_experimental_data_plotting`: Only available in `experiments` mode. Option to display the raw experimental data of
  target job.

`job_name`: Name of target job. List of available jobs are listed below.

**Optional arguments**

`-p, --parallel_num`:

Number of parallel processes. If not provided, it will be selected according to CPU cores.

`-t, --test_mode`:

Whether the code is executed in test mode, which means less sample number and shorter time (several minutes).

#### Sensitivity

This option will execute series of operations related to algorithm development, performance assessment and robustness
analysis based on simulated MID data. Their raw data will be output to `common_data/raw_data/model_data_sensitivity`. If
not specified, all jobs in this analysis rely on the basic model (`base_model`).

**List of jobs**

| Job name in this script                                          | Simulated data size | MID coverage                 | Initial solutions                                                    | Description                                                                                                                                           |
|------------------------------------------------------------------|---------------------|------------------------------|----------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| `raw_model_all_data`                                             | Single              | All-available MID            | Randomly sampled                                                     | Basic optimization based on simulated all-available MID data generated from one known flux vector.                                                    |
| `raw_model_raw_data`                                             | Single              | Experimentally-available MID | Randomly sampled                                                     | Basic optimization based on simulated experimentally-available MID data generated from one known flux vector.                                         |
| `optimization_from_all_data_average_solutions`                   | Single              | All-available MID            | Averaged solutions of `raw_model_all_data`                           | Optimization starting from averaged solutions of `raw_model_all_data` based on simulated all-available MID data.                                      |
| `optimization_from_raw_data_average_solutions`                   | Single              | Experimentally-available MID | Averaged solutions of `raw_model_raw_data`                           | Optimization starting from averaged solutions of `raw_model_raw_data` based on simulated experimentally-available MID data.                           |
| `optimization_from_batched_simulated_all_data`                   | 30                  | All-available MID            | Randomly sampled                                                     | Optimization based on multiple simulated all-available MID data generated from 30 distantly distributed known flux vectors.                           |
| `optimization_from_batched_simulated_raw_data`                   | 30                  | Experimentally-available MID | Randomly sampled                                                     | Optimization based on multiple simulated experimentally-available MID data generated from 30 distantly distributed known flux vectors.                |
| `optimization_from_batched_simulated_all_data_average_solutions` | 30                  | All-available MID            | Averaged solutions of `optimization_from_batched_simulated_all_data` | Optimization starting from averaged solutions of `optimization_from_batched_simulated_all_data` based on simulated all-available MID data.            |
| `optimization_from_batched_simulated_raw_data_average_solutions` | 30                  | Experimentally-available MID | Averaged solutions of `optimization_from_batched_simulated_raw_data` | Optimization starting from averaged solutions of `optimization_from_batched_simulated_raw_data` based on simulated experimentally-available MID data. |
| `data_sensitivity`                                               | Single              | Varied in each set           | Randomly sampled                                                     | Optimization from datasets with different data availability.                                                                                          |

#### Experiments

This option will execute series of operations related to analysis to experimental data, including HCT116, renal
carcinoma, lung tumor and colon cancer cell lines. Their raw data will be output
to `common_data/raw_data/experimental_data_analysis`. All tracing experiments rely on U-13C-glucose.

**List of jobs**

| Job name in this script                              | Model                                                                   | Data source                                                                                                                                  | Tissue type                                 | Total sample size <br/>(combine biological replicates) | Analysis                         | Optimization number of each sample | Description                                                                                                 |
|------------------------------------------------------|-------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|--------------------------------------------------------|----------------------------------|------------------------------------|-------------------------------------------------------------------------------------------------------------|
| `hct116_cultured_cell_line`                          | Basic model (`base_model`)                                              | Published data of HCT-116 labeling experiments [Reid *et al*, 2018](https://doi.org/10.1038/s41467-018-07868-6)                              | Cultured colon cancer cell line             | 1                                                      | Traditional MFA method           | 400                                | Reanalyze the HCT-116 cell line data for verification of our pipeline.                                      |
| `renal_carcinoma_invivo_infusion`                    | Basic model with GLC and CIT buffers (`base_model_with_glc_tca_buffer`) | Published data of infusion experiments for patients with renal carcinoma[Courtney *et al*, 2018](https://doi.org/10.1016/j.cmet.2018.07.020) | Renal carcinoma and brain tumor in patients | 15                                                     | Optimization-averaging algorithm | 100,000                            | Analyze the in vivo infusion data through the optimization-averaging algorithm.                             |
| `renal_carcinoma_invivo_infusion_traditional_method` | Basic model with GLC and CIT buffers (`base_model_with_glc_tca_buffer`) | Published data of infusion experiments for patients with renal carcinoma[Courtney *et al*, 2018](https://doi.org/10.1016/j.cmet.2018.07.020) | Renal carcinoma and brain tumor in patients | 15                                                     | Traditional MFA method           | 400                                | Analyze the same data with the traditional strategy for comparison.                                         |
| `lung_tumor_invivo_infusion`                         | Basic model with GLC and CIT buffers (`base_model_with_glc_tca_buffer`) | Published data of infusion experiments for patients with lung cancer [Faubert *et al*, 2017](https://doi.org/10.1016/j.cell.2017.09.019)     | Lung tumor in patients                      | 35                                                     | Optimization-averaging algorithm | 60,000                             | Analyze the in vivo infusion data of multiple kinds of cancer through the optimization-averaging algorithm. |
| `colon_cancer_cell_line`                             | Basic model (`base_model`)                                              | New data of eight colon cancer cell lines                                                                                                    | Cultured colon cancer cell line             | 16                                                     | Optimization-averaging algorithm | 100,000                            | Analyze the cultured cell data through the optimization-averaging algorithm to verify our finding.          |
| `colon_cancer_cell_line_traditional_method`          | Basic model (`base_model`)                                              | New data of eight colon cancer cell lines                                                                                                    | Cultured colon cancer cell line             | 16                                                     | Traditional MFA method           | 400                                | Analyze the same data with the traditional strategy for comparison.                                         |


### Figures

There are 12 different options under the `figure` manu, of which 5 are main figures, and 6 are supplementary figures. The `all` option can regenerate all figures. For example:

```shell
python main.py figure 1
```

<!--
| Arguments | Figures     | Main figure or supplementary figure |
|-----------|-------------|-------------------------------------|
| `1`       | Figure 1    | Main figure                         |
| `2`       | Figure 2    | Main figure                         |
| `3`       | Figure 3    | Main figure                         |
| `4`       | Figure 4    | Main figure                         |
| `5`       | Figure 5    | Main figure                         |
| `s1`      | Figure S1   | Supplementary figure                |
| `s2`      | Figure S2   | Supplementary figure                |
| `s3`      | Figure S3   | Supplementary figure                |
| `s4`      | Figure S4   | Supplementary figure                |
| `s5`      | Figure S5   | Supplementary figure                |
| `s6`      | Figure S6   | Supplementary figure                |
| `all`     | All figures | All figures                         |
-->

| Arguments | Figures     | Main figure or supplementary figure | Output files                                                       |
|-----------|-------------|-------------------------------------|--------------------------------------------------------------------|
| `1`       | Figure 1    | Main figure                         | [`short_figure_1.pdf`](figures/output_figure/short_figure_1.pdf)   |
| `s1`      | Figure S1   | Supplementary figure                | [`short_figure_s1.pdf`](figures/output_figure/short_figure_s1.pdf) |
| `s2`      | Figure S2   | Supplementary figure                | [`short_figure_s2.pdf`](figures/output_figure/short_figure_s2.pdf) |
| `s3`      | Figure S3   | Supplementary figure                | [`short_figure_s3.pdf`](figures/output_figure/short_figure_s3.pdf) |
| `s4`      | Figure S4   | Supplementary figure                | [`short_figure_s4.pdf`](figures/output_figure/short_figure_s4.pdf) |
| `s5`      | Figure S5   | Supplementary figure                | [`short_figure_s5.pdf`](figures/output_figure/short_figure_s5.pdf) |

## Contributors

**Shiyu Liu**

+ [http://github.com/liushiyu1994](http://github.com/liushiyu1994)

## License

This software is released under the [MIT License](LICENSE).
