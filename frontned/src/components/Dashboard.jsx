import { useContext } from "react";
import UserContext from "../context/UserContext";
import { useNavigate } from "react-router-dom";
const Dashboard = () => {
    const navigate = useNavigate();
    const { user } = useContext(UserContext);
    
    const handleLogout = () => {
        navigate('/logout')
    }


    return (
        <div className="flex flex-col items-center w-screen h-full">
            <header className="w-full flex items-center justify-between text-sm font-bold p-4 bg-gray-500 text-white ">
            <h1>Dashboard</h1>
            { user?.access_token  &&
            <h2>Welcome {user?.user_name}</h2>
            }
            <div>
                <button onClick={handleLogout}>Logout</button>
            </div>
            </header>
        </div>
    );
}

export default Dashboard;