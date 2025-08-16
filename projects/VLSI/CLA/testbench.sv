module CLA_Adder_TB;
  
  // Parameters
  parameter N = 16;
  parameter CLK_PERIOD = 10;
  parameter NUM_TESTS = 26;
  
  // Testbench signals
  logic                clk;
  logic                reset_n;
  logic [N-1:0]        A, B;
  logic                Cin;
  wire [N-1:0]         Sum;
  wire                 Cout;
  
  // Test variables
  integer test_count = 0;
  integer pass_count = 0;
  integer fail_count = 0;
  
  // Test pattern arrays (separate arrays instead of struct)
  reg [N-1:0] test_A [0:NUM_TESTS-1];
  reg [N-1:0] test_B [0:NUM_TESTS-1];
  reg         test_Cin [0:NUM_TESTS-1];
  reg [N-1:0] expected_sum [0:NUM_TESTS-1];
  reg         expected_cout [0:NUM_TESTS-1];
  
  // Instantiate DUT
  CLA_Adder #(.N(N)) dut (
    .clk(clk),
    .reset_n(reset_n),
    .A(A),
    .B(B),
    .Cin(Cin),
    .Sum(Sum),
    .Cout(Cout)
  );
  
  // Clock generation
  initial begin
    clk = 0;
    forever #(CLK_PERIOD/2) clk = ~clk;
  end
  
  // Initialize test patterns
  initial begin
    // Test 0: Zero + Zero
    test_A[0] = 16'h0000; test_B[0] = 16'h0000; test_Cin[0] = 1'b0;
    expected_sum[0] = 16'h0000; expected_cout[0] = 1'b0;
    
    // Test 1: Zero + Zero + Cin
    test_A[1] = 16'h0000; test_B[1] = 16'h0000; test_Cin[1] = 1'b1;
    expected_sum[1] = 16'h0001; expected_cout[1] = 1'b0;
    
    // Test 2: 1 + 1
    test_A[2] = 16'h0001; test_B[2] = 16'h0001; test_Cin[2] = 1'b0;
    expected_sum[2] = 16'h0002; expected_cout[2] = 1'b0;
    
    // Test 3: 1 + 1 + Cin
    test_A[3] = 16'h0001; test_B[3] = 16'h0001; test_Cin[3] = 1'b1;
    expected_sum[3] = 16'h0003; expected_cout[3] = 1'b0;
    
    // Test 4: Max + Zero
    test_A[4] = 16'hFFFF; test_B[4] = 16'h0000; test_Cin[4] = 1'b0;
    expected_sum[4] = 16'hFFFF; expected_cout[4] = 1'b0;
    
    // Test 5: Max + 1 (overflow)
    test_A[5] = 16'hFFFF; test_B[5] = 16'h0001; test_Cin[5] = 1'b0;
    expected_sum[5] = 16'h0000; expected_cout[5] = 1'b1;
    
    // Test 6: Max + Max
    test_A[6] = 16'hFFFF; test_B[6] = 16'hFFFF; test_Cin[6] = 1'b0;
    expected_sum[6] = 16'hFFFE; expected_cout[6] = 1'b1;
    
    // Test 7: Max + Max + Cin
    test_A[7] = 16'hFFFF; test_B[7] = 16'hFFFF; test_Cin[7] = 1'b1;
    expected_sum[7] = 16'hFFFF; expected_cout[7] = 1'b1;
    
    // Test 8: 2^1 + 2^1
    test_A[8] = 16'h0002; test_B[8] = 16'h0002; test_Cin[8] = 1'b0;
    expected_sum[8] = 16'h0004; expected_cout[8] = 1'b0;
    
    // Test 9: 2^2 + 2^2
    test_A[9] = 16'h0004; test_B[9] = 16'h0004; test_Cin[9] = 1'b0;
    expected_sum[9] = 16'h0008; expected_cout[9] = 1'b0;
    
    // Test 10: 2^3 + 2^3
    test_A[10] = 16'h0008; test_B[10] = 16'h0008; test_Cin[10] = 1'b0;
    expected_sum[10] = 16'h0010; expected_cout[10] = 1'b0;
    
    // Test 11: 2^15 + 2^15 (overflow)
    test_A[11] = 16'h8000; test_B[11] = 16'h8000; test_Cin[11] = 1'b0;
    expected_sum[11] = 16'h0000; expected_cout[11] = 1'b1;
    
    // Test 12: 0101... + 1010...
    test_A[12] = 16'h5555; test_B[12] = 16'hAAAA; test_Cin[12] = 1'b0;
    expected_sum[12] = 16'hFFFF; expected_cout[12] = 1'b0;
    
    // Test 13: 1010... + 0101...
    test_A[13] = 16'hAAAA; test_B[13] = 16'h5555; test_Cin[13] = 1'b0;
    expected_sum[13] = 16'hFFFF; expected_cout[13] = 1'b0;
    
    // Test 14: 0101... + 1010... + Cin
    test_A[14] = 16'h5555; test_B[14] = 16'hAAAA; test_Cin[14] = 1'b1;
    expected_sum[14] = 16'h0000; expected_cout[14] = 1'b1;
    
    // Test 15: Random case 1
    test_A[15] = 16'h1234; test_B[15] = 16'h5678; test_Cin[15] = 1'b0;
    expected_sum[15] = 16'h68AC; expected_cout[15] = 1'b0;
    
    // Test 16: Random case 2
    test_A[16] = 16'hABCD; test_B[16] = 16'h1234; test_Cin[16] = 1'b0;
    expected_sum[16] = 16'hBE01; expected_cout[16] = 1'b0;
    
    // Test 17: Mid + 1
    test_A[17] = 16'h7FFF; test_B[17] = 16'h0001; test_Cin[17] = 1'b0;
    expected_sum[17] = 16'h8000; expected_cout[17] = 1'b0;
    
    // Test 18: Signed overflow
    test_A[18] = 16'h8000; test_B[18] = 16'h7FFF; test_Cin[18] = 1'b1;
    expected_sum[18] = 16'h0000; expected_cout[18] = 1'b1;
    
    // Test 19: Carry propagation 8-bit
    test_A[19] = 16'h00FF; test_B[19] = 16'h0001; test_Cin[19] = 1'b0;
    expected_sum[19] = 16'h0100; expected_cout[19] = 1'b0;
    
    // Test 20: Carry propagation 12-bit
    test_A[20] = 16'h0FFF; test_B[20] = 16'h0001; test_Cin[20] = 1'b0;
    expected_sum[20] = 16'h1000; expected_cout[20] = 1'b0;
    
    // Test 21: Carry propagation 15-bit
    test_A[21] = 16'h7FFF; test_B[21] = 16'h0001; test_Cin[21] = 1'b0;
    expected_sum[21] = 16'h8000; expected_cout[21] = 1'b0;
    
    // Test 22: 0 + All 1s
    test_A[22] = 16'h0000; test_B[22] = 16'hFFFF; test_Cin[22] = 1'b0;
    expected_sum[22] = 16'hFFFF; expected_cout[22] = 1'b0;
    
    // Test 23: 0 + All 1s + Cin
    test_A[23] = 16'h0000; test_B[23] = 16'hFFFF; test_Cin[23] = 1'b1;
    expected_sum[23] = 16'h0000; expected_cout[23] = 1'b1;
    
    // Test 24: 1 + (Max-1)
    test_A[24] = 16'h0001; test_B[24] = 16'hFFFE; test_Cin[24] = 1'b0;
    expected_sum[24] = 16'hFFFF; expected_cout[24] = 1'b0;
    
    // Test 25: 1 + (Max-1) + Cin
    test_A[25] = 16'h0001; test_B[25] = 16'hFFFE; test_Cin[25] = 1'b1;
    expected_sum[25] = 16'h0000; expected_cout[25] = 1'b1;
  end
  
  // Task to test a single pattern
  task test_single;
    input integer test_index;
    reg [N:0] expected_result, actual_result;
    begin
      test_count = test_count + 1;
      
      // Apply inputs
      A = test_A[test_index];
      B = test_B[test_index];
      Cin = test_Cin[test_index];
      
      // Wait for combinational logic and one clock cycle
      #1;
      @(posedge clk);
      #1; // Small delay after clock edge
      
      // Check results
      expected_result = {expected_cout[test_index], expected_sum[test_index]};
      actual_result = {Cout, Sum};
      
      if (actual_result === expected_result) begin
        $display("PASS: Test %2d", test_count);
        $display("      A=%h, B=%h, Cin=%b => Sum=%h, Cout=%b", 
                 A, B, Cin, Sum, Cout);
        pass_count = pass_count + 1;
      end else begin
        $display("FAIL: Test %2d", test_count);
        $display("      A=%h, B=%h, Cin=%b", A, B, Cin);
        $display("      Expected: Sum=%h, Cout=%b", expected_sum[test_index], expected_cout[test_index]);
        $display("      Actual:   Sum=%h, Cout=%b", Sum, Cout);
        fail_count = fail_count + 1;
      end
      $display("");
    end
  endtask
  
  // Task to test random pattern
  task test_random;
    input integer test_num;
    reg [N-1:0] rand_A, rand_B;
    reg rand_Cin;
    reg [N:0] expected_result, actual_result;
    reg [N:0] calc_sum;
    begin
      test_count = test_count + 1;
      
      // Generate random inputs
      rand_A = $random();
      rand_B = $random();
      rand_Cin = $random() & 1'b1;
      
      // Calculate expected result
      calc_sum = rand_A + rand_B + rand_Cin;
      
      // Apply inputs
      A = rand_A;
      B = rand_B;
      Cin = rand_Cin;
      
      // Wait for combinational logic and one clock cycle
      #1;
      @(posedge clk);
      #1;
      
      // Check results
      expected_result = calc_sum;
      actual_result = {Cout, Sum};
      
      if (actual_result === expected_result) begin
        $display("PASS: Random Test %2d", test_num);
        $display("      A=%h, B=%h, Cin=%b => Sum=%h, Cout=%b", 
                 A, B, Cin, Sum, Cout);
        pass_count = pass_count + 1;
      end else begin
        $display("FAIL: Random Test %2d", test_num);
        $display("      A=%h, B=%h, Cin=%b", A, B, Cin);
        $display("      Expected: Sum=%h, Cout=%b", calc_sum[N-1:0], calc_sum[N]);
        $display("      Actual:   Sum=%h, Cout=%b", Sum, Cout);
        fail_count = fail_count + 1;
      end
      $display("");
    end
  endtask
  
  // Main test sequence
  initial begin
    integer i;
    
    $display("=== Starting CLA Adder Tests ===");
    $display("Parameter N = %d", N);
    $display("");
    
    // Initialize counters
    test_count = 0;
    pass_count = 0;
    fail_count = 0;
    
    // Reset sequence
    reset_n = 0;
    A = 0;
    B = 0;
    Cin = 0;
    
    repeat(2) @(posedge clk);
    reset_n = 1; // Note: Following your module's reset logic
    repeat(1) @(posedge clk);
    
    // Run all predefined test patterns
    for (i = 0; i < NUM_TESTS; i = i + 1) begin
      test_single(i);
    end
    
    // Generate some random tests
    $display("=== Running Random Tests ===");
    for (i = 1; i <= 10; i = i + 1) begin
      test_random(i);
    end
    
    // Final results
    $display("=== Test Summary ===");
    $display("Total tests: %d", test_count);
    $display("Passed:      %d", pass_count);
    $display("Failed:      %d", fail_count);
    
    if (fail_count == 0) begin
      $display("*** ALL TESTS PASSED! ***");
    end else begin
      $display("*** %d TESTS FAILED ***", fail_count);
    end
    
    // Wait a few more cycles
    repeat(5) @(posedge clk);
    
    $finish;
  end
  
  // Optional: Dump waveforms
  initial begin
    $dumpfile("cla_adder.vcd");
    $dumpvars(0, CLA_Adder_TB);
  end
  
endmodule