

# mysql_secure_installation_Python





## Features

A Python Script to:

* Change MySQL Root Password - for a list of hosts i.e `root@localhost`
* Remove Anonymous User
* Disallow Root Login Remotely
* Remove Test Database



## WHY ?



* Python & **Idempotent** :sunglasses:
  * Means that when you run it again, will not re-execute the commands



---



## Usage



* use the function `mysql_secure_installation`

```python
mysql_secure_installation(login_password='password511',
                          new_password='password51',
                          hosts=['localhost',
                                 '::1',
                                 '127.0.0.1',
                                 'controller.linux.com',
                                 'controller',
                                 'test'])
```



* Example Output

```bash
python mysql.py

{'remove_anonymous_user': 0, 'hosts_success': ['127.0.0.1', 'localhost', '::1'], 'disallow_root_remotely': None, 'hosts_failed': ['test', 'controller', 'controller.linux.com'], 'remove_test_db': 0, 'change_root_pwd': 1}
# 'disallow_root_remotely': None --> because it's "False" by default

python mysql.py

{'remove_anonymous_user': 0, 'stdout': 'Password of root@localhost Already meets the desired state', 'hosts_success': [], 'disallow_root_remotely': None, 'hosts_failed': [], 'remove_test_db': 0, 'change_root_pwd': 0}
```



---



* `login_password` Root password to login to `MySQL`
* `new_password` New desired Root password
* `hosts` A **List** of hosts to change password for, `Note:` all will have the same new password
  * **Default:** `['hostname'] `
* `change_root_password`
  * **Default:** `True`
* `remove_anonymous_user`
  * **Default:** `True`
* `disallow_root_login_remotely`
  * **Default:** `False`
* `remove_test_db`
  * **Default:** `True`





### Output:

* `0` –> `Success`

* `1` –>  `Fail`

  * For `change_root_pwd` - will output `1` if failed to change the password of at least 1 host, for more info check `hosts_success` & `hosts_failed`

    



---



Thank you 

Eslam Gomaa

