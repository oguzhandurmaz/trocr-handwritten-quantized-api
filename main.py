from fastapi import FastAPI, UploadFile, File, HTTPException
from optimum.onnxruntime import ORTModelForVision2Seq
from transformers import TrOCRProcessor
from PIL import Image
import io

app = FastAPI()

# Hugging Face üzerindeki optimize edilmiş repository'miz
REPO_ID = "oguzhandurmaz/trocr-small-handwritten-onnx-int8"

print("INT8 Decoder Quantized TrOCR modeli Hugging Face'den yükleniyor...")
processor = TrOCRProcessor.from_pretrained(REPO_ID)
model = ORTModelForVision2Seq.from_pretrained(REPO_ID)
print("Model başarıyla yüklendi ve çıkarım için hazır!")

@app.post("/ocr")
async def run_ocr(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Görseli modelin beklediği formata getirelim
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        
        # ONNX Runtime üzerinden hızlı CPU çıkarımı
        generated_ids = model.generate(pixel_values)
        extracted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return {
            "status": "success",
            "extracted_text": extracted_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}
