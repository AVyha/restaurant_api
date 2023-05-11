# Restaurant API
This API service created for employees, they can every day create new menu and give score for this or another menu.

## Installation
run this command in terminal
```
git clone https://github.com/AVyha/restaurant_api.git
python -m venv venv
venv\Scripts\activate
pip install -m requirements.txt
```
create `.env` file and fill with yours variable like in example `.env-sample`
```
python manage.py runserver
```

## Endpoints
1. Restaurants `localhost:8000/api/restaurants/`

![ScreenShot](https://imgur.com/4VlewOT.png)

This endpoint allows you to create a restaurant

2. User `localhost:8000/api/user`

![ScreenShot](https://snipboard.io/kLyWr2.jpg)

This endpoint allows you to create a new user


3. Token `localhost:8000/api/token/`

![ScreenShot](https://snipboard.io/wzfZ68.jpg)

You must provide yours credential and copy access token
After access token expired you can use refresh token `localhost:8000/api/token/refresh/` or again use `localhost:8000/api/token/`

![ScreenShot](https://imgur.com/Z8XqwmY.jpg)

This is `ModHeader` extension for google chrome browser, that allows you to be authenticated with JWT token

4. Position `localhost:8000/api/position/`

![ScreenShot](https://imgur.com/7JNpT0D.jpg)

You must be authenticated. With this endpoint you can add different product into daily menu

5. Score `localhost:8000/api/score/`

![ScreenShot](https://imgur.com/SaxoO2j.jpg)

You must be authenticated. You can set your score for daily menu in different restaurants

6. Menu `localhost:8000/api/menu/`

![ScreenShot](https://imgur.com/K60wuTo.jpg)

This endpoint give you information about all menu. You can see all position in this menu, restaurant and average score

`localhost:8000/api/today_menu/` - allow you to view the menu of the current day only


