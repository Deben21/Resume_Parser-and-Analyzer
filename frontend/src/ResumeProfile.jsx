import React, { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faEnvelope,
  faLocationDot,
  faGraduationCap,
  faBuildingColumns,
  faBuilding,
  faBriefcase,
  faUserGear,
  faClock,
} from "@fortawesome/free-solid-svg-icons";
import { faLinkedin } from "@fortawesome/free-brands-svg-icons";

const UserProfile = ({
  id,
  name,
  email,
  location,
  college_name,
  degree,
  companies,
  worked_as,
  skills,
  experience,
  linkedin,
}) => {
  // Remove square brackets and single quotes from the skills string
  const cleanedSkills = skills.replace(/[[\]']+/g, "");

  // Split the cleanedSkills string using commas and trim each skill
  const parsedSkills = cleanedSkills.split(",").map((skill) => skill.trim());

  return (
    <div className="resumeProfile_container">
      <div className="resumeProfile_container_content" key={id}>
        <h3>ID: {id}</h3>
        <h2 className="profile_name">{name}</h2>

        <div className="decorative-underline" />

        <div className="profile_details">
          <div className="field">
            <div className="icon">
              <FontAwesomeIcon icon={faEnvelope} />
            </div>
            <p>
              <strong>Email Address:</strong> {email}
            </p>
          </div>
          <div className="field">
            <div className="icon">
              <FontAwesomeIcon icon={faLocationDot} />
            </div>
            <p>
              <strong>Location:</strong> {location}
            </p>
          </div>
          <div className="field">
            <div className="icon">
              <FontAwesomeIcon icon={faBuildingColumns} />
            </div>
            <p>
              <strong>College:</strong> {college_name}
            </p>
          </div>
          <div className="field">
            <div className="icon">
              <FontAwesomeIcon icon={faGraduationCap} />
            </div>
            <p>
              <strong>Degree:</strong> {degree}
            </p>
          </div>
          <div className="field">
            <div className="icon">
              <FontAwesomeIcon icon={faBuilding} />
            </div>
            <p>
              <strong>Companies Worked:</strong> {companies}
            </p>
          </div>
          <div className="field">
            <div className="icon">
              <FontAwesomeIcon icon={faBriefcase} />
            </div>
            <p>
              <strong>Designation:</strong> {worked_as}
            </p>
          </div>
          <div className="field skill">
            <div className="icon">
              <FontAwesomeIcon icon={faUserGear} />
            </div>
            <p>
              <strong>Skills:</strong>{" "}
              {Array.isArray(parsedSkills)
                ? parsedSkills.map((skill, index) => (
                    <div className="skill_content">
                      <span key={index}>{skill}</span>
                    </div>
                  ))
                : "Skills data not available"}
            </p>
          </div>
          <div className="field">
            <div className="icon">
              <FontAwesomeIcon icon={faClock} />
            </div>
            <p>
              <strong>Experience:</strong> {experience}
            </p>
          </div>
          <div className="field">
            <div className="icon">
              <FontAwesomeIcon icon={faLinkedin} />
            </div>
            <p>
              <strong>Linkedin:</strong> {linkedin}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

const ResumeProfile = () => {
  const [parsedData, setParsedData] = useState([]);

  const fetchData = async () => {
    const myHeaders = new Headers();
    const requestOptions = {
      method: "GET",
      headers: myHeaders,
      redirect: "follow",
    };

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/get_parsed_data/",
        requestOptions
      );
      const result = await response.json();
      setParsedData(result.parsed_data);
    } catch (error) {
      console.error(error);
    }
  };
  useEffect(() => {
    fetchData();
  }, []);

  const handleFetchData = () => {
    // Trigger data fetching when the button is clicked
    fetchData();
  };

  return (
    <>
      <div className="resumeProfile">
        <h1>
          Parsed <span className="gradient-text">Resumes</span>
        </h1>
        <button onClick={handleFetchData} className="fetch_btn">
          Fetch Data
        </button>
        {parsedData.map((item) => (
          <UserProfile
            key={item.id}
            id={item.id}
            name={item.name}
            email={item.email}
            location={item.location}
            college_name={item.college_name}
            degree={item.degree}
            companies={item.companies}
            worked_as={item.worked_as}
            skills={item.skills}
            experience={item.experience}
            linkedin={item.linkedin}
          />
        ))}
      </div>
    </>
  );
};

export default ResumeProfile;
