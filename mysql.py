import MySQLdb as mysql

def check_mysql_connection(host, user, password=''):
    try:
        mysql.connect(host=host, user=user, passwd=password)
        return True
    except  mysql.Error:
        return False


def search_tuple(tups, elem):
    return filter(lambda tup: elem in tup, tups)

def mysql_secure_installation(login_password, new_password, user='root',login_host='localhost', hosts=['hostname'], change_root_password= True, remove_anonymous_user= True, disallow_root_login_remotely= False, remove_test_db= True):
    if isinstance(hosts, str):
        hosts = hosts.split(',')
    info = {'change_root_pwd': None, 'hosts_failed': [], 'hosts_success': [],'remove_anonymous_user': None, 'remove_test_db': None, 'disallow_root_remotely': None }

    def remove_anon_user(cursor):
        if remove_anonymous_user:
            cursor.execute("select user, host from mysql.user where user='';")
            anon_user = cursor.fetchall()
            if len(anon_user) >= 1:
                cursor.execute('use mysql;')
                cursor.execute("DELETE FROM user WHERE user='';")
                cursor.execute("select user, host from mysql.user where user='';")
                check = cursor.fetchall()
                if len(check) >= 1:
                    info['remove_anonymous_user'] = 1
                else:
                    info['remove_anonymous_user'] = 0
            else:
                info['remove_anonymous_user'] = 0

    def remove_testdb(cursor):
        if remove_test_db:
            cursor.execute("show databases;")
            testdb = cursor.fetchall()
            if not search_tuple(testdb, 'testdb'):
                cursor.execute("drop database testdb;")
                info['remove_test_db'] = 0
            else:
                info['remove_test_db'] = 0

            if not search_tuple(testdb, 'testdb'):
                cursor.execute("drop database testdb;")
                info['remove_test_db'] = 0
            else:
                info['remove_test_db'] = 0

    def disallow_root_remotely(cursor):
        if disallow_root_login_remotely:
            cursor.execute("select user, host from mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');")
            remote = cursor.fetchall()
            print(remote)
            print(len(remote))
            if len(remote) >= 1:
                cursor.execute("DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');")
                cursor.execute("flush privileges;")
                info['disallow_root_remotely'] = 0
            else:
                info['disallow_root_remotely'] = 0

    if check_mysql_connection(host=login_host, user=user, password=login_password):
        try:
            connection = mysql.connect(host=login_host, user=user, passwd=login_password, db='mysql')
            cursor = connection.cursor()
            remove_anon_user(cursor)
            remove_testdb(cursor)
            disallow_root_remotely(cursor)
            if change_root_password:
                pwd = {}
                for host in hosts:
                    cursor.execute('use mysql;')
                    cursor.execute(
                        'update user set password=PASSWORD("{}") where User="{}" AND Host="{}";'.format(new_password,
                                                                                                        user, host))
                    cursor.execute('flush privileges;')
                    cursor.execute('select user, host, password from mysql.user where user="{}";'.format(user))
                    data = cursor.fetchall()
                    for d in data:
                        if d[1] == host:
                            pwd['{}'.format(d[1])] = d[2]

                out = set(hosts).symmetric_difference(set(pwd.keys()))
                info['hosts_failed'] = list(out)
                hosts_ = list(set(hosts) - set(list(out)))

                for host in hosts_:
                    if pwd[host] == pwd[login_host]:
                        info['hosts_success'].append(host)
                    else:
                        info['hosts_failed'].append(login_host)

                #if len(info['hosts_success']) >= 1:
                    #info['stdout'] = 'Password for user: {} @ Hosts: {} changed to the desired state'.format(user, info['hosts_success'])
                if len(info['hosts_failed']) >= 1:
                    info['change_root_pwd'] = 1
                #    info['stderr'] = 'Could NOT change password for User: {} @ Hosts: {}'.format(user,info['hosts_failed'])
                else:
                    info['change_root_pwd'] = 0
            connection.close()
        except mysql.Error as e:
            info['change_root_pwd'] = 1
            info['stderr'] = e

    elif check_mysql_connection(host=login_host, user=user, password=new_password):
        connection = mysql.connect(host=login_host, user=user, passwd=new_password, db='mysql')
        cursor_ = connection.cursor()
        remove_anon_user(cursor_)
        remove_testdb(cursor_)
        disallow_root_remotely(cursor_)
        info['change_root_pwd'] = 0
        info['stdout'] = 'Password of {}@{} Already meets the desired state'.format(user, login_host)

    else:
        info['change_root_pwd'] = 1
        info['stdout'] = 'Neither the provided old password nor the new password are correct'
    return info


# Example of Usage

print(mysql_secure_installation(login_password='password51', new_password='password52', hosts=['localhost', '::1', '127.0.0.1', 'controller.linux.com', 'controller', 'test']))







