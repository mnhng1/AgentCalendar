import GoogleLoginButton from "../GoogleLoginButtion"

const Home = () => {    
    return (
        <div className='flex flex-col items-center justify-center h-screen'> 
            A Simple Calendar Agent
            <div className="mt-8">
                
                    <GoogleLoginButton/>
               
            </div>
        </div>
    )
}

export default Home;