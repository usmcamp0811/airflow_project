# Creating User Accounts

Just following along on the [Airflow Documentation](https://airflow.apache.org/security.html).
Had to install `flask_bcrypt`.. Will add to build requirments for the image.
pip install psycopg2-binary
```
import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
user = PasswordUser(models.User())
user.username = 'user'
user.email = 'usmcamp0811@gmail.com'
user.password = 'password'
from sqlalchemy import create_engine
engine = create_engine("postgresql://airflow:airflow@postgres:5432/airflow")
session = settings.Session()
session.add(user)
session.commit()
session.close()
exit()
```

Not sure if I `airflow updatedb` did anything or what but eventually it just started working. The above was used to add user accounts with passwords. Haven't figured out how to add user with password from the
UI yet.
