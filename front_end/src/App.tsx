import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import avengersImage from "./assets/avengers.png";
import nowYouSee from "./assets/nowYouSee.jpg";
import netflix from "./assets/netflix.png";
import max from "./assets/max.jpg";
import { Chart, Doughnut } from "react-chartjs-2";

import { Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  animator
 } from "chart.js";

 ChartJS.register(ArcElement, Tooltip, Legend);


const dummyData: { [key: string]: { image: string; title: string, year: string } } = { avengers_endgame: { image: avengersImage, title: "Avengers End Game", year: "2019" }, now_you_see_me: { image: nowYouSee, title: "Now You See Me", year: "2013" } };


const AWS_API = process.env.AWS_API_URL

function App() {
  const [inputValue, setInputValue] = useState("");
  const [response, setResponse] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isMoved, setIsMoved] = useState(false); // Tracks if the input-container has moved
  const [showResponse, setShowResponse] = useState(false); // Tracks if the response should be displayed
  const [movieName, setMovieName] = useState("");
  const [rating, setRating] = useState(0);

const data = {
  labels: ['Rating', 'Left'],
  datasets: [
    {
      label: 'Rating',
      data: [rating, 10 - rating],
      backgroundColor: [
        "#f3be00",
        'rgba(255, 255, 255, 0.01)',
      ],
      borderColor: [
        "#f3be00",
        'rgba(255, 255, 255, 0.01)',
      ],
      borderWidth: 1,
    },
  ],
};

const options = {
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      enabled: false,
    },
    centerText: {
      display: true,
      text: '75%', // Rating text
      color: '#f3be00',
    },
  },
  animation: {
    delay: 5000, // Delay the start of the animation by 2 seconds
  },

};



  const handleSubmit = async () => {
    try {
      setError("");
      setResponse("");
      setShowResponse(false); // Hide response initially
      setIsLoading(true); // Set loading state to true
      setIsMoved(false); // Reset input-container movement
      const res = await axios.post(
         AWS_API|| "your_default_api_url",
        { url: inputValue },
        { headers: { "Content-Type": "application/json" } }
      );
      setResponse(res.data.summary); // Assume this contains full movie info\
      setRating(res.data.rating + 4);
      setMovieName(res.data.best_product);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(err.message || "An unknown error occurred");
      } else {
        setError("An unknown error occurred");
      }
    } finally {
      console.log(response);
      setIsLoading(false); // Set loading state to false
      setIsMoved(true); // Trigger input-container movement
    }
  };

  useEffect(() => {
    if (isMoved) {
      // Wait for the movement transition to complete (1 second)
      const timer = setTimeout(() => {
        setShowResponse(true); // Show the response after movement completes
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [isMoved]);

  return (
    <div className="App">
      {/* Title */}
      <div className="title">UpfrontAI</div>

      {/* Input Container */}
      <div className={`input-container ${isMoved ? "moved" : ""}`}>
        <input
          className="chakra-petch-medium"
          type="text"
          id="inputText"
          placeholder="Enter Movie Name"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        />
        <button className="button" onClick={handleSubmit} disabled={isLoading}>
          {isLoading ? <div className="loading-spinner"></div> : "Submit"}
        </button>
      </div>

      {/* Additional Dummy Data */}
      {showResponse && !isLoading && (
        <div className="row">
          {/* Movie Name */}
          <div className="col">
            <div className={"response-container visible"} style={{ animationDelay: "0s" }}>
              <div className="image-container">
                  <img src={dummyData[movieName as keyof typeof dummyData]?.image} alt="Movie Poster" className="movie-image" />
                
              </div>
              <div className="text-card chakra-petch-medium">
                <strong className="chakra-petch-bold" style={{ fontSize: "2em" }}>Movie Name:</strong>
                <div >{dummyData[movieName as keyof typeof dummyData]?.title}</div>
                <div >{dummyData[movieName as keyof typeof dummyData]?.year}</div>
              </div>
            </div>

            <div className={"response-container visible small"} style={{ animationDelay: "0.5s" }}>
              <div className="text-card chakra-petch-medium">
                <strong className="chakra-petch-bold" style={{ fontSize: "2em" }}>Recommended:</strong>
                <div >No Recommendations Found</div>
              </div>
            </div>
          </div>



          <div
        id="responseDiv"
        className={`response-container visible imp`}style={{ animationDelay: "1s" }}
      >
        {response && (
          <div className="text-card chakra-petch-medium">
            <strong>AI Review:</strong>
            <div>{response}</div>
          </div>
        )}
        {error && (
          <div>
            <strong>An error occurred:</strong>
            <div>{error}</div>
          </div>
        )}
      </div>
      
      <div className="col">
        <div className={"response-container visible small logo"} style={{ animationDelay: "1.5s" }}>
        <strong className="chakra-petch-bold" style={{ fontSize: "2em" }}>Where to watch:</strong>
         <div className="logo">
          <div className="circle-container">
            <img src={netflix} alt="Netflix Logo" className="circle-image" />
          </div>
          <div className="circle-container">
            <img src={max} alt="Max Logo" className="circle-image" />
          </div>
          </div>
        </div>
        

          <div className="response-container visible ring " style={{ animationDelay: "2s" }}>
          <strong className="chakra-petch-bold" style={{ fontSize: "2em" }}>Rating: {rating}/10 </strong>
            <div className = "chart">
           <Doughnut  data = {data} options = {options} />
           </div>
</div>

         </div>
        </div>
      )}


      

      {/* Response Section */}
      


      
    </div>
  );
}

export default App;
