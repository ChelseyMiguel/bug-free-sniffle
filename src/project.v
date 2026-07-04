/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */
module tt_um_obstacle_avoider (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);
    // Map your inputs from the 8-bit input bus
    wire obstacle  = ui_in[0];
    wire too_close = ui_in[1];

    reg [1:0] state;

    localparam FORWARD = 2'b00;
    localparam TURNING = 2'b01;
    localparam STOPPED = 2'b10;

    always @(posedge clk) begin
        if (!rst_n)
            state <= FORWARD;
        else if (too_close)
            state <= STOPPED;
        else begin
            case (state)
                FORWARD: state <= obstacle ? TURNING : FORWARD;
                TURNING: state <= obstacle ? TURNING : FORWARD;
                STOPPED: state <= FORWARD;
                default: state <= FORWARD;
            endcase
        end
    end

    assign uo_out[0] = (state == FORWARD);
    assign uo_out[1] = (state == TURNING);
    assign uo_out[2] = (state == STOPPED);
    assign uo_out[7:3] = 5'b00000;
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

endmodule
