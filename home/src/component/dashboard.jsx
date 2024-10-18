import React from 'react';
import '../static/css/dashboard.css'
import podcast_cover from '../static/img/2024-10-08generated_image.jpeg'
import arrow from '../static/img/arrow.png'

const Home = () => {
    return (
        <div>
            {/* Header Section */}
            <header>
                {/* Top task bar */}
                <div className="task-bar">
                    <div className="options">
                        <a href="/your-page">Home</a>
                        <a href="/your-page">Episodes</a>
                        <a href="/your-page">About</a>
                    </div>
                </div>

                {/* Main content section */}
                <div className="content">
                    <h1>Tech Podcast</h1>
                    <p>
                        Stay on the cutting edge of technology with in-depth discussions and the latest news.
                        From emerging trends to industry secrets, Tech Pulse brings you the heartbeat of the tech world.
                    </p>
                    <div className="listen-links">
                        <p>Listen on:</p>
                        <a href="https://open.spotify.com/show/04zFo70jK2mzTgLkA2X3XF">
                            <img className="rounded-circle" src="https://pbcdn1.podbean.com/fs1/site/images/admin5/spotify.png" alt="Spotify" />
                        </a>
                        <a href="https://music.amazon.com/podcasts/7705bd11-3fb4-41a5-a171-b6598be89574">
                            <img className="rounded-circle" src="https://pbcdn1.podbean.com/fs1/site/images/admin5/apple-podcast.png" alt="Apple Podcasts" />
                        </a>
                        <a href="https://music.amazon.com/podcasts/7705bd11-3fb4-41a5-a171-b6598be89574">
                            <img className="rounded-circle" src="https://pbcdn1.podbean.com/fs1/site/images/admin5/AmazonMusic.png" alt="Amazon Music" />
                        </a>
                    </div>

                    <div className="generate-podcast">
                        <a href="/your-page" className="generate-button">
                            <span></span>
                            <span></span>
                            <span></span>
                            <span></span>
                            Start Your Podcast Journey
                            <img src={arrow} className="arrow-img" alt="Arrow" />
                        </a>
                    </div>
                </div>
            </header>

            {/* Curve Section */}
            <div className="curve-section">
                <svg id="Curve" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1924 212.552">
                    <path id="curve01" d="M-23.685,359.406S93.525,419.436,253.5,371.375s273.577,1.033,273.577,1.033,113.49,37.939,226.2-3.355,263.749-5.5,290.141,3.355,177.158,52.609,265.227,5.262,191.943-46.8,304.094,6.182,276.982-24.446,276.982-24.446v134.43h-1924V354.945Z" transform="translate(34.287 -281.283)" fill="#00000"></path>
                    <path id="curve02" d="M-2.111,728.749s89.218-48.068,157.482-21.806c72.236,31.039,61.34,53.552,173.542,79.815S454.9,706.923,579.664,706.923s111.41,72.894,213.965,90.951,132.6-53.569,199.093-69.125,137.826-4.511,222.382,54.054,213.326,14.629,251.445-6.7,135.343-73.064,245.343-54.288,210,76.058,210,76.058V911.5h-1924Z" transform="translate(2.111 -698.949)" fill="#00000" opacity="0.421"></path>
                    <path id="curve03" d="M2055.179,850.019v149.1h-1924v-189.1h0c.91-.286,75.2,66.583,191.974,82.357s98.2-77.359,230-82.357,144.632,77.663,267.9,73.383,142.695-95.3,246.795-89.867,140.081,75,245.748,78.165,103.959-84.817,189.279-85.131c127.354-.563,114.822,75.533,200.279,75.544s105.741-66.281,195.854-68.578S2055.179,850.019,2055.179,850.019Z" transform="translate(-131.179 -786.567)" fill="#00000" opacity="0.158"></path>
                </svg>
            </div>

            {/* Podcast Section */}
            <div className="podcast-section">
                <h2>Latest Episodes</h2>

                <div className="podcast-card">
                    <img src={podcast_cover} alt="Podcast Episode" className="podcast-image" />
                    <div className="podcast-info">
                        <h3 className="podcast-title">EP-39: Nobel Winners in Ai 🏅, Cyberattack on Water Utilities 🌊, Elon Musk’s X Strikes Back in Brazil</h3>
                        <p className="podcast-time">11 hours ago</p>
                        <p className="podcast-description">Welcome to echo-pod's tech briefing for Wednesday, October 9th! Today, we cover significant developments in the tech world: Nobel Prize in Physics: Geoffrey Hinton and John Hopfield honored for their pioneering research in artificial intelligence and neural networks, with Hinton reflecting on the implications of his work....</p>
                        <div className="podcast-footer">
                            <button className="btn-icon">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-heart" viewBox="0 0 16 16">
                                    <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"></path>
                                </svg>
                                Likes
                            </button>
                            <button className="btn-icon">
                            <i className="bi bi-arrow-down-square"></i>
                                Download
                            </button>
                            <button class="btn-icon">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                    class="bi bi-share" viewBox="0 0 16 16">
                                    <path
                                        d="M13.5 1a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zM11 2.5a2.5 2.5 0 1 1 .603 1.628l-6.718 3.12a2.499 2.499 0 0 1 0 1.504l6.718 3.12a2.5 2.5 0 1 1-.488.876l-6.718-3.12a2.5 2.5 0 1 1 0-3.256l6.718-3.12A2.5 2.5 0 0 1 11 2.5zm-8.5 4a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm11 5.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z">
                                    </path>
                                </svg>
                                Share
                            </button>
                        </div>
                    </div>
                </div>
                <footer class="footer">
                    <p>&copy; 2024 Tech Podcast. All rights reserved.</p>
                </footer>
            </div>

            {/* Footer Section */}

        </div>
    );
};

export default Home;
