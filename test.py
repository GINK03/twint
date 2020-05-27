import twint

import time

user = "m_kumagai"
start = time.time()
c = twint.Config()
c.Username = user
c.Limit = 100
#c.Hide_output = True
# c.User_full = True
c.Following = True
c.Store_json = True
c.Output = f"test/{user}"
twint.run.Favorites(c)
elapsed = time.time() - start
print(f"total elapsed = {elapsed:0.02f}")
