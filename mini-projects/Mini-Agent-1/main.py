from tools.registry import TOOL_SCHEMAS


def main():
    for tool_name, schema in TOOL_SCHEMAS.items():
        print(f"\n{tool_name}")
        print(schema.model_dump_json(indent=2))


if __name__ == "__main__":
    main()