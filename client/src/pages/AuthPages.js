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
                <Route path="/auth/login" component={Login} />
                <Route path="/auth/updatepassword" component={UpdatePassword} />
                <Route path="/auth/register" component={Register} />
                <Route path="/auth/closeaccount" component={CloseAccount} />
            </Switch>
        </div>
    );
}

export default AuthPages;
