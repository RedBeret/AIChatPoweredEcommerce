import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import Home from "./pages/HomePage";
import ProductDetail from "./pages/ProductDetailPage";
import About from "./pages/AboutPage";
import Checkout from "./pages/CheckoutPage";
import AuthPages from "./pages/AuthPages";
import Contact from "./pages/ContactPage";
import NavbarMenu from "./components/NavbarMenu";
import Footer from "./components/Footer";
import { CartWrapper } from "./components/CartContext";
import { useDispatch } from "react-redux";
import { checkLoginSession } from "./store/actions/authActions";
import { useEffect } from "react";

export default function App() {
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(checkLoginSession());
    }, [dispatch]);
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
                        <Route path="/auth" component={AuthPages} />{" "}
                        <Route path="/contact" component={Contact} />
                    </Switch>
                    <Footer />
                </Router>
            </CartWrapper>
        </div>
    );
}
