import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def your_model(R, T):
    """
    Your model: Total return in % = RT + coefficient×(RT)^2
    Coefficient is 0.005 for RT <= 100, otherwise 0.006.
    """
    RT = R * T
    c = 0.005 if RT <= 100 else 0.006
    return RT + c * (RT ** 2), RT

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
    interest_rates = [3, 5, 7, 10, 12, 15]  # Different interest rates in %
    time_periods = range(1, 11)  # 1 to 10 years
    
    records = []
    for R in interest_rates:
        for T in time_periods:
            pred, RT = your_model(R, T)
            act = actual_compound_interest(R, T)
            err_pct = calculate_error_percentage(pred, act)
            records.append({
                'Interest_Rate': R,
                'Time_Years': T,
                'RT': RT,
                'Model_Return': pred,
                'Actual_Return': act,
                'Error_Percentage': err_pct
            })
    return pd.DataFrame(records)

def analyze_results(df):
    """Analyze and visualize the results"""
    print("ANALYSIS SUMMARY")
    print("================")
    print(f"Total test cases: {len(df)}")
    print(f"Average absolute error: {abs(df['Error_Percentage']).mean():.2f}%")
    print(f"Max error: {df['Error_Percentage'].max():.2f}%")
    print(f"Min error: {df['Error_Percentage'].min():.2f}%")
    
    # 2x2 plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Error vs Time
    for rate in df['Interest_Rate'].unique():
        subset = df[df['Interest_Rate'] == rate]
        ax1.plot(subset['Time_Years'], subset['Error_Percentage'], marker='o', label=f'{rate}%')
    ax1.set_xlabel('Time (Years)')
    ax1.set_ylabel('Error %')
    ax1.set_title('Error vs Time Period')
    ax1.legend(); ax1.grid(alpha=0.3)
    
    # Actual vs Predicted
    ax2.scatter(df['Actual_Return'], df['Model_Return'], c=df['Time_Years'], cmap='viridis', alpha=0.6)
    maxv = max(df['Actual_Return'].max(), df['Model_Return'].max())
    ax2.plot([0, maxv], [0, maxv], 'r--')
    ax2.set_xlabel('Actual Return %'); ax2.set_ylabel('Model Return %')
    ax2.set_title('Predicted vs Actual'); ax2.grid(alpha=0.3)
    
    # Error distribution
    ax3.hist(df['Error_Percentage'], bins=20, edgecolor='black', alpha=0.7)
    ax3.set_xlabel('Error %'); ax3.set_ylabel('Frequency')
    ax3.set_title('Error Distribution'); ax3.grid(alpha=0.3)
    
    # Heatmap
    pivot = df.pivot(index='Interest_Rate', columns='Time_Years', values='Error_Percentage')
    im = ax4.imshow(pivot.values, cmap='RdYlBu_r', aspect='auto')
    ax4.set_xticks(range(len(pivot.columns))); ax4.set_yticks(range(len(pivot.index)))
    ax4.set_xticklabels(pivot.columns); ax4.set_yticklabels(pivot.index)
    ax4.set_xlabel('Time (Years)'); ax4.set_ylabel('Interest Rate (%)')
    ax4.set_title('Error Heatmap')
    plt.colorbar(im, ax=ax4, label='Error %')
    
    plt.tight_layout()
    plt.show()
    
    # New: Error vs RT product
    plt.figure(figsize=(8, 6))
    plt.scatter(df['RT'], df['Error_Percentage'], alpha=0.7)
    plt.xlabel('R × T')
    plt.ylabel('Error Percentage (%)')
    plt.title('Error vs RT Product')
    plt.grid(alpha=0.3)
    plt.show()

if __name__ == "__main__":
    results_df = test_model()
    analyze_results(results_df)

