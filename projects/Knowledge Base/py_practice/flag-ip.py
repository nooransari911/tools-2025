from collections import defaultdict
import json





def detect_ddos(logs, T, K):
    """
    Detects DDoS attacks from a log of requests (CORRECTED).

    Args:
        logs: A list of tuples, where each tuple is (timestamp, ip_address).
        T: The time window in seconds.
        K: The maximum allowed requests within the time window.

    Returns:
        A sorted list of IP addresses that should be flagged, or an empty list
        if no threats are detected. Returns ["No Threats Detected"] as a list.
    """
    ip_timestamps = defaultdict(list)  # Store timestamps for each IP
    flagged_ips = set()

    # 1. Build the complete timestamp list for EACH IP.
    for timestamp, ip in logs:
        ip_timestamps[ip].append(timestamp)

    # 2. Process EACH IP's timestamps to check for DDoS.
    for ip, timestamps in ip_timestamps.items():
        # Iterate through the timestamps for the current IP.
        for i in range(len(timestamps)):
            # Calculate the window start for the *current* timestamp.
            window_start = timestamps[i] - T

            # Count requests within the current window.
            count = 0
            for j in range(i, -1, -1):  # Iterate backwards from current timestamp.
                if timestamps[j] > window_start:
                    count += 1
                else:
                    break # Optimization: Stop when outside the window.

            if count > K:
                flagged_ips.add(ip)
                break  # Once flagged, no need to check further for this IP.


    if not flagged_ips:
        return ["No Threats Detected"]
    else:
        return sorted(list(flagged_ips))


def main():
    """Reads input from stdin and calls the detect_ddos function."""
    N, T, K = map(int, input().split())
    logs = []

    windows = defaultdict(lambda: defaultdict(int))  # Store timestamps for each IP


    for _ in range(N):
        timestamp, ip_address = input().split()
        logs.append((int(timestamp), ip_address))
        windows [int (timestamp) // T] [ip_address] += 1

    result = detect_ddos(logs, T, K)
    print(" ".join(result))
    print ("\n\ndict:")
    print(json.dumps(windows, default=str, indent=4))


    

if __name__ == "__main__":
    main()
