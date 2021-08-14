import importlib
import os.path
import yaml
from collections import defaultdict

import click

# TODO: tests

@click.group(name="openscm-ar6-wg1-data-compilation")
def cli():
    """
    Command-line interface
    """
    pass


@cli.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("config_yaml")
def compile(config_yaml):
    r"""
    Compile data

    Data is compiled according to the configuration in ``config_yaml``
    """
    with open(config_yaml) as fh:
        configs = yaml.safe_load(fh)

    # run compilations
    for source, cfg in configs.items():
        # TODO: logging instead
        print(f"Processing {source}")
        compile_func_str = cfg["compile_function"]
        print(f"Processing using {compile_func_str}")
        compile_func_str_split = compile_func_str.split(".")
        compile_module_str = ".".join(compile_func_str_split[ : - 1])

        compile_module = importlib.import_module(compile_module_str)
        compile_func = getattr(compile_module, compile_func_str_split[-1])

        # call the compilation
        raw_data_path = cfg["raw_data_path"]
        print(f"Raw data path {raw_data_path}")
        out_scmrun = compile_func(
            raw_data_path=raw_data_path,
        )

        print("Checking output metadata")
        output_variables = out_scmrun.get_unique_meta("variable")
        cfg_variables = cfg["variables"].keys()
        for v in cfg_variables:
            if v not in output_variables:
                error_msg = (
                    f"{v} not in output_variables: {output_variables}"
                )
                raise ValueError(error_msg)

        for v in output_variables:
            if v not in cfg_variables:
                error_msg = (
                    f"{v} not in config file: {config_yaml}"
                )
                raise ValueError(error_msg)

        # TODO: check that all variables (incl. units) agree with nomenclature

        # save results
        out_file = cfg["output_data_path"]
        os.makedirs(os.path.dirname(out_file), exist_ok=True)

        print(f"Saving to {out_file}")
        if cfg["annual_data"] is True:
            print("Saving with year time axis")
            out_scmrun.timeseries(time_axis="year").to_csv(out_file)
        else:
            print("Saving with datetime time axis")
            out_scmrun.to_csv(out_file)
