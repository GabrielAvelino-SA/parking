# Parking
### Descrição

REST API para comtrole de estacionamento de carros

### Começando

para executar o projeto, sera nescessario intalar os pacotno arquivo ```req.txt ``` no diretorio rais do projeto

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

### Referencias
[Placa Mercosul](https://carbig.com/dicas/entenda-novas-placas-padrao-mercosul) | 
[django](https://www.djangoproject.com/) | 
[djangoRest](https://www.django-rest-framework.org/) |
[Bootstrap](https://getbootstrap.com/)