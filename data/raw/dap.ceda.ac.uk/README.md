The data in this directory can be downloaded from https://catalogue.ceda.ac.uk/uuid/ae4f1eb6fce24adcb92ddca1a7838a5c.

Alternately, the following script will download the data if `wget` is installed.

```bash
#!/bin/bash
# To match our workflow, run this script from the same directory as
# the `compilation-config.yaml` file in the root of the git repository
OUTPUT_DIRECTORY="data/raw"

wget -e robots=off --mirror --no-parent -r https://dap.ceda.ac.uk/badc/ar6_wg1/data/spm/spm_01/v20210809/ --directory-prefix="${OUTPUT_DIRECTORY}"
wget -e robots=off --mirror --no-parent -r https://dap.ceda.ac.uk/badc/ar6_wg1/data/spm/spm_04/v20210809/ --directory-prefix="${OUTPUT_DIRECTORY}"
wget -e robots=off --mirror --no-parent -r https://dap.ceda.ac.uk/badc/ar6_wg1/data/spm/spm_07/v20210809/ --directory-prefix="${OUTPUT_DIRECTORY}"
wget -e robots=off --mirror --no-parent -r https://dap.ceda.ac.uk/badc/ar6_wg1/data/spm/spm_08/v20210809/ --directory-prefix="${OUTPUT_DIRECTORY}"
wget -e robots=off --mirror --no-parent -r https://dap.ceda.ac.uk/badc/ar6_wg1/data/spm/spm_10/v20210809/ --directory-prefix="${OUTPUT_DIRECTORY}"
```
