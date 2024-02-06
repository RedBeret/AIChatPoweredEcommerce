import React, { createContext, useContext, useState } from "react";

const CartContext = createContext();

export const useCartContext = () => useContext(CartContext);

export const CartWrapper = ({ children }) => {
    const [cartItems, setCartItems] = useState([]);

    const removeFromCart = (productId) => {
        setCartItems(cartItems.filter((item) => item.id !== productId));
    };

    const updateQuantity = (productId, newQuantity) => {
        setCartItems((currentItems) => {
            return currentItems.map((item) => {
                if (item.id === productId) {
                    return { ...item, quantity: newQuantity };
                }
                return item;
            });
        });
    };

    const addToCart = (product) => {
        setCartItems((currentItems) => {
            const isProductInCart = currentItems.some(
                (item) => item.id === product.id
            );
            if (isProductInCart) {
                return currentItems.map((item) =>
                    item.id === product.id
                        ? { ...item, quantity: item.quantity + 1 }
                        : item
                );
            } else {
                return [...currentItems, { ...product, quantity: 1 }];
            }
        });
    };

    return (
        <CartContext.Provider
            value={{ cartItems, addToCart, updateQuantity, removeFromCart }}
        >
            {children}
        </CartContext.Provider>
    );
};
