# Automated Flux Analysis


## Synopsis

This software is developed for efficient 13C metabolic flux analysis (MFA). Given a metabolic network model, it can load data of mass isotopomer distribution (MID) measured by mass spectrometry (MS), and robustly find a solution that accurately fit MID data.

Besides MFA function, this software also includes codes for sensitivity analysis and analyses of several experimental data, as well as visualization of results and plotting of figures for the paper that it is published.

## Requirements

This software is developed and tested on Python 3.8. It also relies on following Python packages:

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
Models utilized in this software are in `scripts/model` folder.

The folder `base_model` contains the base model and its derivatives utilized in algorithm development, sensitivity analysis and experimental data analysis for cultured cells.

Another folder `invivo_infusion_model` contains the model for analysis of infusion data from patients, which is slightly different from base model in several reactions.

## Data
All <sup>13</sup>C-isotope labeling data are in `scripts/data` folder. 

Infusion data from patients with renal, brain  and lung cancer are from [Faubert *et al*, 2017](https://doi.org/10.1016/j.cell.2017.09.019) and [Courtney *et al*, 2018](https://doi.org/10.1016/j.cmet.2018.07.020) (`renal_carcinoma/data.xlsx` and `lung_tumor/data.xlsx`) .

Labeling data from cultured cell line HCT-116 are from [Reid *et al*, 2018](https://doi.org/10.1038/s41467-018-07868-6) (`colon_cancer_cell_line/data.xlsx`).

Data from other colon cancer cell lines are produced in this study (`colon_cancer_cell_line/data.xlsx`).

These raw data are loaded and converted to standard form for MFA.

## Algorithm and Solver
Algorithm and solver utilized in this study are located in the `scripts/src/core` folder.

The `model` and `data` folder include some class definition and corresponding processing functions. Specifically, EMU algorithm is encoded in `model/emu_analyzer_functions.py`.

Most optimizations are based on `slsqp_solver` and `slsqp_numba_solver`. As their names indicate, the `slsqp_numba_solver` is implemented based on `numba` package for faster execution (roughly 50% time reduction). However, the numba version has the memory leak problem in parallelized executions in Linux system. If running for long time (longer than 50 hours), the normal version is recommended.


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

This script could also be executed as a raw Python project. Make sure Python 3.8 and all required packages are correctly installed. First switch to a target directory and download the source code:

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

This instruction means running a `computation`, which is a `flux_analysis` process of data in `experiments` named `hct116_cultured_cell_line` in test mode (`-t`). 
Detailed argument list will be explained below.

## Arguments

There two different options under the main manu:
- `figure`: Option to generate figures in paper. This option must be executed after that analysis results are generated by the `computation` option.
- `computation`: Option to run most computations.

### Computations

There four different options under the `computation` manu:
- `simulation`: Option to generate simulated MID data
- `sensitivity`: Option to analyze protocol, model, data and config sensitivity of MFA
- `experiments`: Option to run MFA for several experimental data analyses
- `standard_name`: Option to output standard name of metabolites and reactions

#### Simulation

This is a paragraph to explain the simulation argument


#### Sensitivity

This is a paragraph to explain the sensitivity argument


#### Experiments

This is a paragraph to explain the experiments argument


#### Standard name

This is a paragraph to explain the standard_name argument


<!---
The list will be available in the future

### List of models

| Model name in this script | Model name in methods | Source tissue | Sink tissue            | Circulating metabolites    | Data source                          | Description                                                                                                                       |
|---------------------------|-----------------------|---------------|------------------------|----------------------------|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| `model1`                  | Model A               | Liver         | Heart                  | Glucose; Lactate           | Low-infusion glucose data: mouse M1  | Basic two-tissue model.                                                                                                           |
| `model1_unfitted`         | Model A               | Liver         | Heart                  | Glucose; Lactate           | Low-infusion glucose data: mouse M1  | Unfitted result of basic two-tissue model, as the negative result of fitting.                                                     |
| `model1_all`              | Model A               | Liver         | All 8 tissues          | Glucose; Lactate           | Low-infusion glucose data: mouse M1  | Basic two-tissue model with different sink tissues.                                                                               |
| `model1_all_m5`           | Model A               | Liver         | All 8 tissues          | Glucose; Lactate           | Low-infusion glucose data: mouse M5  | Basic two-tissue model with different sink tissues and different mouse data.                                                      |
| `model1_all_m9`           | Model A               | Liver         | All 8 tissues          | Glucose; Lactate           | Low-infusion glucose data: mouse M9  | Basic two-tissue model with different sink tissues and different mouse data.                                                      |
| `model1_all_lactate`      | Model A               | Liver         | All 8 tissues          | Glucose; Lactate           | Low-infusion lactate data: mouse M3  | Basic two-tissue model with different sink tissues and different infusion data.                                                   |
| `model1_all_lactate_m4`   | Model A               | Liver         | All 8 tissues          | Glucose; Lactate           | Low-infusion lactate data: mouse M4  | Basic two-tissue model with different sink tissues and different infusion data.                                                   |
| `model1_all_lactate_m10`  | Model A               | Liver         | All 8 tissues          | Glucose; Lactate           | Low-infusion lactate data: mouse M10 | Basic two-tissue model with different sink tissues and different infusion data.                                                   |
| `model1_all_lactate_m11`  | Model A               | Liver         | All 8 tissues          | Glucose; Lactate           | Low-infusion lactate data: mouse M11 | Basic two-tissue model with different sink tissues and different infusion data.                                                   |
| `parameter`               | Model A               | Liver         | Heart                  | Glucose; Lactate           | Low-infusion data: mouse M1          | Sensitivity analysis of data and other constraint fluxes.                                                                         |
| `model6`                  | Model B               | Liver         | Skeletal muscle        | Glucose; Lactate           | High-infusion data: mouse M1         | Two-tissue model with high-infusion data in different mouse strain.                                                               |
| `model6_unfitted`         | Model B               | Liver         | Skeletal muscle        | Glucose; Lactate           | High-infusion data: mouse M1         | Unfitted result of two-tissue model with high-infusion flux, as the negative result of fitting.                                   |
| `model6_m2`               | Model B               | Liver         | Skeletal muscle        | Glucose; Lactate           | High-infusion data: mouse M2         | Two-tissue model with high-infusion data in different mouse strain.                                                               |
| `model6_m3`               | Model B               | Liver         | Skeletal muscle        | Glucose; Lactate           | High-infusion data: mouse M3         | Two-tissue model with high-infusion data in different mouse strain.                                                               |
| `model6_m4`               | Model B               | Liver         | Skeletal muscle        | Glucose; Lactate           | High-infusion data: mouse M4         | Two-tissue model with high-infusion data in different mouse strain.                                                               |
| `model3`                  | Model D               | Liver         | Heart                  | Glucose; Pyruvate; Lactate | Low-infusion glucose data: mouse M1  | Two-tissue model with three circulatory metabolites.                                                                              |
| `model3_unfitted`         | Model D               | Liver         | Heart                  | Glucose; Pyruvate; Lactate | Low-infusion glucose data: mouse M1  | Unfitted result of two-tissue model with three circulatory metabolites, as the negative result of fitting.                        |
| `model3_all`              | Model D               | Liver         | All 8 tissues          | Glucose; Pyruvate; Lactate | Low-infusion glucose data: mouse M1  | Two-tissue model with three circulatory metabolites and different sink tissues.                                                   |
| `model5`                  | Model C               | Liver         | Heart; Skeletal muscle | Glucose; Lactate           | Low-infusion data: mouse M1          | Three-tissue model.                                                                                                               |
| `model5_comb2`            | Model C               | Liver         | Brain; Skeletal muscle | Glucose; Lactate           | Low-infusion data: mouse M1          | Three-tissue model.                                                                                                               |
| `model5_comb3`            | Model C               | Liver         | Heart; Brain           | Glucose; Lactate           | Low-infusion data: mouse M1          | Three-tissue model.                                                                                                               |
| `model5_unfitted`         | Model C               | Liver         | Heart; Skeletal muscle | Glucose; Lactate           | Low-infusion data: mouse M1          | Unfitted result of three-tissue model, as the negative result of fitting.                                                         |
| `model7`                  | Model E               | Liver         | Skeletal muscle        | Glucose; Pyruvate; Lactate | High-infusion data: mouse M1         | Two-tissue model with three circulatory metabolites and high-infusion data.                                                       |
| `model7_unfitted`         | Model E               | Liver         | Skeletal muscle        | Glucose; Pyruvate; Lactate | High-infusion data: mouse M1         | Unfitted result of two-tissue model with three circulatory metabolites and high-infusion flux, as the negative result of fitting. |

-->

### Other Parameters

`-p, --parallel_num`:
    
Number of parallel processes. If not provided, it will be selected according to CPU cores.

`-t, --test_mode`:

Whether the code is executed in test mode, which means less sample number and shorter time (several minites).


## Contributors

**Shiyu Liu**

+ [http://github.com/liushiyu1994](http://github.com/liushiyu1994)

## License

This software is released under the [MIT License](LICENSE-MIT).
