from __future__ import annotations

from math import exp
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "src/assets/posts/asymptotic_equivalent_curves.svg"

WIDTH = 480
HEIGHT = 560
MIN_DIMENSION = min(WIDTH, HEIGHT)

PLOT_LEFT = WIDTH * 0.117
PLOT_RIGHT = WIDTH * 0.9
PLOT_TOP = HEIGHT * 0.129
PLOT_BOTTOM = HEIGHT * 0.786
FONT_SIZE = MIN_DIMENSION * 0.032
AXIS_STROKE_WIDTH = MIN_DIMENSION * 0.0024
BASE_CURVE_STROKE_WIDTH = MIN_DIMENSION * 0.0054
ASYMPTOTIC_CURVE_STROKE_WIDTH = MIN_DIMENSION * 0.0063
LABEL_OFFSET_Y = HEIGHT * 0.043
LABEL_GAP_Y = HEIGHT * 0.068
SAMPLES = max(80, round(WIDTH * 0.1875))

X_MIN = -1.0
X_MAX = 5.0


def f(x: float) -> float:
    return x + exp(-x)


def g(x: float) -> float:
    return x


RAW_Y_MIN = min(0.0, g(X_MIN), f(X_MIN))
RAW_Y_MAX = max(0.0, g(X_MAX), f(X_MAX), f(X_MIN))
Y_PADDING = (RAW_Y_MAX - RAW_Y_MIN) * 0.07
Y_MIN = RAW_Y_MIN - Y_PADDING
Y_MAX = RAW_Y_MAX + Y_PADDING


def sx(x: float) -> float:
    return PLOT_LEFT + (x - X_MIN) / (X_MAX - X_MIN) * (PLOT_RIGHT - PLOT_LEFT)


def sy(y: float) -> float:
    return PLOT_BOTTOM - (y - Y_MIN) / (Y_MAX - Y_MIN) * (PLOT_BOTTOM - PLOT_TOP)


def sampled_path(fn, samples: int = SAMPLES) -> str:
    points = []
    for i in range(samples + 1):
        x = X_MIN + (X_MAX - X_MIN) * i / samples
        points.append((sx(x), sy(fn(x))))

    commands = [f"M {points[0][0]:.2f} {points[0][1]:.2f}"]
    commands.extend(f"L {x:.2f} {y:.2f}" for x, y in points[1:])
    return " ".join(commands)


def domain_x(ratio: float) -> float:
    return X_MIN + (X_MAX - X_MIN) * ratio


def main() -> None:
    f_path = sampled_path(f)
    g_path = sampled_path(g)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
  <title id="title">Asymptotically equivalent curves</title>
  <desc id="desc">A dark, minimal plot of f(x)=x+e^-x and g(x)=x, showing the curves approach each other as x increases.</desc>
  <rect width="100%" height="100%" fill="#080808" />

  <style>
    text {{
      font-family: Georgia, "Times New Roman", serif;
      fill: #b8b8b8;
      font-size: {FONT_SIZE:.2f}px;
    }}
    .gold {{
      fill: #d4af37;
    }}
    .paper {{
      fill: #d8d2c2;
    }}
    .axis {{
      stroke: #d8d2c2;
      stroke-width: {AXIS_STROKE_WIDTH:.2f};
    }}
  </style>

  <g class="axis" fill="none" stroke-linecap="square">
    <path d="M {PLOT_LEFT} {sy(0):.2f} H {PLOT_RIGHT}" />
    <path d="M {sx(0):.2f} {PLOT_BOTTOM} V {PLOT_TOP}" />
  </g>

  <path
    d="{g_path}"
    fill="none"
    stroke="#d8d2c2"
    stroke-width="{BASE_CURVE_STROKE_WIDTH:.2f}"
    stroke-linecap="round"
    stroke-linejoin="round"
  />

  <path
    d="{f_path}"
    fill="none"
    stroke="#d4af37"
    stroke-width="{ASYMPTOTIC_CURVE_STROKE_WIDTH:.2f}"
    stroke-linecap="round"
    stroke-linejoin="round"
  />
</svg>
"""
    OUTPUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
