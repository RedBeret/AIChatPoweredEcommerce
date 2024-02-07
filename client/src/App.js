import React, { useEffect } from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect,
} from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { checkLoginSession } from "./store/actions/authActions";

// Your imports
import Home from "./pages/HomePage";
import ProductDetail from "./pages/ProductDetailPage";
import About from "./pages/AboutPage";
import Checkout from "./pages/CheckoutPage";
import AuthPages from "./pages/AuthPages";
import Contact from "./pages/ContactPage";
import Confirmation from "./pages/ConfirmationPage";
import NavbarMenu from "./components/NavbarMenu";
import Footer from "./components/Footer";
import { CartWrapper } from "./components/CartContext";

export default function App() {
    const dispatch = useDispatch();
    const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

    // Protected Route for Confirmation page
    const ProtectedRoute = ({ component: Component, ...rest }) => (
        <Route
            {...rest}
            render={(props) =>
                isAuthenticated ? (
                    <Component {...props} />
                ) : (
                    <Redirect to="/auth/login" />
                )
            }
        />
    );

    return (
        <div>
            <CartWrapper>
                <Router>
                    <NavbarMenu />
                    <Switch>
                        <Route exact path="/" component={Home} />
                        <Route
                            path="/productdetail/:id"
                            component={ProductDetail}
                        />
                        <Route path="/about" component={About} />
                        <Route path="/checkout" component={Checkout} />
                        <Route path="/confirmation" component={Confirmation} />
                        <Route path="/auth" component={AuthPages} />
                        <Route path="/contact" component={Contact} />
                        {/* <Route
                            path="/tech-support"
                            component={TechSupportChatbot}
                        />{" "} */}
                    </Switch>
                    <Footer />
                </Router>
            </CartWrapper>
        </div>
    );
}

//App.js
