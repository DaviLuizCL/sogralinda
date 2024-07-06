
# Minha sogra, um amor de pessoa

Pensando na querida que gerou minha noiva, como não dei nada a ela além de estresse, porquê não unir minha falta do que fazer com a vontade de programar? Resolvi fazer um site pra minha linda cobra, digo, sogra.





## Variáveis de Ambiente

Lembre-se de alimentar a variável de ambiente secret_key

WINDOWS -> No explorar, digite "variaveis", vá em "Editar as variáveis de ambiente" -> Novo, e coloque sua HASH

Linux -> Abra seu terminal favorito
-> echo 'export SECRET_KEY="sua-chave-secreta"' >> ~/.bashrc
-> source ~/.bashrc
```python
    import os
secret_key = os.getenv('SECRET_KEY')
if secret_key is None:
    raise ValueError("Problemas com a variável de ambiente")

app.config['SECRET_KEY'] = secret_key

```


## Autor

- [@davilcl](https://www.github.com/davilcl)


## Usado por

Esse projeto é usado pelas seguintes empresas:

- Se eu adular muito, minha sogra.

