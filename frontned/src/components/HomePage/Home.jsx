import GoogleLoginButton from "../GoogleLoginButtion"
import hand_homepage from "../../assets/hand_homepage.png"
const Home = () => {
    return (
        <div className="flex flex-col items-center justify-center h-screen text-2xl bg-gray-100">
            <div className="absolute text-xl font-bold m-4 left-5 top-1">
                Recal
            </div>
            <div className="text-center m-5 text-5xl font-bold font-sans"> Chat, Schedule, Manage</div>
            <div className="text-center mt-5 mb-8 text-2xl font-semibold">
            Chat with your calendar to manage events effortlessly.
            </div>
            <div className="flex flex-col items-center mb-8">
                <img src={hand_homepage} alt="hand_homepage" className="w-1/2 mb-8 rounded-lg " />
                <GoogleLoginButton />
            </div>
        </div>
    );
}

export default Home;