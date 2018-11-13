def update_users():
    import csv
    filename = '/tmp/care3_all.csv'

    result = dict(error=[], exists_id_same=[], exists_id_exists=[], exists_id_updated=[], nonexists_id_exists=[], nonexists_created=[])
    #auth_user.id,auth_user.first_name,auth_user.last_name,auth_user.email,auth_user.employee_id
    #['976', 'Obaidullah', 'Obaid', 'Obaidullah14363@care.awcc', '14363']
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:

            # first check if the email already exists
            # if so, then check if id is same, if not, check if id already exists, if not, then update id and name
            # if email doesn't exist, then check if id already exists, if not, then create user, set password
            # if id already exists, then create user, and log new id
            try:
                id = int(row[0])
            except:
                result['error'].append(row)
                current.logger.error(row)
            else:
                e = db(db.auth_user.email.lower() == row[3].lower()).select().first()
                t = db(db.auth_user.id == id).select().first()

                if e:
                    if e['id'] == row[0]:
                        result['exists_id_same'].append(row)
                    else:
                        if t:
                            result['exists_id_exists'].append((row, t['id']))
                        else:
                            result['exists_id_updated'].append((row, e['id']))
                            #db(db.auth_user.id == e['id']).update(id=id, first_name=row[1], last_name=row[2], employee_id=row[4])
                else:
                    if t:
                        result['nonexists_id_exists'].append((row, t['id']))
                    else:
                        t = db.auth_user.insert(id=id, first_name=row[1], last_name=row[2], email=row[3], employee_id=row[4], password='awcc123')
                        result['nonexists_created'].append((row, t))

    return dict(result=result)

