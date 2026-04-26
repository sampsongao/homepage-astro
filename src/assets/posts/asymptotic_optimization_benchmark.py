from __future__ import annotations

import csv
from math import comb, exp, lgamma, log, log10
from pathlib import Path
from statistics import median
from time import perf_counter


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "src" / "assets" / "posts"
CSV_PATH = OUTPUT_DIR / "asymptotic_optimization_benchmark.csv"
ERROR_PLOT_PATH = OUTPUT_DIR / "asymptotic_optimization_error_vs_N.svg"
RUNTIME_PLOT_PATH = OUTPUT_DIR / "asymptotic_optimization_runtime_vs_N.svg"


def log_choose(a: int, b: int) -> float:
    if b < 0 or b > a:
        return float("-inf")
    return lgamma(a + 1) - lgamma(b + 1) - lgamma(a - b + 1)


def hypergeom_pmf(k: int, N: int, K: int, n: int) -> float:
    return exp(log_choose(K, k) + log_choose(N - K, n - k) - log_choose(N, n))


def hypergeom_pmf_naive(k: int, N: int, K: int, n: int) -> float:
    numerator = comb(K, k) * comb(N - K, n - k)
    denominator = comb(N, n)
    return numerator / denominator


def binom_pmf(k: int, n: int, p: float) -> float:
    if p == 0:
        return 1.0 if k == 0 else 0.0
    if p == 1:
        return 1.0 if k == n else 0.0
    return exp(log_choose(n, k) + k * log(p) + (n - k) * log(1 - p))


def binom_pmf_naive(k: int, n: int, p: float) -> float:
    if p == 0:
        return 1.0 if k == 0 else 0.0
    if p == 1:
        return 1.0 if k == n else 0.0
    return comb(n, k) * (p**k) * ((1 - p) ** (n - k))


def valid_k_values(N: int, K: int, n: int) -> range:
    low = max(0, n - (N - K))
    high = min(n, K)
    return range(low, high + 1)


def evaluate_exact_curve(N: int, K: int, n: int, ks: list[int]) -> list[float]:
    return [hypergeom_pmf(k, N, K, n) for k in ks]


def evaluate_exact_curve_naive(N: int, K: int, n: int, ks: list[int]) -> list[float]:
    return [hypergeom_pmf_naive(k, N, K, n) for k in ks]


def evaluate_approx_curve(n: int, p: float, ks: list[int]) -> list[float]:
    return [binom_pmf(k, n, p) for k in ks]


def evaluate_approx_curve_naive(n: int, p: float, ks: list[int]) -> list[float]:
    return [binom_pmf_naive(k, n, p) for k in ks]


def measure_average_runtime(fn, min_elapsed: float = 0.05, trials: int = 5) -> float:
    samples = []
    for _ in range(trials):
        iterations = 1
        elapsed = 0.0
        while elapsed < min_elapsed:
            start = perf_counter()
            for _ in range(iterations):
                fn()
            elapsed = perf_counter() - start
            if elapsed < min_elapsed:
                iterations *= 2
        samples.append(elapsed / iterations)
    return median(samples)


def benchmark_error_case(N: int, success_ratio: float = 0.2, n: int = 200) -> dict[str, float]:
    K = int(success_ratio * N)
    p = K / N
    ks = list(valid_k_values(N, K, n))

    exact = evaluate_exact_curve(N, K, n, ks)
    approx = evaluate_approx_curve(n, p, ks)

    max_abs_error = max(abs(e - a) for e, a in zip(exact, approx))
    total_variation = 0.5 * sum(abs(e - a) for e, a in zip(exact, approx))

    return {
        "N": float(N),
        "K": float(K),
        "n": float(n),
        "support_size": float(len(ks)),
        "n_over_N": n / N,
        "max_abs_error": max_abs_error,
        "total_variation": total_variation,
    }


def benchmark_runtime_case(N: int, success_ratio: float = 0.2, n: int = 200) -> dict[str, float]:
    K = int(success_ratio * N)
    p = K / N
    ks = list(valid_k_values(N, K, n))

    naive_exact_time = measure_average_runtime(
        lambda: evaluate_exact_curve_naive(N, K, n, ks),
        min_elapsed=0.01,
        trials=3,
    )
    approx_time = measure_average_runtime(
        lambda: evaluate_approx_curve_naive(n, p, ks),
        min_elapsed=0.01,
        trials=3,
    )
    optimized_exact_time = measure_average_runtime(
        lambda: evaluate_exact_curve(N, K, n, ks),
        min_elapsed=0.01,
        trials=3,
    )
    optimized_approx_time = measure_average_runtime(
        lambda: evaluate_approx_curve(n, p, ks),
        min_elapsed=0.01,
        trials=3,
    )

    return {
        "N": float(N),
        "K": float(K),
        "n": float(n),
        "support_size": float(len(ks)),
        "n_over_N": n / N,
        "naive_exact_time_s": naive_exact_time,
        "optimized_exact_time_s": optimized_exact_time,
        "naive_approx_time_s": approx_time,
        "optimized_approx_time_s": optimized_approx_time,
        "naive_speedup": naive_exact_time / approx_time if approx_time else float("inf"),
        "optimized_speedup": optimized_exact_time / optimized_approx_time if optimized_approx_time else float("inf"),
    }


def write_csv(results: list[dict[str, float]], path: Path) -> None:
    fieldnames = list(results[0].keys())
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def svg_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def format_sci(value: float) -> str:
    return f"{value:.1e}"


def format_ms(value: float) -> str:
    return f"{value * 1_000:.3f}"


def make_ticks_log10(low: float, high: float) -> list[float]:
    start = int(log10(low))
    end = int(log10(high))
    return [10**power for power in range(start, end + 1)]


def make_ticks_linear(low: float, high: float, count: int = 5) -> list[float]:
    if high == low:
        return [low]
    step = (high - low) / count
    return [low + step * i for i in range(count + 1)]


def data_to_svg_path(
    points: list[tuple[float, float]],
    x_map,
    y_map,
) -> str:
    commands = []
    for idx, (x, y) in enumerate(points):
        prefix = "M" if idx == 0 else "L"
        commands.append(f"{prefix} {x_map(x):.2f} {y_map(y):.2f}")
    return " ".join(commands)


def render_line_chart(
    path: Path,
    title: str,
    x_label: str,
    y_label: str,
    series: list[dict[str, object]],
    x_log: bool = False,
    y_log: bool = False,
    y_tick_formatter=None,
    y_padding_ratio: float = 0.05,
) -> None:
    width = 960
    height = 560
    margin_left = 88
    margin_right = 24
    margin_top = 56
    margin_bottom = 68
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    xs = [x for s in series for x, _ in s["points"]]
    ys = [y for s in series for _, y in s["points"] if y > 0 or not y_log]

    x_min = min(xs)
    x_max = max(xs)
    y_min = min(ys)
    y_max = max(ys)

    if x_log:
        x_min_log = log10(x_min)
        x_max_log = log10(x_max)
        x_map = lambda x: margin_left + (log10(x) - x_min_log) / (x_max_log - x_min_log) * plot_width
        x_ticks = make_ticks_log10(x_min, x_max)
        x_tick_label = lambda x: f"1e{int(log10(x))}"
    else:
        x_map = lambda x: margin_left + (x - x_min) / (x_max - x_min) * plot_width
        x_ticks = make_ticks_linear(x_min, x_max)
        x_tick_label = lambda x: f"{int(x):,}"

    if y_log:
        y_min_log = log10(y_min)
        y_max_log = log10(y_max)
        y_map = lambda y: margin_top + plot_height - (log10(y) - y_min_log) / (y_max_log - y_min_log) * plot_height
        y_ticks = make_ticks_log10(y_min, y_max)
        y_tick_label = y_tick_formatter or format_sci
    else:
        if y_max == y_min:
            y_min = 0.0
        else:
            padding = (y_max - y_min) * y_padding_ratio
            y_min = max(0.0, y_min - padding)
            y_max = y_max + padding
        y_map = lambda y: margin_top + plot_height - (y - y_min) / (y_max - y_min) * plot_height
        y_ticks = make_ticks_linear(y_min, y_max)
        y_tick_label = y_tick_formatter or (format_sci if y_max < 0.01 else lambda y: f"{y:.3f}")

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#0b0f14" />',
        f'<text x="{width / 2}" y="30" fill="#f5f7fa" font-size="22" text-anchor="middle" font-family="Inter, Arial, sans-serif">{svg_escape(title)}</text>',
        f'<line x1="{margin_left}" y1="{margin_top + plot_height}" x2="{margin_left + plot_width}" y2="{margin_top + plot_height}" stroke="#7f8ea3" stroke-width="1"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_height}" stroke="#7f8ea3" stroke-width="1"/>',
    ]

    for tick in x_ticks:
        x = x_map(tick)
        svg_lines.append(
            f'<line x1="{x:.2f}" y1="{margin_top}" x2="{x:.2f}" y2="{margin_top + plot_height}" stroke="#1b2530" stroke-width="1"/>'
        )
        label = svg_escape(x_tick_label(tick))
        svg_lines.append(
            f'<text x="{x:.2f}" y="{margin_top + plot_height + 26}" fill="#c3cfdb" font-size="12" text-anchor="middle" font-family="Inter, Arial, sans-serif">{label}</text>'
        )

    for tick in y_ticks:
        y = y_map(tick)
        svg_lines.append(
            f'<line x1="{margin_left}" y1="{y:.2f}" x2="{margin_left + plot_width}" y2="{y:.2f}" stroke="#1b2530" stroke-width="1"/>'
        )
        label = svg_escape(y_tick_label(tick))
        svg_lines.append(
            f'<text x="{margin_left - 10}" y="{y + 4:.2f}" fill="#c3cfdb" font-size="12" text-anchor="end" font-family="Inter, Arial, sans-serif">{label}</text>'
        )

    for s in series:
        path_d = data_to_svg_path(s["points"], x_map, y_map)
        svg_lines.append(
            f'<path d="{path_d}" fill="none" stroke="{s["color"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        for x, y in s["points"]:
            svg_lines.append(
                f'<circle cx="{x_map(x):.2f}" cy="{y_map(y):.2f}" r="4" fill="{s["color"]}"/>'
            )

    legend_x = margin_left + plot_width - 180
    legend_y = margin_top + 12
    for idx, s in enumerate(series):
        y = legend_y + idx * 24
        svg_lines.append(
            f'<line x1="{legend_x}" y1="{y}" x2="{legend_x + 22}" y2="{y}" stroke="{s["color"]}" stroke-width="3"/>'
        )
        svg_lines.append(
            f'<text x="{legend_x + 30}" y="{y + 4}" fill="#f5f7fa" font-size="13" font-family="Inter, Arial, sans-serif">{svg_escape(str(s["label"]))}</text>'
        )

    svg_lines.append(
        f'<text x="{margin_left + plot_width / 2}" y="{height - 18}" fill="#f5f7fa" font-size="14" text-anchor="middle" font-family="Inter, Arial, sans-serif">{svg_escape(x_label)}</text>'
    )
    svg_lines.append(
        f'<text x="22" y="{margin_top + plot_height / 2}" fill="#f5f7fa" font-size="14" text-anchor="middle" transform="rotate(-90 22 {margin_top + plot_height / 2})" font-family="Inter, Arial, sans-serif">{svg_escape(y_label)}</text>'
    )
    svg_lines.append("</svg>")
    path.write_text("\n".join(svg_lines))


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    error_N_values = [1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000]
    runtime_N_values = [200, 500, 1_000, 2_000, 5_000, 10_000, 20_000]

    error_results = [benchmark_error_case(N) for N in error_N_values]
    runtime_results = [benchmark_runtime_case(N) for N in runtime_N_values]

    csv_rows = []
    for row in error_results:
        runtime_row = next((r for r in runtime_results if r["N"] == row["N"]), None)
        merged = dict(row)
        if runtime_row:
            merged.update(
                {
                    "naive_exact_time_s": runtime_row["naive_exact_time_s"],
                    "optimized_exact_time_s": runtime_row["optimized_exact_time_s"],
                    "naive_approx_time_s": runtime_row["naive_approx_time_s"],
                    "optimized_approx_time_s": runtime_row["optimized_approx_time_s"],
                    "naive_speedup": runtime_row["naive_speedup"],
                    "optimized_speedup": runtime_row["optimized_speedup"],
                }
            )
        else:
            merged.update(
                {
                    "naive_exact_time_s": "",
                    "optimized_exact_time_s": "",
                    "naive_approx_time_s": "",
                    "optimized_approx_time_s": "",
                    "naive_speedup": "",
                    "optimized_speedup": "",
                }
            )
        csv_rows.append(merged)

    write_csv(csv_rows, CSV_PATH)

    error_series = [
        {
            "label": "Total variation distance",
            "color": "#5eead4",
            "points": [(row["N"], max(row["total_variation"], 1e-16)) for row in error_results],
        },
        {
            "label": "Max absolute error",
            "color": "#f59e0b",
            "points": [(row["N"], max(row["max_abs_error"], 1e-16)) for row in error_results],
        },
    ]
    render_line_chart(
        ERROR_PLOT_PATH,
        title="Approximation Error vs N",
        x_label="Population size N (log scale)",
        y_label="Error (log scale)",
        series=error_series,
        x_log=True,
        y_log=True,
    )

    runtime_series = [
        {
            "label": "Naive exact hypergeometric",
            "color": "#60a5fa",
            "points": [(row["N"], row["naive_exact_time_s"]) for row in runtime_results],
        },
        {
            "label": "Naive binomial approximation",
            "color": "#f472b6",
            "points": [(row["N"], row["naive_approx_time_s"]) for row in runtime_results],
        },
        {
            "label": "lgamma exact hypergeometric",
            "color": "#94a3b8",
            "points": [(row["N"], row["optimized_exact_time_s"]) for row in runtime_results],
        },
        {
            "label": "lgamma binomial approximation",
            "color": "#facc15",
            "points": [(row["N"], row["optimized_approx_time_s"]) for row in runtime_results],
        },
    ]
    render_line_chart(
        RUNTIME_PLOT_PATH,
        title="Runtime vs N: Naive and lgamma Implementations",
        x_label="Population size N (log scale)",
        y_label="Average time per full PMF evaluation (ms)",
        series=runtime_series,
        x_log=True,
        y_log=False,
        y_tick_formatter=format_ms,
        y_padding_ratio=0.15,
    )

    print(f"Wrote {CSV_PATH.name}")
    print(f"Wrote {ERROR_PLOT_PATH.name}")
    print(f"Wrote {RUNTIME_PLOT_PATH.name}")
    print()
    print("Error summary:")
    for row in error_results:
        print(
            f"N={int(row['N']):>8}  "
            f"n/N={row['n_over_N']:.6f}  "
            f"tv={row['total_variation']:.3e}"
        )
    print()
    print("Runtime summary:")
    for row in runtime_results:
        print(
            f"N={int(row['N']):>8}  "
            f"naive={row['naive_exact_time_s']:.3e}s  "
            f"lgamma={row['optimized_exact_time_s']:.3e}s  "
            f"naive_approx={row['naive_approx_time_s']:.3e}s  "
            f"lgamma_approx={row['optimized_approx_time_s']:.3e}s  "
            f"naive_speedup={row['naive_speedup']:.2f}x"
        )


if __name__ == "__main__":
    main()
