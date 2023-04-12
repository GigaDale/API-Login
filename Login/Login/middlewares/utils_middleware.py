import hashlib

# Gera um hash a partir de um dict retornado do json 
def gen_hash(valor, campo):
    return hashlib.md5(valor[campo].encode()).hexdigest()