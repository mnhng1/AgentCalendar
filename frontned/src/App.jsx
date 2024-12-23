
import './App.css'
import { useEffect, useState } from 'react'
import { GoogleOAuthProvider } from '@react-oauth/google'
import { BrowserRouter, Routes, Route} from 'react-router-dom'
import Dashboard from './components/Dashboard'
import Home from './components/HomePage/Home'
import UserContext from './context/UserContext'
import Logout from './components/LogoutPage/Logout'

function App() {
  const [user, setUser] = useState([])
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

    if (response.ok){
      setUser({...user, user_name: user_name, access_token: access_token})
    }
     else{
      setUser({...user, user_name: null, access_token: null})
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_name')
     }
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
        <Route path='/dashboard' element={<Dashboard/>}/>
        <Route path='/logout' element={<Logout/>}/>
      </Routes>
      </GoogleOAuthProvider>
    </UserContext.Provider>
    </BrowserRouter>
    
  )
}

export default App
