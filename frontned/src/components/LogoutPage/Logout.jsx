import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import UserContext from "../../context/UserContext";


const Logout = () => { 
    const navigate = useNavigate();
    const { setUser } = useContext(UserContext);


    useEffect(() => {
        setUser({})
        localStorage.removeItem('access_token')
        localStorage.removeItem('user_name')
        navigate('/')
    },[])

    return(
        <div>
            Logout
        </div>
    )

}

export default Logout;