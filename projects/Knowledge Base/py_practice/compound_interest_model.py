import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def your_model(R, T):
    """
    Your model: Total return in % = RT + 0.6×10^(-2)×(RT)^2
    This is a quadratic model: RT + 0.006×(RT)^2
    """
    RT = R * T
    if (RT <= 100):
        return (RT + 0.005 * (RT ** 2))
    else:
        return (RT + 0.006 * (RT ** 2))

def actual_compound_interest(R, T, principal=100):
    """
    Actual compound interest formula: A = P(1 + r)^t
    Total return % = ((A - P) / P) * 100
    """
    r = R / 100  # Convert percentage to decimal
    final_amount = principal * (1 + r) ** T
    total_return_percent = ((final_amount - principal) / principal) * 100
    return total_return_percent

def calculate_error_percentage(predicted, actual):
    """Calculate percentage error"""
    return ((predicted - actual) / actual) * 100

def test_model():
    """Test the model for different interest rates and time periods up to 10 years"""
    
    # Test parameters
    interest_rates = [3, 5, 7, 10, 12, 15]  # Different interest rates in %
    time_periods = range(1, 11)  # 1 to 10 years
    
    results = []
    
    print("COMPOUND INTEREST MODEL TESTING")
    print("=" * 60)
    print(f"Your Model: Total Return % = RT + 0.006×(RT)²")
    print(f"Actual Formula: Total Return % = ((1 + R/100)^T - 1) × 100")
    print("=" * 60)
    
    for R in interest_rates:
        print(f"\nINTEREST RATE: {R}% per annum")
        print("-" * 50)
        print(f"{'Year':<4} {'Your Model':<12} {'Actual':<12} {'Error %':<10}")
        print("-" * 50)
        
        for T in time_periods:
            predicted = your_model(R, T)
            actual = actual_compound_interest(R, T)
            error_pct = calculate_error_percentage(predicted, actual)
            
            results.append({
                'Interest_Rate': R,
                'Time_Years': T,
                'Your_Model_Return': predicted,
                'Actual_Return': actual,
                'Error_Percentage': error_pct
            })
            
            print(f"{T:<4} {predicted:<12.2f} {actual:<12.2f} {error_pct:<10.2f}")
    
    return pd.DataFrame(results)

def analyze_results(df):
    """Analyze and visualize the results"""
    
    print("\n" + "=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)
    
    # Overall statistics
    print(f"Total test cases: {len(df)}")
    print(f"Average absolute error: {abs(df['Error_Percentage']).mean():.2f}%")
    print(f"Maximum error: {df['Error_Percentage'].max():.2f}%")
    print(f"Minimum error: {df['Error_Percentage'].min():.2f}%")
    
    # Error by time period
    print(f"\nError tends to {'increase' if df.groupby('Time_Years')['Error_Percentage'].mean().is_monotonic_increasing else 'vary'} with longer time periods")
    
    # Create visualizations
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Error vs Time for different interest rates
    for rate in df['Interest_Rate'].unique():
        subset = df[df['Interest_Rate'] == rate]
        ax1.plot(subset['Time_Years'], subset['Error_Percentage'], 
                marker='o', label=f'{rate}% p.a.')
    ax1.set_xlabel('Time (Years)')
    ax1.set_ylabel('Error Percentage (%)')
    ax1.set_title('Model Error vs Time Period')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Actual vs Predicted Returns
    ax2.scatter(df['Actual_Return'], df['Your_Model_Return'], 
               c=df['Time_Years'], cmap='viridis', alpha=0.6)
    # Perfect prediction line
    max_val = max(df['Actual_Return'].max(), df['Your_Model_Return'].max())
    ax2.plot([0, max_val], [0, max_val], 'r--', label='Perfect Prediction')
    ax2.set_xlabel('Actual Return (%)')
    ax2.set_ylabel('Your Model Return (%)')
    ax2.set_title('Predicted vs Actual Returns')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Error distribution
    ax3.hist(df['Error_Percentage'], bins=20, edgecolor='black', alpha=0.7)
    ax3.set_xlabel('Error Percentage (%)')
    ax3.set_ylabel('Frequency')
    ax3.set_title('Distribution of Prediction Errors')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Heatmap of errors
    pivot_table = df.pivot(index='Interest_Rate', columns='Time_Years', values='Error_Percentage')
    im = ax4.imshow(pivot_table.values, cmap='RdYlBu_r', aspect='auto')
    ax4.set_xticks(range(len(pivot_table.columns)))
    ax4.set_yticks(range(len(pivot_table.index)))
    ax4.set_xticklabels(pivot_table.columns)
    ax4.set_yticklabels(pivot_table.index)
    ax4.set_xlabel('Time (Years)')
    ax4.set_ylabel('Interest Rate (%)')
    ax4.set_title('Error Heatmap')
    plt.colorbar(im, ax=ax4, label='Error %')
    
    plt.tight_layout()
    plt.show()
    
    return df

# Run the test
if __name__ == "__main__":
    # Test the model
    results_df = test_model()
    
    # Analyze and visualize results
    final_df = analyze_results(results_df)
    
    # Show some specific examples
    print("\n" + "=" * 60)
    print("SPECIFIC EXAMPLES")
    print("=" * 60)
    
    examples = [
        (5, 5),   # 5% for 5 years
        (10, 3),  # 10% for 3 years
        (7, 10),  # 7% for 10 years
        (15, 8),  # 15% for 8 years (higher rate, longer period)
    ]
    
    for R, T in examples:
        predicted = your_model(R, T)
        actual = actual_compound_interest(R, T)
        error = calculate_error_percentage(predicted, actual)
        
        print(f"\n{R}% interest for {T} years:")
        print(f"  Your model predicts: {predicted:.2f}% total return")
        print(f"  Actual compound interest: {actual:.2f}% total return")
        print(f"  Error: {error:.2f}%")
        
        if error > 0:
            print(f"  Your model OVERESTIMATES by {abs(error):.2f}%")
        else:
            print(f"  Your model UNDERESTIMATES by {abs(error):.2f}%")
