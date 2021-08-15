The data is stored in this directory.

The `raw` directory contains the raw data, in the same format and directory structure as it can be downloaded from the WG1 archive.
We do not store the raw data as part of this repository, but we provide this directory in case users wish to copy our workflow.

The `interim` directory contains any interim data products, as created by the compilation scripts (see `README.md` in the root of this repository for instructions about compiling the data).

The `processed` directory contains the processed data products, also as created by the compilation scripts (see `README.md` in the root of this repository for instructions about compiling the data).
All data in this directory is in a uniform csv-based format, ready for use directly with automated processing software and notably perfectly suited for use with the scmdata and pyam repositories.
