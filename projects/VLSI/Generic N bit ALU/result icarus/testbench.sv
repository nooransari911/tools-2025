// Simple testbench for the ALU module with correct timing
module alu_testbench;
  parameter N = 16;
  
  // Testbench signals
  reg clk;
  reg rst_n;
  reg [7:0] sel;
  reg [N-1:0] A, B;
  wire [N-1:0] Z;
  wire Zsc;
  wire [7:0] status;
  
  // Clock generation
  initial begin
    clk = 0;
    forever #5 clk = ~clk;  // 10ns clock period
  end
  
  // Instantiate the ALU
  ALU #(.N(N)) DUT (
    .clk(clk),
    .reset_n(rst_n),
    .sel(sel),
    .A(A),
    .B(B),
    .Z(Z),
    .Zsc(Zsc),
    .status(status)
  );
  
  // Test procedure
  initial begin
    // Initialize waveform dump
    $dumpfile("alu_test.vcd");
    $dumpvars(0, alu_testbench);
    
    // Display header
    $display("ALU Testbench Starting...");
    $display("");
    $display("Time\tSel\tA\t\tB\t\tZ\t\tZ_exp\t\tZsc\tZsc_exp\tStatus\tC\tS\tP\tZ\tV\tDescription");
    $display("----\t---\t----\t\t----\t\t----\t\t-----\t\t---\t-------\t------\t-\t-\t-\t-\t-\t-----------");
    $display("");
    
    // Initialize signals
    rst_n = 0;
    sel = 8'h00;
    A = 16'h0000;
    B = 16'h0000;
    
    // Reset sequence
    repeat(3) @(posedge clk);
    rst_n = 1;
    repeat(2) @(posedge clk);
    
    // Test Case 1: Addition - Normal case
    $display("=== ARITHMETIC OPERATIONS ===");
    test_operation(8'h00, 16'h1234, 16'h5678, "ADD: Normal");
    
    // Test Case 2: Addition - Overflow (positive + positive = negative)
    test_operation(8'h00, 16'h7FFF, 16'h0001, "ADD: Pos Overflow");
    
    // Test Case 3: Addition - Underflow (negative + negative = positive)  
    test_operation(8'h00, 16'h8000, 16'h8000, "ADD: Neg Overflow");
    
    // Test Case 4: Addition - Zero result
    test_operation(8'h00, 16'hFFFF, 16'h0001, "ADD: Zero Result");
    
    test_operation(8'h00, 16'h0000, 16'h0000, "ADD: Zero + Zero");
    
    test_operation(8'h00, 16'hFFFF, 16'hFFFF, "ADD: -1 + -1");
    
    $display("=== LOGICAL OPERATIONS ===");
    
    // Test Case 5: Vector AND
    test_operation(8'h01, 16'hAAAA, 16'h5555, "AND: Alternating");
    
    // Test Case 6: Vector OR
    test_operation(8'h02, 16'h0F0F, 16'hF0F0, "OR: Complementary");
    
    // Test Case 7: Vector NAND
    test_operation(8'h03, 16'hFFFF, 16'hFFFF, "NAND: All ones");
    
    // Test Case 8: Vector NOT on A
    test_operation(8'h04, 16'hA5A5, 16'h0000, "NOT A: Pattern");
    
    // Test Case 9: Vector NOT on B
    test_operation(8'h05, 16'h0000, 16'hA5A5, "NOT B: Pattern");
    
    $display("=== REDUCTION OPERATIONS ===");
    
    // Test Case 10: Reduction AND on A (all bits AND)
    test_operation(8'h06, 16'hFFFF, 16'h0000, "RED AND: All 1s");
    
    // Test Case 11: Reduction OR on A (all bits OR)  
    test_operation(8'h07, 16'h0001, 16'h0000, "RED OR: One bit");
    
    // Test reduction operations with zero
    test_operation(8'h06, 16'h0000, 16'h0000, "RED AND: Zero");
    test_operation(8'h07, 16'h0000, 16'h0000, "RED OR: Zero");
    
    $display("=== EDGE CASES ===");
    
    // Test unknown operation
    test_operation(8'hFF, 16'h1234, 16'h5678, "Unknown Op");
    
    repeat(5) @(posedge clk);
    $display("");
    $display("Testbench completed.");
    $finish;
  end
  
  // Task to perform a test operation
  task test_operation;
    input [7:0] operation;
    input [N-1:0] input_a;
    input [N-1:0] input_b;
    input [200*8:1] description;
    
    reg [N:0] expected_sum;
    reg [N-1:0] expected_z;
    reg expected_zsc;
    
    begin
      // Calculate expected values
      case (operation)
        8'h00: begin // Addition
          expected_sum = input_a + input_b;
          expected_z = expected_sum[N-1:0];
          expected_zsc = 1'bx; // Not used for addition
        end
        8'h01: expected_z = input_a & input_b; // AND
        8'h02: expected_z = input_a | input_b; // OR
        8'h03: expected_z = ~(input_a & input_b); // NAND
        8'h04: expected_z = ~input_a; // NOT A
        8'h05: expected_z = ~input_b; // NOT B
        8'h06: begin // Reduction AND
          expected_zsc = &input_a;
          expected_z = 16'hxxxx; // Z not used for reduction operations
        end
        8'h07: begin // Reduction OR
          expected_zsc = |input_a;
          expected_z = 16'hxxxx; // Z not used for reduction operations
        end
        default: begin
          expected_z = 16'hxxxx;
          expected_zsc = 1'bx;
        end
      endcase
      
      // For logical operations (not reduction), Zsc is not used
      if (operation >= 8'h01 && operation <= 8'h05) begin
        expected_zsc = 1'bx;
      end
      
      // Set inputs and wait for clock edge
      sel = operation;
      A = input_a;
      B = input_b;
      
      // Wait one clock cycle for inputs to be processed
      @(posedge clk);
      
      // Wait another clock cycle for outputs to be registered
      @(posedge clk);
      
      // Small delay for signal propagation
      #1;
      
      // Display results with expected values
      if (operation >= 8'h06 && operation <= 8'h07) begin
        // For reduction operations, show Zsc expected value
        $display("%0t\t%02h\t%04h\t\t%04h\t\t%04h\t\t%04h\t\t%0d\t%0d\t\t%02h\t\t%0d\t%0d\t%0d\t%0d\t%0d\t%0s",
                 $time, sel, A, B, Z, expected_z, Zsc, expected_zsc, status,
                 status[0], status[1], status[2], status[3], status[4], description);
      end else begin
        // For vector operations, show Z expected value
        $display("%0t\t%02h\t%04h\t\t%04h\t\t%04h\t\t%04h\t\t%0d\t%0s\t\t%02h\t\t%0d\t%0d\t%0d\t%0d\t%0d\t%0s",
                 $time, sel, A, B, Z, expected_z, Zsc, "x", status,
                 status[0], status[1], status[2], status[3], status[4], description);
      end
      
      // Verify the result
      verify_operation(operation, input_a, input_b, description);
      
      $display(""); // Blank line for readability
    end
  endtask
  
  // Task to verify operation results
  task verify_operation;
    input [7:0] operation;
    input [N-1:0] input_a;
    input [N-1:0] input_b;
    input [200*8:1] description;
    
    reg [N:0] expected_sum;
    reg [N-1:0] expected_z;
    reg expected_zsc;
    reg expected_carry, expected_sign, expected_parity, expected_zero, expected_overflow;
    reg error_found;
    
    begin
      error_found = 0;
      
      case (operation)
        8'h00: begin // Addition
          expected_sum = input_a + input_b;
          expected_z = expected_sum[N-1:0];
          expected_carry = expected_sum[N];
          expected_sign = expected_z[N-1];
          expected_parity = ~^expected_z;
          expected_zero = ~|expected_z;
          expected_overflow = (~input_a[N-1] & ~input_b[N-1] & expected_z[N-1]) | 
                             (input_a[N-1] & input_b[N-1] & ~expected_z[N-1]);
          
          if (Z !== expected_z) begin
            $display("  ERROR: Z mismatch - Expected: %04h, Got: %04h", expected_z, Z);
            error_found = 1;
          end
          if (status[0] !== expected_carry) begin
            $display("  ERROR: Carry mismatch - Expected: %b, Got: %b", expected_carry, status[0]);
            error_found = 1;
          end
          if (status[1] !== expected_sign) begin
            $display("  ERROR: Sign mismatch - Expected: %b, Got: %b", expected_sign, status[1]);
            error_found = 1;
          end
          if (status[2] !== expected_parity) begin
            $display("  ERROR: Parity mismatch - Expected: %b, Got: %b", expected_parity, status[2]);
            error_found = 1;
          end
          if (status[3] !== expected_zero) begin
            $display("  ERROR: Zero mismatch - Expected: %b, Got: %b", expected_zero, status[3]);
            error_found = 1;
          end
          if (status[4] !== expected_overflow) begin
            $display("  ERROR: Overflow mismatch - Expected: %b, Got: %b", expected_overflow, status[4]);
            error_found = 1;
          end
        end
        
        8'h01: begin // AND
          expected_z = input_a & input_b;
          expected_parity = ~^expected_z;
          expected_zero = ~|expected_z;
          
          if (Z !== expected_z) begin
            $display("  ERROR: AND result mismatch - Expected: %04h, Got: %04h", expected_z, Z);
            error_found = 1;
          end
        end
        
        8'h02: begin // OR
          expected_z = input_a | input_b;
          expected_parity = ~^expected_z;
          expected_zero = ~|expected_z;
          
          if (Z !== expected_z) begin
            $display("  ERROR: OR result mismatch - Expected: %04h, Got: %04h", expected_z, Z);
            error_found = 1;
          end
        end
        
        8'h03: begin // NAND
          expected_z = ~(input_a & input_b);
          expected_parity = ~^expected_z;
          expected_zero = ~|expected_z;
          
          if (Z !== expected_z) begin
            $display("  ERROR: NAND result mismatch - Expected: %04h, Got: %04h", expected_z, Z);
            error_found = 1;
          end
        end
        
        8'h04: begin // NOT A
          expected_z = ~input_a;
          expected_parity = ~^expected_z;
          expected_zero = ~|expected_z;
          
          if (Z !== expected_z) begin
            $display("  ERROR: NOT A result mismatch - Expected: %04h, Got: %04h", expected_z, Z);
            error_found = 1;
          end
        end
        
        8'h05: begin // NOT B
          expected_z = ~input_b;
          expected_parity = ~^expected_z;
          expected_zero = ~|expected_z;
          
          if (Z !== expected_z) begin
            $display("  ERROR: NOT B result mismatch - Expected: %04h, Got: %04h", expected_z, Z);
            error_found = 1;
          end
        end
        
        8'h06: begin // Reduction AND
          expected_zsc = &input_a;
          expected_parity = ~^expected_zsc;
          expected_zero = ~|expected_zsc;
          
          if (Zsc !== expected_zsc) begin
            $display("  ERROR: Reduction AND result mismatch - Expected: %b, Got: %b", expected_zsc, Zsc);
            error_found = 1;
          end
        end
        
        8'h07: begin // Reduction OR  
          expected_zsc = |input_a;
          expected_parity = ~^expected_zsc;
          expected_zero = ~|expected_zsc;
          
          if (Zsc !== expected_zsc) begin
            $display("  ERROR: Reduction OR result mismatch - Expected: %b, Got: %b", expected_zsc, Zsc);
            error_found = 1;
          end
        end
        
        default: begin
          // For unknown operations, just check if outputs are X or defined
          if (!error_found) begin
            $display("  INFO: Unknown operation - outputs may be undefined");
          end
        end
      endcase
      
      if (!error_found && operation <= 8'h07) begin
        $display("  PASS: Operation verified successfully");
      end
    end
  endtask
  
endmodule