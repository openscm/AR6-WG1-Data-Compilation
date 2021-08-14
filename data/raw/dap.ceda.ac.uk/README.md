The data in this directory can be downloaded from https://catalogue.ceda.ac.uk/uuid/ae4f1eb6fce24adcb92ddca1a7838a5c.

Alternately, the following script will download the data if `wget` is installed.

```bash
#!/bin/bash
OUTPUT_DIRECTORY="./"

wget -e robots=off --mirror --no-parent -r https://dap.ceda.ac.uk/badc/ar6_wg1/data/spm/spm_01/v20210809/ --directory-prefix="${OUTPUT_DIRECTORY}"
wget -e robots=off --mirror --no-parent -r https://dap.ceda.ac.uk/badc/ar6_wg1/data/spm/spm_04/v20210809/ --directory-prefix="${OUTPUT_DIRECTORY}"
wget -e robots=off --mirror --no-parent -r https://dap.ceda.ac.uk/badc/ar6_wg1/data/spm/spm_08/v20210809/ --directory-prefix="${OUTPUT_DIRECTORY}"
```
