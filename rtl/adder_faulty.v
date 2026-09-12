module adder(
    input  [3:0] a,
    input  [3:0] b,
    output [4:0] sum
);

assign sum = a + b + 1;

endmodule