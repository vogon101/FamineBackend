import math
import numbers

import pandas as pd


class JsonStr:
    value = None

    def __init__(self, v):
        self.value = v

    def __str__(self):
        return "{}".format(self.value)


def df_to_json(df: pd.DataFrame) -> JsonStr:
    return JsonStr(to_json_string(
        dict(
            columns=list(df.columns),
            rows=[list(row.values) for _, row in df.iterrows()]
        )
    ))


def to_json_string(obj) -> str:
    if isinstance(obj, dict):
        s = ""
        if len(obj.keys()) == 0:
            s = "{}"
        else:
            s = "{ "
            for k, v in obj.items():
                s += '"{}" : {}, '.format(k, to_json_string(v))
            s = s[:-2] + " }"
        return s

    elif isinstance(obj, tuple):
        return "[" + ",".join([to_json_string(x) for x in obj]) + "]"

    elif isinstance(obj, list):
        return "[" + ", ".join([to_json_string(x) for x in obj]) + "]"

    elif isinstance(obj, pd.DataFrame):
        return df_to_json(obj)
    elif isinstance(obj, str):
        return '"{}"'.format(obj)
    elif isinstance(obj, bool):
        return "true" if obj else "false"
    elif isinstance(obj, JsonStr):
        return obj.value
    elif isinstance(obj, numbers.Number) and math.isnan(obj):
        return '"NaN"'
    else:
        return str(obj)
