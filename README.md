# Weather Auth Backend

A **FastAPI** service that provides **user registration**, **authentication** and 
**administration** features, plus integration with different weather APIs to fetch 
weather data. 

**Authenticated users** can request current weather or hourly forecasts for any given 
geographic location (latitude & longitude).

---

## Integrated Weather APIs
- [**OpenMeteo API**](https://open-meteo.com/en/docs) 
- [**MeteoSource API**](https://www.meteosource.com/documentation) 


## Features

- **User Management**
  - **Register** new users (`POST /auth/register/`)  
  - **Login** with JWT (`POST /auth/login/`)  
  - **Logout** (`POST /auth/logout/`)
  - **Get current user** (`GET /users/me/`)
  - **Update user email** (`POST /users/update/email/`)
  - **Update user password** (`POST /users/update/password/`)

- **Admin Features**
  - **List of users** (`GET /admin/get_all_users/`)  
  - **Delete user** (`POST /admin/delete_user/`)  
  - **Update user role** (`POST /admin/change_user_role/`)
  - **Update user active status** (`POST /admin/change_user_active_status/`)

- **Weather Endpoints**
  - **Current weather** (`POST /weather/current/`)
  - **Hourly weather forecast** (`POST /weather/hourly_forecast/`)

- **Security**
  - OAuth2 password flow with **Bearer** tokens
  - Password hashing with **PassLib**
  - Protected routes via JWT validation

- **Database & Migrations**
  - **SQLAlchemy** models
  - **Alembic** for migrations

- **Testing & Quality**
  - ~~Unit & integration tests with **pytest**~~
  - `pre-commit` hooks: **ruff**, **black**, **isort**, **flake8**
