
import { useGoogleLogin } from "@react-oauth/google";
import GoogleButton from "react-google-button";
import { useNavigate } from 'react-router-dom'
import './GoogleLoginButton.css' 
import { useContext } from 'react'
import UserContext from '../context/UserContext'

const GoogleLoginButton = () => {
  const navigate = useNavigate()
  const { setUser } = useContext(UserContext);
  const handleSuccess = async (codeResponse) => {
    console.log(codeResponse)
    try {
        const response = await fetch(
            'http://localhost:8000/user/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    code: codeResponse.code
                })
            }
        )
        const data = await response.json()
        const { access_token, user_name } = data;

        localStorage.setItem('access_token', access_token)
        localStorage.setItem('user_name', user_name)

        setUser({ user_name, access_token })

        navigate('/dashboard')
    } catch (error) {
        console.log(error)
        alert('Login failed')
    } 
    

    //Destruct response (come with jwt token)

    
  };

  const login = useGoogleLogin({
    onSuccess: handleSuccess,
    scope: 'openid https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
    flow: "auth-code",
  });

  return (
    <div className="gradient-border">
      <div className="flex items-center justify-center">
        <GoogleButton onClick={login} label="Sign in with Google 🚀" />
      </div>
    </div>
  );
};

export default GoogleLoginButton;