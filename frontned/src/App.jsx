
import './App.css'

import { GoogleOAuthProvider } from '@react-oauth/google'
import { BrowserRouter, Routes, Route} from 'react-router-dom'
import Dashboard from './components/Dashboard'
import Home from './components/HomePage/Home'


function App() {
  return (
    <BrowserRouter>
      <GoogleOAuthProvider clientId="289516299379-aiv4tfh8p9l76g35sqqflos92jup60fj.apps.googleusercontent.com">
      <Routes>
        <Route path='/' element={<Home/>}/>
        <Route path='/dashboard' element={<Dashboard/>}/>
      </Routes>
      </GoogleOAuthProvider>
    </BrowserRouter>
    
  )
}

export default App
