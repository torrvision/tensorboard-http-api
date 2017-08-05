# JSON messages format

Here is an example of a formatted json message for a summary (self-explanatory):

    {
        "wall_time": 1501914380.786504,
        "step": 1,
        "summaries": [
            {"tag": "accuracy", "type": "scalar", "value": 0.8},
            {"tag": "loss", "type": "scalar", "value": 13415.0}
        ]
    }

More examples will come as supported types are added.
