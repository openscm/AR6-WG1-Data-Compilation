from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def unmangle_stats(inscmrun):
    out = inscmrun.copy()
    out["statistic"] = out["variable"].apply(lambda x: x.split("|")[-1])
    out["variable"] = out["variable"].apply(lambda x: "|".join(x.split("|")[:-1]))
    
    return out


def convert_stats_to_quantile(s):
    if s == "Median":
        return 0.5
    if s == "Mean":
        return 0.5
    
    return float(s.strip("%")) / 100
