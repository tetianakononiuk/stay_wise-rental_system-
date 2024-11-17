# Stay Wise Rental System API

This project is an API for apartment reservations. It allows users to manage apartments (with addresses), make
reservations, and leave reviews.

## Features

- **Apartments and Addresses:**
    - Landlords can create and update apartments and their addresses.
    - All users can view apartments.

- **Search and Filtering:**
    - Users can enter keywords to search in apartment titles and descriptions.
    - Filtering by parameters:
        - **Price:** Users can specify a minimum and maximum price.
        - **Location:** Users can specify a city or region in Germany.
        - **Number of rooms:** Users can specify a range for the number of rooms.
        - **Type of apartment:** Users can choose the type of housing (apartment, house, flat, etc.).
    - Sorting results:
        - **By price:** Ability to sort by ascending or descending price.
        - **By created date:** Ability to sort by newest or oldest listings.

- **Booking:**
    - Renters can create and update reservations.
    - Landlords can approve reservations through a dedicated endpoint.
    - Renters can cancel reservations through a dedicated endpoint, but not later than 5 days before the start date.

- **Reviews:**
    - Renters can leave reviews.
    - All users can view reviews.

- **Users:**
    - It's possible to create new user - landlord or usual renter
    - User can sign in to the system
    - User can log out from the system
    - JWT token used for authentication process
    - Automatic saving of tokens integrated to the system (via cookies)

## Endpoints

### Addresses

- `GET /addresses/` - View existing addresses (Landlords only)
- `POST /addresses/` - Create a new address (Landlords only)
- `GET /addresses/:id/` - Retrieve an address (Landlords only)
- `PUT /addresses/:id/` - Update an address (Landlords only)
- `DELETE /addresses/:id/` - Delete an address (Landlords only)

### Apartments

- `GET /apartments/` - View all apartments
- `POST /apartments/` - Create a new apartment (Landlords only)
- `GET /apartments/:id/` - Retrieve an apartment
- `PUT /apartments/:id/` - Update an apartment (Landlords only)
- `DELETE /apartments/:id/` - Delete an apartment (Landlords only)

### Booking

- `GET /booking/` - View all reservations (Renters can view only own reservations, Landlords can view reservations
  for apartments they own.)
- `POST /booking/` - Create a new reservation (Renters only)
- `GET /booking/:id/` - Retrieve a reservation (Renters can view only own reservation, Landlords can view
  reservation for apartment they own.)
- `PUT /booking/:id/` - Update a reservation (Renters only)
- `DELETE /booking/:id/` - Delete a reservation (Renters only)
- `PUT /booking/:id/approve/` - Approve a reservation (Landlords only)
- `PUT /booking/:id/cancel/` - Cancel a reservation (Renters only, must be more than 5 days before the start date)

### Reviews

- `GET /reviews/` - View all reviews
- `POST /reviews/` - Create a new review (Renters only)
- `GET /reviews/:id/` - Retrieve a review
- `PUT /reviews/:id/` - Update a review (Renters only)
- `DELETE /reviews/:id/` - Delete a review (Renters only)

### Users

- `POST /sign-up/` - Register new account
- `POST /sign-in/` - Login to the system
- `POST /logout/` - Log out from the system

## Permissions

- **Landlords:**
    - Can create and update apartments and addresses.
    - Can approve reservations.

- **Renters:**
    - Can create and update reservations.
    - Can cancel reservations, but not later than 3 days before the start date.
    - Can leave reviews.

- **All Users:**
    - Can view all apartments and reviews.


