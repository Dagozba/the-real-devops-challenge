db.auth('challenge_user', 'secretpassword')

db = db.getSiblingDB('restaurants_db')

db.createUser({
  user: 'challenge_user',
  pwd: 'secretpassword',
  roles: [
    {
      role: 'root',
      db: 'admin',
    },
  ],
});
