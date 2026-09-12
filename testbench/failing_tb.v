`timescale 1ns/1ps

module adder_faulty_tb;

    reg [3:0] a;
    reg [3:0] b;
    wire [4:0] sum;

    adder_faulty uut (
        .a(a),
        .b(b),
        .sum(sum)
    );

    initial begin

        a = 4'd5;
        b = 4'd3;

        #10;

        if (sum == 5'd8)
            $display("PASS: Test passed");
        else
            $display(
                "FAIL: expected=8 actual=%d",
                sum
            );

        $finish;

    end

endmodule