# Weather Auth Backend

A **FastAPI** service that provides **user registration**, **authentication** and 
**administration** features, plus integration with the 
[**OpenMeteo API**](https://open-meteo.com/en/docs) to fetch weather data.

**Authenticated users** can request current weather or forecasts for any given 
geographic location (latitude & longitude).

---

## Features

- **User Management**  
  - **Register** new users (`POST /auth/register`)  
  - **Login** with JWT (`POST /auth/login`)  
  - **Logout** (`POST /auth/logout`)
  - **Get current user** (`GET /users/me`)
  - **Update user email** (`POST /users/update/email`)
  - **Update user password** (`POST /users/update/password`)

- **Admin Features**  
  - **List of users** (`GET /admin/get_all_users`)  
  - **Delete user** (`POST /admin/delete_user/{user_id}`)  
  - **Update user role** (`POST /admin/change_user_role/{user_id}`)
  - **Update user active status** (`POST /admin/change_user_active_status/{user_id}`)

- **Weather Endpoints**  
  - **Current weather** (`POST /weather/current`)  
  - **Weather forecast** (`POST /weather/forecast`)

- **Security**  
  - ~~OAuth2 password flow with **Bearer** tokens~~  
  - Password hashing with **PassLib**  
  - Protected routes via JWT validation

- **Database & Migrations**  
  - **SQLAlchemy** models  
  - **Alembic** for migrations  

- **Testing & Quality**  
  - ~~Unit & integration tests with **pytest**~~  
  - `pre-commit` hooks: **ruff**, **black**, **isort**, **flake8**
