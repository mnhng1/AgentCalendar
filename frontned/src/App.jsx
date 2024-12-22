
import './App.css'
import GoogleLoginButton from './components/GoogleLoginButtion'
import { GoogleOAuthProvider } from '@react-oauth/google'
import { BrowserRouter } from 'react-router-dom'
function App() {
 

  return (
    <BrowserRouter>
      <GoogleOAuthProvider clientId="289516299379-aiv4tfh8p9l76g35sqqflos92jup60fj.apps.googleusercontent.com">
      <div className='flex items-center justify-center'> 
        Home
        <GoogleLoginButton/>
      </div>
      </GoogleOAuthProvider>
    </BrowserRouter>
    
  )
}

export default App
