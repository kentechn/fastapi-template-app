#!/bin/bash
python -m uvicorn src.main:app --host 0.0.0.0 --log-level warning