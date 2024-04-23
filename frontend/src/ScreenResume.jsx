import React, { useState, useEffect } from "react";
import Aos from "aos";
import "aos/dist/aos.css";
import JobProfile from "./JobProfile";

const ScreenResume = () => {
  useEffect(() => {
    Aos.init({ duration: 2000, once: true });
  }, []);

  const [file, setFile] = useState(null);
  const [parsedjdData, setParsedjdData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
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
    formdata.append("jd", file);

    const requestOptions = {
      method: "POST",
      body: formdata,
      redirect: "follow",
    };

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/jdparser/",
        requestOptions
      );
      const result = await response.json();
      console.log(result.success)
      setParsedjdData(result.sucess); // Update the parsedData state
    } catch (error) {
      console.error(error);
      setError("Error parsing the resume.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="screen">
        <div className="screen_container">
          <h1 data-aos="fade-right">
            Screen Your <span className="gradient-text">Resume</span>
          </h1>
          <div className="screen_container_content" data-aos="fade-left">
            <h1>Job Parser</h1>
            <form onSubmit={handleSubmit}>
              <label htmlFor="job">Upload Job:</label>
              <input
                type="file"
                id="jd"
                accept=".pdf,.doc,.docx"
                onChange={handleFileChange}
              />
              <button type="submit" disabled={loading}>
                Post Job
              </button>
              {loading && <div className="parser_loading"></div>}
              {error && <p>{error}</p>}
            </form>

              {parsedjdData && (
              <div>
                <h2>Parsed Data:</h2>
                <pre>{JSON.stringify(parsedjdData, null, 2)}</pre>
              </div>
            )} 
            
          </div>
        </div>
      </div>
      <JobProfile />
    </>
  );
};
export default ScreenResume;

//   return (
//     <>
//       <div className="screen">
//         <div className="screen_container">
//           <div className="screen_container_content" data-aos="fade-left">
//             <h1>Screen Your Resume</h1>
//             <form onSubmit={handleSubmit}>
//               <textarea
//                 placeholder="Enter The Job Description For Your Role"
//                 value={textAreaValue}
//                 onChange={(e) => setTextAreaValue(e.target.value)}
//               />

//               <div className="submit">
//                 <button type="submit" className="submit-button">
//                   Submit
//                 </button>
//               </div>
//             </form>
//           </div>
//         </div>
//       </div>
//     </>
//   );
// };