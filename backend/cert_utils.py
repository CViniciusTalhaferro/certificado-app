from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def ler_certificado(caminho_arquivo, senha):
    with open(caminho_arquivo, 'rb') as f:
        pfx_data = f.read()

    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
        pfx_data, senha.encode(), backend=default_backend()
    )

    if not certificate:
        raise ValueError("Certificado não encontrado no arquivo.")

    subject = certificate.subject
    nome_empresa = subject.get_attributes_for_oid(x509.NameOID.ORGANIZATION_NAME)[0].value
    cnpj_attr = subject.get_attributes_for_oid(x509.ObjectIdentifier("2.16.76.1.3.3"))
    cnpj = cnpj_attr[0].value if cnpj_attr else "CNPJ não encontrado"

    validade = certificate.not_valid_after
    return nome_empresa, cnpj, validade
