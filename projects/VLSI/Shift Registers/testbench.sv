module tb_PISO_SIPO_clean;
  // Parameters
  parameter N = 16;
  parameter TEST_WIDTH = 32;
  parameter CLK_PERIOD = 10;
  
  // Testbench signals
  reg clk;
  reg reset_n;
  
  // Test patterns
  reg [TEST_WIDTH-1:0] test_patterns [0:9];
  integer test_num;
  
  // PISO signals
  reg piso_load;
  reg [TEST_WIDTH-1:0] piso_data_in;
  reg piso_serial_in;
  wire piso_serial_out;
  
  // SIPO for end-to-end test
  reg sipo_load;
  wire [TEST_WIDTH-1:0] sipo_data_out;
  
  // SIPO for PISO verification
  reg piso_verify_load;
  wire [TEST_WIDTH-1:0] piso_verify_data;
  
  // Instantiate PISO under test
  PISO_N #(.N(TEST_WIDTH)) piso_dut (
    .clk(clk),
    .load(piso_load),
    .reset_n(reset_n),
    .data_bus(piso_data_in),
    .serial_in(piso_serial_in),
    .serial_out(piso_serial_out)
  );
  
  // SIPO for end-to-end testing
  SIPO_N #(.N(TEST_WIDTH)) sipo_endtoend (
    .clk(clk),
    .load(sipo_load),
    .reset_n(reset_n),
    .serial_in(piso_serial_out),
    .default_serial_in(1'b0),
    .serial_out(),
    .store_reg(sipo_data_out)
  );
  
  // SIPO for PISO verification
  SIPO_N #(.N(TEST_WIDTH)) sipo_verify (
    .clk(clk),
    .load(piso_verify_load),
    .reset_n(reset_n),
    .serial_in(piso_serial_out),
    .default_serial_in(1'b0),
    .serial_out(),
    .store_reg(piso_verify_data)
  );
  
  // Clock generation
  initial begin
    clk = 0;
    forever #(CLK_PERIOD/2) clk = ~clk;
  end
  
  // Initialize test patterns
  initial begin
    test_patterns[0] = 32'hDEADBEEF;
    test_patterns[1] = 32'h00000000;
    test_patterns[2] = 32'hFFFFFFFF;
    test_patterns[3] = 32'hAAAAAAAA;
    test_patterns[4] = 32'h55555555;
    test_patterns[5] = 32'h12345678;
    test_patterns[6] = 32'h9ABCDEF0;
    test_patterns[7] = 32'h80000000;
    test_patterns[8] = 32'h00000001;
    test_patterns[9] = 32'hF0F0F0F0;
  end
  
  // Main test sequence
  initial begin
    // Initialize
    reset_n = 0;
    piso_load = 0;
    sipo_load = 0;
    piso_verify_load = 0;
    piso_data_in = 0;
    piso_serial_in = 0;
    
    $display("");
    $display("=====================================");
    $display("    PISO-SIPO CLEAN TESTBENCH");
    $display("    Testing %0d-bit transmission", TEST_WIDTH);
    $display("=====================================");
    $display("");
    
    // Reset
    #(CLK_PERIOD * 3);
    reset_n = 1;
    #(CLK_PERIOD * 2);
    
    // Run tests
    for (test_num = 0; test_num < 10; test_num++) begin
      test_single_pattern(test_patterns[test_num], test_num + 1);
    end
    
    // Summary
    $display("");
    $display("=====================================");
    $display("    ALL TESTS COMPLETED SUCCESSFULLY");
    $display("    Total patterns tested: %0d", test_num);
    $display("=====================================");
    $display("");
    
    $finish;
  end
  
  // Task for testing single pattern
  task test_single_pattern(input [TEST_WIDTH-1:0] pattern, input integer test_id);
    begin
      $display("\n\nTest %2d:  Pattern = 0x%h", test_id, pattern);
      
      // Test 1: PISO standalone verification
      $display ("    Testing PISO Standalone for  0x%h", pattern);
      test_piso_standalone(pattern);
      
      $display ("\n     Testing     End-to-end for  0x%h", pattern);
      // Test 2: End-to-end PISO->SIPO verification  
      test_end_to_end(pattern);
      
      $display("");
    end
  endtask
  
  // Task for PISO standalone test
  task test_piso_standalone(input [TEST_WIDTH-1:0] pattern);
    begin
      // Load pattern into PISO
      piso_data_in = pattern;
      piso_serial_in = 1'b0;
      piso_load = 1;
      #(CLK_PERIOD);
      piso_load = 0;
      
      // Shift all bits through PISO into verification SIPO
      #(CLK_PERIOD * TEST_WIDTH);
      
      // Load verification SIPO output
      piso_verify_load = 1;
      #(CLK_PERIOD);
      piso_verify_load = 0;
      #(CLK_PERIOD);
      
      $display("         Sent: 0x%h", pattern);
      $display("          Got: 0x%h", piso_verify_data);
      
      // Check result
      if (piso_verify_data === pattern) begin
        $display("         PISO Test:     PASS");
      end else begin
        $display("         PISO Test:     FAIL - Expected: 0x%h, Got: 0x%h", 
                 pattern, piso_verify_data);
        $finish;
      end
    end
  endtask
  
  // Task for end-to-end test
  task test_end_to_end(input [TEST_WIDTH-1:0] pattern);
    begin
      // Load pattern into PISO
      piso_data_in = pattern;
      piso_serial_in = 1'b0;
      piso_load = 1;
      #(CLK_PERIOD);
      piso_load = 0;
      
      // Shift all bits from PISO to SIPO
      #(CLK_PERIOD * TEST_WIDTH);
      
      // Load SIPO shift register to output
      sipo_load = 1;
      #(CLK_PERIOD);
      sipo_load = 0;
      #(CLK_PERIOD);
      
      $display("         Sent: 0x%h", pattern);
      $display("          Got: 0x%h", sipo_data_out);
      
      // Simple assertion check
      if (sipo_data_out === pattern) begin
        $display("         End-to-End:   PASS");
      end else begin
        $display("         End-to-End:   FAIL - Expected: 0x%h, Got: 0x%h", 
                 pattern, sipo_data_out);
        $finish;
      end
    end
  endtask
  
  // Waveform generation
  initial begin
    $dumpfile("piso_sipo_clean.vcd");
    $dumpvars(0, tb_PISO_SIPO_clean);
  end
  
endmodule