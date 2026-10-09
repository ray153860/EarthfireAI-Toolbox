import argparse
import json

from .calculations import convert, dimensions, fit_csv, gradient, hydrostatic


def build_parser():
    parser = argparse.ArgumentParser(prog="earthfire-toolbox")
    sub = parser.add_subparsers(dest="command", required=True)
    item = sub.add_parser("convert"); item.add_argument("value", type=float); item.add_argument("from_unit"); item.add_argument("to_unit")
    item = sub.add_parser("dimensions"); item.add_argument("left"); item.add_argument("right")
    item = sub.add_parser("hydrostatic"); item.add_argument("density", type=float); item.add_argument("density_unit"); item.add_argument("tvd", type=float); item.add_argument("tvd_unit")
    item = sub.add_parser("gradient"); item.add_argument("density", type=float); item.add_argument("density_unit")
    item = sub.add_parser("fit-csv"); item.add_argument("path"); item.add_argument("--no-header", action="store_true")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.command == "convert": result = convert(args.value, args.from_unit, args.to_unit)
        elif args.command == "dimensions": result = dimensions(args.left, args.right)
        elif args.command == "hydrostatic": result = hydrostatic(args.density, args.density_unit, args.tvd, args.tvd_unit)
        elif args.command == "gradient": result = gradient(args.density, args.density_unit)
        else: result = fit_csv(args.path, not args.no_header)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, allow_nan=False))
        return 1


if __name__ == "__main__": raise SystemExit(main())
