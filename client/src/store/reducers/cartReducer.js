import {
    ADD_TO_CART,
    REMOVE_FROM_CART,
    UPDATE_QUANTITY,
} from "../actions/cartActions";

const initialState = {
    cartItems: [],
};

export const cartReducer = (state = initialState, action) => {
    switch (action.type) {
        case ADD_TO_CART:
            const newItem = action.payload;
            // Check if item is already in cart
            const existingItem = state.cartItems.find(
                (item) => item.product.id === newItem.product.id
            );
            if (existingItem) {
                // Update quantity
                return {
                    ...state,
                    cartItems: state.cartItems.map((item) =>
                        item.product.id === newItem.product.id
                            ? {
                                  ...item,
                                  quantity: item.quantity + newItem.quantity,
                              }
                            : item
                    ),
                };
            } else {
                // Add new item
                return {
                    ...state,
                    cartItems: [...state.cartItems, newItem],
                };
            }
        case REMOVE_FROM_CART:
            return {
                ...state,
                cartItems: state.cartItems.filter(
                    (item) => item.product.id !== action.payload.productId
                ),
            };
        case UPDATE_QUANTITY:
            return {
                ...state,
                cartItems: state.cartItems.map((item) =>
                    item.product.id === action.payload.productId
                        ? { ...item, quantity: action.payload.quantity }
                        : item
                ),
            };
        default:
            return state;
    }
};
export default cartReducer;
