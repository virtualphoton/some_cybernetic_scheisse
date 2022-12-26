// import React, { useState, useEffect } from "react";
// import { ReactTerminal } from "react-terminal";
// import { BrowserRouter, Routes, Route} from "react-router-dom";
// import Main from './pages/Main'
// import Login from './pages/Login'
//
// import { GoogleLogin } from 'react-google-login';
// import { gapi } from 'gapi-script';

// const clientId = '543749207333-rscj6i8f4b6fvqj5bkepiso3rtt38dvk.apps.googleusercontent.com';

import React, { useState, useEffect } from 'react';
import { GoogleLogin, GoogleLogout } from 'react-google-login';
import { gapi, loadAuth2 } from 'gapi-script';

const clientId = '543749207333-rscj6i8f4b6fvqj5bkepiso3rtt38dvk.apps.googleusercontent.com';

function App() {
    const [ user, setUser ] = useState({name: null, id: null});

    const updateUser = (currentUser) => {
      const name = currentUser.getBasicProfile().getName();
      const id = currentUser.getBasicProfile().getId();
      console.log(currentUser)
      setProfile({
        name: name,
        id: id
      });
    };

    const attachSignin = (element, auth2) => {
      auth2.attachClickHandler(element, {},
        (googleUser) => {
          updateUser(googleUser);
        }, (error) => {
        console.log(JSON.stringify(error))
      });
    };

    useEffect(() => {
        const initClient = async () => {
          const auth2 = await loadAuth2(gapi, clientId, '');
          if (auth2.isSignedIn.get()) {
              updateUser(auth2.currentUser.get())
          } else {
              attachSignin(document.getElementById('customBtn'), auth2);
          }
          gapi.client.init({
              clientId: clientId,
              scope: ''
          });
        };
        gapi.load('client:auth2', initClient);
    });

    const onSuccess = (res) => {
      console.log(res);
        setProfile(res.profileObj);
    };

    const onFailure = (err) => {
        console.log('failed', err);
    };

    const logOut = () => {
        setProfile(null);
    };

    return (
        <div>
            <h2>React Google Login</h2>
            <br />
            <br />
            {profile ? (
                <div>
                    <img src={profile.imageUrl} alt="user image" />
                    <h3>User Logged in</h3>
                    <p>Name: {profile.name}</p>
                    <p>Email Address: {profile.email}</p>
                    <br />
                    <br />
                    <GoogleLogout clientId={clientId} buttonText="Log out" onLogoutSuccess={logOut} />
                </div>
            ) : (
                <GoogleLogin
                    clientId={clientId}
                    buttonText="Sign in with Google"
                    onSuccess={onSuccess}
                    onFailure={onFailure}
                    cookiePolicy={'single_host_origin'}
                    isSignedIn={true}
                />
            )}
        </div>
    );
}
export default App;
  // return (
  //   <BrowserRouter>
  //     <Routes>
  //       <Route path="/" element={<Main/>}>
  //         <Route path="login" element={<Login />} />
  //         <Route path="*" element={<Main/>} />
  //       </Route>
  //     </Routes>
  //   </BrowserRouter>
  // );
// }
//
// export default App;
