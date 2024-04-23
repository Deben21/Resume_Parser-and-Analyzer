import React, { useState, useEffect } from "react";
import Aos from "aos";
import "aos/dist/aos.css";
import ResumeProfile from "./ResumeProfile";

const Parser = () => {
  const [file, setFile] = useState(null);
  const [parsedData, setParsedData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    Aos.init({ duration: 2000, once: true });
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null); // Clear previous errors
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    if (!file) {
      setError("Please select a file.");
      setLoading(false);
      return;
    }

    const formdata = new FormData();
    formdata.append("resume", file);

    const requestOptions = {
      method: "POST",
      body: formdata,
      redirect: "follow",
    };

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/resumeparser/",
        requestOptions
      );
      const result = await response.json();
      setParsedData(result.parsed_data); // Update the parsedData state
    } catch (error) {
      console.error(error);
      setError("Error parsing the resume.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="parser">
        <div className="parsing_container">
          <h1 data-aos="fade-right">
            Start Using Our <span className="gradient-text">Service</span>
          </h1>
          <div className="parsing_container_content" data-aos="fade-left">
            <h1>Resume Parser</h1>
            <form onSubmit={handleSubmit}>
              <label htmlFor="resume">Upload Resume:</label>
              <input
                type="file"
                id="resume"
                accept=".pdf,.doc,.docx"
                onChange={handleFileChange}
              />
              <button type="submit" disabled={loading}>
                Parse Resume
              </button>
              {loading && <div className="parser_loading"></div>}
              {error && <p>{error}</p>}
            </form>
            {parsedData && (
              <div>
                <h2>Parsed Data:</h2>
                <pre>{JSON.stringify(parsedData, null, 2)}</pre>
              </div>
            )}
          </div>
        </div>
      </div>
      <ResumeProfile />
    </>
  );
};

export default Parser;
