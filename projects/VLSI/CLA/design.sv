module CLA_Adder #(
  parameter N=16
) (
  input                  clk,
  input                  reset_n,
  input [N-1:0]          A, B,
  input                  Cin,

  output reg [N-1:0]     Sum,
  output reg             Cout
);

  logic [N-1:0]        next_sum;
  logic  			   next_cout;
  reg [N:0]            Cs;
  logic [N-1:0]        P, G;
  assign P = A ^ B;
  assign G = A & B;

  
  
  always_comb begin
    Cs [0] = Cin;
    for (int i=0; i<N; i++) begin
      Cs [i+1]     = (P[i] & Cs[i]) | (G[i]);
  	end
    next_sum      = P ^ (Cs [N-1:0]);
    next_cout     = Cs [N];
  end
  
  always @(posedge clk) begin
    if (!reset_n) begin
      Sum  <= 0;
      Cout <= 0;
    end
    else begin
      Sum  <= next_sum;
      Cout <= next_cout;
    end
  end
endmodule