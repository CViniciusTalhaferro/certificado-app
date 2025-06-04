# main.py (FastAPI + Scheduler + Email)
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.background import BackgroundTasks
from pydantic import BaseModel
from datetime import datetime, timedelta
import uvicorn
import cert_utils
import os
import shutil
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "./certificados"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mock database
db = []

class Certificado(BaseModel):
    nome_empresa: str
    cnpj: str
    validade: datetime
    senha: str
    email: str

@app.post("/upload_certificado")
async def upload_certificado(
    file: UploadFile,
    senha: str = Form(...),
    email: str = Form(...),
):
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        nome_empresa, cnpj, validade = cert_utils.ler_certificado(filepath, senha)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    cert_data = {
        "nome_empresa": nome_empresa,
        "cnpj": cnpj,
        "validade": validade,
        "senha": senha,  # Criptografar em versão real
        "email": email,
        "avisos_enviados": 0
    }
    db.append(cert_data)
    return JSONResponse(content=cert_data)

@app.get("/certificados")
def listar_certificados():
    hoje = datetime.now()
    for cert in db:
        dias_restantes = (cert["validade"] - hoje).days
        cert["dias_restantes"] = dias_restantes
        if dias_restantes <= 0:
            cert["status"] = "Vencido"
        elif dias_restantes <= 30:
            cert["status"] = "Perto de vencer"
        else:
            cert["status"] = "Válido"
    return db

# Email configuration (substitua com seu servidor real)
EMAIL_HOST = "email-ssl.com.br"
EMAIL_PORT = 587
EMAIL_USER = "contato@talhaferro.cnt.br"
EMAIL_PASS = "Cont@t0T@lhaferro*2024+"

def enviar_email(destinatario, assunto, corpo):
    msg = MIMEText(corpo, "html")
    msg["Subject"] = assunto
    msg["From"] = EMAIL_USER
    msg["To"] = destinatario

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, destinatario, msg.as_string())

def verificar_alertas():
    hoje = datetime.now()
    for cert in db:
        dias_restantes = (cert["validade"] - hoje).days
        if dias_restantes <= 30:
            avisos = cert.get("avisos_enviados", 0)
            if dias_restantes == 30 or dias_restantes in [20, 10, 0]:
                if avisos < 4:
                    corpo = f"<b>Aviso:</b><br>O certificado da empresa <b>{cert['nome_empresa']}</b> (CNPJ {cert['cnpj']}) vence em <b>{dias_restantes} dias</b>."
                    try:
                        enviar_email(cert["email"], "[Alerta] Vencimento de Certificado Digital", corpo)
                        cert["avisos_enviados"] = avisos + 1
                    except Exception as e:
                        print(f"Erro ao enviar e-mail: {e}")

# Agendamento diário
scheduler = BackgroundScheduler()
scheduler.add_job(verificar_alertas, "interval", hours=24)
scheduler.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
