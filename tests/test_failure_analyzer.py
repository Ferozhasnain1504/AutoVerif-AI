from agent.failure_analyzer import FailureAnalyzer


def main():

    analyzer = FailureAnalyzer()

    print("\n========== TEST 1: PASS ==========")

    pass_result = {
        "status": "PASS",
        "passed_tests": 10,
        "failed_tests": 0,
        "output": "PASS: all tests passed",
        "errors": [],
    }

    feedback = analyzer.analyze(
        pass_result
    )

    print(feedback)

    print("\n========== TEST 2: FAIL ==========")

    fail_result = {
        "status": "FAIL",
        "passed_tests": 8,
        "failed_tests": 2,
        "output": (
            "PASS: test 1\n"
            "FAIL: a=15 b=15 expected=30 actual=31\n"
            "FAIL: a=7 b=8 expected=15 actual=16\n"
        ),
        "errors": [],
    }

    feedback = analyzer.analyze(
        fail_result
    )

    print(feedback)

    print("\n========== TEST 3: COMPILE ERROR ==========")

    compile_result = {
        "status": "COMPILE_ERROR",
        "passed_tests": 0,
        "failed_tests": 0,
        "output": "",
        "errors": "Syntax error in testbench",
    }

    feedback = analyzer.analyze(
        compile_result
    )

    print(feedback)


if __name__ == "__main__":
    main()