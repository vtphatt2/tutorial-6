"""Generate local signed demo JWTs. Never use demo tokens for production."""
import argparse
from src.api.auth import create_demo_token


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", choices=["manager", "technician"], required=True)
    parser.add_argument("--email", default="instructor@fieldco.com")
    args = parser.parse_args()
    print(create_demo_token(args.email, args.role))


if __name__ == "__main__":
    main()
