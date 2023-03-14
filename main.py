import MetaTrader5 as mt5
import time

# Conecta-se ao MetaTrader 5
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Seleciona o símbolo do par de moedas
symbol = "EURUSD"

# Obtém a informação do símbolo
symbol_info = mt5.symbol_info(symbol)

# Se o símbolo não existir, fecha o programa
if not symbol_info:
    print(symbol, "not found")
    mt5.shutdown()
    quit()

# Imprime informações sobre o símbolo
print(symbol, "info:")
print("  ask:", symbol_info.ask)
print("  bid:", symbol_info.bid)
print("  spread:", symbol_info.ask - symbol_info.bid)
print("  digits:", symbol_info.digits)
print("  trade_mode:", symbol_info.trade_mode)

# Define o tipo de ordem a ser utilizada
order_type = input("Digite FOK para uma ordem FOK ou IOC para uma ordem IOC: ")
while order_type not in ["FOK", "IOC"]:
    order_type = input("Opção inválida. Digite FOK para uma ordem FOK ou IOC para uma ordem IOC: ")

# Coloca uma ordem de compra
lot = 0.01
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20
start_time = time.time()

if order_type == "FOK":
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 100 * point,
        "tp": price + 100 * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open buy",
        #"type_time": mt5.ORDER_TIME_FOK,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
else:
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY_STOP,
        "price": price + 50 * point, # Defina a distância que você deseja colocar a ordem
        "sl": price - 100 * point,
        "tp": price + 100 * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open buy stop",
        #"type_time": mt5.ORDER_TIME_IOC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

result = mt5.order_send(request)

if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("Erro ao enviar a ordem de compra:", result.comment)
else:
    print("Ordem de compra enviada com sucesso")
    print(result)
    execution_time = (time.time() - start_time) * 1000
    print("Tempo de execução da ordem de compra: %.2f ms" % execution_time)
time.sleep(5)

time.sleep(5)
# Coloque uma ordem de venda
price = mt5.symbol_info_tick(symbol).bid
start_time = time.time()
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_SELL,
    "price": price,
    "sl": price + 100 * point,
    "tp": price - 100 * point,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script open sell",
    #"type_time": type_time, # defina o tipo de ordem aqui
    "type_filling": mt5.ORDER_FILLING_RETURN,
}
result = mt5.order_send(request)

if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("Erro ao enviar a ordem de venda:", result.comment)
else:
    print("Ordem de venda enviada com sucesso")
    print(result)
    execution_time = (time.time() - start_time) * 1000
    print("Tempo de execução da ordem de venda: %.2f ms" % execution_time)

# Desconecte-se do MetaTrader 5
mt5.shutdown()