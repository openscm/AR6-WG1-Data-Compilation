# Data Compilation & Figures from the IPCC AR6 WG1

© 2021 [Contributors](CONTRIBUTORS.md); licensed under the [BSD-3-Clause License](LICENSE).

[![license](https://img.shields.io/github/license/openscm/AR6-WG1-Data-Compilation)](https://github.com/openscm/AR6-WG1-Data-Compilation/blob/main/LICENSE)

## Overview

The IPCC's [AR6 WG1 Report](https://www.ipcc.ch/report/ar6/wg1/)
published in August 2021 contains a lot of useful data and figures.
The data is available at the [CEDA Archive](https://data.ceda.ac.uk/badc/ar6_wg1/data/)
under a Creative Commons CC-BY license, but the formats are quite diverse
and not easy to handle.

### Data resources

This repository compiles the data into a uniform, csv-based data format
following the standard established by the Integrated Assessment Modeling Consortium
([IAMC](https://www.iamconsortium.org)) and used by IPCC WG3.

The format used in this repository is directly compatible with
the **scmdata** and **pyam** Python packages (see dependencies below),
but can be easily read with Excel or scripts written in other programming languages.

### Figures and analysis

This repository contains Jupyter notebooks that replicate several key figures
of the IPCC AR6 WG1 report to facilitate reproducibility of the assessment
and re-use in subsequent research and analysis.

## Dependencies

The data and notebooks in this repository use the dependencies specified in `environment.yml`.
A high-level overview of the packages is below:
 - [pyam](https://pyam-iamc.readthedocs.io)
   (note that this package is distributed on pypi as `pyam-iamc`)
 - [scmdata](https://scmdata.readthedocs.io)
 - [seaborn](https://seaborn.pydata.org)
 - [tqdm](https://tqdm.github.io)
 - [xarray](https://xarray.pydata.org/en/stable)
 - [notebook](https://jupyter-notebook.readthedocs.io/en/latest/?badge=latest)

The required packages can be installed with conda: `conda env create -f environment.yml`.

## Compiling the data

The data is compiled using `openscm-ar6-wg1-data-compilation compile`.
This command-line interface takes a single argument, `config_yaml`, which defines the data sources, which data is expected, where the raw data is stored, where the outputs should be written and also includes relevant metadata.
An example is given in the root of this repository in `compilation-config.yaml`.
Once the data is compiled, it will be in the specified output directories and ready for use.
TODO: also spit out variables and definitions as part of compilation

For information about the data directories, see `data/README`.

## Acknowledgement

We are grateful for the terrific work by [Robin Matthews](https://twitter.com/georobin),
[Özge Yelekçi](https://twitter.com/OzgeYelekci), [Melissa Gomis](https://twitter.com/MelichatGo),
[Lina Sitz](https://twitter.com/lina_sitz), the [CEDA Archive](https://www.ceda.ac.uk)
and many researchers and WG1 TSU staff in compiling, validating and publishing the data
under a license that permits re-use.
