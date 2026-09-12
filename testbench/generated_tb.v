module tb_adder;

    reg [3:0] a;
    reg [3:0] b;
    wire [4:0] sum;

    reg [4:0] expected_sum;
    integer i, j;
    integer error_count;

    // Instantiate Design Under Test (DUT)
    adder dut (
        .a(a),
        .b(b),
        .sum(sum)
    );

    initial begin
        error_count = 0;

        // Exhaustive testing of all combinations (16 * 16 = 256 test cases)
        // This includes minimum values (0,0), maximum values (15,15),
        // boundary carry-out transitions (8+7 vs 8+8), and single-bit toggles.
        for (i = 0; i < 16; i = i + 1) begin
            for (j = 0; j < 16; j = j + 1) begin
                a = i;
                b = j;
                expected_sum = a + b;
                #10;

                if (sum !== expected_sum) begin
                    $display("FAIL: a = %d, b = %d | expected sum = %d, got sum = %d", a, b, expected_sum, sum);
                    error_count = error_count + 1;
                end else begin
                    $display("PASS: a = %d, b = %d | expected sum = %d, got sum = %d", a, b, expected_sum, sum);
                end
            end
        end

        // Final verification summary
        if (error_count == 0) begin
            $display("PASS: All 256 tests passed.");
        end else begin
            $display("FAIL: Total failures = %0d", error_count);
        end

        $finish;
    end

endmodule