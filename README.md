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

The data and notebooks in this repository use the following packages: 

 - [pyam](https://pyam-iamc.readthedocs.io)
   (note that this package is distributed on pypi as `pyam-iamc`)
 - [scmdata](https://scmdata.readthedocs.io) 
