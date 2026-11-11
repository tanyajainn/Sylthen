"""Compare session alert thresholds on paired synthetic triage scenarios."""
from argparse import ArgumentParser
from itertools import product
import json

from backend.detection.engine import analyze_events


def scenarios():
    # Labels describe the scripted workflow independently of the detector.
    workflows = [
        ("ordinary lab exercise", False, "LAB_SERVICE"),
        ("simulated incident with tagged destination", True, "SIMULATED_C2"),
        ("simulated incident with missing destination metadata", True, None),
    ]
    for (name, incident, destination), dwell, screenshot in product(
        workflows, (39, 40, 100), (False, True)
    ):
        events = [{"event_type": "key_event", "data": {"dwell_ms": dwell}}]
        if screenshot:
            events.append({"event_type": "screenshot_event", "data": {"authorized": True}})
        metadata = {} if destination is None else {"destination_type": destination}
        events.append({"event_type": "network_event", "data": metadata})
        yield name, incident, dwell, screenshot, events


def evaluate():
    cases = []
    for name, incident, dwell, screenshot, events in scenarios():
        result = analyze_events(events)
        cases.append(dict(workflow=name, incident=incident, dwell_ms=dwell,
                          screenshot=screenshot, score=result["risk"]["score"],
                          rules=[f.rule_id for f in result["findings"]]))

    rows = []
    for threshold in (20, 40, 70):
        counts = dict(TP=0, FP=0, TN=0, FN=0)
        for case in cases:
            alert = case["score"] >= threshold
            correct = alert == case["incident"]
            counts[("T" if correct else "F") + ("P" if alert else "N")] += 1
        tp, fp, fn = counts["TP"], counts["FP"], counts["FN"]
        rows.append(dict(threshold=threshold, **counts,
                         precision=tp / (tp + fp) if tp + fp else None,
                         recall=tp / (tp + fn) if tp + fn else None))
    return dict(benchmark_version=1, sessions=cases, thresholds=rows)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print all cases and scores")
    args = parser.parse_args()
    report = evaluate()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("18 synthetic sessions | 6 ordinary, 12 simulated incidents")
        print("Threshold   TP   FP   TN   FN   Precision   Recall")
        for row in report["thresholds"]:
            metrics = [("n/a" if row[k] is None else format(row[k], ".1%"))
                       for k in ("precision", "recall")]
            print("{threshold:9} {TP:4} {FP:4} {TN:4} {FN:4}".format(**row),
                  f"{metrics[0]:>11} {metrics[1]:>8}")
