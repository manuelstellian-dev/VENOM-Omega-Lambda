# VENOM Model Files

This directory contains TensorFlow Lite model files for the VENOM system.

## Required Models

The following models are required for full functionality:

### omega_model.tflite
- **Purpose**: Primary LLM model for Ω-AIOS layer
- **Size**: ~500MB - 2GB
- **Format**: TensorFlow Lite
- **Quantization**: INT8 or FP16 recommended for mobile

### vision_model.tflite
- **Purpose**: Vision processing for multimodal input
- **Size**: ~100MB - 500MB
- **Format**: TensorFlow Lite

### voice_model.tflite
- **Purpose**: Speech recognition and synthesis
- **Size**: ~50MB - 200MB
- **Format**: TensorFlow Lite

## Obtaining Models

Due to size constraints, model files are not included in this repository.

### Options:

1. **Download Pre-trained Models**
   - Visit the VENOM releases page
   - Download model bundles
   - Extract to this directory

2. **Train Your Own**
   - Use the training scripts in `scripts/train/`
   - Export to TensorFlow Lite format
   - Place in this directory

3. **Use Git LFS** (if configured)
   ```bash
   git lfs pull
   ```

## Model Placement

Place downloaded `.tflite` files directly in this directory:

```
models/
├── omega_model.tflite
├── vision_model.tflite
├── voice_model.tflite
└── README.md (this file)
```

## Git LFS Tracking

This repository is configured to track `.tflite` files with Git LFS.
See `.gitattributes` for configuration.

## Fallback Behavior

If models are not present, the system will:
- Use stub responses for LLM queries
- Log warnings about missing models
- Continue operating in reduced functionality mode

## Security Note

**Never commit unencrypted proprietary or sensitive model files.**
Use model encryption or access control as appropriate.
