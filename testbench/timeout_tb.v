`timescale 1ns/1ps

module timeout_tb;

    initial begin
        $display("Starting timeout test...");

        forever begin
            #1;
        end
    end

endmodule