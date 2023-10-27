# Parking
### Descrição

REST API para comtrole de reservas de estacionamento

### Começando

Para executar o projeto, sera nescessario ter o [Python](https://www.python.org/downloads/) Instalado na sua maquina, 

### Build

1. Clonar projeto
    ``````
    git clone https://github.com/GabrielAvelino-SA/parking.git
    ``````

1. No diretorio raiz do projeto Instale os pacotes em ```req.txt```
    ```
    pip install -r req.txt
    ```

1. Start Project
    ```
    python manage.py runserver
    ```

### Poutes
POST -> Nova Reserva
```
/parking/
```

POST -> Lista de Reservas
```
/parking/list/
```

GET -> Historico e detalhes de reserva por placa
```
/parking/<str:plate>/
```

POST -> Pagamento
```
/parking/<str:plate>/pay/
```

POST -> CheckOut
```
/parking/<str:plate>/out/
```


### API-Routes

POST -> Nova reserva no Estaqcionamento
```
/parking/api/
```

GET ->lista de reservas
```
/parking/api/list/
```

GET -> Historico e detalhes de reservasa por placa
```
/parking/api/<str:plate>/
```

PUT -> pagamento
```
/parking/api/<str:plate>/pay
```
w
PUT -> CheckOut
```
/parking/api/<str:plate>/out
```

### New features

- Tela Login do Usuario
    - permições

- Sistema de pagamento
    - calcular valor a ser pago
    - Escolha o Methodo de pagamento
        - pix
        - cartão
    - PDF Com dados da reserva/pagamento
    - Envio por email/comprovante

- Deletar dados do veiculo
- Buscar dados de veiculo por placa e id
- criar filtro por status de pagamento, checkin, checout, data e tempo.



### Referencias
[Placa Mercosul](https://carbig.com/dicas/entenda-novas-placas-padrao-mercosul) | 
[django](https://www.djangoproject.com/) | 
[djangoRest](https://www.django-rest-framework.org/) |
[Bootstrap](https://getbootstrap.com/)