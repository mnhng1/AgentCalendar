
import './App.css'
import { useEffect, useState } from 'react'
import { GoogleOAuthProvider } from '@react-oauth/google'
import { BrowserRouter, Routes, Route} from 'react-router-dom'
import Dashboard from './components/Dashboard'
import Home from './components/HomePage/Home'
import UserContext from './context/UserContext'
import Logout from './components/LogoutPage/Logout'
import PrivateRoute from './context/PrivateRoute'

function App() {
  const [user, setUser] = useState({user_name: null, access_token: null})
  const [loading, setLoading] = useState(true);
  const vertify_token = async () => {
    const access_token = localStorage.getItem('access_token')
    const user_name = localStorage.getItem('user_name')

    const response = await fetch('http://localhost:8000/user/token/verify/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      
      },
      body: JSON.stringify({
        token: access_token,
      })
    })

    if (response.ok) {
      setUser({
        user_name: user_name, 
        access_token: access_token
      })
    } else {
      setUser({
        user_name: null,
        access_token: null
      })
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_name')
    }
    setLoading(false);
  }

  useEffect(() => {
    vertify_token()
  },[])
  
  return (
    <BrowserRouter>
    <UserContext.Provider value={{user, setUser}}>
      <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
      <Routes>
        <Route path='/' element={<Home/>}/>
        
          <Route path='/dashboard' element={ <PrivateRoute><Dashboard/></PrivateRoute>}/>
       
        <Route path='/logout' element={<Logout/>}/>
      </Routes>
      </GoogleOAuthProvider>
    </UserContext.Provider>
    </BrowserRouter>
    
  )
}

export default App
