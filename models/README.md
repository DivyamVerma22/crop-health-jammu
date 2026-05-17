# Models

Trained model artefacts live here at runtime, but they are **not** committed to Git because they are large.

After installation, populate this directory either through Git LFS or by running:

```bash
python scripts/download_model.py
```

The expected artefact is `Best_model.pkl` — the Random Forest selected in notebook 3.
