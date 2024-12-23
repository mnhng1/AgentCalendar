import { useContext } from "react";
import UserContext from "../context/UserContext";
import { useNavigate } from "react-router-dom";
import Chat from "./ChatUI/Chat";
const Dashboard = () => {
    const navigate = useNavigate();
    const { user } = useContext(UserContext);
    
    const handleLogout = () => {
        navigate('/logout')
    }

    return (
        <div className="flex flex-col w-screen min-h-screen bg-gray-100">
            <header className="w-full flex items-center justify-between text-sm font-bold p-4 bg-gray-500 text-white">
                <h1>Dashboard</h1>
                { user?.access_token  &&
                <h2>Welcome {user?.user_name}</h2>
                }
                <div>
                    <button 
                        onClick={handleLogout}
                        className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                    >
                        Logout
                    </button>
                </div>
            </header>
            <main className="flex-1 p-4">
                <Chat />
            </main>
        </div>
    );
}

export default Dashboard;