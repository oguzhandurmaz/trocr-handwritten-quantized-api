# TrOCR ONNX INT8 - Lightweight OCR Microservice

A lightweight, CPU-optimized FastAPI microservice for Optical Character Recognition (OCR) utilizing **Microsoft's TrOCR** powered by **ONNX Runtime** and **Dynamic INT8 Quantization**. 

Designed specifically for resource-constrained VDS environments (Dockerized, low RAM footprint) to accurately recognize both **handwritten notes/notebooks** and **printed text** (books, magazines, screenshots).

---

## GitHub Repository Description (About)
> A lightweight, CPU-optimized FastAPI & Docker OCR microservice powered by Microsoft's TrOCR with ONNX Runtime and INT8 dynamic quantization for handwritten and printed text.

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
```

---

## Quick Start (Docker Deployment)

### 1. Clone the Repository
```bash
git clone https://github.com/oguzhandurmaz/trocr-onnx-ocr.git
cd trocr-onnx-ocr
```

### 2. Configure Docker Compose
Ensure your `docker-compose.yml` is configured (with memory limits to protect your server resources):
```yaml
version: '3.8'

services:
  trocr-onnx-ocr:
    build: .
    container_name: trocr-onnx-ocr-api
    restart: unless-stopped
    ports:
      - "8000:8000"
    deploy:
      resources:
        limits:
          memory: 1G
    environment:
      - PYTHONUNBUFFERED=1
```

### 3. Build and Run
```bash
docker compose up -d --build
```

The service will automatically download the optimized model repository (`oguzhandurmaz/trocr-small-handwritten-onnx-int8`) from Hugging Face on the first startup.

---

## API Usage

### Health Check
- **Endpoint:** `GET /health`
- **Response:** `{"status": "healthy"}`

### Run OCR
- **Endpoint:** `POST /ocr`
- **Payload:** `multipart/form-data` with key `file` (Image file: PNG, JPG, JPEG)

#### Example cURL Request:
```bash
curl -X 'POST' \
  'http://localhost:8000/ocr' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@recipe_note.jpg'
```

#### Example JSON Response:
```json
{
  "status": "success",
  "extracted_text": "1 cay kasigi tuz ekleyip iyice karistirin."
}
```

---

## n8n Integration

This microservice can be seamlessly integrated into workflow automation tools like **n8n** using an **HTTP Request Node**:
- **Method:** `POST`
- **URL:** `http://trocr-onnx-ocr-api:8000/ocr` (or your VDS IP/domain)
- **Body Content Type:** `Multipart/Form-Data`
- **Parameter:** `file` -> Binary file from previous nodes (`{{ $binary.data }}`)

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
