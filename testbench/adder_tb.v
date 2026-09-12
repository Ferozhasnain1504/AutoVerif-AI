`timescale 1ns/1ps

module adder_tb;

    reg [3:0] a;
    reg [3:0] b;

    wire [4:0] sum;

    adder uut (
        .a(a),
        .b(b),
        .sum(sum)
    );

    task check_result;

        input [3:0] test_a;
        input [3:0] test_b;
        input [4:0] expected;

        begin

            a = test_a;
            b = test_b;

            #10;

            if (sum == expected) begin

                $display(
                    "PASS: a=%d b=%d sum=%d",
                    a,
                    b,
                    sum
                );

            end
            else begin

                $display(
                    "FAIL: a=%d b=%d expected=%d actual=%d",
                    a,
                    b,
                    expected,
                    sum
                );

            end

        end

    endtask


    initial begin

        $display("Starting verification...");

        check_result(4'd0, 4'd0, 5'd0);

        check_result(4'd5, 4'd3, 5'd8);

        check_result(4'd15, 4'd15, 5'd30);

        $display("Verification completed.");

        #1000000;

    end

endmodule