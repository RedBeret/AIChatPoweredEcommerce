import React, { createContext, useContext, useState } from "react";
import { useSelector } from "react-redux";

const CartContext = createContext();

export const useCartContext = () => useContext(CartContext);

export const CartWrapper = ({ children }) => {
    const [cartItems, setCartItems] = useState([]);
    const user = useSelector((state) => state.auth.user);

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

    const addToCart = (product, color, quantity = 1) => {
        setCartItems((currentItems) => {
            const existingProductIndex = currentItems.findIndex(
                (item) => item.id === product.id && item.colorId === color.id
            );

            if (existingProductIndex >= 0) {
                const updatedItems = currentItems.map((item, index) => {
                    if (index === existingProductIndex) {
                        return { ...item, quantity: item.quantity + quantity };
                    }
                    return item;
                });
                return updatedItems;
            } else {
                const newItem = {
                    id: product.id,
                    name: product.name,
                    price: product.price,
                    image_path: product.image_path,
                    color: color.name,
                    colorId: color.id,
                    quantity,
                    userId: user?.id,
                };
                return [...currentItems, newItem];
            }
        });
    };
    const clearCart = () => {
        setCartItems([]);
    };

    return (
        <CartContext.Provider
            value={{
                cartItems,
                addToCart,
                updateQuantity,
                removeFromCart,
                clearCart,
            }}
        >
            {children}
        </CartContext.Provider>
    );
};
