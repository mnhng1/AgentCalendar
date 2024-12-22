
import { useGoogleLogin } from "@react-oauth/google";
import GoogleButton from "react-google-button";
import { useNavigate } from 'react-router-dom'

const GoogleLoginButton = () => {
  
  const handleSuccess = (codeResponse) => {
    console.log(codeResponse)
    try {
        const response = fetch(
            'http://localhost:8000/user/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    code: codeResponse.code
                })
            }
        )
        console.log(response)
    } catch (error) {
        console.log(error)
    }
    

    //Destruct response (come with jwt token)

    
  };

  const login = useGoogleLogin({
    onSuccess: handleSuccess,
    flow: "auth-code",
  });

  return (
    <div className="flex items-center justify-center">
      {/* <button onClick={() => login()}>Sign in with Google 🚀</button> */}
      <GoogleButton onClick={login} label="Sign in with Google 🚀" />
    </div>
  );
};

export default GoogleLoginButton;