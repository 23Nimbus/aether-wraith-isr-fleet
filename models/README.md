Models
======

This directory is intended to store trained machine learning models used by
the Æther Wraith AI overlay.  The anomaly detection classifier referenced
in `agents/aether_ai.py` should be serialised as `anomaly_classifier.joblib` and
placed here.  Because binary model artefacts can be large and may contain
sensitive information, `models/*.joblib` is ignored by Git via `.gitignore`.

To obtain a working model you can train your own classifier and drop the
resulting Joblib file into this directory.