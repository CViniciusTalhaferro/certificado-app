import React, { useEffect, useState } from 'react';
import axios from 'axios';

function CertList() {
  const [certificados, setCertificados] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/certificados')
      .then(res => setCertificados(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h2>Certificados Cadastrados</h2>
      <table border="1" cellPadding="10" style={{ width: '100%', textAlign: 'left' }}>
        <thead>
          <tr>
            <th>Empresa</th>
            <th>CNPJ</th>
            <th>Validade</th>
            <th>Dias Restantes</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {certificados.map((c, i) => (
            <tr key={i} style={{ backgroundColor: c.status === 'Vencido' ? '#ffcccc' : c.status === 'Perto de vencer' ? '#fff0b3' : '#ccffcc' }}>
              <td>{c.nome_empresa}</td>
              <td>{c.cnpj}</td>
              <td>{new Date(c.validade).toLocaleDateString()}</td>
              <td>{c.dias_restantes}</td>
              <td>{c.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default CertList;
