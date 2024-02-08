import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./reducers/authReducer";
import cartReducer from "./reducers/cartReducer";
import productReducer from "./reducers/productReducer";
import orderReducer from "./reducers/orderReducer";
import shippingReducer from "./reducers/shippingReducer";

const store = configureStore({
    reducer: {
        auth: authReducer,
        cart: cartReducer,
        products: productReducer,
        orders: orderReducer,
        shipping: shippingReducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: false,
        }),
});

export default store;

//src/store/index.js
