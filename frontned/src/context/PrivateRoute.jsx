import UserContext from "./UserContext"
import { Navigate } from 'react-router-dom'
import { useContext } from 'react'
import PropTypes from 'prop-types'
const PrivateRoute = ({ children }) => {
    const { user, loading} = useContext(UserContext);
    if (loading) {
        return (<div>Loading...</div>); // Show a loading indicator while verifying token
    }
    return user.access_token ? children : <Navigate to='/' />;
  };



PrivateRoute.propTypes = {
    children: PropTypes.node.isRequired
}

export default PrivateRoute;


