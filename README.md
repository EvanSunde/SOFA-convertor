# SOFA to WAV BRIR Extractor

A specialized Python utility for extracting discrete Binaural Room Impulse Response (BRIR) or any SOFA files from standard `.sofa` containers.

### WHY ?

This tool was built to solve a specific performance bottleneck in real-time spatial audio rendering.

Raw `.sofa` files often contain thousands of measurement points and can be computationally expensive to parse and query during runtime. For high-performance audio engines (such as WebAudio or real-time C++ convolution), using a full SOFA loader introduces unnecessary overhead.

**The goal of this project is to pre-bake the spatial data:**

* **Reduce Latency:** By converting complex SOFA lookups into simple static `.wav` files.
* **Optimize Processing:** Targeted for use with ~16k sample length kernels (or similar short IRs) to ensure zero-delay convolution in real-time applications.
* **Simplify Implementation:** Allows developers to use standard convolution reverbs instead of specialized SOFA decoders.

### HOW ?

1. **Parses SOFA Containers:** Reads standard AES69-2015 `.sofa` files (commonly used for HRTF/BRIR datasets like SADIE II).
2. **Nearest-Neighbor Mapping:** robustly identifies the correct Head-Related Transfer Function (HRTF) measurements for standard surround sound speaker positions (5.1, 7.1, etc.).
* *Note: This uses Euclidean distance to handle floating-point inaccuracies in metadata, ensuring the closest valid measurement is found without interpolation artifacts.*


3. **Normalization:** Auto-scales audio to prevent clipping while maximizing dynamic range (default target: -0.5 dB).
4. **Export:** Saves individual channels as high-quality `32-bit Float` WAV files, ready for immediate use in audio engines.

### 🛠️ Prerequisites

You need Python installed, along with the following dependencies:

```bash
pip install numpy h5py soundfile

```

### WAY TO USE

1. Place your `.sofa` file in the project directory (e.g., `D1_48K_24bit_0.3s_FIR_SOFA.sofa`).
2. Update the `sofa_path` variable in `main.py` if your filename differs.
3. Run the script:

```bash
python main.py

```

4. The extracted impulse responses will appear in the `./safe_wavs` folder.

### Configuration

You can customize the virtual speaker layout by modifying the `target_angles` dictionary in the script. The default configuration is optimized for a cinematic **7.1.2** layout:

```python
target_angles = {
    # Standard Plane (Elevation 0)
    "FC_0":    [0, 0],   # Front Center
    "FL_45":   [45, 0],  # Front Left (Widened for cinema)
    "FR_315":  [315, 0], # Front Right
    "SL_90":   [90, 0],  # Side Left
    "SR_270":  [270, 0], # Side Right
    "BL_135":  [135, 0], # Back Left
    "BR_225":  [225, 0], # Back Right

    # Height Channels (Elevation 45)
    "TopL_90": [90, 45],
    "TopR_270": [270, 45]
}

```
