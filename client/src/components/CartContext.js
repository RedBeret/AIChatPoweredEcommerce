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

    const addToCart = (product, color) => {
        setCartItems((currentItems) => {
            // Check if the product with the same color is already in the cart
            const isProductInCart = currentItems.some(
                (item) => item.id === product.id && item.color === color
            );
            if (isProductInCart) {
                // If the product with the same color is already in the cart, update the quantity
                return currentItems.map((item) =>
                    item.id === product.id && item.color === color
                        ? { ...item, quantity: item.quantity + 1 }
                        : item
                );
            } else {
                // If the product with the same color is not in the cart, add a new item
                return [
                    ...currentItems,
                    { ...product, quantity: 1, color: color },
                ];
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
