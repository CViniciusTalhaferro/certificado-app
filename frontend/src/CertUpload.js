import React, { useState } from 'react';
import axios from 'axios';

function CertUpload() {
  const [file, setFile] = useState(null);
  const [senha, setSenha] = useState('');
  const [email, setEmail] = useState('');
  const [mensagem, setMensagem] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !senha || !email) return alert('Preencha todos os campos');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('senha', senha);
    formData.append('email', email);

    try {
      const res = await axios.post('http://localhost:8000/upload_certificado', formData);
      setMensagem('Certificado cadastrado com sucesso!');
    } catch (err) {
      setMensagem('Erro ao cadastrar: ' + err.response.data.detail);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <h2>Cadastro de Certificado</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <input type="password" placeholder="Senha do certificado" value={senha} onChange={(e) => setSenha(e.target.value)} />
      <input type="email" placeholder="Email para alertas" value={email} onChange={(e) => setEmail(e.target.value)} />
      <button type="submit">Cadastrar</button>
      {mensagem && <p>{mensagem}</p>}
    </form>
  );
}

export default CertUpload;
