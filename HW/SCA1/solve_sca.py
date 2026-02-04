import numpy as np
from tqdm import tqdm

sbox = (
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
)

HW = [bin(x).count("1") for x in range(256)]

def load_data():
    print("Loading data...")
    data = np.load('solve/sca1.npz')
    traces = data['traces']
    plaintexts = data['plaintexts']
    print("Data loaded.")
    return traces, plaintexts

def cpa(traces, plaintexts, num_traces=1000):
    traces = traces[:num_traces]
    plaintexts = plaintexts[:num_traces]
    
    num_points = traces.shape[1]
    key_length = 16
    recovered_key = []

    print(f"Running CPA with {num_traces} traces...")

    # Pre-calculate mean of traces for correlation
    # We can do this efficiently
    # Correlation(X, Y) = E[(X - E[X]) * (Y - E[Y])] / (std(X) * std(Y))
    
    # We will process byte by byte
    for byte_idx in range(key_length):
        print(f"Analyzing byte {byte_idx}...")
        max_cpa = -1
        best_guess = -1
        
        # Consider all key candidates
        # To speed up, we can vectorize over traces
        
        pt_byte = plaintexts[:, byte_idx]
        
        # Hypothetical intermediate values for all 256 key candidates
        # Shape: (256, num_traces)
        # However, for huge number of traces, (256, 100000) might be big for memory (25MB * 256 is huge?)
        # 100000 floats is 800KB. 256 * 800KB is ~200MB. That fits in memory easily.
        
        print("Creating hypothesis matrix...")
        hyp_power = np.zeros((256, num_traces))
        for k in range(256):
            val = np.bitwise_xor(pt_byte, k)
            # Apply SBox
            val = np.array([sbox[v] for v in val])
            # Hamming Weight
            hyp_power[k] = np.array([HW[v] for v in val])
            
        print("Calculating correlations...")
        
        # Correlation requires columns of traces and rows of hyp_power
        # Traces: (num_traces, num_points)
        # Hyp_power: (256, num_traces)
        
        # Let's clean up calculation using numpy
        # corr(X, Y) where X is (N, T) and Y is (K, N)?? No.
        # We want corr between one column of traces (N,) and one row of hyp_power (N,)
        
        # Let's normalize traces first to speed up
        # Subtract mean, divide by std
        t_mean = np.mean(traces, axis=0) # (num_points,)
        t_std = np.std(traces, axis=0)
        t_norm = (traces - t_mean) # (num_traces, num_points)
        # Handle zero std? hopefully not an issue in real traces
        
        # Normalize hypothesis
        h_mean = np.mean(hyp_power, axis=1, keepdims=True) # (256, 1)
        h_std = np.std(hyp_power, axis=1, keepdims=True) # (256, 1)
        h_norm = (hyp_power - h_mean) # (256, num_traces)

        # Correlation matrix: (256, num_points)
        # Dot product: (256, num_traces) @ (num_traces, num_points) -> (256, num_points)
        # The result must be divided by (N * t_std * h_std)
        # Wait, correlation coefficient is usually just dot(norm_x, norm_y) / N if both are standard normal
        # Here we didn't divide by std yet.
        
        numerator = np.dot(h_norm, t_norm) # (256, num_points)
        denominator = num_traces * np.dot(h_std, t_std.reshape(1, -1)) # (256, num_points)
        
        # Avoid division by zero
        # denominator[denominator == 0] = 1e-10 
        
        correlations = numerator / denominator
        correlations = np.abs(correlations)
        
        # Find max correlation for each key candidate across all time points
        max_corrs = np.max(correlations, axis=1) # (256,)
        
        best_guess = np.argmax(max_corrs)
        max_cpa = max_corrs[best_guess]
        
        recovered_key.append(best_guess)
        print(f"Byte {byte_idx} best guess: 0x{best_guess:02x} (corr: {max_cpa:.4f})")
    
    return recovered_key 

if __name__ == "__main__":
    traces, plaintexts = load_data()
    # Try with 5000 traces first
    key = cpa(traces, plaintexts, num_traces=20000)
    
    print(" Recovered Key: ", end="")
    print(', '.join([f"0x{k:02x}" for k in key]))
    
    # Format as requested
    hex_key = "".join([f"{k:02x}" for k in key])
    print(f"Flag: 0xL4ugh{{{hex_key}}}")
