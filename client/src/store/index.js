import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./reducers/authReducer";
import cartReducer from "./reducers/cartReducer";
import productReducer from "./reducers/productReducer";
import orderReducer from "./reducers/orderReducer";
import shippingReducer from "./reducers/shippingReducer";
import chatReducer from "./reducers/chatReducer";
import messagesReducer from "./reducers/messagesReducer";

const store = configureStore({
    reducer: {
        auth: authReducer,
        cart: cartReducer,
        products: productReducer,
        orders: orderReducer,
        shipping: shippingReducer,
        chat: chatReducer,
        messages: messagesReducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: false,
        }),
});

export default store;

//src/store/index.js
