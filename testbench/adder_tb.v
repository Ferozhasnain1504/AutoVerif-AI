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

    initial begin

        $display("Starting simulation...");

        a = 4'd0;
        b = 4'd0;
        #10;

        $display("a=%d b=%d sum=%d", a, b, sum);

        a = 4'd5;
        b = 4'd3;
        #10;

        $display("a=%d b=%d sum=%d", a, b, sum);

        a = 4'd15;
        b = 4'd15;
        #10;

        $display("a=%d b=%d sum=%d", a, b, sum);

        $finish;

    end

endmodule