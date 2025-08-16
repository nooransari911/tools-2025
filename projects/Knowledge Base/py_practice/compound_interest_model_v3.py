import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def your_model(R, T):
    """
    Quadratic approximation:
      Return% ≈ RT + c*(RT)^2
    where c = 0.005 for RT ≤ 100, else 0.006.
    """
    RT = R * T
    c = 0.005 if RT <= 100 else 0.006
    return RT + c * (RT ** 2)

def actual_compound_interest(R, T, principal=100):
    """
    Exact compound interest:
      A = P * (1 + r)^T
      Return% = ((A - P) / P) * 100
    """
    r = R / 100
    final_amount = principal * (1 + r) ** T
    return (final_amount - principal) / principal * 100

def calculate_error_percentage(predicted, actual):
    """
    Growth‐factor relative error:
      pred_factor = 1 + predicted/100
      act_factor  = 1 + actual/100
      error% = (pred_factor/act_factor - 1) * 100
    """
    pred_factor = 1 + predicted / 100
    act_factor  = 1 + actual    / 100
    return (pred_factor / act_factor - 1) * 100

def test_model(interest_rates, time_periods):
    """
    Build DataFrame of model vs actual returns and error.
    """
    records = []
    for R in interest_rates:
        for T in time_periods:
            pred = your_model(R, T)
            act  = actual_compound_interest(R, T)
            err  = calculate_error_percentage(pred, act)
            records.append({
                'Interest_Rate': R,
                'Time_Years': T,
                'RT': R * T,
                'Model_Return%': pred,
                'Actual_Return%': act,
                'Error%': err
            })
    return pd.DataFrame.from_records(records)

def analyze_results(df):
    """
    Print summary statistics and show four plots:
      1. Error vs Time for each rate
      2. Error distribution
      3. Error heatmap
      4. Error vs RT product
    """
    print("\nANALYSIS SUMMARY")
    print("================")
    print(f"Total cases: {len(df)}")
    print(f"Average abs error: {df['Error%'].abs().mean():.2f}%")
    print(f"Max error: {df['Error%'].max():.2f}%")
    print(f"Min error: {df['Error%'].min():.2f}%\n")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    ax1, ax2, ax3, ax4 = axes.flatten()
    
    # 1) Error vs Time
    for rate in sorted(df['Interest_Rate'].unique()):
        subset = df[df['Interest_Rate'] == rate]
        ax1.plot(subset['Time_Years'], subset['Error%'], marker='o', label=f'{rate}%')
    ax1.set_xlabel('Time (Years)')
    ax1.set_ylabel('Error (%)')
    ax1.set_title('Error vs Time Period')
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # 2) Error distribution
    ax2.hist(df['Error%'], bins=20, edgecolor='black')
    ax2.set_xlabel('Error (%)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of Relative Errors')
    ax2.grid(alpha=0.3)
    
    # 3) Error heatmap
    pivot = df.pivot(index='Interest_Rate', columns='Time_Years', values='Error%')
    im = ax3.imshow(pivot, aspect='auto', cmap='RdYlBu_r')
    ax3.set_xticks(np.arange(pivot.shape[1]))
    ax3.set_yticks(np.arange(pivot.shape[0]))
    ax3.set_xticklabels(pivot.columns)
    ax3.set_yticklabels(pivot.index)
    ax3.set_xlabel('Time (Years)')
    ax3.set_ylabel('Interest Rate (%)')
    ax3.set_title('Error Heatmap')
    fig.colorbar(im, ax=ax3, label='Error (%)')
    
    # 4) Error vs RT product
    ax4.scatter(df['RT'], df['Error%'], alpha=0.7, marker='x')
    ax4.set_xlabel('R × T')
    ax4.set_ylabel('Error (%)')
    ax4.set_title('Error vs RT Product')
    ax4.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    rates = [3, 5, 7, 10, 12, 15]
    years = range(1, 11)
    
    df_results = test_model(rates, years)
    analyze_results(df_results)

