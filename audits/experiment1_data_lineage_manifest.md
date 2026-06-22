# Experiment 1 Data Lineage Manifest

SHA256 hashes were computed over raw file bytes at audit time.

| File | SHA256 |
|---|---|
| `data/experiment1.csv` | `98e8beec4938f61b889d8bf7c83a0a37e43512c73e4ce4501ec6ee4afeb42d2c` |
| `data/experiment1_trajectory_rater_responses_gemini_3_1_flash_lite.md` | `9789514385d2bbe0cb1c688558b943326513eec3c0e0bf3d083c7a876111e888` |
| `data/experiment1_snapshot_rater_responses_gemini_3_1_flash_lite.md` | `945104fffb51f744f76e6236637f8cc8faa0c21c04043d4edf63ad1a9aa6d69b` |
| `data/experiment1_full_results_gemini_3_1_flash_lite.csv` | `bb9c5c9ecc2e2cf9ac6444691f788140d428b1c478ab8fb4e68902d135fe00ba` |
| `data/experiment1_final_metrics_gemini_3_1_flash_lite.json` | `44914d5d46fbcb56a8d4d583e64bc1d5503f57e9f69580bba8b9d11b3b7cc9c8` |
| `data/experiment1_final_summary_gemini_3_1_flash_lite.md` | `c165f86e59672ea03d486d119ef0a4f138e58d84779a9ad3d3e0697421b0ba4d` |
| `prompts/blind_rater_prompt.md` | `cf7e3b8dafbb82a2669f17e2038b5b3662a1b5e37480f8905483495590275fe7` |
| `prompts/snapshot_rater_prompt.md` | `902b3f271d167e2caf91e733202650bc76fdadbca9a1bece9140d86011cebd06` |
| `rubric.md` | `debbdc85d16e65750579b685ecc998571b93ed35b06d07a9c5c99fbe9b05802f` |
| `run_gemini_trajectory_rater_experiment1_flash_lite.py` | `82152dffa594d67ce146ebd027074289d58e97c417f9634474c3d0d793f4fa3c` |
| `run_gemini_snapshot_rater_experiment1_flash_lite.py` | `5f73569dafba5bbe5461f6a1b12fbd5ca66c86a9ca1828d443d0a86eda3d9dfb` |
| `integrate_flash_lite_trajectory_rater.py` | `4090feef9dd095fbdbe3de1a37cde0963fa8671519d5664b366a2d55194e4639` |
| `integrate_flash_lite_snapshot_rater.py` | `0110b90fe6bbeaca310d308674df16eb655c0ff5cf1af562fa91596a0a0f42c6` |
| `scripts/analyze_experiment1_trajectory_flash_lite.py` | `44ae2c432792091cac90bfc37d4c00d25b7ef1b3f6713183b357283d0ee0eb0c` |
| `scripts/analyze_experiment1_full_flash_lite.py` | `2084650c8d984ecccc768f61f1c588f1fc5d68dee6b918123af4eb35baa9120f` |
| `scripts/audit_experiment1_robustness.py` | `58cfb9cf531112046b98613e7487ec4d7c559893ed0f7677a509a1d48f6a017a` |

## Local Derivation Chain

`experiment1.csv` + trajectory ledger -> trajectory integration/analysis -> snapshot ledger + snapshot integration -> full analysis -> robustness audit.
