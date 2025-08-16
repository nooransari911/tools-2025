module PISO_N_obsolete_v1 #(
  parameter N=16
)(
  input clk,
  input load,
  input reset_n,
  input [N-1:0] data_bus,
  output serial_out
);
  reg [N-1:0] shift_reg;
  wire         default_shiftin;

  typedef enum logic [1:0]{
    SHIFT    = 2'b10,
    LOAD     = 2'b11,
    RESET_0  = 2'b00,
    RESET_1  = 2'b01
  } OPCODET;

  assign default_shiftin = 1'b0;
  assign serial_out      = shift_reg [N-1];

  
  OPCODET opcode;
  //assign opcode = OPCODET'({reset_n, load});

  
  always @(posedge clk) begin
    for (int i=N-1; i>0; i--) begin
      case ({reset_n, load})
        SHIFT:   shift_reg [i]      <= shift_reg [i-1];
        LOAD:    shift_reg [i]      <= data_bus  [i];
        RESET_0: shift_reg [i]      <= 1'b0;
        RESET_1: shift_reg [i]      <= 1'b0;
      endcase
  	end
  end
  
  always @(posedge clk) begin
    case (opcode)
      SHIFT:   shift_reg [0]      <= default_shiftin;
      LOAD:    shift_reg [0]      <= data_bus  [0];
      RESET_0: shift_reg [0]      <= 1'b0;
      RESET_1: shift_reg [0]      <= 1'b0;
    endcase
  end
endmodule

    
    

module PISO_N_obsolete_v2 #(
  parameter N=16
)(
  input clk,
  input load,
  input reset_n,
  input [N-1:0] data_bus,
  output serial_out
);
  reg [N-1:0]  shift_reg;
  wire         default_shiftin;

  typedef enum logic [1:0]{
    SHIFT    = 2'b10,
    LOAD     = 2'b11,
    RESET_0  = 2'b00,
    RESET_1  = 2'b01
  } OPCODET;

  assign default_shiftin = 1'b0;
  assign serial_out      = shift_reg [N-1];

  
  OPCODET opcode;
  assign opcode = OPCODET'({reset_n, load});

  
  always @(posedge clk) begin
    case (opcode)
      SHIFT:   shift_reg      <= {shift_reg [N-2:0], default_shiftin};
      LOAD:    shift_reg      <= data_bus;
      RESET_0: shift_reg      <= {N {default_shiftin}};
      RESET_1: shift_reg      <= {N {default_shiftin}};
    endcase
  end
endmodule



module PISO_N #(
  parameter N=16
)(
  input clk,
  input load,
  input reset_n,
  input [N-1:0] data_bus,
  input serial_in,
  output serial_out
);
  reg [N-1:0]  shift_reg;

  typedef enum logic [1:0]{
    SHIFT    = 2'b10,
    LOAD     = 2'b11,
    RESET_0  = 2'b00,
    RESET_1  = 2'b01
  } OPCODET;

  assign serial_out      =  shift_reg [N-1];

  
  OPCODET opcode;
  assign opcode = OPCODET'({reset_n, load});

  
  always @(posedge clk) begin
    case (opcode)
      SHIFT:   shift_reg      <= {shift_reg [N-2:0], serial_in};
      LOAD:    shift_reg      <= data_bus;
      RESET_0: shift_reg      <= {N {serial_in}};
      RESET_1: shift_reg      <= {N {serial_in}};
    endcase
  end
endmodule

    
module SIPO_N #(
  parameter N=16
)(
  input clk,
  input load,
  input reset_n,
  input serial_in,
  input default_serial_in,
  output serial_out,
  output reg [N-1:0] store_reg
);
  reg [N-1:0]  shift_reg;

  typedef enum logic [1:0]{
    SHIFT    = 2'b10,
    LOAD     = 2'b11,
    RESET_0  = 2'b00,
    RESET_1  = 2'b01
  } OPCODET;

  assign serial_out      =  shift_reg [N-1];

  
  OPCODET opcode;
  assign opcode = OPCODET'({reset_n, load});

  
  always @(posedge clk) begin
    case (opcode)
      SHIFT:   shift_reg      <= {shift_reg [N-2:0], serial_in};
      LOAD:    store_reg      <= shift_reg;
      RESET_0: {shift_reg, store_reg}      <= {2*N {default_serial_in}};
      RESET_1: {shift_reg, store_reg}      <= {2*N {default_serial_in}};
    endcase
  end
endmodule
    