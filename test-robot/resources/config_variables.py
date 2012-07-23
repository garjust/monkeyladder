GLOBAL_USERS = {
    'ADMIN': ('user.admin', 'admin1', 'User Admin'),
    'A': ('user.a', 'password', 'User A'),
    'B': ('user.b', 'password', 'User B'),
    'C': ('user.c', 'password', 'User C'),
    'D': ('user.d', 'password', 'User E'),
    'E': ('user.e', 'password', 'User D'),
    'F': ('user.f', 'password', 'User F'),
    'LONG': ('user.long', 'password', 'User Longnameduserishappytoprovidetheirlongnametotestnamelength'),
    'NOEMAIL': ('user.noemail', 'password', 'User No Email'),
    'NONAME': ('user.noname', 'password', ''),
    'SHORT': ('user.short', 'password', 'u s'),
}

DEFAULT_ADMIN = GLOBAL_USERS['ADMIN']
DEFAULT_USER = GLOBAL_USERS['B']