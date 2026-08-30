r"""
Recursion base cases, progress, per-call locals, and shared arguments.

Run:
    python practice\P4_Functions_and_Generators\C19_Advanced_Function_Topics\05_recursion_base_progress_and_shared_objects.py
"""


def normalize_recursive(keys, index, trace, root_keys, root_trace):
    remaining = len(keys) - index
    frame_snapshot = {"index": index, "remaining": remaining}
    trace.append(
        {
            "frame": frame_snapshot,
            "keys_is_root": keys is root_keys,
            "trace_is_root": trace is root_trace,
        }
    )

    if index == len(keys):
        return []

    current = keys[index].strip().casefold()
    tail = normalize_recursive(
        keys,
        index + 1,
        trace,
        root_keys,
        root_trace,
    )
    return [current, *tail]


def normalize_loop(keys):
    result = []
    for key in keys:
        result.append(key.strip().casefold())
    return result


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    keys = [" Menu.Start ", "Menu.Quit", " Settings.Audio "]
    trace = []

    section("1. A recursive definition needs both a base case and a step")
    predict("Which call reaches the base case and stops making recursive calls?")
    result = normalize_recursive(keys, 0, trace, keys, trace)
    print("result ->", result)
    print(
        "index and remaining ->",
        tuple(
            (entry["frame"]["index"], entry["frame"]["remaining"])
            for entry in trace
        ),
    )
    print(
        "Rule: index == len(keys) is the base case; every recursive step uses "
        "index + 1."
    )

    section("2. Each call has local bindings while arguments can share objects")
    predict("Are frame snapshots distinct even though keys and trace are shared?")
    frames = tuple(entry["frame"] for entry in trace)
    print(
        "adjacent frame snapshots are distinct ->",
        all(left is not right for left, right in zip(frames, frames[1:])),
    )
    print("every keys binding refers to root ->", all(e["keys_is_root"] for e in trace))
    print(
        "every trace binding refers to root ->",
        all(e["trace_is_root"] for e in trace),
    )
    print(
        "Rule: recursive calls create separate local bindings; passing the same "
        "mutable argument does not copy that object."
    )

    section("3. A progress measure supports the termination argument")
    predict("Does remaining decrease strictly until it reaches zero?")
    remaining_values = tuple(entry["frame"]["remaining"] for entry in trace)
    print("remaining values ->", remaining_values)
    print(
        "strictly decreases ->",
        all(
            current > following
            for current, following in zip(remaining_values, remaining_values[1:])
        ),
    )

    empty_keys = []
    empty_trace = []
    empty_result = normalize_recursive(
        empty_keys, 0, empty_trace, empty_keys, empty_trace
    )
    print("empty input result ->", empty_result)
    print("empty input call count ->", len(empty_trace))
    print(
        "Rule: a reachable base case plus a step that moves toward it explains "
        "termination for this finite input."
    )

    section("4. A loop can match the data result without matching call structure")
    predict("Does equal output mean recursion and iteration have identical behavior?")
    loop_result = normalize_loop(keys)
    print("loop result ->", loop_result)
    print("results equal ->", loop_result == result)
    print("result lists are distinct ->", loop_result is not result)
    print("input unchanged ->", keys)
    print(
        "Boundary: this compares result semantics only; it is not a performance "
        "benchmark and does not make the two control-flow structures identical."
    )


if __name__ == "__main__":
    main()
