import React from "react";
import { Switch, Route } from "react-router-dom";

import Login from "../components/Login";
import UpdatePassword from "../components/UpdatePassword";
import Register from "../components/Register";
import CloseAccount from "../components/CloseAccount";
function AuthPages() {
    return (
        <div>
            <Switch>
                <Route path="/login" component={Login} />
                <Route path="/updatepassword" component={UpdatePassword} />
                <Route path="/register" component={Register} />
                <Route path="/closeaccount" component={CloseAccount} />
            </Switch>
        </div>
    );
}

export default AuthPages;
