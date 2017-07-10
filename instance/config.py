SECRET_KEY = 'Sm9obiBTY2hyb20ga2lja3MgYXNz' #Flask使用这个密钥来对cookies和别的东西进行签名。你应该在instance文件夹中设定这个值，并不要把它放入版本控制中。你可以在下一节读到关于instance文件夹的更多信息。
STRIPE_API_KEY = 'SmFjb2IgS2FwbGFuLU1vc3MgaXMgYSBoZXJv'
SQLALCHEMY_DATABASE_URI= \
"postgresql://user:TWljaGHFgiBCYXJ0b3N6a2lld2ljeiEh@localhost/databasename"

DEBUG = True
SQLALCHEMY_ECHO = True