from agent.rtl_analyzer import RTLAnalyzer


def main():

    analyzer = RTLAnalyzer()

    result = analyzer.analyze(
        "rtl/adder.v"
    )

    print("\n========== RTL ANALYSIS ==========")

    print("Module:", result["module"])

    print("\nInputs:")

    for name, width in result["inputs"].items():

        print(
            f"  {name}: {width} bits"
        )

    print("\nOutputs:")

    for name, width in result["outputs"].items():

        print(
            f"  {name}: {width} bits"
        )

    print("\nAssignments:")

    for assignment in result["assignments"]:

        print(
            f"  {assignment['target']} = "
            f"{assignment['expression']}"
        )


if __name__ == "__main__":
    main()