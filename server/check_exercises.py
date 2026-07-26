from server.app import app

if __name__ == '__main__':
    with app.test_client() as c:
        r = c.get('/exercises')
        print(r.status_code)
        print(r.get_data(as_text=True))
