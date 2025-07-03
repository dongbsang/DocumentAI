import React, { useState } from "react";
import axios from "axios";

function App() {
  const apiUrl = process.env.REACT_APP_API_BASE_URL;

  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [info, setInfo] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await axios.post(`${apiUrl}/upload`, formData);
    setText(res.data.text);
    setInfo(res.data.info);
  };

  return (
    <div style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h2>Document AI OCR</h2>
      <input
        type="file"
        onChange={e => setFile(e.target.files[0])}
        style={{ marginBottom: 10 }}
      />
      <button onClick={handleUpload}>업로드 및 분석</button>

      <h3>OCR 결과</h3>
      <textarea
        rows={10}
        value={text}
        readOnly
        style={{ width: "100%" }}
      />

      <h3>추출 정보</h3>
      <pre>{JSON.stringify(info, null, 2)}</pre>
    </div>
  );
}

export default App;