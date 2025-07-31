import { useState } from "react"; //useState: React hook to manage local state (like variables)
import axios from "axios"; //axios: For sending HTTP requests

function HumanDetector() {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [resultImageUrl, setResultImageUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [humanCount, setHumanCount] = useState(null);  

  const onFileChange = (e) => {
    setUploadedImage(e.target.files[0]);
    setResultImageUrl(null);
    setHumanCount(null);
    setErrorMsg("");
  };

  const onDetectClick = async () => {
    if (!uploadedImage) {
      setErrorMsg("Please select an image first.");
      return;
    }
    const formData = new FormData(); //FormData Prepares image to be sent as multipart/form-data 
    formData.append("file", uploadedImage);

    try {
      setIsLoading(true);
      const response = await axios.post("http://localhost:8000/detect/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        responseType: "blob",
      });

      //Getting human count from header
      const count = response.headers["x-human-count"];
      setHumanCount(parseInt(count,10) || 0);

      const imageBlob = new Blob([response.data], { type: "image/jpeg" });
      const imageUrl = URL.createObjectURL(imageBlob);
      setResultImageUrl(imageUrl);
      setErrorMsg("");
    } catch (err) {
      setErrorMsg("Detection failed. Please try again.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "30px" }}>
      <h1 style={{ color: "#fff" }}>Human Detector</h1>

      <input type="file" accept="image/*" onChange={onFileChange} />
      <br /><br />

      <button onClick={onDetectClick} style={{ padding: "10px 20px" }}>
        {isLoading ? "Processing..." : "Detect"}
      </button>

      {errorMsg && <p style={{ color: "red" }}>{errorMsg}</p>}

      {/* Human detection count */}
      {humanCount !== null && !isLoading && !errorMsg && (
        <p style={{ color: "white", fontWeight: "bold" }}>
          {humanCount > 0
            ? ` Detected ${humanCount} human${humanCount > 1 ? "s" : ""}`
            : " No human detected"}
        </p>
      )}

      {resultImageUrl && (
        <div>
          <h3 style={{ color: "white" }}>Detection Result:</h3>
          <img src={resultImageUrl} alt="Detected Output" style={{ maxWidth: "80%" }} />
        </div>
      )}
    </div>
  );
}

export default HumanDetector;