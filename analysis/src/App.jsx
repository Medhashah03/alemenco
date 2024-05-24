import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; // Import your CSS file for styling

function App() {
  const [image, setImage] = useState(null);
  const [name, setName] = useState('');
  const [tableData, setTableData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [imageTitles, setImageTitles] = useState([]);
  const [submitted, setSubmitted] = useState(false);
  const [imageId, setImageId] = useState(null); // Add state to store image ID

  useEffect(() => {
    fetchImageTitles();
  }, []);

  const fetchImageTitles = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/image_titles/');
      setImageTitles(response.data);
    } catch (error) {
      console.error('Error fetching image titles:', error);
    }
  };

  const handleImageChange = (e) => {
    const selectedImage = e.target.files[0];
    setImage(selectedImage);
  };

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!image || !name) {
      setError('Please provide both an image and a name.');
      return;
    }

    setLoading(true);
    setError('');
    setSubmitted(false);

    const formData = new FormData();
    formData.append('image', image);
    formData.append('title', name);

    try {
      const uploadResponse = await axios.post('http://127.0.0.1:8000/api/upload_image/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const imageId = uploadResponse.data.image_id;
      setImageId(imageId); // Save the image ID for future use

      const processResponse = await axios.get(`http://127.0.0.1:8000/api/display_image_result/${imageId}/`);

      setTableData(processResponse.data.result);
      setSubmitted(true);
    } catch (err) {
      setError('An error occurred while processing the request.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (imageId) {
      window.location.href = `http://127.0.0.1:8000/api/download-result/${imageId}/`;
    } else {
      setError('No image to download.');
    }
  };

  return (
    <div className="App">
      <div className="container">
        <div className="form-section">
          <h2>Enter Image and Name Input</h2>
          <div className="form-container">
            <form onSubmit={handleSubmit}>
              <div>
                <label htmlFor="name">Patient Name:   </label>
                <input type="text" id="name" value={name} onChange={handleNameChange} />
              </div>
              <div>
                <label htmlFor="image">Image of Strip:   </label>
                <input type="file" id="image" accept="image/*" onChange={handleImageChange} />
              </div>
              <button type="submit">Submit</button>
              {submitted && (
                <button className="download-button" onClick={handleDownload}>Download Result in json</button>
              )}
            </form>
            {loading && <p>Loading...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
          </div>
        </div>
        
        {submitted && (
          <div className="image-and-table-section">
            <div className="image-section">
              {submitted && (
                <div className="image-container">
                  <h3>Image</h3>
                  <img src={URL.createObjectURL(image)} alt="Entered" />
                </div>
              )}
            </div>
            <div className="table-section">
              {tableData && (
                <div className="table-container">
                  <h3>Image Result</h3>
                  <table>
                    <thead>
                      <tr>
                        <th>Key</th>
                        <th>Value</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(tableData).map(([key, value]) => (
                        <tr key={key}>
                          <td>{key}</td>
                          <td>
                            {Array.isArray(value) ? (
                              <ul>
                                {value.map((val, index) => (
                                  <li key={index}>{val.toString()}</li>
                                ))}
                              </ul>
                            ) : (
                              value
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
