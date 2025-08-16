module ALU_obsolete #(
  parameter N = 16
) (
  input              clk,
  input              rst_n,
  input      [7:0]   sel,
  input      [N-1:0] A, B,
  output [N-1:0]     Z,
  output             Zsc,
  output [7:0]       status
);
  // STEP 2: Create SEPARATE internal registers
  reg [N-1:0] Z_reg;
  reg         Zsc_reg;
  reg [7:0]   status_reg;
  
  reg [(N-1):0]      Ztemp;
  reg                Zsctemp;
  reg [7:0]          statustemp;
  

  
  always @(*) begin
    Ztemp           = {N {1'bx}};
    Zsctemp         = 1'bx;
    statustemp      = {8{1'b0}};
    case (sel)
      8'h00: begin // Add
        {statustemp [0], Ztemp} = A + B;
        statustemp [1] = Ztemp [(N-1)]; // Sign
        statustemp [2] = ~^ Ztemp;          // Even Parity
        statustemp [3] = ~| Ztemp;          // Zeroes
        statustemp [4] = (~ A [(N-1)] & ~ B [(N-1)] & Ztemp [(N-1)]) | (A [(N-1)] & B [(N-1)] & ~ Ztemp [(N-1)]);         // Overflow
      end
      
      8'h01: begin // Vector AND
        Ztemp = A & B;
        statustemp [2] = ~^ Ztemp;          // Even Parity
        statustemp [3] = ~| Ztemp;          // Zeroes
      end
      
      8'h02: begin // Vector OR
        Ztemp = A | B;
        statustemp [2] = ~^ Ztemp;          // Even Parity
        statustemp [3] = ~| Ztemp;          // Zeroes
      end
      
      8'h03: begin // Vector NAND
        Ztemp = ~ (A & B);
        statustemp [2] = ~^ Ztemp;          // Even Parity
        statustemp [3] = ~| Ztemp;          // Zeroes
      end
      
      8'h04: begin // Vector NOT on A
        Ztemp = ~ A;
        statustemp [2] = ~^ Ztemp;          // Even Parity
        statustemp [3] = ~| Ztemp;          // Zeroes
      end

      8'h05: begin // Vector NOT on B
        Ztemp = ~ B;
        statustemp [2] = ~^ Ztemp;          // Even Parity
        statustemp [3] = ~| Ztemp;          // Zeroes
      end

      8'h06: begin // Reduction AND on A
        Zsctemp = & A;
        statustemp [2] = ~^ Zsctemp;          // Even Parity
        statustemp [3] = ~| Zsctemp;          // Zeroes
      end
      8'h07: begin // Reduction OR on A
        Zsctemp = | A;
        statustemp [2] = ~^ Zsctemp;          // Even Parity
        statustemp [3] = ~| Zsctemp;          // Zeroes
      end
      
      
      default: begin
        Ztemp = {(N){1'bx}};
        Zsctemp = 1'bx;
        statustemp = {8{1'b0}};
      end
    endcase
  end
  // STEP 3 (Part A): The sequential block now only uses the internal _reg variables
  always @(posedge clk) begin
    if (!rst_n) begin
      Z_reg      <= {(N){1'b0}};
      Zsc_reg    <= 1'b0;
      status_reg <= {8{1'b0}};
    end else begin
      Z_reg      <= Ztemp;
      Zsc_reg    <= Zsctemp;
      status_reg <= statustemp;
    end
  end

  // STEP 3 (Part B): Connect internal registers to the output ports
  assign Z      = Z_reg;
  assign Zsc    = Zsc_reg;
  assign status = status_reg;
endmodule




module ALU #(
  parameter N=16
) (
  input              clk,
  input              reset_n,
  input [N-1:0]      A, B,
  input [7:0]        sel,

  output reg [N-1:0]     Z,
  output reg             Zsc,
  output reg [7:0]       status
);

  
  reg [(N-1):0]      Z_next;
  reg                Zsc_next;
  reg [7:0]          status_next;
  
  typedef enum logic [7:0] {
    ADD      = 8'h00,
    VEC_AND  = 8'h01,
    VEC_OR   = 8'h02,
    VEC_NAND = 8'h03,
    VEC_NOTA = 8'h04,
    VEC_NOTB = 8'h05,
    RED_ANDA = 8'h06,
    RED_ORA  = 8'h07
  } OPCODET;
  
  OPCODET opcode;
  assign opcode = OPCODET'(sel);
  
  always @(*) begin
    Z_next           = {N {1'b0}};
    Zsc_next         = 1'b0;
    status_next      = {8{1'b0}};

    case (opcode)
      ADD: begin
        {status_next[0], Z_next} = A + B;
        status_next[1] = Z_next[N-1]; // Sign
        status_next[2] = ~^ Z_next;     // Even Parity
        status_next[3] = ~| Z_next;     // Zeroes
        status_next[4] = (~A[N-1] & ~B[N-1] & Z_next[N-1]) | (A[N-1] & B[N-1] & ~Z_next[N-1]); // Overflow
      end

      VEC_AND: begin
        Z_next = A & B;
        status_next[2] = ~^ Z_next; // Even Parity
        status_next[3] = ~| Z_next; // Zeroes
      end

      VEC_OR: begin
        Z_next = A | B;
        status_next[2] = ~^ Z_next; // Even Parity
        status_next[3] = ~| Z_next; // Zeroes
      end

      VEC_NAND: begin
        Z_next = ~(A & B);
        status_next[2] = ~^ Z_next; // Even Parity
        status_next[3] = ~| Z_next; // Zeroes
      end

      VEC_NOTA: begin
        Z_next = ~A;
        status_next[2] = ~^ Z_next; // Even Parity
        status_next[3] = ~| Z_next; // Zeroes
      end

      VEC_NOTB: begin
        Z_next = ~B;
        status_next[2] = ~^ Z_next; // Even Parity
        status_next[3] = ~| Z_next; // Zeroes
      end

      RED_ANDA: begin
        Zsc_next = &A;
        status_next[2] = ~^ Zsc_next; // Even Parity
        status_next[3] = ~| Zsc_next; // Zeroes
      end

      RED_ORA: begin
        Zsc_next = |A;
        status_next[2] = ~^ Zsc_next; // Even Parity
        status_next[3] = ~| Zsc_next; // Zeroes
      end

      default: begin
        Z_next     = {N{1'bx}};
        Zsc_next   = 1'bx;
        status_next = {8{1'b0}};
      end
    endcase
  end
  
  always @(posedge clk) begin
    if (!reset_n) begin
      Z       <= {(N){1'b0}};
      Zsc     <= 1'b0;
      status  <= {8{1'b0}};
    end
    else begin
      Z       <= Z_next;
      Zsc     <= Zsc_next;
      status  <= status_next;
    end
  end
endmodule