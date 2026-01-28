import numpy as np
import h5py
import soundfile as sf
import os

sofa_path = "D1_48K_24bit_0.3s_FIR_SOFA.sofa"
output_dir = "./safe_wavs"

# Format: "Filename": [Azimuth, Elevation]
# SADIE II usually has elevations at 30, 60, 90 (Zenith)
# target_angles = {
#     # Bed Layer (Elevation 0)
#     "FL_30":   [30, 0],
#     "FR_330":  [330, 0],
#     "FC_0":    [0, 0],
#     "SL_90":   [90, 0],
#     "SR_270":  [270, 0],
#     "BL_150":  [150, 0],
#     "BR_210":  [210, 0],
#
#     # Height Layer (Elevation 45 or 60 usually works best)
#     # 90 deg Azimuth (Left) + 45 deg Up
#     "TopL_45": [90, 45],
#     # 270 deg Azimuth (Right) + 45 deg Up
#     "TopR_45": [270, 45]
# }

target_angles = {
    # Center is perfect at 0,0
    "FC_0":    [0, 0],

    # Use 45 instead of 30 for a wider, more cinematic soundstage
    "FL_45":   [45, 0],
    "FR_315":  [315, 0],

    # Side Surrounds are perfect at 90/270
    "SL_90":   [90, 0],
    "SR_270":  [270, 0],

    # Back Surrounds - 135/225 are the standard 'Back' positions
    "BL_135":  [135, 0],
    "BR_225":  [225, 0],

    # Heights - Indices 16 and 40 in your list are perfect matches
    "TopL_90": [90, 45],
    "TopR_270": [270, 45]
}


def extract():
    try:
        with h5py.File(sofa_path, 'r') as f:
            source_pos = f['SourcePosition'][:]
            ir_data = f['Data.IR'][:]

            # Create lists for easier searching
            # SourcePosition is [Azimuth, Elevation, Radius]
            azimuths = source_pos[:, 0]
            elevations = source_pos[:, 1]

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            for name, (t_azi, t_ele) in target_angles.items():
                # Find best match for BOTH Azimuth and Elevation
                # We calculate "distance" in 2D space to find nearest point
                dist = np.sqrt((azimuths - t_azi)**2 + (elevations - t_ele)**2)
                idx = dist.argmin()

                real_azi = azimuths[idx]
                real_ele = elevations[idx]

                raw_audio = ir_data[idx, :, :].T

                # Normalize
                peak = np.max(np.abs(raw_audio))
                if peak > 0:
                    normalized = (raw_audio / peak) * 0.95
                    filename = f"{output_dir}/{name}.wav"
                    sf.write(filename, normalized, 48000, subtype='FLOAT')
                    print(f"Saved {name}: Target[{t_azi}, {t_ele}] -> Found[{real_azi:.1f}, {real_ele:.1f}]")
                else:
                    print(f"Skipping {name} (Silent)")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract()
