# TrOCR ONNX INT8 - Lightweight OCR Microservice

A lightweight, CPU-optimized FastAPI microservice for Optical Character Recognition (OCR) utilizing **Microsoft's TrOCR** powered by **ONNX Runtime** and **Dynamic INT8 Quantization**. 

Designed specifically for resource-constrained VDS environments (Dockerized, low RAM footprint) to accurately recognize both **handwritten notes/notebooks** and **printed text** (books, magazines, screenshots).

---

## Architecture & Optimizations

- **Base Model:** [`microsoft/trocr-small-handwritten`](https://huggingface.co/microsoft/trocr-small-handwritten) (VisionEncoderDecoder architecture).
- **Format:** ONNX (FP32 encoder + dynamically quantized INT8 merged decoder).
- **Quantization:** ONNX Runtime dynamic quantization (`QInt8` weights, `MatMul` ops only) resulting in a **28% smaller weight size** and faster CPU inference with virtually no loss in CER/WER accuracy.
- **Serving:** FastAPI + Uvicorn with a Singleton pattern (model loaded once into memory on startup) wrapped in a secure Docker container.

---

## Project Structure

```text
├── main.py             # FastAPI application & ONNX inference logic
├── requirements.txt    # Python dependencies
├── Dockerfile          # Optimized container image definition
└── docker-compose.yml  # Docker Compose configuration with RAM limits
